import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    import mlflow
    import mlflow.sklearn

    MLFLOW_AVAILABLE = True
except Exception:
    MLFLOW_AVAILABLE = False


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "anemia_peru_synthetic.csv"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def build_preprocessor():
    numeric_features = [
        "age_months",
        "wealth_quintile",
        "maternal_education_years",
        "altitude_m",
        "sex_male",
        "rural",
        "recent_iron_supplement",
        "recent_diarrhea",
        "safe_water",
    ]
    categorical_features = ["region"]

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )


def prepare_split(df: pd.DataFrame, seed: int, test_size: float):
    X = df.drop(columns=["target_anemia", "block_id"])
    y = df["target_anemia"]

    splitter = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train_idx, test_idx = next(splitter.split(X, y))

    X_train = X.iloc[train_idx].copy()
    X_test = X.iloc[test_idx].copy()
    y_train = y.iloc[train_idx].copy()
    y_test = y.iloc[test_idx].copy()

    return X_train, X_test, y_train, y_test


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    pipe = Pipeline(
        steps=[
            ("preprocess", build_preprocessor()),
            ("model", model),
        ]
    )
    pipe.fit(X_train, y_train)

    y_prob = pipe.predict_proba(X_test)[:, 1]
    y_pred = pipe.predict(X_test)

    metrics = {
        "model": name,
        "auc_roc": float(roc_auc_score(y_test, y_prob)),
        "pr_auc": float(average_precision_score(y_test, y_prob)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
    }

    return pipe, metrics


def main(seed: int, test_size: float = 0.25):
    set_seed(seed)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Run `python data/create_dataset.py` first."
        )

    # Synthetic placeholder data to validate the reproducibility stack.
    # This is not real ENDES microdata and must not be interpreted as real
    # evidence about anemia in Peru.
    df = pd.read_csv(DATA_PATH)
    X_train, X_test, y_train, y_test = prepare_split(df, seed=seed, test_size=test_size)

    models = {
        "logreg": LogisticRegression(max_iter=1000, solver="lbfgs", random_state=seed),
        "random_forest": RandomForestClassifier(
            n_estimators=250, min_samples_leaf=5, random_state=seed
        ),
    }

    fitted = {}
    results = []

    for name, model in models.items():
        fitted_model, metrics = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        fitted[name] = fitted_model
        results.append(metrics)
        print(
            f"[{name}] seed={seed} "
            f"AUC-ROC={metrics['auc_roc']:.4f} "
            f"PR-AUC={metrics['pr_auc']:.4f} "
            f"Accuracy={metrics['accuracy']:.4f} "
            f"F1={metrics['f1']:.4f} "
            f"Recall={metrics['recall']:.4f}"
        )

    return fitted, results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--test_size", type=float, default=0.25)
    args = parser.parse_args()
    main(seed=args.seed, test_size=args.test_size)
