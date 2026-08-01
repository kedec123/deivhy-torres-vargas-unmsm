"""Run fixed-seed exploratory models and record them in local MLflow."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import mlflow
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from train import FEATURES, evaluate_model, load_training_data


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "endes_anemia_children_2019_2024.csv"
RESULTS_PATH = ROOT / "05_pipeline" / "docs" / "experiment_results.csv"
MLRUNS_PATH = ROOT / "mlruns"
SEEDS = [13, 21, 42, 87, 100]


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
        for model_name in ("logistic_regression", "random_forest"):
            metrics, _ = evaluate_model(data, model_name, seed)
            with mlflow.start_run(run_name=f"{model_name}_seed_{seed}"):
                mlflow.log_params(
                    {
                        "model": model_name,
                        "seed": seed,
                        "test_size": 0.25,
                        "features": ",".join(FEATURES),
                        "dataset_sha256": dataset_hash,
                        "git_commit": commit,
                        "purpose": "exploratory_non_clinical",
                    }
                )
                mlflow.log_metrics({key: value for key, value in metrics.items() if isinstance(value, float)})
            results.append(metrics)
            print(f"{model_name} seed={seed}: AUC={metrics['auc_roc']:.4f}, F1={metrics['f1']:.4f}")

    pd.DataFrame(results).to_csv(RESULTS_PATH, index=False)
    print(f"Saved {len(results)} experiment rows to {RESULTS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
