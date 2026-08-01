"""Train an exploratory, non-clinical anemia classification baseline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "endes_anemia_children_2019_2024.csv"
NUMERIC_FEATURES = ["age_months", "mother_education_code", "wealth_quintile"]
CATEGORICAL_FEATURES = ["child_sex_code", "residence_code", "department_code", "survey_year"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def load_training_data(path: Path = DATA_PATH) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype={"department_code": "string"})
    required = FEATURES + ["anemia_legacy", "survey_weight", "analysis_id"]
    return frame.dropna(subset=["anemia_legacy", "survey_weight"])[required].copy()


def build_pipeline(model_name: str, seed: int) -> Pipeline:
    numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("encode", OneHotEncoder(handle_unknown="ignore"))])
    preprocessor = ColumnTransformer([("numeric", numeric, NUMERIC_FEATURES), ("categorical", categorical, CATEGORICAL_FEATURES)])
    if model_name == "logistic_regression":
        model = LogisticRegression(max_iter=2000, random_state=seed, class_weight="balanced")
    elif model_name == "random_forest":
        model = RandomForestClassifier(n_estimators=300, min_samples_leaf=8, random_state=seed, n_jobs=-1, class_weight="balanced")
    else:
        raise ValueError("model_name must be 'logistic_regression' or 'random_forest'")
    return Pipeline([("preprocess", preprocessor), ("model", model)])


def evaluate_model(frame: pd.DataFrame, model_name: str, seed: int, test_size: float = 0.25) -> tuple[dict, pd.DataFrame]:
    train, test = train_test_split(frame, test_size=test_size, random_state=seed, stratify=frame["anemia_legacy"])
    pipeline = build_pipeline(model_name, seed)
    pipeline.fit(train[FEATURES], train["anemia_legacy"], model__sample_weight=train["survey_weight"])
    probabilities = pipeline.predict_proba(test[FEATURES])[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "seed": seed,
        "model": model_name,
        "sample_size": len(frame),
        "test_size": len(test),
        "auc_roc": roc_auc_score(test["anemia_legacy"], probabilities),
        "pr_auc": average_precision_score(test["anemia_legacy"], probabilities),
        "accuracy": accuracy_score(test["anemia_legacy"], predictions),
        "f1": f1_score(test["anemia_legacy"], predictions),
        "recall": recall_score(test["anemia_legacy"], predictions),
    }
    prediction_frame = test[["analysis_id", "anemia_legacy", "survey_weight", "child_sex_code", "residence_code", "department_code", "survey_year"]].copy()
    prediction_frame["predicted_probability"] = probabilities
    prediction_frame["predicted_label"] = predictions
    return metrics, prediction_frame


def main() -> None:
    data = load_training_data()
    for model_name in ("logistic_regression", "random_forest"):
        metrics, _ = evaluate_model(data, model_name, seed=42)
        formatted = " ".join(f"{key}={value:.4f}" for key, value in metrics.items() if isinstance(value, float))
        print(f"{model_name}: {formatted}")


if __name__ == "__main__":
    main()
