# Child Anemia in Peru: ENDES 2019-2024

**Author:** Deivhy Torres Vargas<br>
**Course:** Research Methods and Scientific Integrity in AI and Advanced Technologies, UNMSM<br>
**Study focus:** Trends and factors associated with anemia among children aged 6-35 months in Peru.

## Project in one paragraph

This repository develops a reproducible secondary analysis of anonymized ENDES microdata. The main study asks how legacy-comparable anemia prevalence changed between 2019 and 2024 and how it was distributed by child, maternal, household, and territorial characteristics. It is a population-level descriptive and associative study, not a causal evaluation or a clinical prediction system.

The project also documents the methodological and integrity work requested in the course: a paradigm statement, a method choice, protocol versions, an auditable literature review, a reproducible data pipeline, an ethics and data-management plan, a model card, and a separate fairness exercise. The folders follow the course sequence so the research argument can be read from beginning to end.

## Repository map

| Folder | Purpose |
|---|---|
| `01_paradigm/` | Quantitative paradigm justification and research question. |
| `02_method/` | E.D.F.C.V. comparison of three candidate methods. |
| `03_protocol/` | The short outline (`v0.1`), full first draft (`v1.0`), v2.0 response template, venue analysis, and pre-submission checklist. |
| `04_literature/` | Search records, screening log, PRISMA flow, included studies, and gap analysis. |
| `05_pipeline/` | Scripts, Colab notebook, compatibility files, results, environment record, and instructions for the ENDES workflow. |
| `06_repro_audit/` to `12_integrity/` | Reproducibility, documentation, ethics, data stewardship, fairness, and integrity materials. |
| `14_peer_review/` and `reflections/` | Templates that must be completed with real peer feedback and the author's own reflection. |
| `data/` | Data contract and DVC-managed ENDES source archives and processed analytical CSV. |

## Data and reproducibility

The analysis-ready file is `data/processed/endes_anemia_children_2019_2024.csv`. It contains one de-identified row for every eligible child aged 6-35 months in the official ENDES modules for 2019-2024. Original archives and the processed CSV are managed with DVC; Git stores their metadata, code, and DVC lock information rather than the data files themselves.

The DVC remote is a shared Google Drive folder. No credentials are committed. Because Google can block DVC's shared OAuth client, the documented project route is a local service-account configuration; see [`data/DVC_ACCESS.md`](data/DVC_ACCESS.md). The source manifest, data dictionary, population definition, and build checks are in `data/metadata/`.

## Reproduce the technical workflow

Python 3.11 is the reference environment. Google Colab is the recommended classroom route; open [`05_pipeline/notebook.ipynb`](05_pipeline/notebook.ipynb) and run it from the beginning after requesting access to the DVC Drive folder.

For local work on Windows:

```powershell
uv venv --python 3.11 .venv
uv pip install --python .venv -r requirements.txt
.\.venv\Scripts\dvc pull
.\.venv\Scripts\dvc repro
.\.venv\Scripts\mlflow ui --backend-store-uri .\mlruns
```

The final command opens the local MLflow interface at `http://127.0.0.1:5000`. Full commands, expected outputs, recorded hardware, Docker Compose option, and the final stranger-test checklist are documented in [`05_pipeline/README.md`](05_pipeline/README.md).

## Scope and responsible use

The primary outcome uses the legacy ENDES anemia category (`HW57`) across all six years to keep the historical series internally comparable. ENDES 2024 also includes new fields aligned with the updated guideline; those are retained only for a sensitivity check and are not mixed into the primary trend. Therefore, the repository does not present its legacy 2024 estimate as the current official national figure.

The model is an exploratory learning exercise. It must not be used for diagnosis, triage, eligibility decisions, or ranking children, households, departments, or communities. Before submission, the author must complete the remaining real peer reviews and reflective log, add the instructor as a repository collaborator using the account provided in class, verify DVC access from a clean clone, and create the final tag.
