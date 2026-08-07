# Validated Execution Environment

## Reference software

This revision was executed in a clean local Python 3.12.13 environment using pandas 2.2.2, scikit-learn 1.5.2, MLflow 2.19.0, and the dependencies pinned in `05_pipeline/requirements.txt`. The Docker image targets Python 3.11; the public-source workflow is intended to be compatible with Python 3.11 or later. The analysis, experiment, and fairness scripts are rerun when a published code or dependency change requires new output evidence.

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

Pinned libraries and five prespecified random splits make the workflow inspectable within the documented environment. Minor differences can still arise across operating systems or low-level numerical libraries, particularly for tree ensembles. The repository therefore records the dataset SHA-256, split seed, parameters, and metrics in portable CSV summaries instead of treating one metric value as portable proof of model quality. A clean clone retrieves public official ENDES archives through `data/download_endes.py`; no Google Drive credential is required. Docker remains a separate check because it requires a Docker-enabled machine.
