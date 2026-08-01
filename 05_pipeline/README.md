# 05_pipeline - Reproducible ENDES Workflow

This folder contains the technical component of the child-anemia study. It builds a de-identified analytical CSV from official ENDES 2019-2024 modules, produces weighted descriptive summaries, and records fixed-seed exploratory models in MLflow. The model is a course exercise, not a clinical tool.

## Folder map

| Path | Purpose |
|---|---|
| `.dvc/` | DVC configuration. The remote identifier is public; credentials remain local. |
| `data/create_dataset.py` | Builds the analytical CSV from untouched ENDES source archives. |
| `data/endes_anemia_children_2019_2024.csv.dvc` | DVC pointer to the de-identified analytical CSV. |
| `data/raw/` | Local ENDES archives. This directory is never committed to Git. |
| `src/analyze_endes.py` | Creates weighted descriptive tables, a trend figure, and a plain-language report. |
| `src/train.py` | Defines leakage-aware preprocessing and the exploratory models. |
| `src/run_experiments.py` | Runs five fixed seeds, records parameters and metrics in MLflow, and saves the summary chart. |
| `docs/` | Source manifest, variable dictionary, quality checks, descriptive output, and experiment results. |
| `notebook.ipynb` | Google Colab walkthrough of the same workflow. |
| `mlruns/` | Local MLflow tracking store created when experiments run. |

## Dataset and interpretation boundary

The analytical file contains one de-identified row per eligible child aged 6-35 months in ENDES 2019-2024. Construction temporarily joins `REC44`, `REC21`, and `REC0111` using ENDES keys, then excludes those direct keys from the released CSV. `docs/source_manifest.csv`, `docs/data_dictionary.csv`, `docs/analysis_population.md`, and `docs/quality_checks.md` record the source, variables, population, and checks.

The primary outcome is the legacy ENDES anemia category (`HW57`) so that the 2019-2024 series uses one internally consistent definition. The newer 2024 fields are retained only for a sensitivity discussion. No result in this repository should be read as the current official prevalence figure under the revised 2024 definition.

## Run locally

Use Python 3.11. From this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\dvc pull
.\.venv\Scripts\python src\analyze_endes.py
.\.venv\Scripts\python src\run_experiments.py
.\.venv\Scripts\mlflow ui --backend-store-uri .\mlruns
```

Open `http://127.0.0.1:5000` to inspect the local MLflow runs.

The DVC remote is a shared Google Drive folder. Do not commit a token or a credential file. If Google's shared OAuth application is blocked, create a service account in a private Google Cloud project, share the Drive folder with that account, and configure its JSON key locally:

```powershell
.\.venv\Scripts\dvc remote modify storage --local gdrive_use_service_account true
.\.venv\Scripts\dvc remote modify storage --local gdrive_service_account_json_file_path "C:\path\to\service-account.json"
```

## Google Colab

Open [`notebook.ipynb`](notebook.ipynb) in Colab and run the cells from the beginning. The notebook installs the dependencies, retrieves the DVC data, validates the CSV, creates descriptive outputs, and runs the fixed experiment set. If Colab asks for a restart after installing packages, restart the runtime and rerun from the first cell.

## Docker

Build from this folder:

```powershell
docker build -t endes-anemia-pipeline .
docker run -it --rm -v "${PWD}:/project" endes-anemia-pipeline
```

Inside the container, configure DVC credentials locally and run the same commands listed above. Docker is not installed on the workstation used for this repository, so a container execution must still be checked on a Docker-enabled machine.
