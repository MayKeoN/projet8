"""
prepare_csv_seeds.py
--------------------
Load the three raw CSV sources into seeds/ with normalized column names.

No transformation — raw values preserved as-is.
dtype=str on read prevents pandas from casting codes like "01" to integer 1.
All values come out as strings in the CSV regardless (pandas to_csv behaviour).

Sources → Seeds:
  data/DATASET+-+MAJ+...csv  →  seeds/students_raw.csv
  data/v_departement_2024.csv  →  seeds/cog_departement.csv
  data/v_region_2024.csv       →  seeds/cog_region.csv
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    (
        ROOT / "data" / "DATASET+-+MAJ+-+P8+-+1040-+DA+-+DATA+-+DATASET+-+MAJ+-+P8+-+1040-+DA+-+DATA.csv",
        ROOT / "seeds" / "students_raw.csv",
    ),
    (
        ROOT / "data" / "v_departement_2024.csv",
        ROOT / "seeds" / "cog_departement.csv",
    ),
    (
        ROOT / "data" / "v_region_2024.csv",
        ROOT / "seeds" / "cog_region.csv",
    ),
]


def process(src: Path, dst: Path) -> None:
    df = pd.read_csv(src, encoding="utf-8", dtype=str)
    df.columns = [c.strip().upper() for c in df.columns]
    df.to_csv(dst, index=False, encoding="utf-8")
    print(f"{src.name} → {dst.name} ({len(df)} rows)")


def main() -> None:
    for src, dst in FILES:
        if not src.exists():
            print(f"MISSING: {src.name} — skipping")
            continue
        process(src, dst)


if __name__ == "__main__":
    main()
