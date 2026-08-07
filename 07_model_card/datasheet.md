# Datasheet for the ENDES Analytical CSV

## Motivation and composition

`endes_anemia_children_2019_2024.csv` is a project-specific, de-identified analytical file built from the anonymous public-use ENDES modules. It contains one row per eligible child aged 6-35 completed months with a valid legacy anemia category, covering 2019-2024. The build currently produces 57,539 rows.

## Collection and processing

The source is the official INEI ENDES microdata catalogue. For each year, the pipeline reads the child haemoglobin module (`REC44`), birth history (`REC21`), and mother/household module (`REC0111`). The original archives remain unchanged in local `data/raw/` and are excluded from Git. They are joined temporarily using ENDES keys, then the keys are excluded. A project-generated `analysis_id` is not an ENDES identifier and is only a reproducibility label.

## Variables and labels

The primary label is `anemia_legacy`, derived from `HW57`: categories 1-3 are coded as anemia and category 4 as no anemia. The data dictionary gives every variable, source field, coding boundary, and intended analytical role. `HW57A` and `HW56A` are retained for the 2024 sensitivity discussion only.

## Recommended use

Use the CSV for documented descriptive and exploratory association analyses inside this repository. Consult `analysis_population.md`, `quality_checks.md`, and the source manifest before analysis. Use weights and design variables appropriately for population inference.

## Prohibited or cautionary use

Do not attempt to re-identify a child, link the file to external individual-level records, or treat it as a clinical registry. Do not combine the primary legacy outcome with the 2024 updated outcome as if they were one unbroken measure. Do not infer individual causation from cross-sectional associations.

## Maintenance and distribution

The de-identified analytical CSV is represented by a DVC pointer, while its reproducible construction uses public official ENDES archive URLs and committed SHA-256 checks. Git retains code, metadata and aggregate outputs; MLflow is recreated locally and is not committed because it embeds machine paths. Any release outside this documented workflow must still be checked against INEI terms and the project data-management plan.

## Dataset composition

| Aspect | Record |
|---|---|
| Unit of analysis | One eligible child record from the public-use survey modules |
| Time coverage | ENDES 2019-2024 |
| Eligibility | Age 6-35 completed months and a valid legacy `HW57` category |
| Records in current build | 57,539 |
| Direct identifiers in released CSV | None |
| Sampling-design fields retained | Normalized weight, cluster, and stratum |
| Geographic detail retained | Department code and urban-rural residence; no coordinate or household key |

The released analytical file is smaller than the source modules by design. It is not a replica of ENDES and it should not be used to reconstruct an ENDES respondent or household record.

## Processing decisions

The build reads the untouched archives, standardises field names in memory, joins the required modules on temporary ENDES keys, applies the age and outcome rules, derives the binary legacy outcome, and removes the join keys before writing the CSV. The source archives are not edited. `source_manifest.csv` records the archive checksum and transformation path, while `quality_checks.md` records the expected row count, age range, and basic contract checks.

No primary outcome value is imputed. Missing explanatory values remain available to the downstream training pipeline, where imputation is fitted within the training partition only. The processed file contains both legacy and updated 2024 measurement fields so that the difference can be inspected; only the legacy definition is used for the historical primary outcome.

## Collection context and representativeness

ENDES is a repeated household survey, not a clinical registry or a census. The dataset is appropriate for the specified survey population when weights and design information are handled correctly. It does not represent children outside the eligible age range, children missing a valid primary outcome, or every biological and service factor relevant to anemia. Annual prevalence uses Taylor-linearized design-based uncertainty with ENDES strata and primary sampling units, alongside a stratified-cluster bootstrap comparison. The adjusted association model remains model-based and non-causal.

## Sensitive use and distribution controls

Although the analytical CSV excludes direct identifiers, it remains research data. Users must not attempt re-identification, join it to external person-level data, publish small cells, or use it to label a family, community, or department as inherently high risk. The original archives stay local, the processed CSV is represented by its DVC pointer, and MLflow is regenerated locally. Any broader sharing requires a new review of INEI conditions, disclosure risk, and the data-management plan.
