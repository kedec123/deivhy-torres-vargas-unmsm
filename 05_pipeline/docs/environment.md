# Recorded Execution Environment

## Reference software

The pipeline was executed locally on 31 July 2026 using Python 3.11.15, pandas 2.2.2, scikit-learn 1.5.2, MLflow 2.19.0, and DVC 3.55.2. The exact pins are in the repository-level `requirements.txt`.

## Workstation used for the recorded outputs

| Item | Recorded value |
|---|---|
| Operating system | Windows 11 Home, 64-bit, version 10.0.26200 |
| CPU | Intel Core i7-9750H, 6 cores / 12 logical processors |
| Installed memory | 32 GB |
| GPU present | NVIDIA GeForce RTX 2060, approximately 4 GB adapter memory |
| Compute actually used | CPU; the ENDES scripts do not require GPU acceleration |

The GPU is listed for transparency only. It was not used to produce the documented analysis or experiment outputs. Docker was not installed on this workstation, so container execution remains a required final verification on a Docker-enabled machine.

## Expected variation

Fixed seeds and pinned libraries make the workflow reproducible within the documented environment. Minor differences can still arise across operating systems or low-level numerical libraries, particularly for random forest. The repository therefore records the dataset SHA-256, Git commit, seed, parameters, and metrics for each MLflow run instead of treating one metric value as portable proof of model quality.
