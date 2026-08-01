# Data Management Plan

## Data lifecycle

The project receives anonymous official ENDES module archives, creates a de-identified analysis file, and produces aggregate tables, figures, code, and MLflow tracking artifacts. The source archives and processed CSV are versioned with DVC; Git holds the code, metadata, checksums, and lock files. The source manifest is the authoritative record of origin and transformation.

## Access and security

The DVC remote is a shared Google Drive folder managed by the repository owner. Access is limited to authorised course collaborators. Credentials stay in local DVC configuration and must never be committed. The repository currently contains no direct identifiers in the processed CSV, but it should still be treated as research data rather than redistributed casually.

## FAIR and documentation commitments

Findability is supported by stable file names, the source manifest, and Git history. Accessibility is controlled through DVC permissions. Interoperability comes from UTF-8 CSV, a machine-readable dictionary, and pinned software versions. Reuse is supported by a documented analytical population, reproducible build script, and explicit limitations.

## Legal and retention considerations

The project will follow the applicable conditions of INEI microdata access and the Peruvian Personal Data Protection Law (Law No. 29733). It will not attempt re-identification or use the data for a purpose outside this course protocol. The owner will retain the repository and DVC artefacts through course evaluation and any approved thesis extension, then archive or securely remove access according to institutional guidance and the source terms.

## Backup, versioning, and incident response

GitHub is the code and documentation history; DVC/Drive is the data-artifact store. Source checksums make accidental file substitution visible. If access is exposed, credentials will be revoked or rotated, the remote sharing list reviewed, and any affected collaborator notified. If a data-quality issue is found, it will be logged, fixed in a new commit, and connected to the relevant protocol or results revision.
