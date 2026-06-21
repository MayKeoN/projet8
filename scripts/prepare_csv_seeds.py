"""Charge les trois CSV sources brutes vers seeds/ avec en-têtes normalisés. dtype=str évite la conversion de codes comme '01' en entier."""
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
