"""Download and verify the official public ENDES archives needed by this project.

No Google Drive account, DVC credential, or private key is required.  The URLs
and expected SHA-256 values are recorded in ``docs/source_manifest.csv`` and
are checked before the archives are accepted for dataset construction.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from create_dataset import MODULES, RAW_DIR, sha256


CHUNK_SIZE = 1024 * 1024


def source_records(years: list[int]) -> list[tuple[int, str, str, str]]:
    """Return one record per required public source archive."""
    records = []
    for year in years:
        for role, (filename, _module, url) in MODULES[year].items():
            records.append((year, role, filename, url))
    return records


def expected_hashes() -> dict[str, str]:
    """Read the committed source manifest, keyed by locally stored archive name."""
    manifest = Path(__file__).resolve().parents[1] / "docs" / "source_manifest.csv"
    if not manifest.exists():
        raise FileNotFoundError(f"Missing committed source manifest: {manifest}")
    with manifest.open(encoding="utf-8", newline="") as handle:
        return {row["downloaded_file"]: row["sha256"] for row in csv.DictReader(handle)}


def download(url: str, destination: Path) -> None:
    """Download one file atomically, without retaining an incomplete archive."""
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = Request(url, headers={"User-Agent": "ENDES-reproducibility-workflow/1.0"})
    with urlopen(request, timeout=120) as response, temporary.open("wb") as output:
        while chunk := response.read(CHUNK_SIZE):
            output.write(chunk)
    temporary.replace(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the public ENDES archives needed to rebuild this dataset.")
    parser.add_argument("--years", nargs="+", type=int, choices=sorted(MODULES), default=sorted(MODULES))
    parser.add_argument("--force", action="store_true", help="Redownload archives even when their SHA-256 is valid.")
    parser.add_argument("--verify-only", action="store_true", help="Check local archives without downloading missing files.")
    arguments = parser.parse_args()

    hashes = expected_hashes()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for year, role, filename, url in source_records(arguments.years):
        destination = RAW_DIR / filename
        expected = hashes.get(filename)
        if expected is None:
            raise KeyError(f"No expected SHA-256 for {filename} in source_manifest.csv")
        valid = destination.exists() and sha256(destination) == expected
        if valid and not arguments.force:
            print(f"Verified {year} {role}: {filename}")
            continue
        if arguments.verify_only:
            state = "missing" if not destination.exists() else "checksum mismatch"
            raise RuntimeError(f"{year} {role}: {filename} is {state}")
        if destination.exists():
            destination.unlink()
        print(f"Downloading {year} {role}: {url}")
        download(url, destination)
        actual = sha256(destination)
        if actual != expected:
            destination.unlink(missing_ok=True)
            raise RuntimeError(f"Checksum mismatch for {filename}: expected {expected}, received {actual}")
        print(f"Verified {year} {role}: {filename}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ENDES download failed: {error}", file=sys.stderr)
        raise
