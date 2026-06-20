# Child Anemia Peru - Reproducible Baseline Pipeline

Reproducible baseline pipeline for the child anemia project in Peru.

**Author:** Deivhy Torres  
**Course:** Research Methods and Scientific Integrity in AI and Advanced Technologies - UNMSM

## What this is

This folder provides a small, reproducible analytical baseline for the doctoral project. It does **not** use real ENDES microdata yet. Instead, it uses a **synthetic ENDES-like dataset** designed to resemble plausible child, maternal, household, and territorial variables related to anemia in Peru.

The goal is to validate the reproducibility workflow itself:

- version control with Git
- data snapshot logic with DVC
- experiment tracking with MLflow
- environment portability with Docker

## Important note

The file `data/anemia_peru_synthetic.csv` is fully synthetic and exists only for methodological demonstration. It must **never** be interpreted as real national evidence about anemia prevalence or policy impact.

## Project structure

- `data/create_dataset.py` - generates the synthetic ENDES-like dataset
- `data/anemia_peru_synthetic.csv` - current synthetic snapshot
- `data/anemia_peru_synthetic.csv.dvc` - DVC pointer for the dataset snapshot
- `src/train.py` - trains baseline models and reports metrics
- `src/run_experiments.py` - runs the pipeline across multiple random seeds
- `docs/experiment_results.csv` - saved experiment summary
- `requirements.txt` - Python dependencies
- `Dockerfile` - portable container environment

## Reproduce the baseline

Recommended on Windows: use Python 3.12 for the smoothest MLflow setup.

1. Create the virtual environment
```bash
uv venv --python 3.12 .venv
```

2. Install dependencies
```bash
uv pip install --python .venv -r requirements.txt
```

3. Regenerate the synthetic dataset if needed
```bash
.\.venv\Scripts\python data/create_dataset.py
```

4. Run one baseline experiment
```bash
.\.venv\Scripts\python src/train.py --seed 42
```

5. Run all experiments and create `mlruns/`
```bash
.\.venv\Scripts\python src/run_experiments.py
```

## Expected behavior

The script trains:

- a logistic regression baseline
- a random forest comparison model

Both models predict the probability of anemia from synthetic variables such as:

- child age in months
- rural residence
- household wealth
- maternal education
- recent iron supplementation
- recent diarrhea
- safe water access
- region and altitude

## Current experiment summary

The current synthetic baseline was run across 5 seeds (`13, 21, 42, 87, 100`) and the results were saved to `docs/experiment_results.csv`.

Average performance across seeds:

| Model | AUC-ROC | PR-AUC | Accuracy | F1 | Recall |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6484 | 0.6017 | 0.6080 | 0.5634 | 0.5383 |
| Random Forest | 0.6251 | 0.5850 | 0.5913 | 0.5509 | 0.5340 |

## MLflow

If `mlflow` is installed, `src/run_experiments.py` logs each run automatically inside `05_pipeline/mlruns/`.

By default, the script logs parameters and metrics. Model artifact logging is disabled by default to keep the classroom setup lightweight on Windows. If you want model files too, run:
```bash
$env:MLFLOW_LOG_MODELS="1"
.\.venv\Scripts\python src/run_experiments.py
```

To inspect runs:
```bash
.\.venv\Scripts\mlflow ui --backend-store-uri .\mlruns
```

Then open:
`http://127.0.0.1:5000`

If MLflow is not installed, the experiments still run and save a CSV summary in `docs/experiment_results.csv`.

## DVC note

This repository includes a small synthetic CSV for transparency and ease of classroom review. In a real research workflow, cleaned ENDES extracts or derived analytical tables should be stored through a proper DVC remote, not committed directly to Git.
