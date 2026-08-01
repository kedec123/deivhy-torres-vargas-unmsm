# Data Management Plan

## Data lifecycle

The project receives anonymous official ENDES module archives, creates a de-identified analysis file, and produces aggregate tables, figures, code, and MLflow tracking artifacts. The original archives remain local and are excluded from Git; the processed CSV is represented by a DVC pointer. Git holds code, metadata, checksums, aggregate outputs, and MLflow tracking records. The source manifest is the authoritative record of origin and transformation.

## Access and security

The DVC remote is a shared Google Drive folder managed by the repository owner. Access is limited to authorised course collaborators. Credentials stay in local DVC configuration and must never be committed. The repository currently contains no direct identifiers in the processed CSV, but it should still be treated as research data rather than redistributed casually.

## FAIR and documentation commitments

Findability is supported by stable file names, the source manifest, and Git history. Accessibility is controlled through DVC permissions. Interoperability comes from UTF-8 CSV, a machine-readable dictionary, and pinned software versions. Reuse is supported by a documented analytical population, reproducible build script, and explicit limitations.

## Legal and retention considerations

The project will follow the applicable conditions of INEI microdata access and the Peruvian Personal Data Protection Law (Law No. 29733). It will not attempt re-identification or use the data for a purpose outside this course protocol. The owner will retain the repository and DVC artefacts through course evaluation and any approved thesis extension, then archive or securely remove access according to institutional guidance and the source terms.

## Backup, versioning, and incident response

GitHub is the code and documentation history; DVC/Drive is the data-artifact store. Source checksums make accidental file substitution visible. If access is exposed, credentials will be revoked or rotated, the remote sharing list reviewed, and any affected collaborator notified. If a data-quality issue is found, it will be logged, fixed in a new commit, and connected to the relevant protocol or results revision.

## Data inventory and responsibility

| Asset | Location | Versioning method | Access level | Responsible action |
|---|---|---|---|---|
| Original ENDES archives | `05_pipeline/data/raw/` | Local files excluded from Git | Restricted to authorised collaborators | Preserve unchanged; verify checksum. |
| De-identified analytical CSV | `05_pipeline/data/` | DVC pointer and local cache | Restricted research use | Rebuild only through the documented script. |
| Metadata and data contract | `05_pipeline/docs/` | Git | Repository collaborators | Review when a field or rule changes. |
| Aggregate figures and tables | `05_pipeline/docs/` | Git | Repository readers | Regenerate after a documented code or data change. |
| MLflow tracking store | `05_pipeline/mlruns/` | Git-tracked experiment metadata | Repository readers | Preserve run provenance and avoid manual edits. |

## FAIR implementation record

| Principle | Concrete project practice | Boundary |
|---|---|---|
| Findable | Stable paths, source manifest, checksums, Git commits, DVC files, and named outputs. | These records identify the project artefacts; they do not assign a public DOI. |
| Accessible | Data can be retrieved through DVC by authorised collaborators with a private service-account configuration. | Access is controlled and depends on the source terms and Drive permissions. |
| Interoperable | UTF-8 CSV, machine-readable dictionary, explicit coding, Python scripts, and pinned packages. | Codes retain ENDES meanings and must be read with the dictionary. |
| Reusable | Population rules, transformation script, quality checks, ethics boundary, and model documentation are included. | Reuse must respect INEI conditions and the stated non-clinical purpose. |

## Anonymisation and disclosure control

The project removes case and household join keys before writing the analytical file. It retains only the minimum geographic detail needed for the stated analysis: department code and urban-rural residence. It does not retain coordinates, names, addresses, telephone numbers, free text, or any direct identifier. This is a risk-reduction measure, not a guarantee that a derived dataset is risk-free.

Publicly shared tables should suppress or aggregate small cells when a combination of age, year, department, and subgroup could reveal a sparsely represented population. The present repository publishes national and broad residence summaries. A later table with finer geographic detail requires a documented disclosure review before publication.

## Retention, transfer, and closure

The repository and DVC artefacts will be retained through course evaluation and any approved thesis continuation, subject to the applicable source conditions. Access will be reviewed when a collaborator leaves the project. At closure, the owner will archive the code and metadata necessary to understand the work, remove collaborators who no longer need access, and securely remove private credentials and any data copies that cannot be retained under the source terms. A final data-disposition decision must be recorded rather than assumed.

## Quality assurance and change control

The build script is the only approved route for regenerating the analytical CSV. It checks the expected modules, eligibility age range, outcome presence, analysis-ID uniqueness, and positive sampling weights. The resulting checks are written to `05_pipeline/docs/quality_checks.md`. The notebook is validated as JSON and the full build, analysis, and fixed-seed experiment sequence is rerun before publication.

A material change is any change to a source archive, variable definition, age rule, outcome definition, join logic, model feature set, seed set, or output interpretation. For a material change, the author must update the relevant script or parameter file, regenerate the dependent outputs, inspect the DVC state, update the protocol and data documentation where necessary, and make a descriptive Git commit. A change must not be hidden by manually editing a generated result file.

## Secure access workflow

1. The repository owner keeps the Google service-account JSON key outside the repository.
2. The Drive folder is shared only with the required service-account or collaborator identity.
3. Each collaborator configures the private key path with `dvc remote modify --local`; `.dvc/config.local` remains ignored by Git.
4. Access is removed when the course collaboration ends or a person no longer needs the data.
5. If a credential or unintended copy is exposed, the owner rotates or revokes access, reviews DVC/Drive permissions, documents the incident, and regenerates affected data artefacts if their integrity is uncertain.

## Planned sharing package

If the project is approved for sharing beyond the course, the default package will be code, pinned dependencies, the DVC configuration without credentials, metadata, aggregate outputs, protocol records, and documentation. The raw archives and processed child-level CSV will not be made public automatically. Any release decision must name the intended audience, legal basis, source-data conditions, disclosure controls, licence, and a contact for correction requests.
