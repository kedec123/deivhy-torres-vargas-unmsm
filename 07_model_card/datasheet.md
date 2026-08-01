# Datasheet for the ENDES Analytical CSV

## Motivation and composition

`endes_anemia_children_2019_2024.csv` is a project-specific, de-identified analytical file built from the anonymous public-use ENDES modules. It contains one row per eligible child aged 6-35 completed months with a valid legacy anemia category, covering 2019-2024. The build currently produces 57,539 rows.

## Collection and processing

The source is the official INEI ENDES microdata catalogue. For each year, the pipeline reads the child haemoglobin module (`REC44`), birth history (`REC21`), and mother/household module (`REC0111`). The original archives are kept unchanged under DVC. They are joined temporarily using ENDES keys, then the keys are excluded. A project-generated `analysis_id` is not an ENDES identifier and is only a reproducibility label.

## Variables and labels

The primary label is `anemia_legacy`, derived from `HW57`: categories 1-3 are coded as anemia and category 4 as no anemia. The data dictionary gives every variable, source field, coding boundary, and intended analytical role. `HW57A` and `HW56A` are retained for the 2024 sensitivity discussion only.

## Recommended use

Use the CSV for documented descriptive and exploratory association analyses inside this repository. Consult `analysis_population.md`, `quality_checks.md`, and the source manifest before analysis. Use weights and design variables appropriately for population inference.

## Prohibited or cautionary use

Do not attempt to re-identify a child, link the file to external individual-level records, or treat it as a clinical registry. Do not combine the primary legacy outcome with the 2024 updated outcome as if they were one unbroken measure. Do not infer individual causation from cross-sectional associations.

## Maintenance and distribution

Data files are DVC-managed in an access-controlled Google Drive remote. Git retains code and metadata. Access should be granted only to authorised course collaborators, and any release outside that group must be checked against the INEI terms and the project data-management plan.
