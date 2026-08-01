"""Render a compact visual summary from the saved MLflow experiment table."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "05_pipeline" / "docs" / "experiment_results.csv"
OUTPUT = ROOT / "05_pipeline" / "docs" / "mlflow_runs.png"


def main() -> None:
    results = pd.read_csv(RESULTS)
    averages = results.groupby("model", as_index=False)[["auc_roc", "pr_auc", "f1"]].mean().melt(id_vars="model", var_name="metric", value_name="value")
    figure, axis = plt.subplots(figsize=(8, 4.5))
    for model, color in (("logistic_regression", "#8d2f23"), ("random_forest", "#396a50")):
        subset = averages[averages["model"] == model]
        axis.plot(subset["metric"], subset["value"], marker="o", linewidth=2, label=model.replace("_", " "), color=color)
    axis.set(title="Exploratory ENDES experiments: mean metric across five seeds", xlabel="Metric", ylabel="Score", ylim=(0, 1))
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(OUTPUT, dpi=180)
    plt.close(figure)


if __name__ == "__main__":
    main()
