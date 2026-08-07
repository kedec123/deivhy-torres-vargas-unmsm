# Stranger-Test Checklist

Use this checklist from a clean clone. The default route does not require DVC access, a Google login or a service-account key.

- [ ] Clone the repository and switch to the intended commit or release tag.
- [ ] Create a Python 3.11+ environment and install `05_pipeline/requirements.txt`.
- [ ] From `05_pipeline`, run `python data/download_endes.py`. Confirm that all 18 official archives pass their SHA-256 checks against `docs/source_manifest.csv`.
- [ ] Run `python data/create_dataset.py` and `python data/verify_dataset.py`. Confirm that the resulting CSV matches `data/endes_anemia_children_2019_2024.csv.dvc`.
- [ ] Run `python src/analyze_endes.py`, `python src/survey_analysis.py`, `python src/sensitivity_2024.py`, and `python src/run_experiments.py`.
- [ ] Confirm that `analysis_by_year_with_ci.csv` contains Taylor-linearized design-based intervals and that `analysis_ci_method_comparison.csv` contains the bootstrap comparison.
- [ ] Confirm that `modelled_year_effects_vs_2019.csv` has adjusted effects for 2020-2024 relative to 2019, labelled as model-based associations.
- [ ] Compare regenerated outputs with committed summaries. Small platform-level floating-point differences should be recorded, not hidden.
- [ ] Optionally open `mlflow ui --backend-store-uri .\.mlruns` locally after `run_experiments.py`; the store is intentionally not committed.

## DVC note

The DVC pointer records the expected checksum and file size of the analytical CSV. A project owner may configure a private local DVC cache, but it is not required for independent reproduction and no private remote or credential is part of this checklist.
