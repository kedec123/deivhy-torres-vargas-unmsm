# Child Anemia Peru - Reproducible Baseline Pipeline

Reproducible baseline pipeline for the child anemia project in Peru.

**Author:** Deivhy Torres  
**Course:** Research Methods and Scientific Integrity in AI and Advanced Technologies - UNMSM

## Purpose of this folder

This folder is the Session 5 technical artifact. It demonstrates the reproducibility stack required by the course using a small **synthetic ENDES-like dataset** rather than real ENDES microdata.

Its job is modest but important: show that the project can track data, record experiments, document the environment, and be rerun in a clean, explicit workflow.

## Recommended environment

The recommended environment for this artifact is **Google Colab**, because that is the classroom workflow used in the course. Local execution is still possible and documented below, but Colab is the main presentation path for this repository.

Open the notebook directly in Colab:

[Open in Colab](https://colab.research.google.com/github/kedec123/deivhy-torres-vargas-unmsm/blob/main/05_pipeline/notebook.ipynb)

## What is included

- `data/create_dataset.py` - creates the synthetic dataset
- `data/anemia_peru_synthetic.csv.dvc` - DVC pointer for the tracked dataset
- `src/train.py` - runs one baseline experiment
- `src/run_experiments.py` - runs the multi-seed experiment set and logs results
- `docs/experiment_results.csv` - saved experiment summary
- `notebook.ipynb` - Colab-friendly notebook for setup, inspection, and demonstration
- `mlruns/` - MLflow tracking output already generated for the current baseline
- `Dockerfile` - environment description for container-based reproduction

## Important limitation

`data/anemia_peru_synthetic.csv` is a synthetic teaching dataset. It is useful for reproducibility practice only. It must not be treated as evidence about real anemia prevalence in Peru.

## Google Colab workflow

This is the simplest way to show the Session 5 artifact in class or in a review:

1. Open `05_pipeline/notebook.ipynb` from GitHub or by using the Colab link above.
2. Run the setup cells that clone the repository and install dependencies.
3. Move into the `05_pipeline/` folder inside the Colab runtime.
4. Run the notebook cells that inspect the synthetic dataset and saved experiment results.
5. If needed, run the training script or the multi-seed experiment script from within the notebook.

If you want visible evidence for the deliverable, Colab execution can be shown through:

- saved notebook outputs,
- `docs/experiment_results.csv`,
- the `mlruns/` folder already committed in the repository,
- optional screenshots from the MLflow UI.

## How to add a notebook to this folder

If you create or update a notebook in Colab, use **File -> Save a copy in GitHub** and select this repository plus the path `05_pipeline/notebook.ipynb`. If GitHub save is not available, download the notebook as `.ipynb` and place it in this same folder before committing and pushing.

## Local reproduction workflow

Recommended on Windows: use Python 3.12.

1. Create the environment

```bash
uv venv --python 3.12 .venv
```

2. Install dependencies

```bash
uv pip install --python .venv -r requirements.txt
```

If Google Colab shows a warning about preinstalled packages, restart the runtime once after installation and then run the notebook again from the top.

3. Recover or regenerate the dataset

If the dataset is already available locally, you can keep it as is. If you want to regenerate the synthetic file from scratch:

```bash
.\.venv\Scripts\python data/create_dataset.py
```

If you prefer to pull the tracked artifact through DVC after configuring authentication:

```bash
.\.venv\Scripts\dvc pull
```

4. Run one baseline model training

```bash
.\.venv\Scripts\python src/train.py --seed 42
```

5. Run the full experiment set and generate MLflow runs

```bash
.\.venv\Scripts\python src/run_experiments.py
```

6. Open the MLflow UI

```bash
.\.venv\Scripts\mlflow ui --backend-store-uri .\mlruns
```

Then open `http://127.0.0.1:5000`.

## DVC configuration

This project is prepared to use **Google Drive** as the DVC remote target. The current remote points to a personal Google Drive path so the owner can authenticate and push or pull data from the same account.

Before final course submission to an external reviewer, this should be upgraded to a **shared Google Drive folder ID**, because that is more appropriate for multi-user access than a personal `root` path.

If authentication is needed for the first time, DVC will prompt for browser-based authorization. Credentials should stay local and must not be committed.

## Current baseline

The current baseline uses two simple models:

- logistic regression
- random forest

The current saved run summary covers 5 seeds (`13, 21, 42, 87, 100`) and is stored in `docs/experiment_results.csv`.

## Docker note

The Dockerfile is included to meet the course reproducibility requirements and to document the intended environment. In this machine, Docker could not be validated locally because Docker is not installed, so container execution remains a documented path rather than a verified one.
