# 05_pipeline — Reproducible ENDES workflow

This is the technical component of the study of child anemia in Peru. Its main contribution is a weighted repeated cross-sectional analysis of ENDES 2019-2024; the classifier is a separate, exploratory learning exercise and is not clinical decision support.

## Reproduce from a clean clone — no credential required

The default route rebuilds the analytical CSV from the official public ENDES archives. It requires network access and local disk space for the 18 downloaded ZIP files, but no Google, DVC or service-account credential.

```powershell
cd 05_pipeline
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python data\download_endes.py
.\.venv\Scripts\python data\create_dataset.py
.\.venv\Scripts\python data\verify_dataset.py
.\.venv\Scripts\python src\analyze_endes.py
.\.venv\Scripts\python src\survey_analysis.py
.\.venv\Scripts\python src\sensitivity_2024.py
.\.venv\Scripts\python src\run_experiments.py
```

`data/download_endes.py` downloads every archive listed in `docs/source_manifest.csv`, verifies its SHA-256, and never accepts an archive whose checksum differs from the committed manifest. `create_dataset.py` then performs the documented temporary join, removes direct ENDES keys and recreates the de-identified CSV. The expected analytical CSV checksum is recorded in `data/endes_anemia_children_2019_2024.csv.dvc`.

## Analysis outputs

- `docs/analysis_by_year_with_ci.csv`: primary annual prevalence estimates with Taylor-linearized design-based 95% intervals using ENDES weights, strata and PSUs.
- `docs/analysis_by_year_bootstrap_ci.csv`: stratified-cluster bootstrap sensitivity intervals.
- `docs/analysis_ci_method_comparison.csv`: direct comparison of the two interval methods.
- `docs/modelled_year_effects_vs_2019.csv`: adjusted, model-based year effects against the 2019 reference year. These are associations, not causal effects.
- `docs/sensitivity_2024.csv`: separate comparison of legacy `HW57` and updated `HW57A` definitions in 2024.
- `docs/fieldwork_context_2020.md`: official collection-context note used to avoid over-reading the 2020 point estimate.

The annual trend uses legacy `HW57` for all six years to preserve internal measurement comparability. The updated 2024 definition is never mixed into the historical series.

## DVC and MLflow

The `.dvc` pointer remains in the repository as a compact version record for the analytical CSV. No shared DVC remote is committed and `dvc pull` is not the reviewer route; project owners may configure a private cache locally if useful. No credential, token or local configuration file belongs in Git.

`.mlruns/` is deliberately local and ignored because MLflow embeds machine-specific paths. Running `src/run_experiments.py` recreates a local tracking store with the same three models and five prespecified stratified 80/20 splits (15 runs). The portable evidence committed to Git is `docs/experiment_results.csv` and `docs/experiment_summary.csv`.

## Google Colab

Open `notebook.ipynb` in Colab. Its default route installs dependencies, downloads and verifies the public official archives only when the analytical CSV is absent, rebuilds the data, and then executes the documented analysis.

## Interpretation boundaries

- The design-based annual intervals quantify sampling uncertainty; the adjusted logistic model's intervals are model-based.
- ENDES 2020 collection was adapted during the COVID-19 emergency, including telephone interviews and a gradual return to in-person collection with biosecurity measures. The 2020 observation must not be over-read as a definitive epidemiological change.
- No analysis here diagnoses children, ranks people or communities, estimates clinical utility, or establishes a causal effect.
