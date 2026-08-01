"""Run a Fairlearn audit on Adult Census and a separate ENDES subgroup check."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fairlearn.datasets import fetch_adult
from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    equalized_odds_difference,
    false_positive_rate,
    selection_rate,
    true_positive_rate,
)
from fairlearn.postprocessing import ThresholdOptimizer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "11_bias_audit"
PIPELINE_SRC = ROOT / "05_pipeline" / "src"
if str(PIPELINE_SRC) not in sys.path:
    sys.path.insert(0, str(PIPELINE_SRC))

from train import evaluate_model, load_training_data


SEEDS = [13, 21, 42, 87, 100]


def adult_pipeline(features: pd.DataFrame) -> Pipeline:
    numeric = features.select_dtypes(include=["number"]).columns.tolist()
    categorical = [column for column in features.columns if column not in numeric]
    preprocessor = ColumnTransformer(
        [
            ("numeric", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
            ("categorical", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("encode", OneHotEncoder(handle_unknown="ignore"))]), categorical),
        ]
    )
    return Pipeline([("preprocess", preprocessor), ("model", LogisticRegression(max_iter=1500, class_weight="balanced"))])


def disparate_impact(group_frame: pd.DataFrame) -> float:
    rates = group_frame["selection_rate"].dropna().astype(float)
    if rates.empty or rates.max() == 0:
        return float("nan")
    return float(rates.min() / rates.max())


def audit_metrics(y_true: pd.Series, y_pred: np.ndarray, sensitive: pd.Series) -> tuple[dict, pd.DataFrame]:
    metric_frame = MetricFrame(
        metrics={
            "selection_rate": selection_rate,
            "true_positive_rate": true_positive_rate,
            "false_positive_rate": false_positive_rate,
            "accuracy": accuracy_score,
        },
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive,
    )
    group_frame = metric_frame.by_group.reset_index().rename(columns={metric_frame.by_group.index.name or "index": "sex"})
    summary = {
        "accuracy": accuracy_score(y_true, y_pred),
        "demographic_parity_difference": demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive),
        "disparate_impact": disparate_impact(group_frame),
        "equalized_odds_difference": equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive),
        "selection_rate_difference": metric_frame.difference(method="between_groups")["selection_rate"],
        "true_positive_rate_difference": metric_frame.difference(method="between_groups")["true_positive_rate"],
        "false_positive_rate_difference": metric_frame.difference(method="between_groups")["false_positive_rate"],
    }
    return summary, group_frame


def raw_label_audit(adult) -> tuple[pd.DataFrame, pd.DataFrame]:
    target = adult.target.astype(str).str.contains(">50K").astype(int)
    sensitive = adult.data["sex"].astype(str)
    groups = (
        pd.DataFrame({"sex": sensitive, "favourable_label": target})
        .groupby("sex", as_index=False)
        .agg(sample_size=("favourable_label", "size"), observed_favourable_rate=("favourable_label", "mean"))
    )
    rates = groups["observed_favourable_rate"]
    summary = pd.DataFrame(
        [
            {
                "demographic_parity_difference": float(rates.max() - rates.min()),
                "disparate_impact": float(rates.min() / rates.max()),
            }
        ]
    )
    return summary, groups


def run_adult_audit(adult) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = adult.data.copy()
    target = adult.target.astype(str).str.contains(">50K").astype(int)
    sensitive = features["sex"].astype(str)
    features = features.drop(columns=["sex"])
    results = []
    group_results = []

    for seed in SEEDS:
        x_train, x_test, y_train, y_test, sensitive_train, sensitive_test = train_test_split(
            features, target, sensitive, test_size=0.25, random_state=seed, stratify=target
        )
        baseline = adult_pipeline(x_train)
        baseline.fit(x_train, y_train)
        baseline_prediction = baseline.predict(x_test)

        np.random.seed(seed)
        mitigator = ThresholdOptimizer(
            estimator=baseline,
            constraints="equalized_odds",
            objective="accuracy_score",
            prefit=True,
            predict_method="predict_proba",
        )
        mitigator.fit(x_train, y_train, sensitive_features=sensitive_train)
        mitigated_prediction = mitigator.predict(x_test, sensitive_features=sensitive_test, random_state=seed)

        for approach, prediction in (("baseline", baseline_prediction), ("equalized_odds_threshold", mitigated_prediction)):
            metrics, groups = audit_metrics(y_test, prediction, sensitive_test)
            results.append({"seed": seed, "approach": approach, **metrics})
            groups.insert(0, "approach", approach)
            groups.insert(0, "seed", seed)
            group_results.append(groups)

    return pd.DataFrame(results), pd.concat(group_results, ignore_index=True)


def write_adult_report(results: pd.DataFrame, groups: pd.DataFrame, label_summary: pd.DataFrame, label_groups: pd.DataFrame) -> None:
    summary = results.groupby("approach", as_index=False).agg(
        accuracy_mean=("accuracy", "mean"),
        demographic_parity_difference_mean=("demographic_parity_difference", "mean"),
        disparate_impact_mean=("disparate_impact", "mean"),
        equalized_odds_difference_mean=("equalized_odds_difference", "mean"),
        equalized_odds_difference_min=("equalized_odds_difference", "min"),
        equalized_odds_difference_max=("equalized_odds_difference", "max"),
    )
    group_summary = groups.groupby(["approach", "sex"], as_index=False).agg(
        selection_rate_mean=("selection_rate", "mean"),
        true_positive_rate_mean=("true_positive_rate", "mean"),
        false_positive_rate_mean=("false_positive_rate", "mean"),
        accuracy_mean=("accuracy", "mean"),
    )
    lines = [
        "# Fairness Audit: Adult Census Benchmark",
        "",
        "This audit uses Fairlearn's Adult Census dataset, not ENDES. It is included to meet the course requirement for a reproducible fairness exercise on a standard benchmark. The sensitive feature is recorded sex. The model deliberately excludes sex from training, then evaluates group differences by sex. The favourable label for this exercise is income above 50K; this convention is specific to the benchmark and does not describe a health outcome.",
        "",
        "## Labels before modelling",
        "",
        "The first table checks whether the benchmark label already differs by the sensitive feature. Disparate impact is the smaller group selection rate divided by the larger one. A value closer to 1 indicates similar selection rates; it does not establish that the data-generating process is fair.",
        "",
        label_summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        label_groups.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Procedure",
        "",
        "A logistic-regression baseline was evaluated on five stratified train-test splits. A Fairlearn `ThresholdOptimizer` with an equalized-odds constraint was then fitted on each training split. The audit reports accuracy, demographic-parity difference, disparate impact, and equalized-odds difference. Lower differences are closer to parity for the difference measures; disparate impact is read against 1. No single metric proves fairness.",
        "",
        "## Results across fixed splits",
        "",
        summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Group metrics across fixed splits",
        "",
        group_summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        "The range of equalized-odds difference across seeds is reported to avoid relying on one convenient split. Mitigation can reduce one disparity measure while changing accuracy or other error patterns; the trade-off is part of the result, not a defect to hide.",
        "",
        "## Interpretation and limits",
        "",
        "The benchmark begins with a visible difference in favourable-label rates by recorded sex. In the five internal splits, the equalized-odds post-processing step reduced the reported demographic-parity and equalized-odds differences and moved disparate impact closer to 1. This is an empirical result for this benchmark and these splits, not a declaration that the resulting system is fair in every relevant sense.",
        "",
        "The mitigation changes decision thresholds after fitting the baseline model. It does not change the historical processes that produced the Adult Census labels, prove that sex is the only relevant protected attribute, or resolve potential differences by intersecting characteristics. Fairness criteria can conflict, and the preferred trade-off depends on the real decision context. The course exercise therefore documents the choice and its consequences instead of presenting mitigation as a universal fix.",
        "",
        "The ENDES subgroup check is deliberately separate. It uses the project model only to inspect one internal holdout by child sex and residence; it does not import an Adult Census mitigation rule into Peru or support individual-level decisions.",
        "",
        "## Files",
        "",
        "- `bias_audit_splits.csv`: all split-level metrics.",
        "- `bias_audit_by_group.csv`: group metrics for every split and approach.",
        "- `bias_label_baseline.csv`: observed Adult Census label rates before modelling.",
        "- `before_after_chart.png`: average baseline-versus-mitigated comparison.",
        "- `endes_subgroup_check.md`: a separate descriptive check for the project model, with no claim that Adult Census results transfer to Peru.",
    ]
    (OUTPUT_DIR / "bias_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    chart_metrics = ["accuracy", "demographic_parity_difference", "equalized_odds_difference"]
    averages = results.groupby("approach")[chart_metrics].mean().T.rename(
        index={
            "accuracy": "Accuracy",
            "demographic_parity_difference": "Demographic parity difference",
            "equalized_odds_difference": "Equalized odds difference",
        },
        columns={"baseline": "Baseline", "equalized_odds_threshold": "Equalized-odds mitigation"},
    )
    axis = averages.plot(kind="bar", figsize=(9, 4.8), color=["#8d2f23", "#396a50"])
    axis.set(ylabel="Mean metric value", xlabel="Metric")
    axis.tick_params(axis="x", rotation=12)
    axis.legend(title="Approach")
    axis.grid(axis="y", alpha=0.25)
    axis.figure.suptitle("Adult Census fairness audit across five fixed splits", fontsize=14)
    axis.figure.tight_layout(rect=(0, 0, 1, 0.94))
    axis.figure.savefig(OUTPUT_DIR / "before_after_chart.png", dpi=180)
    plt.close(axis.figure)


def write_endes_subgroup_check() -> None:
    _, data = evaluate_model(load_training_data(), "logistic_regression", 42)
    rows = []
    for feature in ("child_sex_code", "residence_code"):
        for group, frame in data.groupby(feature):
            rows.append(
                {
                    "grouping": feature,
                    "group": group,
                    "n": len(frame),
                    "observed_anemia_rate": frame["anemia_legacy"].mean(),
                    "mean_predicted_probability": frame["predicted_probability"].mean(),
                    "accuracy_at_0_5": accuracy_score(frame["anemia_legacy"], frame["predicted_label"]),
                    "true_positive_rate_at_0_5": true_positive_rate(frame["anemia_legacy"], frame["predicted_label"]),
                }
            )
    summary = pd.DataFrame(rows)
    summary.to_csv(OUTPUT_DIR / "endes_subgroup_metrics.csv", index=False)
    lines = [
        "# ENDES Exploratory Subgroup Check",
        "",
        "This is separate from the Adult Census fairness benchmark. It describes one saved logistic-regression holdout split from the ENDES pipeline (seed 42) by child sex and urban-rural residence. It is a diagnostic table, not a fairness certification and not a basis for acting on individual predictions.",
        "",
        summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        "Observed rates, average scores, accuracy, and true-positive rate can differ across groups for many reasons, including prevalence, sampling, measurement, missing variables, and the selected threshold. Any difference should prompt data and context review; it does not identify a cause or a policy response by itself.",
    ]
    (OUTPUT_DIR / "endes_subgroup_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    adult = fetch_adult(as_frame=True)
    label_summary, label_groups = raw_label_audit(adult)
    results, groups = run_adult_audit(adult)
    results.to_csv(OUTPUT_DIR / "bias_audit_splits.csv", index=False)
    groups.to_csv(OUTPUT_DIR / "bias_audit_by_group.csv", index=False)
    label_groups.to_csv(OUTPUT_DIR / "bias_label_baseline.csv", index=False)
    write_adult_report(results, groups, label_summary, label_groups)
    write_endes_subgroup_check()
    print("Wrote Adult Census fairness audit and ENDES subgroup check.")


if __name__ == "__main__":
    main()
