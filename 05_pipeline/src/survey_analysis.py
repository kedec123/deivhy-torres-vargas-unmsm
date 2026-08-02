"""Estimate design-aware descriptive uncertainty and adjusted associations.

This module is deliberately separate from the exploratory classifier.  It
answers the population-level research question with the ENDES sampling weight,
stratum and cluster fields; it does not make clinical predictions.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "endes_anemia_children_2019_2024.csv"
DOCS_DIR = ROOT / "docs"
BOOTSTRAP_REPLICATES = 300
BOOTSTRAP_SEED = 20260802


def load_analysis_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load records with the outcome and survey-design fields needed here."""
    required = [
        "survey_year",
        "anemia_legacy",
        "survey_weight",
        "cluster_code",
        "stratum_code",
        "age_months",
        "child_sex_code",
        "mother_education_code",
        "wealth_quintile",
        "residence_code",
        "department_code",
    ]
    frame = pd.read_csv(path, dtype={"department_code": "string"})
    return frame.dropna(subset=required).copy()


def weighted_prevalence(frame: pd.DataFrame, weights: np.ndarray | None = None) -> float:
    """Return weighted anemia prevalence for a non-empty analysis frame."""
    current_weights = frame["survey_weight"].to_numpy() if weights is None else weights
    return float(np.average(frame["anemia_legacy"].to_numpy(), weights=current_weights))


def stratified_cluster_bootstrap_ci(
    frame: pd.DataFrame,
    replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float, float]:
    """Estimate a 95% interval by resampling ENDES clusters within strata.

    It preserves the observed number of clusters in each stratum.  The result
    is a design-aware uncertainty estimate for this course-stage descriptive
    analysis, not an official INEI replicate-weight estimate.
    """
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
    replicates_values: list[float] = []

    for _ in range(replicates):
        counts = np.zeros(working["_cluster_index"].max() + 1, dtype=float)
        for cluster_ids in strata_clusters:
            sampled = rng.choice(cluster_ids, size=len(cluster_ids), replace=True)
            counts += np.bincount(sampled, minlength=len(counts))
        replicate_weights = base_weights * counts[cluster_index]
        replicates_values.append(float(np.average(outcome, weights=replicate_weights)))

    point = weighted_prevalence(working)
    lower, upper = np.quantile(replicates_values, [0.025, 0.975])
    return point, float(lower), float(upper)


def annual_prevalence_with_intervals(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for survey_year, group in frame.groupby("survey_year", sort=True):
        point, lower, upper = stratified_cluster_bootstrap_ci(
            group, seed=BOOTSTRAP_SEED + int(survey_year)
        )
        rows.append(
            {
                "survey_year": int(survey_year),
                "sample_size": len(group),
                "weighted_anemia_prevalence": point,
                "ci_95_lower": lower,
                "ci_95_upper": upper,
                "bootstrap_replicates": BOOTSTRAP_REPLICATES,
            }
        )
    return pd.DataFrame(rows)


def adjusted_associations(frame: pd.DataFrame) -> pd.DataFrame:
    """Fit a weighted logistic association model with model-based intervals."""
    working = frame.copy()
    # ENDES expansion weights are rescaled so that they retain relative weights
    # without being interpreted by statsmodels as millions of literal copies.
    working["analysis_weight"] = working["survey_weight"] / working["survey_weight"].mean()
    formula = (
        "anemia_legacy ~ age_months + C(child_sex_code) + C(mother_education_code) "
        "+ C(wealth_quintile) + C(residence_code) + C(department_code) + C(survey_year)"
    )
    fitted = smf.glm(
        formula=formula,
        data=working,
        family=sm.families.Binomial(),
        var_weights=working["analysis_weight"],
    ).fit()
    intervals = fitted.conf_int()
    table = pd.DataFrame(
        {
            "term": fitted.params.index,
            "coefficient_log_odds": fitted.params.values,
            "odds_ratio": np.exp(fitted.params.values),
            "ci_95_lower": np.exp(intervals[0].values),
            "ci_95_upper": np.exp(intervals[1].values),
            "p_value": fitted.pvalues.values,
        }
    )
    return table.loc[table["term"] != "Intercept"].reset_index(drop=True)


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    data = load_analysis_data()
    annual = annual_prevalence_with_intervals(data)
    associations = adjusted_associations(data)
    annual.to_csv(DOCS_DIR / "analysis_by_year_with_ci.csv", index=False)
    associations.to_csv(DOCS_DIR / "adjusted_associations.csv", index=False)

    report = [
        "# Design-aware uncertainty and adjusted associations",
        "",
        "Annual prevalence intervals use a stratified cluster bootstrap (300 replicates) with ENDES stratum and cluster fields. The adjusted association model is a weighted logistic regression with model-based 95% intervals. These estimates describe observed associations; they do not establish causality.",
        "",
        "## Annual weighted prevalence with 95% intervals",
        "",
        annual.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Interpretation boundary",
        "",
        "The bootstrap is a transparent design-aware course implementation, not an official INEI replicate-weight estimator. The logistic model uses relative survey weights and model-based intervals; a full survey-design variance model remains a later methodological extension. It is an association model, not a prediction model and not evidence of a causal effect.",
        "",
        "The primary trend continues to use legacy `HW57` in every year. A separate 2024 sensitivity comparison is produced by `sensitivity_2024.py`.",
    ]
    (DOCS_DIR / "survey_analysis_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Saved annual intervals and {len(associations)} adjusted association rows to {DOCS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
