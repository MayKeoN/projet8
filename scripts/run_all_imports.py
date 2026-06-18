"""
run_all_imports.py
------------------
Run all seed preparation scripts in order.

Usage:
    python scripts/run_all_imports.py

Then:
    dbtf build
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str) -> None:
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(SCRIPTS / script)], check=True, cwd=ROOT)


def main() -> None:
    run("prepare_csv_seeds.py")
    run("prepare_insee_seed.py")
    print("\nAll seeds ready. Next: dbtf build")


if __name__ == "__main__":
    main()
