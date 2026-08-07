"""Run exploratory models across five prespecified random splits in MLflow."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import mlflow
import matplotlib.pyplot as plt
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from train import FEATURES, evaluate_model, load_training_data


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "endes_anemia_children_2019_2024.csv"
RESULTS_PATH = ROOT / "docs" / "experiment_results.csv"
SUMMARY_PATH = ROOT / "docs" / "experiment_summary.csv"
MLRUNS_PATH = ROOT / ".mlruns"
SEEDS = [13, 21, 42, 87, 100]
TEST_FRACTION = 0.20


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except subprocess.CalledProcessError:
        return "unavailable"


def render_experiment_summary(results: pd.DataFrame) -> None:
    averages = results.groupby("model", as_index=False)[["auc_roc", "pr_auc", "f1"]].mean().melt(
        id_vars="model", var_name="metric", value_name="value"
    )
    figure, axis = plt.subplots(figsize=(8, 4.5))
    for model_name, color in (("logistic_regression", "#8d2f23"), ("random_forest", "#396a50"), ("extra_trees", "#0f4c81")):
        subset = averages[averages["model"] == model_name]
        axis.plot(subset["metric"], subset["value"], marker="o", linewidth=2, label=model_name.replace("_", " "), color=color)
    axis.set(title="Exploratory ENDES experiments: mean metric across five random splits", xlabel="Metric", ylabel="Score", ylim=(0, 1))
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(ROOT / "docs" / "mlflow_runs.png", dpi=180)
    plt.close(figure)


def main() -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MLRUNS_PATH.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(MLRUNS_PATH.resolve().as_uri())
    mlflow.set_experiment("endes_child_anemia_exploratory")
    data = load_training_data()
    dataset_hash = file_sha256(DATA_PATH)
    commit = git_commit()
    results = []

    for seed in SEEDS:
        for model_name in ("logistic_regression", "random_forest", "extra_trees"):
            metrics, _ = evaluate_model(data, model_name, seed, test_size=TEST_FRACTION)
            with mlflow.start_run(run_name=f"{model_name}_seed_{seed}"):
                mlflow.log_params(
                    {
                        "model": model_name,
                        "seed": seed,
                        "test_fraction": TEST_FRACTION,
                        "features": ",".join(FEATURES),
                        "dataset_sha256": dataset_hash,
                        "git_commit": commit,
                        "purpose": "exploratory_non_clinical",
                        "split_protocol": "stratified_80_20_prespecified_seed",
                    }
                )
                mlflow.log_metrics({key: value for key, value in metrics.items() if isinstance(value, float)})
            results.append(metrics)
            print(f"{model_name} seed={seed}: AUC={metrics['auc_roc']:.4f}, F1={metrics['f1']:.4f}")

    results_frame = pd.DataFrame(results)
    results_frame.to_csv(RESULTS_PATH, index=False)
    summary = results_frame.groupby("model")[["auc_roc", "pr_auc", "accuracy", "f1", "recall"]].agg(["mean", "std", "min", "max"])
    summary.columns = [f"{column[0]}_{column[1]}" for column in summary.columns]
    summary = summary.reset_index()
    summary.to_csv(SUMMARY_PATH, index=False)
    render_experiment_summary(results_frame)
    print(f"Saved {len(results)} experiment rows and split summary to {RESULTS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
