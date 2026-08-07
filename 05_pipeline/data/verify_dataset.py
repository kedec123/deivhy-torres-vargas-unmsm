"""Verify that the rebuilt analytical CSV matches its committed DVC pointer."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent
CSV_PATH = DATA_DIR / "endes_anemia_children_2019_2024.csv"
POINTER_PATH = DATA_DIR / "endes_anemia_children_2019_2024.csv.dvc"


def digest(path: Path) -> str:
    hasher = hashlib.md5()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def pointer_value(name: str) -> str:
    match = re.search(rf"^\s*-?\s*{re.escape(name)}:\s*(\S+)\s*$", POINTER_PATH.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find {name} in {POINTER_PATH.name}")
    return match.group(1)


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing analytical CSV: {CSV_PATH}")
    expected_md5 = pointer_value("md5")
    expected_size = int(pointer_value("size"))
    actual_md5 = digest(CSV_PATH)
    actual_size = CSV_PATH.stat().st_size
    if actual_md5 != expected_md5 or actual_size != expected_size:
        raise RuntimeError(
            f"Dataset verification failed: expected md5={expected_md5}, size={expected_size}; "
            f"received md5={actual_md5}, size={actual_size}."
        )
    print(f"Dataset verified: md5={actual_md5}, size={actual_size} bytes")


if __name__ == "__main__":
    main()
