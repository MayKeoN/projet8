"""
Generate the 4 analysis charts for the Projet 8 presentation.
Output: deliverables/charts/*.png (UTF-8 labels, 150 dpi)
"""

from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.rcParams["figure.dpi"] = 150
matplotlib.rcParams["font.family"] = "DejaVu Sans"

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "deliverables" / "mart_profil_sociodemographique.csv"
OUT = ROOT / "deliverables" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

# Normalize column names to lower-case for safety
df.columns = [c.upper() for c in df.columns]

# ── Chart 1 ─ Effectifs par région (barres, toutes années, Gender=Total) ──────
region_totals = (
    df[(df["GENDER"] == "Total") & df["STUDENT_COUNT"].notna()]
    .groupby("REGION")["STUDENT_COUNT"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(region_totals.index, region_totals.values, color="#2E75B6", edgecolor="white")
ax.set_title("Effectifs OCR par région — cumulé 2022–2025", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Nombre d'étudiants")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=45)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " ")))
# Annotate IDF bar
for bar, label in zip(bars, region_totals.index):
    if label == "Île-de-France":
        pct = region_totals[label] / region_totals.sum() * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 15,
            f"{pct:.1f} %",
            ha="center", va="bottom", fontsize=9, color="#C00000", fontweight="bold",
        )
plt.tight_layout()
p1 = OUT / "graph_regions.png"
fig.savefig(p1)
plt.close(fig)
print(f"Saved {p1}")

# ── Chart 2 ─ Évolution annuelle des inscriptions (courbe) ────────────────────
yearly = (
    df[(df["GENDER"] == "Total") & (df["AGE_GROUP"] != "Total") & df["STUDENT_COUNT"].notna()]
    .groupby("YEAR")["STUDENT_COUNT"]
    .sum()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(yearly.index, yearly.values, marker="o", linewidth=2.5, color="#2E75B6", markersize=8)
for x, y in zip(yearly.index, yearly.values):
    ax.annotate(
        f"{int(y):,}".replace(",", " "),
        (x, y), textcoords="offset points", xytext=(0, 10),
        ha="center", fontsize=10, fontweight="bold",
    )
ax.set_title("Évolution des inscriptions par année", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Nombre d'étudiants")
ax.set_xticks(yearly.index)
ax.set_ylim(0, yearly.max() * 1.25)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " ")))
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
p2 = OUT / "graph_yearly.png"
fig.savefig(p2)
plt.close(fig)
print(f"Saved {p2}")

# ── Chart 3 ─ Taux « Non renseigné » par année (barres) ──────────────────────
nr_by_year = (
    df[(df["GENDER"] == "Non renseigne") & df["STUDENT_COUNT"].notna()]
    .groupby("YEAR")["STUDENT_COUNT"].sum()
)
total_by_year = (
    df[(df["GENDER"] == "Total") & (df["AGE_GROUP"] != "Total") & df["STUDENT_COUNT"].notna()]
    .groupby("YEAR")["STUDENT_COUNT"].sum()
)
nr_rate = (nr_by_year / total_by_year * 100).sort_index()

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(nr_rate.index.astype(str), nr_rate.values, color="#ED7D31", edgecolor="white")
for bar, val in zip(bars, nr_rate.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{val:.1f} %",
        ha="center", va="bottom", fontsize=11, fontweight="bold",
    )
ax.set_title("Taux de genre « Non renseigné » par année (%)", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("% des inscrits")
ax.set_ylim(0, nr_rate.max() * 1.25)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
p3 = OUT / "graph_nr_rate.png"
fig.savefig(p3)
plt.close(fig)
print(f"Saved {p3}")

# ── Chart 4 ─ students_per_100k par région (2022–2025 moyenne, Gender=Total) ─
bench = (
    df[
        (df["GENDER"] == "Total")
        & df["STUDENTS_PER_100K"].notna()
        & (df["REGION"] != "DROM")
    ]
    .groupby("REGION")["STUDENTS_PER_100K"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(bench.index, bench.values, color="#375623", edgecolor="white")
ax.set_title(
    "Taux d'inscription pour 100 000 hab. par région — moyenne 2022–2025\n(DROM exclu — pas de benchmark INSEE)",
    fontsize=12, fontweight="bold", pad=12,
)
ax.set_ylabel("Étudiants / 100 000 hab.")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
p4 = OUT / "graph_100k.png"
fig.savefig(p4)
plt.close(fig)
print(f"Saved {p4}")

print("\nAll 4 charts written to:", OUT)
