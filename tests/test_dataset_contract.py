import importlib.util
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "endes_anemia_children_2019_2024.csv"


def test_processed_dataset_contract():
    data = pd.read_csv(DATA_PATH, dtype={"department_code": "string"})
    required = {
        "analysis_id",
        "survey_year",
        "age_months",
        "anemia_legacy",
        "child_sex_code",
        "mother_education_code",
        "wealth_quintile",
        "residence_code",
        "survey_weight",
        "cluster_code",
        "stratum_code",
        "department_code",
    }
    assert required.issubset(data.columns)
    assert data["analysis_id"].is_unique
    assert set(data["survey_year"].unique()) == {2019, 2020, 2021, 2022, 2023, 2024}
    assert data["age_months"].between(6, 35).all()
    assert set(data["anemia_legacy"].unique()) <= {0, 1}
    assert (data["survey_weight"] > 0).all()
    assert data["department_code"].nunique() == 25


def test_pipeline_scripts_import_without_side_effects():
    for name in ("build_endes_dataset", "analyze_endes", "train", "run_experiments"):
        path = ROOT / "05_pipeline" / "src" / f"{name}.py"
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
