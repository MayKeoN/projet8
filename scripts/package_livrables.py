"""
package_livrables.py
--------------------
Génère le dossier zip de livraison OCR Projet 8.

Structure produite :
    Monfray_Yukel_Projet8_DA_062026/
        Monfray_Yukel_1_fichier_062026.csv        ← à placer dans data/ avant de lancer
        Monfray_Yukel_2_workflow_062026/           ← archive git propre du projet
        Monfray_Yukel_3_presentation_062026.pptx  ← à placer dans data/ avant de lancer

Usage :
    python scripts/package_livrables.py

Prérequis :
    - mart_profil_sociodemographique.csv dans le dossier data/deliverables/
    - Présentation finale .pptx dans le dossier data/deliverables/
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT    = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT.parent / "Monfray_Yukel_Projet8_DA_062026"
DELIVERABLES = ROOT / "data" / "deliverables"

CSV_SRC  = DELIVERABLES / "mart_profil_sociodemographique.csv"
PPTX_SRC = DELIVERABLES / "Projet8_OCR_Presentation.pptx"

CSV_DST  = OUT_DIR / "Monfray_Yukel_1_fichier_062026.csv"
WF_DST   = OUT_DIR / "Monfray_Yukel_2_workflow_062026"
PPTX_DST = OUT_DIR / "Monfray_Yukel_3_presentation_062026.pptx"


def check_inputs() -> None:
    missing = []
    if not CSV_SRC.exists():
        missing.append(f"  CSV manquant : {CSV_SRC}")
    if not PPTX_SRC.exists():
        missing.append(f"  PPTX manquant : {PPTX_SRC}")
    if missing:
        print("Fichiers manquants :")
        for m in missing:
            print(m)
        print("\nDéposer ces fichiers dans data/deliverables/ puis relancer.")
        sys.exit(1)


def build_workflow_archive() -> None:
    """Archive git propre du projet (sans target/, logs/, venv/, etc.)"""
    WF_DST.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "archive", "--format=zip", f"--output={WF_DST}.zip", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Erreur git archive : {result.stderr}")
        sys.exit(1)

    # Extraire dans le sous-dossier
    shutil.unpack_archive(f"{WF_DST}.zip", WF_DST)
    Path(f"{WF_DST}.zip").unlink()
    print(f"  Workflow archivé : {WF_DST.name}/")


def main() -> None:
    print(f"Dossier de sortie : {OUT_DIR}")

    # Nettoyage si run précédent
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    check_inputs()

    # 1. CSV
    shutil.copy2(CSV_SRC, CSV_DST)
    print(f"  CSV copié : {CSV_DST.name}")

    # 2. Workflow dbt (archive git)
    build_workflow_archive()

    # 3. Présentation
    shutil.copy2(PPTX_SRC, PPTX_DST)
    print(f"  Présentation copiée : {PPTX_DST.name}")

    # Zip final
    zip_path = ROOT.parent / "Monfray_Yukel_Projet8_DA_062026"
    shutil.make_archive(str(zip_path), "zip", ROOT.parent, OUT_DIR.name)
    shutil.rmtree(OUT_DIR)

    print(f"\nZip produit : {zip_path}.zip")
    print("Prêt à déposer sur la plateforme OCR.")


if __name__ == "__main__":
    main()
