# Reproducible ENDES Pipeline

This folder contains the technical component of the child anemia study. It builds a de-identified analytical CSV from official ENDES 2019-2024 modules, produces weighted descriptive summaries, and runs small exploratory classification experiments. The models are for reproducibility practice only. They are not clinical tools and must not be used to diagnose, triage, or make decisions about children, families, or territories.

## What each file does

| Path | Role |
|---|---|
| `src/build_endes_dataset.py` | Reads untouched ENDES archives from `data/raw/`, joins modules, removes direct survey identifiers, and builds the processed CSV. |
| `src/analyze_endes.py` | Produces weighted annual and residence summaries plus a trend figure. |
| `src/train.py` | Defines leakage-aware preprocessing and two exploratory models. |
| `src/run_experiments.py` | Runs five fixed seeds for logistic regression and random forest and logs parameters, metrics, data hash, and Git commit in MLflow. |
| `notebook.ipynb` | Colab-oriented walkthrough of the same workflow. |
| `docs/` | Human-readable analysis results and experiment table generated from the real CSV. |
| `data/README.md` | Session 5 compatibility note pointing to the canonical repository-level DVC data contract. |
| `Dockerfile` and `requirements.txt` | Compatibility entry points for the course layout; the canonical environment files remain at the repository root. |

## Reference environment

Use Python **3.11**. The pinned dependencies are at the repository root in `requirements.txt`; `Dockerfile` uses the same Python version.

```powershell
uv venv --python 3.11 .venv
uv pip install --python .venv -r requirements.txt
```

## Reproduce locally

1. Follow [`data/DVC_ACCESS.md`](../data/DVC_ACCESS.md) to configure a local service account with access to the shared Google Drive folder. Do not put a Google token or a credential file in Git.

2. Retrieve the source archives and analytical output.

```powershell
.\.venv\Scripts\dvc pull
```

3. Reproduce the pipeline. Activate the environment first so `dvc repro` uses its Python interpreter.

```powershell
.\.venv\Scripts\Activate.ps1
dvc repro
```

This rebuilds `data/processed/endes_anemia_children_2019_2024.csv`, updates the data metadata, writes descriptive outputs in `05_pipeline/docs/`, and reruns the fixed-seed experiments.

4. Inspect the results.

```powershell
Get-Content .\05_pipeline\docs\analysis_report.md
Get-Content .\05_pipeline\docs\experiment_results.csv
```

5. Open MLflow.

```powershell
mlflow ui --backend-store-uri .\mlruns
```

Then open `http://127.0.0.1:5000` in a browser.

## Google Colab route

Open the notebook from the current project branch:

[Open in Colab](https://colab.research.google.com/github/kedec123/deivhy-torres-vargas-unmsm/blob/feature/endes-course-completion/05_pipeline/notebook.ipynb)

Run each cell in order. The notebook clones the repository, installs the same root requirements, asks DVC to retrieve data, validates the CSV, runs the descriptive script and experiments, and shows the saved result tables. The first DVC request may open a Google sign-in flow. Use an account that has access to the project's shared Drive folder.

If a Colab runtime reports dependency warnings after installation, use **Runtime -> Restart session**, then run the notebook from the beginning. Do not skip the data-retrieval and validation cells; otherwise variables loaded by earlier cells will be missing.

## DVC and MLflow evidence

`dvc.yaml` records the build, analysis, and experiment commands. `dvc.lock` records the exact data dependency state. The DVC remote URL is an access-controlled Google Drive folder ID in `.dvc/config`; authentication is local to each user. `mlruns/` is the canonical local MLflow store and is also DVC-managed because it contains generated tracking artifacts.

The source manifest gives the direct INEI download URL and SHA-256 checksum for every archive. `quality_checks.md` verifies the eligibility population, no duplicated analysis IDs, the intended age range, positive weights, and the legacy-versus-updated 2024 measurement boundary.

## Reproducibility safeguards

| Risk | Project control | Evidence to inspect |
|---|---|---|
| Data substitution | Archive checksums, DVC pointers, and a locked data-build stage. | `data/metadata/source_manifest.csv`, `data/raw.dvc`, and `dvc.lock`. |
| Identifier leakage | ENDES join keys are used only during construction and omitted from the analytical CSV. | `src/build_endes_dataset.py` and `data/metadata/analysis_population.md`. |
| Preprocessing leakage | Imputation, scaling, and encoding are fitted inside the training pipeline after the split. | `src/train.py`. |
| Unrecorded experiment choices | Five seeds, model names, metrics, data hash, and Git commit are logged in MLflow. | `src/run_experiments.py`, `mlruns.dvc`, and `docs/mlflow_runs.png`. |
| Definition drift in 2024 | The legacy category is retained for the historical series; the updated 2024 field is separate. | `data/metadata/quality_checks.md` and `docs/analysis_report.md`. |

The current internal experiment table records ten model-and-seed runs. It is useful for checking that the same pipeline executes under stated conditions. It is not an evaluation of clinical usefulness, a substitute for design-based public-health inference, or a model-selection contest for deployment.

## Expected outcome files

After a successful local reproduction, `05_pipeline/docs/` contains the weighted annual and residence tables, a trend figure, a plain-language analysis report, the ten-run experiment table, and an MLflow-run summary figure. `11_bias_audit/` contains a separate Adult Census benchmark audit and an ENDES subgroup diagnostic. The files are intentionally separated so that Adult Census fairness results are not misrepresented as ENDES results.

## Docker status

The root `Dockerfile` and `docker-compose.yml` document the same Python 3.11 environment. Build from the repository root:

```powershell
docker build -t endes-anemia-pipeline .
docker run -it --rm -v "${PWD}:/project" endes-anemia-pipeline
```

Inside the container, configure DVC credentials locally, run `dvc pull`, then run `dvc repro`. `docker compose up` starts a Jupyter workbench on port 8888 and MLflow on port 5000. See [`docs/environment.md`](docs/environment.md) for the recorded workstation and [`docs/reproduction_checklist.md`](docs/reproduction_checklist.md) for the final stranger test.

Docker is not available in the current workstation environment, so a container run must still be verified on a machine with Docker before final submission. This limitation is stated openly rather than treated as a completed test.
