"""Create transparent weighted descriptive summaries for the ENDES dataset."""

from __future__ import annotations

import hashlib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "endes_anemia_children_2019_2024.csv"
DOCS_DIR = ROOT / "docs"


def weighted_summary(frame: pd.DataFrame, groups: list[str]) -> pd.DataFrame:
    rows = []
    for keys, group in frame.groupby(groups, dropna=False):
        keys = keys if isinstance(keys, tuple) else (keys,)
        valid = group.dropna(subset=["anemia_legacy", "survey_weight"])
        weight_total = valid["survey_weight"].sum()
        prevalence = (valid["anemia_legacy"] * valid["survey_weight"]).sum() / weight_total
        row = dict(zip(groups, keys))
        row.update(
            sample_size=len(valid),
            weighted_population=weight_total,
            weighted_anemia_prevalence=prevalence,
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(groups).reset_index(drop=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(DATA_PATH, dtype={"department_code": "string"})
    by_year = weighted_summary(data, ["survey_year"])
    by_year_residence = weighted_summary(data, ["survey_year", "residence_code"])
    by_year.to_csv(DOCS_DIR / "analysis_by_year.csv", index=False)
    by_year_residence.to_csv(DOCS_DIR / "analysis_by_year_residence.csv", index=False)

    figure, axis = plt.subplots(figsize=(8, 4.5))
    axis.plot(by_year["survey_year"], by_year["weighted_anemia_prevalence"] * 100, marker="o", color="#8d2f23", linewidth=2)
    axis.set(title="Weighted legacy-comparable anemia prevalence", xlabel="ENDES year", ylabel="Prevalence (%)")
    axis.set_ylim(0, max(55, (by_year["weighted_anemia_prevalence"] * 100).max() + 5))
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(DOCS_DIR / "anemia_trend.png", dpi=180)
    plt.close(figure)

    lines = [
        "# Weighted descriptive analysis",
        "",
        "This report describes the de-identified analytical CSV built from the official ENDES modules. Estimates use the normalized ENDES individual weight (`V005/1,000,000`) as a descriptive weight. Formal annual uncertainty is produced separately by `src/survey_analysis.py`, which reports Taylor-linearized design-based intervals and a stratified-cluster bootstrap comparison. This descriptive script intentionally does not duplicate those inferential calculations.",
        "",
        f"- Dataset SHA-256: `{sha256(DATA_PATH)}`",
        f"- Eligible children: {len(data):,}",
        "- Outcome: legacy-comparable binary anemia category derived from `HW57`.",
        "- Scope: children aged 6-35 months in ENDES 2019-2024.",
        "",
        "## Trend by year",
        "",
        by_year.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Interpretation boundary",
        "",
        "The series is designed for internal comparability because it uses the legacy field in all years. It should not be substituted for the official 2024 figure produced with the updated measurement definition. The table is descriptive, not causal evidence; use `analysis_by_year_with_ci.csv` for the corresponding design-based annual intervals.",
    ]
    (DOCS_DIR / "analysis_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote descriptive outputs to {DOCS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
