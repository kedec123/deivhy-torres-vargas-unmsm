"""Render the SVG PRISMA flow to a PNG for platforms that do not preview SVG."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parent


def box(axis, x, y, width, height, title, body, color):
    axis.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.02", facecolor=color, edgecolor="#8d2f23", linewidth=1.6))
    axis.text(x + width / 2, y + height * 0.64, title, ha="center", va="center", fontsize=11, fontweight="bold")
    axis.text(x + width / 2, y + height * 0.32, body, ha="center", va="center", fontsize=9, wrap=True)


def main():
    figure, axis = plt.subplots(figsize=(10, 8))
    axis.set(xlim=(0, 10), ylim=(0, 10))
    axis.axis("off")
    figure.suptitle("PRISMA flow: focused review of child anemia in Peru", fontsize=16, fontweight="bold")
    entries = [
        (3, 8.25, 4, 0.85, "Records identified", "PubMed (n = 10) + SciELO (n = 2)\nTotal (n = 12)", "#f7f3e8"),
        (3, 6.8, 4, 0.75, "Duplicates removed", "No duplicate records (n = 0)", "#f7f3e8"),
        (3, 5.35, 4, 0.75, "Title and abstract screening", "Records screened (n = 12); exclusions (n = 0)", "#f7f3e8"),
        (3, 3.9, 4, 0.75, "Full-text assessment", "Full texts assessed for eligibility (n = 12)", "#f7f3e8"),
        (3, 1.9, 4, 0.85, "Studies included in review", "Included studies (n = 10)", "#edf3ed"),
    ]
    for entry in entries:
        box(axis, *entry)
    box(axis, 7.5, 3.45, 2.3, 1.4, "Full-text exclusions", "Wrong target age (n = 1)\nNo usable 6-35 month\nstratum (n = 1)", "#edf3ed")
    for y_start, y_end in ((8.25, 7.55), (6.8, 6.1), (5.35, 4.65), (3.9, 2.75)):
        axis.annotate("", xy=(5, y_end), xytext=(5, y_start), arrowprops={"arrowstyle": "->", "color": "#52616b", "lw": 1.4})
    axis.annotate("", xy=(7.5, 4.25), xytext=(7, 4.25), arrowprops={"arrowstyle": "->", "color": "#52616b", "lw": 1.4})
    axis.text(5, 0.7, "Counts are calculated from screening_log.csv (search date: 31 July 2026).", ha="center", fontsize=8)
    figure.tight_layout()
    figure.savefig(ROOT / "prisma_diagram.png", dpi=180)


if __name__ == "__main__":
    main()
