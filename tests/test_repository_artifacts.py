from pathlib import Path

import nbformat
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_notebook_is_valid_and_contains_real_data_workflow():
    notebook_path = ROOT / "05_pipeline" / "notebook.ipynb"
    notebook = nbformat.read(notebook_path, as_version=4)
    nbformat.validate(notebook)
    source = "\n".join("".join(cell.source) for cell in notebook.cells)
    assert "dvc pull" in source
    assert "anemia_peru_synthetic" not in source
    assert "analyze_endes.py" in source
    assert "run_experiments.py" in source


def test_literature_screening_and_prisma_counts_agree():
    screening = pd.read_csv(ROOT / "04_literature" / "screening_log.csv")
    assert (screening["decision"] == "included").sum() == 10
    assert (screening["decision"] == "excluded").sum() == 2
    assert len(screening) == 12
    assert (ROOT / "04_literature" / "prisma_diagram.svg").exists()
    assert (ROOT / "04_literature" / "prisma_diagram.png").stat().st_size > 1_000


def test_source_manifest_covers_three_modules_per_year():
    manifest = pd.read_csv(ROOT / "data" / "metadata" / "source_manifest.csv")
    assert len(manifest) == 18
    assert manifest.groupby("survey_year")["module"].nunique().eq(3).all()
    assert manifest["sha256"].str.fullmatch(r"[0-9a-f]{64}").all()
