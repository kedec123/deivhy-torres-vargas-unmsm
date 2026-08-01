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


def test_course_completion_structure_and_reproducibility_guards():
    required_paths = [
        "03_protocol/protocol_v2.0.md",
        "03_protocol/pre_submission_checklist.md",
        "03_protocol/target_venue_analysis.md",
        "05_pipeline/Dockerfile",
        "05_pipeline/data/README.md",
        "05_pipeline/docs/environment.md",
        "05_pipeline/docs/reproduction_checklist.md",
        "06_repro_audit/reproducibility_audit.md",
        "07_model_card/model_card.md",
        "07_model_card/datasheet.md",
        "09_ethics/ethics_protocol.md",
        "10_data_mgmt/data_management_plan.md",
        "11_bias_audit/bias_label_baseline.csv",
        "12_integrity/ai_prompt_log/README.md",
        "14_peer_review/peer_reviews/review_form_1.md",
        "14_peer_review/peer_reviews/review_form_2.md",
        "reflections/reflective_log.md",
        "docker-compose.yml",
    ]
    assert all((ROOT / relative_path).exists() for relative_path in required_paths)
    assert "always_changed" not in (ROOT / "dvc.yaml").read_text(encoding="utf-8")
    assert "synthetic" not in (ROOT / "05_pipeline" / "README.md").read_text(encoding="utf-8").lower()
