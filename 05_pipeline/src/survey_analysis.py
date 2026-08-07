"""Estimate ENDES prevalence uncertainty and adjusted associations.

The annual estimates use the ENDES final weight, strata and primary sampling
units.  Taylor linearization is the primary design-based variance estimator;
the stratified cluster bootstrap is retained as a transparent sensitivity
check.  The association model remains explicitly model-based and non-causal.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import t as student_t


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "endes_anemia_children_2019_2024.csv"
DOCS_DIR = ROOT / "docs"
BOOTSTRAP_REPLICATES = 300
BOOTSTRAP_SEED = 20260802


def load_analysis_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load records containing the outcome and complex-design variables."""
    required = [
        "survey_year", "anemia_legacy", "survey_weight", "cluster_code", "stratum_code",
        "age_months", "child_sex_code", "mother_education_code", "wealth_quintile",
        "residence_code", "department_code",
    ]
    frame = pd.read_csv(path, dtype={"department_code": "string"})
    return frame.dropna(subset=required).copy()


def weighted_prevalence(frame: pd.DataFrame, weights: np.ndarray | None = None) -> float:
    """Return the weighted prevalence for a non-empty analysis frame."""
    current_weights = frame["survey_weight"].to_numpy() if weights is None else weights
    return float(np.average(frame["anemia_legacy"].to_numpy(), weights=current_weights))


def taylor_linearized_proportion(frame: pd.DataFrame) -> dict[str, float | int]:
    """Estimate a proportion with stratified-PSU Taylor linearization.

    The variance uses the first-stage with-replacement approximation over
    primary sampling units within ENDES strata.  For a weighted ratio Y/X, the
    linearized PSU contribution is Y_hi - p*X_hi.  This is a design-based
    estimator for annual prevalence, not a model-based standard error.
    """
    working = frame[["anemia_legacy", "survey_weight", "stratum_code", "cluster_code"]].copy()
    working["weighted_outcome"] = working["anemia_legacy"] * working["survey_weight"]
    total_weight = float(working["survey_weight"].sum())
    estimate = float(working["weighted_outcome"].sum() / total_weight)
    psu_totals = (
        working.groupby(["stratum_code", "cluster_code"], as_index=False)
        .agg(weighted_outcome=("weighted_outcome", "sum"), weighted_total=("survey_weight", "sum"))
    )
    psu_totals["linearized_total"] = psu_totals["weighted_outcome"] - estimate * psu_totals["weighted_total"]

    variance_numerator = 0.0
    degrees_of_freedom = 0
    usable_strata = 0
    for _, stratum in psu_totals.groupby("stratum_code", sort=False):
        psu_count = len(stratum)
        if psu_count < 2:
            continue
        centered = stratum["linearized_total"] - stratum["linearized_total"].mean()
        variance_numerator += (psu_count / (psu_count - 1)) * float((centered**2).sum())
        degrees_of_freedom += psu_count - 1
        usable_strata += 1

    if degrees_of_freedom <= 0:
        raise ValueError("Taylor linearization requires at least two PSUs in one or more strata.")
    standard_error = float(np.sqrt(variance_numerator) / total_weight)
    critical_value = float(student_t.ppf(0.975, degrees_of_freedom))
    return {
        "weighted_anemia_prevalence": estimate,
        "taylor_standard_error": standard_error,
        "taylor_ci_95_lower": max(0.0, estimate - critical_value * standard_error),
        "taylor_ci_95_upper": min(1.0, estimate + critical_value * standard_error),
        "design_degrees_of_freedom": degrees_of_freedom,
        "design_strata": usable_strata,
        "design_psus": int(len(psu_totals)),
    }


def stratified_cluster_bootstrap_ci(
    frame: pd.DataFrame,
    replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float, float]:
    """Bootstrap PSUs with replacement within strata as a sensitivity check."""
    working = frame.reset_index(drop=True).copy()
    working["_cluster_index"] = pd.factorize(
        pd.MultiIndex.from_frame(working[["stratum_code", "cluster_code"]])
    )[0]
    strata_clusters = (
        working[["stratum_code", "_cluster_index"]]
        .drop_duplicates()
        .groupby("stratum_code", sort=False)["_cluster_index"]
        .apply(lambda values: values.to_numpy())
        .tolist()
    )
    cluster_index = working["_cluster_index"].to_numpy()
    base_weights = working["survey_weight"].to_numpy()
    outcome = working["anemia_legacy"].to_numpy()
    rng = np.random.default_rng(seed)
    values: list[float] = []
    for _ in range(replicates):
        counts = np.zeros(working["_cluster_index"].max() + 1, dtype=float)
        for cluster_ids in strata_clusters:
            sampled = rng.choice(cluster_ids, size=len(cluster_ids), replace=True)
            counts += np.bincount(sampled, minlength=len(counts))
        values.append(float(np.average(outcome, weights=base_weights * counts[cluster_index])))
    lower, upper = np.quantile(values, [0.025, 0.975])
    return weighted_prevalence(working), float(lower), float(upper)


