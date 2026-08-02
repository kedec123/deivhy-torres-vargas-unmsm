"""Compare the retained legacy and updated ENDES anemia definitions in 2024."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "endes_anemia_children_2019_2024.csv"
DOCS_DIR = ROOT / "docs"


def weighted_rate(frame: pd.DataFrame, column: str) -> float:
    valid = frame.dropna(subset=[column, "survey_weight"])
    return float((valid[column] * valid["survey_weight"]).sum() / valid["survey_weight"].sum())


def main() -> None:
    data = pd.read_csv(DATA_PATH, dtype={"department_code": "string"})
    subset = data.loc[data["survey_year"] == 2024].copy()
    subset["anemia_new_2024"] = subset["anemia_new_2024_level"].isin([1, 2, 3]).astype("Int64")
    legacy = weighted_rate(subset, "anemia_legacy")
    updated = weighted_rate(subset, "anemia_new_2024")
    summary = pd.DataFrame(
        [
            {"definition": "Legacy comparable HW57", "weighted_anemia_prevalence": legacy},
            {"definition": "Updated 2024 HW57A", "weighted_anemia_prevalence": updated},
        ]
    )
    summary.to_csv(DOCS_DIR / "sensitivity_2024.csv", index=False)
    report = [
        "# 2024 anemia-definition sensitivity comparison",
        "",
        "This comparison is limited to 2024. It shows why the updated field is not mixed into the 2019-2024 primary trend.",
        "",
        summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        "The difference reflects a measurement-definition comparison, not evidence that the population burden changed by that amount.",
    ]
    (DOCS_DIR / "sensitivity_2024_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Saved 2024 sensitivity comparison to {DOCS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
