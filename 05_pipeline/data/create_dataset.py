"""Build an analysis-ready child anemia dataset from official ENDES modules.

The script never alters the original ZIP archives. It extracts the three
required modules in a temporary directory, joins them on ENDES keys, and
writes a de-identified analytical CSV for the research project.
"""

from __future__ import annotations

import csv
import hashlib
import io
import shutil
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from dbfread import DBF


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(__file__).resolve().parent
RAW_DIR = DATA_DIR / "raw"
METADATA_DIR = ROOT / "docs"
OUTPUT_PATH = DATA_DIR / "endes_anemia_children_2019_2024.csv"
PUBLIC_SAMPLE_PATH = DATA_DIR / "endes_anemia_children_2019_2024_sample.csv"
PUBLIC_SAMPLE_ROWS_PER_YEAR = 50
PUBLIC_SAMPLE_SEED = 2026
RETRIEVAL_DATE = "2026-07-31"

MODULES = {
    2019: {
        "mother": ("ENDES_2019_module66.zip", "REC0111", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/DBF/691-Modulo66.zip"),
        "birth": ("ENDES_2019_module67.zip", "REC21", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/DBF/691-Modulo67.zip"),
        "child": ("ENDES_2019_module74.zip", "REC44", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/DBF/691-Modulo74.zip"),
    },
    2020: {
        "mother": ("ENDES_2020_module1631.zip", "REC0111", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/739-Modulo1631.zip"),
        "birth": ("ENDES_2020_module1632.zip", "REC21", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/739-Modulo1632.zip"),
        "child": ("ENDES_2020_module1638.zip", "REC44", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/739-Modulo1638.zip"),
    },
    2021: {
        "mother": ("ENDES_2021_module1631.zip", "REC0111", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/760-Modulo1631.zip"),
        "birth": ("ENDES_2021_module1632.zip", "REC21", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/760-Modulo1632.zip"),
        "child": ("ENDES_2021_module1638.zip", "REC44", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/760-Modulo1638.zip"),
    },
    2022: {
        "mother": ("ENDES_2022_module1631.zip", "REC0111", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/786-Modulo1631.zip"),
        "birth": ("ENDES_2022_module1632.zip", "REC21", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/786-Modulo1632.zip"),
        "child": ("ENDES_2022_module1638.zip", "REC44", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/786-Modulo1638.zip"),
    },
    2023: {
        "mother": ("ENDES_2023_module1631.zip", "REC0111", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/910-Modulo1631.zip"),
        "birth": ("ENDES_2023_module1632.zip", "REC21", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/910-Modulo1632.zip"),
        "child": ("ENDES_2023_module1638.zip", "REC44", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/910-Modulo1638.zip"),
    },
    2024: {
        "mother": ("ENDES_2024_module1631.zip", "REC0111", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/968-Modulo1631.zip"),
        "birth": ("ENDES_2024_module1632.zip", "REC21", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/968-Modulo1632.zip"),
        "child": ("ENDES_2024_module1638.zip", "REC44", "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/CSV/968-Modulo1638.zip"),
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="latin-1", errors="replace", newline="") as handle:
        first_line = handle.readline()
        sample = first_line + handle.read(4096)
    if first_line.lower().startswith("sep="):
        delimiter = first_line.strip()[-1]
        skiprows = 1
    else:
        delimiter = csv.Sniffer().sniff(sample, delimiters=",;").delimiter
        skiprows = 0
    return pd.read_csv(path, sep=delimiter, skiprows=skiprows, encoding="latin-1", low_memory=False)


def read_module(archive: Path, module_name: str) -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as temporary:
        temp_dir = Path(temporary)
        with zipfile.ZipFile(archive) as zipped:
            candidates = [
                name for name in zipped.namelist()
                if Path(name).stem.upper().startswith(module_name.upper()) and Path(name).suffix.lower() in {".csv", ".dbf"}
            ]
            if len(candidates) != 1:
                raise ValueError(f"Expected one {module_name} file in {archive.name}; found {candidates}")
            extracted = Path(zipped.extract(candidates[0], temp_dir))

        if extracted.suffix.lower() == ".dbf":
            frame = pd.DataFrame(iter(DBF(str(extracted), load=True, char_decode_errors="replace")))
        else:
            frame = read_csv(extracted)

    frame.columns = [str(column).upper() for column in frame.columns]
    if "CASEID" in frame:
        frame["CASEID"] = frame["CASEID"].astype(str).str.strip()
    return frame


def numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce") if column in frame else pd.Series(np.nan, index=frame.index)


def build_year(year: int) -> pd.DataFrame:
    files = MODULES[year]
    mother = read_module(RAW_DIR / files["mother"][0], files["mother"][1])
    birth = read_module(RAW_DIR / files["birth"][0], files["birth"][1])
    child = read_module(RAW_DIR / files["child"][0], files["child"][1])

    for frame, index_name in ((birth, "BIDX"), (child, "HWIDX")):
        if index_name in frame:
            frame[index_name] = numeric(frame, index_name)

    joined = child.merge(
        birth[["CASEID", "BIDX", "B4"]],
        left_on=["CASEID", "HWIDX"],
        right_on=["CASEID", "BIDX"],
        how="left",
        validate="many_to_one",
    ).merge(
        mother[["CASEID", "V005", "V021", "V022", "V023", "V024", "V025", "V106", "V190"]],
        on="CASEID",
        how="left",
        validate="many_to_one",
    )

    legacy_level = numeric(joined, "HW57")
    new_level = numeric(joined, "HW57A")
    age = numeric(joined, "HW1")
    eligible = age.between(6, 35) & legacy_level.isin([1, 2, 3, 4])
    joined = joined.loc[eligible].copy()

    legacy_level = numeric(joined, "HW57")
    new_level = numeric(joined, "HW57A")
    department = numeric(joined, "V024").round().astype("Int64").astype("string").str.zfill(2)
    output = pd.DataFrame(
        {
            "survey_year": year,
            "age_months": numeric(joined, "HW1"),
            "hemoglobin_g_dl": numeric(joined, "HW53"),
            "hemoglobin_adjusted_legacy_g_dl": numeric(joined, "HW56"),
            "hemoglobin_adjusted_new_2024_g_dl": numeric(joined, "HW56A"),
            "anemia_legacy_level": legacy_level,
            "anemia_new_2024_level": new_level,
            "anemia_legacy": legacy_level.isin([1, 2, 3]).astype("int8"),
            "child_sex_code": numeric(joined, "B4"),
            "mother_education_code": numeric(joined, "V106"),
            "wealth_quintile": numeric(joined, "V190"),
            "residence_code": numeric(joined, "V025"),
            "survey_weight": numeric(joined, "V005") / 1_000_000,
            "cluster_code": numeric(joined, "V021"),
            "stratum_code": numeric(joined, "V022").fillna(numeric(joined, "V023")),
            "department_code": department,
        }
    )
    output.insert(0, "analysis_id", [f"{year}_{number:05d}" for number in range(1, len(output) + 1)])
    return output


def write_metadata(dataset: pd.DataFrame) -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for year, modules in MODULES.items():
        for role, (filename, module, url) in modules.items():
            archive = RAW_DIR / filename
            manifest_rows.append(
                {
                    "survey_year": year,
                    "role": role,
                    "module": module,
                    "source_url": url,
                    "retrieval_date": RETRIEVAL_DATE,
                    "downloaded_file": filename,
                    "sha256": sha256(archive),
                    "transformation": "Read original archive without modification; joined to the analytic child record by ENDES keys.",
                }
            )
    pd.DataFrame(manifest_rows).to_csv(METADATA_DIR / "source_manifest.csv", index=False)

    dictionary = [
        ("analysis_id", "Project-generated non-identifying row label.", "string", "Generated", "2019-2024", "Audit and reproducibility only"),
        ("survey_year", "ENDES collection year.", "integer", "Generated", "2019-2024", "Trend"),
        ("age_months", "Child age in completed months.", "numeric", "REC44.HW1", "2019-2024", "Eligibility and predictor"),
        ("hemoglobin_g_dl", "Observed child hemoglobin value recorded by ENDES.", "numeric", "REC44.HW53", "2019-2024", "Descriptive only"),
        ("hemoglobin_adjusted_legacy_g_dl", "Altitude-adjusted hemoglobin under the legacy ENDES field.", "numeric", "REC44.HW56", "2019-2024", "Comparability check"),
        ("hemoglobin_adjusted_new_2024_g_dl", "2024 field aligned with the updated national definition.", "numeric", "REC44.HW56A", "2024", "Sensitivity check"),
        ("anemia_legacy_level", "Legacy ENDES anemia category: 1-3 anemia, 4 no anemia.", "integer", "REC44.HW57", "2019-2024", "Outcome derivation"),
        ("anemia_new_2024_level", "2024 updated anemia category, retained for sensitivity analysis.", "integer", "REC44.HW57A", "2024", "Sensitivity only"),
        ("anemia_legacy", "Binary legacy-comparable anemia outcome: 1 if category 1-3, 0 if category 4.", "integer", "Derived from HW57", "2019-2024", "Primary outcome"),
        ("child_sex_code", "ENDES child sex code.", "integer", "REC21.B4", "2019-2024", "Predictor and subgroup"),
        ("mother_education_code", "ENDES maternal education code.", "integer", "REC0111.V106", "2019-2024", "Predictor"),
        ("wealth_quintile", "ENDES household wealth quintile code.", "integer", "REC0111.V190", "2019-2024", "Predictor"),
        ("department_code", "ENDES department code used for the departmental domain.", "string", "REC0111.V024", "2019-2024", "Predictor and subgroup"),
        ("residence_code", "ENDES urban-rural residence code.", "integer", "REC0111.V025", "2019-2024", "Predictor and subgroup"),
        ("survey_weight", "Normalized individual sampling weight (V005 divided by 1,000,000).", "numeric", "REC0111.V005", "2019-2024", "Weighted descriptive estimates"),
        ("cluster_code", "Primary sampling unit code.", "integer", "REC0111.V021", "2019-2024", "Design documentation"),
        ("stratum_code", "Sampling stratum code; V022 with V023 fallback.", "integer", "REC0111.V022/V023", "2019-2024", "Design documentation"),
    ]
    pd.DataFrame(dictionary, columns=["variable", "definition", "type", "source", "years_available", "analytic_role"]).to_csv(
        METADATA_DIR / "data_dictionary.csv", index=False
    )

    yearly = dataset.groupby("survey_year", as_index=False).agg(
        eligible_children=("analysis_id", "size"),
        unweighted_legacy_anemia_prevalence=("anemia_legacy", "mean"),
        positive_weights=("survey_weight", lambda value: int((value > 0).sum())),
    )
    checks = [
        "# Dataset quality checks",
        "",
        "The file was built from the official anonymous ENDES modules listed in `source_manifest.csv`. The analytical output contains no ENDES case, household, or person identifier.",
        "",
        "## Build checks",
        "",
        f"- Rows in the final eligibility population: {len(dataset):,}.",
        f"- Duplicate analysis identifiers: {int(dataset['analysis_id'].duplicated().sum())}.",
        f"- Age range: {dataset['age_months'].min():.0f} to {dataset['age_months'].max():.0f} months.",
        f"- Missing primary outcome: {int(dataset['anemia_legacy'].isna().sum())}.",
        "- The figures below are unweighted checks only; publication-style prevalence estimates are produced separately with the sampling weights.",
        "",
        "## By year",
        "",
        yearly.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Comparability note",
        "",
        "The primary series uses the legacy ENDES category `HW57` in every year, including 2024. ENDES 2024 also contains the updated fields `HW56A/HW57A`; those fields are retained only for a transparent 2024 sensitivity check. The legacy series should not be presented as the official 2024 estimate reported under the updated national directive.",
    ]
    (METADATA_DIR / "quality_checks.md").write_text("\n".join(checks) + "\n", encoding="utf-8")

    population = """# Analysis population

The primary analytical population is children aged 6 to 35 completed months who have a valid legacy ENDES anemia category (`HW57`) in ENDES 2019-2024. This age range matches the project question and the age group used in recent official reporting.

The build keeps one record per eligible child after joining the child haemoglobin module (`REC44`), the birth-history module (`REC21`), and the household/mother characteristics module (`REC0111`). The join keys are used only during construction and are excluded from the released analytical CSV.

Records outside the age range, without a valid legacy anemia category, or without a successful module join are excluded. Missing covariates are retained in the data contract and handled explicitly by each downstream analysis; no outcome value is imputed. The primary outcome is a legacy-comparable binary indicator derived from `HW57`. The updated 2024 definition is retained as a sensitivity field and is not mixed into the historical trend.

The dataset supports population description and exploratory prediction. It is not a clinical decision tool, and associations in the data must not be interpreted as causal effects.
"""
    (METADATA_DIR / "analysis_population.md").write_text(population, encoding="utf-8")


def write_public_inspection_sample(dataset: pd.DataFrame) -> None:
    """Write a small, balanced inspection sample without internal design fields."""
    samples = [
        group.sample(n=PUBLIC_SAMPLE_ROWS_PER_YEAR, random_state=PUBLIC_SAMPLE_SEED + int(year))
        for year, group in dataset.groupby("survey_year", sort=True)
    ]
    public_columns = [column for column in dataset.columns if column not in {"analysis_id", "cluster_code", "stratum_code"}]
    public_sample = pd.concat(samples, ignore_index=True).loc[:, public_columns]
    public_sample.to_csv(PUBLIC_SAMPLE_PATH, index=False)


def main() -> None:
    missing = [filename for modules in MODULES.values() for filename, _, _ in modules.values() if not (RAW_DIR / filename).exists()]
    if missing:
        raise FileNotFoundError("Missing ENDES archives in data/raw: " + ", ".join(missing))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = pd.concat([build_year(year) for year in sorted(MODULES)], ignore_index=True)
    dataset.to_csv(OUTPUT_PATH, index=False)
    write_public_inspection_sample(dataset)
    write_metadata(dataset)
    print(
        f"Built {OUTPUT_PATH.relative_to(ROOT)} with {len(dataset):,} eligible children and "
        f"{PUBLIC_SAMPLE_PATH.relative_to(ROOT)} with {PUBLIC_SAMPLE_ROWS_PER_YEAR * len(MODULES):,} inspection rows."
    )


if __name__ == "__main__":
    main()
