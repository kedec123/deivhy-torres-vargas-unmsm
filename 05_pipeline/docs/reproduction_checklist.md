# Stranger-Test Checklist

Use this checklist from a clean clone before presenting the repository as fully reproducible.

- [ ] Clone the repository and switch to the intended commit or release tag.
- [ ] Create a Python 3.11 environment and install `05_pipeline/requirements.txt`.
- [ ] Configure the local-only Google Drive service-account settings described in `05_pipeline/README.md`.
- [ ] Run `dvc pull` and confirm that `data/endes_anemia_children_2019_2024.csv` is restored and matches its DVC pointer. The original ENDES archives are obtained separately from INEI and remain local in `data/raw/`.
- [ ] Run `python src/analyze_endes.py` and `python src/run_experiments.py`, then compare the regenerated descriptive and experiment outputs with the committed summaries.
- [ ] Open MLflow with `mlflow ui --backend-store-uri .\\mlruns` and inspect the ten fixed-seed runs.
- [ ] Build the image with `docker build -t endes-anemia-pipeline .` and repeat at least the descriptive command in the container.
- [ ] Record the operating system, Python version, package versions, and any numerical differences found.

At the time of the latest repository update, local execution checks passed. The shared Drive transfer and Docker build are deliberately left unchecked until the repository owner configures a private Google service-account key and uses a Docker-enabled machine.
