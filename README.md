# Child Anemia in Peru

Doctoral course project for *Research Methods and Scientific Integrity in AI and Advanced Technologies* at UNMSM.

**Author:** Deivhy Torres Vargas
**Topic:** Weighted trends and observed inequalities in anemia among Peruvian children aged 6-35 months, using anonymous ENDES microdata from 2019 to 2024.

## Repository Structure

- `01_paradigm/` - Quantitative paradigm justification (Session 1).
- `02_method/` - Method-Fit Matrix (Session 2).
- `03_protocol/` - Research protocol drafts v0.1 and v1.0 (Session 3).
- `04_literature/` - Focused systematic review, PRISMA diagram, and gap analysis (Session 4).
- `05_pipeline/` - Reproducible ENDES workflow with DVC, MLflow, Docker, and a Colab notebook (Session 5).
- `06_repro_audit/` - Reproducibility audit of an accessible health-ML article (Session 6).
- `07_model_card/` - Model card and datasheet (Session 7).
- *(Session 8 is an integration checkpoint; its feedback is incorporated into the protocol.)*
- `09_ethics/` - Ethics protocol for anonymous secondary data (Session 9).
- `10_data_mgmt/` - Data management plan (Session 10).
- `11_bias_audit/` - Reproducible fairness exercise and its mitigation comparison (Session 11).
- `12_integrity/` - Retraction analysis and project AI-use policy (Session 12).

## Reproduce the Pipeline

See [`05_pipeline/README.md`](05_pipeline/README.md) for the complete workflow. The short local route is:

```powershell
cd 05_pipeline
python -m pip install -r requirements.txt
dvc pull
python src/run_experiments.py
```

The project uses a de-identified analytical CSV. It is for population-level description and an exploratory reproducibility exercise, not for diagnosis, triage, or decisions about children, families, or territories.

A public 300-row inspection sample is available at [`05_pipeline/data/endes_anemia_children_2019_2024_sample.csv`](05_pipeline/data/endes_anemia_children_2019_2024_sample.csv). It is provided only to make the dataset structure visible in GitHub; it is not used for analysis, prevalence estimates, or model training.

## Reproduce the Bias Audit

See [`11_bias_audit/bias_audit_report.md`](11_bias_audit/bias_audit_report.md). The fairness exercise uses the Adult Census benchmark, not ENDES, and its results must not be transferred to health decisions.
