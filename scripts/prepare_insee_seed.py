"""Extrait les estimations INSEE (XLSX) vers seeds/insee_population_raw.csv. Normalise les noms de colonnes pour SQL ; valeurs brutes conservées (nettoyage en staging dbt)."""
from __future__ import annotations

import unicodedata
from pathlib import Path

import pandas as pd

ROOT   = Path(__file__).resolve().parents[1]
INPUT  = ROOT / "data" / "estim-pop-dep-sexe-aq-1975-2025.xlsx"
OUTPUT = ROOT / "seeds" / "insee_population_raw.csv"

YEARS    = ["2022", "2023", "2024", "2025"]
PREFIXES = ["ensemble", "hommes", "femmes"]  # matches XLSX row 4, left to right

# Sheet layout (0-indexed rows)
AGE_BAND_ROW = 4   # row with age band labels ("0 à 4 ans", ..., "Total")
DATA_START   = 5   # first data row


def normalize(label: str) -> str:
    """'0 à 4 ans' → '0_a_4_ans'"""
    label = label.lower().strip()
    label = unicodedata.normalize("NFD", label)
    label = "".join(c for c in label if unicodedata.category(c) != "Mn")
    return label.replace(" ", "_")


def extract_year(path: Path, year: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=year, header=None, dtype=str)

    # Build column names from age band labels (one group of 22, repeated 3 times)
    age_bands = raw.iloc[AGE_BAND_ROW, 2:23].tolist()
    columns = ["dep_code", "dep_name"]
    for prefix in PREFIXES:
        for band in age_bands:
            columns.append(f"{prefix}_{normalize(str(band))}")

    # Slice data rows, stop at first fully empty row
    data = raw.iloc[DATA_START:].reset_index(drop=True)
    cutoff = data.isnull().all(axis=1).idxmax()
    data = data.iloc[:cutoff, : len(columns)]

    data.columns = columns
    data.insert(0, "year", year)
    return data


def main() -> None:
    frames = []
    for year in YEARS:
        df = extract_year(INPUT, year)
        print(f"{year}: {len(df)} rows")
        frames.append(df)

    out = pd.concat(frames, ignore_index=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT, index=False, encoding="utf-8")
    print(f"\nWrote {len(out)} rows → {OUTPUT}")


if __name__ == "__main__":
    main()
