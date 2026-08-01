# Data Contract

This folder separates three kinds of material:

| Location | Contents | Versioning approach |
|---|---|---|
| `raw/` | Original anonymous ENDES module archives downloaded from INEI. | DVC only. |
| `processed/` | De-identified child-level analytical CSV created by the build script. | DVC pipeline output. |
| `metadata/` | Source manifest, variable dictionary, population rules, and quality checks. | Git. |

The raw archives are not modified. `05_pipeline/src/build_endes_dataset.py` reads them in a temporary location, joins the modules, and removes ENDES case and household identifiers from the analytical file. The released analytical CSV is still research data, not an unrestricted public extract; access to the DVC remote should be limited to the course team and other authorised users.

To retrieve the DVC-managed files, ask the repository owner for access to the shared Google Drive remote and run:

```powershell
dvc pull
```

The primary dataset uses the legacy ENDES anemia category across 2019-2024 for internal comparability. See `metadata/analysis_population.md` and `metadata/quality_checks.md` before using the file.