def annual_uncertainty(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    taylor_rows, bootstrap_rows = [], []
    for survey_year, group in frame.groupby("survey_year", sort=True):
        taylor = taylor_linearized_proportion(group)
        point, bootstrap_lower, bootstrap_upper = stratified_cluster_bootstrap_ci(
            group, seed=BOOTSTRAP_SEED + int(survey_year)
        )
        taylor_rows.append({"survey_year": int(survey_year), "sample_size": len(group), **taylor, "ci_method": "Taylor linearization"})
        bootstrap_rows.append(
            {
                "survey_year": int(survey_year), "sample_size": len(group),
                "weighted_anemia_prevalence": point, "bootstrap_ci_95_lower": bootstrap_lower,
                "bootstrap_ci_95_upper": bootstrap_upper, "bootstrap_replicates": BOOTSTRAP_REPLICATES,
                "ci_method": "Stratified cluster bootstrap",
            }
        )
    return pd.DataFrame(taylor_rows), pd.DataFrame(bootstrap_rows)


def adjusted_associations(frame: pd.DataFrame) -> pd.DataFrame:
    """Fit a weighted, adjusted association model with model-based intervals."""
    working = frame.copy()
    working["analysis_weight"] = working["survey_weight"] / working["survey_weight"].mean()
    formula = (
        "anemia_legacy ~ age_months + C(child_sex_code) + C(mother_education_code) "
        "+ C(wealth_quintile) + C(residence_code) + C(department_code) + C(survey_year)"
    )
    fitted = smf.glm(
        formula=formula, data=working, family=sm.families.Binomial(),
        var_weights=working["analysis_weight"],
    ).fit()
    intervals = fitted.conf_int()
    table = pd.DataFrame(
        {
            "term": fitted.params.index, "coefficient_log_odds": fitted.params.values,
            "odds_ratio": np.exp(fitted.params.values),
            "ci_95_lower": np.exp(intervals[0].values), "ci_95_upper": np.exp(intervals[1].values),
            "p_value": fitted.pvalues.values,
        }
    )
    return table.loc[table["term"] != "Intercept"].reset_index(drop=True)


def year_effects(associations: pd.DataFrame) -> pd.DataFrame:
    """Return adjusted modelled year effects relative to the 2019 reference year."""
    effects = associations.loc[associations["term"].str.startswith("C(survey_year)")].copy()
    effects["survey_year"] = effects["term"].str.extract(r"T\.(\d{4})").astype(int)
    effects.insert(0, "reference_year", 2019)
    return effects[["reference_year", "survey_year", "odds_ratio", "ci_95_lower", "ci_95_upper", "p_value"]].sort_values("survey_year")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    data = load_analysis_data()
    taylor, bootstrap = annual_uncertainty(data)
    associations = adjusted_associations(data)
    effects = year_effects(associations)
    comparison = taylor.merge(
        bootstrap[["survey_year", "bootstrap_ci_95_lower", "bootstrap_ci_95_upper", "bootstrap_replicates"]],
        on="survey_year", validate="one_to_one",
    )
    comparison["ci_lower_absolute_difference"] = (comparison["taylor_ci_95_lower"] - comparison["bootstrap_ci_95_lower"]).abs()
    comparison["ci_upper_absolute_difference"] = (comparison["taylor_ci_95_upper"] - comparison["bootstrap_ci_95_upper"]).abs()

    taylor.to_csv(DOCS_DIR / "analysis_by_year_with_ci.csv", index=False)
    bootstrap.to_csv(DOCS_DIR / "analysis_by_year_bootstrap_ci.csv", index=False)
    comparison.to_csv(DOCS_DIR / "analysis_ci_method_comparison.csv", index=False)
    associations.to_csv(DOCS_DIR / "adjusted_associations.csv", index=False)
    effects.to_csv(DOCS_DIR / "modelled_year_effects_vs_2019.csv", index=False)

    report = [
        "# Design-based uncertainty and adjusted associations", "",
        "Annual prevalence uses ENDES final weights, strata and primary sampling units. Taylor linearization is the primary design-based variance estimator. A stratified-cluster bootstrap with 300 replicates is retained as an independent sensitivity check. Both methods estimate the same legacy-comparable weighted prevalence; their intervals are compared in `analysis_ci_method_comparison.csv`.", "",
        "## Annual weighted prevalence: Taylor linearization", "", taylor.to_markdown(index=False, floatfmt=".4f"), "",
        "## Bootstrap comparison", "", comparison[["survey_year", "taylor_ci_95_lower", "taylor_ci_95_upper", "bootstrap_ci_95_lower", "bootstrap_ci_95_upper"]].to_markdown(index=False, floatfmt=".4f"), "",
        "## Modelled year effects", "", effects.to_markdown(index=False, floatfmt=".4f"), "",
        "## Interpretation boundary", "",
        "Taylor intervals provide design-based uncertainty for the annual prevalence estimates under a stratified first-stage PSU variance approximation. The adjusted logistic model uses relative survey weights but its confidence intervals and p-values are model-based; they describe adjusted associations only, not a full design-based regression variance and never causal effects. The primary trend uses legacy `HW57` in every year. The separate 2024 `HW57A` sensitivity analysis is not mixed into the trend.",
    ]
    (DOCS_DIR / "survey_analysis_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Saved Taylor intervals, bootstrap comparison and {len(effects)} modelled year effects to {DOCS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
