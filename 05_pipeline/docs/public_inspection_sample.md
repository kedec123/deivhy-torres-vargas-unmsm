# Public Inspection Sample

The repository includes `../data/endes_anemia_children_2019_2024_sample.csv` so readers can inspect the analytical structure directly in GitHub. It contains 300 rows: 50 deterministically selected records from each ENDES year between 2019 and 2024.

The sample excludes the project-generated `analysis_id`, cluster code, and stratum code. It preserves the remaining analytical columns so the documented variable definitions can be checked against a real CSV structure.

This file is a teaching and inspection artefact. It is not a representative extract, must not be used to calculate prevalence, and must not be used to train or evaluate a model. The full de-identified analytical CSV remains separately versioned; its metadata and provenance are documented in the DVC record, source manifest, data dictionary, and quality checks.
