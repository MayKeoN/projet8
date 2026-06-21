"""
Generate the 4 analysis charts for the Projet 8 presentation.
Output: deliverables/charts/*.png (UTF-8 labels, 150 dpi)
Chart designs aligned with analyse_colab.ipynb.
"""

from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.rcParams["figure.dpi"] = 150
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["grid.alpha"] = 0.3

BLUE  = "#1f6aa5"
CORAL = "#e05a4e"
TEAL  = "#2a9d8f"
GOLD  = "#e9c46a"
GRAY  = "#adb5bd"

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "deliverables" / "mart_profil_sociodemographique.csv"
OUT = ROOT / "deliverables" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)
df.columns = [c.upper() for c in df.columns]

# ── Chart 1 ─ Effectifs par région ────────────────────────────────────────────
region_totals = (
    df[df["GENDER"] == "Total"]
    .groupby("REGION")["STUDENT_COUNT"]
    .sum().dropna()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(13, 5))
bars = ax.bar(region_totals.index, region_totals.values, color=BLUE, width=0.7, edgecolor="white")
for bar, val in zip(bars, region_totals.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
            f"{int(val):,}".replace(",", "\u202f"),
            ha="center", va="bottom", fontsize=8.5)
idf_pct = region_totals[region_totals.index.str.contains("Île-de-France", na=False)].sum() / region_totals.sum() * 100
ax.set_title(f"Effectifs OCR par r\u00e9gion \u2014 Parcours Data 2022\u20132025\n\u00cele-de-France\u202f: {idf_pct:.1f}\u202f% des inscriptions",
             fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Nombre d'\u00e9tudiants")
ax.tick_params(axis="x", rotation=40)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "\u202f")))
plt.tight_layout()
p1 = OUT / "graph_regions.png"
fig.savefig(p1, bbox_inches="tight")
plt.close(fig)
print(f"Saved {p1}")

# ── Chart 2 ─ Évolution annuelle ──────────────────────────────────────────────
yearly = (
    df[df["GENDER"] == "Total"]
    .groupby("YEAR")["STUDENT_COUNT"]
    .sum().dropna().sort_index()
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(yearly.index.astype(int), yearly.values,
        marker="o", linewidth=2.5, markersize=8, color=BLUE)
for year, val in yearly.items():
    ax.annotate(f"{int(val):,}".replace(",", "\u202f"),
                xy=(year, val), xytext=(0, 12), textcoords="offset points",
                ha="center", fontsize=10, fontweight="bold", color=BLUE)
ax.set_title("\u00c9volution des inscriptions au parcours Data OCR", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Nombre d'\u00e9tudiants")
ax.set_xlabel("Ann\u00e9e")
ax.set_xticks(yearly.index.astype(int))
ax.set_ylim(0, yearly.max() * 1.25)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "\u202f")))
plt.tight_layout()
p2 = OUT / "graph_yearly.png"
fig.savefig(p2, bbox_inches="tight")
plt.close(fig)
print(f"Saved {p2}")

# ── Chart 3 ─ Taux « Non renseigné » ──────────────────────────────────────────
nr = df[df["GENDER"] == "Non renseigne"].groupby("YEAR")["STUDENT_COUNT"].sum().dropna()
total_yr = df[df["GENDER"] == "Total"].groupby("YEAR")["STUDENT_COUNT"].sum().dropna()
nr_rate = (nr / total_yr * 100).sort_index()

fig, ax = plt.subplots(figsize=(8, 4))
bar_colors = [CORAL, CORAL, TEAL, TEAL]
bars = ax.bar(nr_rate.index.astype(int), nr_rate.values,
              color=bar_colors[:len(nr_rate)], width=0.6, edgecolor="white")
for bar, val in zip(bars, nr_rate.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f"{val:.1f}\u202f%", ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_title("Taux de genre non renseign\u00e9 par ann\u00e9e", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("% des inscriptions")
ax.set_xlabel("Ann\u00e9e")
ax.set_xticks(nr_rate.index.astype(int))
ax.set_ylim(0, nr_rate.max() * 1.25)
ax.axhline(y=10, color=GRAY, linestyle="--", linewidth=1, label="Seuil 10\u202f%")
ax.legend(fontsize=9)
plt.tight_layout()
p3 = OUT / "graph_nr_rate.png"
fig.savefig(p3, bbox_inches="tight")
plt.close(fig)
print(f"Saved {p3}")

# ── Chart 4 ─ Taux /100k par région (Corse exclue : 0 étudiant OCR) ──────────
bench = (
    df[
        (df["GENDER"] == "Total")
        & df["STUDENTS_PER_100K"].notna()
        & ~df["REGION"].str.contains("Corse", case=False, na=False)
    ]
    .groupby("REGION")["STUDENTS_PER_100K"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(13, 5))
colors = [CORAL if str(r) == "Île-de-France" else TEAL for r in bench.index]
bars = ax.bar(bench.index, bench.values, color=colors, width=0.7, edgecolor="white")
for bar, val in zip(bars, bench.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
            f"{val:.1f}", ha="center", va="bottom", fontsize=8.5)
mean_val = bench.mean()
ax.axhline(y=mean_val, color=GOLD, linestyle="--", linewidth=1.5,
           label=f"Moyenne\u202f: {mean_val:.1f}")
ax.set_title("\u00c9tudiants OCR pour 100\u202f000 habitants \u2014 moyenne 2022\u20132025",
             fontsize=12, fontweight="bold", pad=12)
ax.set_ylabel("\u00c9tudiants / 100\u202f000 hab.")
ax.tick_params(axis="x", rotation=40)
ax.legend(fontsize=9)
plt.tight_layout()
p4 = OUT / "graph_100k.png"
fig.savefig(p4, bbox_inches="tight")
plt.close(fig)
print(f"Saved {p4}")

print("\nAll 4 charts written to:", OUT)

# ── DAG diagram ───────────────────────────────────────────────────────────────
import matplotlib.patches as mpatches

# figsize=(16,7): ratio 2.29 → at 9.64" slide width → image height ≈ 4.2" (fits in 4.78")
fig, ax = plt.subplots(figsize=(16, 7))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
fig.patch.set_facecolor("#F8F9FA")
ax.set_facecolor("#F8F9FA")

ax.text(0.5, 0.97,
        "Pipeline dbt  \u00b7  Snowflake  \u00b7  4 seeds  \u00b7  8 mod\u00e8les  \u00b7  57 tests",
        ha="center", va="top", fontsize=13, fontweight="bold", color="#1F4E79")

# Layer header uses ONE combined line — avoids any sublabel/node collision.
# Box heights are generous; nodes sit in the lower 40% of each box.
_layers = [
    {"label": "RAW  (seeds)",
     "yb": 0.73, "yt": 0.91,
     "bg": "#DDEEFF", "border": "#2E75B6", "tc": "#1F4E79",
     "nodes": ["students_raw", "insee_population_raw", "cog_departement", "cog_region"]},
    {"label": "STAGING  (views \u2014 nettoyage 1:1, sans jointure)",
     "yb": 0.49, "yt": 0.67,
     "bg": "#DDF0DD", "border": "#4A8C4E", "tc": "#2A5A2E",
     "nodes": ["stg_students", "stg_insee_population", "stg_cog_departement", "stg_cog_region"]},
    {"label": "INTERMEDIATE  (views \u2014 jointures inter-sources & agr\u00e9gations)",
     "yb": 0.25, "yt": 0.43,
     "bg": "#FFF0DD", "border": "#C87C3B", "tc": "#7A4A1E",
     "nodes": ["int_cog_departement_region", "int_students_by_year_region", "int_insee_by_year_region"]},
    {"label": "MART  (table mat\u00e9rialis\u00e9e \u2014 livrable final)",
     "yb": 0.07, "yt": 0.19,
     "bg": "#EEDDEE", "border": "#8B5E8B", "tc": "#5A3A5A",
     "nodes": ["mart_profil_sociodemographique"]},
]

for layer in _layers:
    rect = mpatches.FancyBboxPatch(
        (0.04, layer["yb"]), 0.92, layer["yt"] - layer["yb"],
        boxstyle="round,pad=0.005",
        facecolor=layer["bg"], edgecolor=layer["border"], linewidth=2,
    )
    ax.add_patch(rect)
    # Header at top of box
    ax.text(0.5, layer["yt"] - 0.018,
            layer["label"],
            ha="center", va="top", fontsize=12, fontweight="bold", color=layer["tc"])
    # Nodes in lower 35% of box — well clear of header text
    node_y = layer["yb"] + (layer["yt"] - layer["yb"]) * 0.28
    nodes = layer["nodes"]
    n = len(nodes)
    for j, node in enumerate(nodes):
        x = 0.5 if n == 1 else (0.1 + j * (0.8 / (n - 1)))
        ax.text(x, node_y, node, ha="center", va="center",
                fontsize=10, color="#444444")

# Arrows connect box bottoms to next box tops
for y1, y2 in [(0.73, 0.67), (0.49, 0.43), (0.25, 0.19)]:
    ax.annotate("", xy=(0.5, y2), xytext=(0.5, y1),
                arrowprops=dict(arrowstyle="->", color="#777777", lw=2, mutation_scale=16))

ax.text(0.5, 0.025,
        "Staging : renommage + cast uniquement  \u00b7  "
        "Intermediate : jointures COG, harmonisation \u00e2ge, agr\u00e9gations  \u00b7  "
        "Mart : FULL OUTER JOIN, students_per_100k",
        ha="center", va="bottom", fontsize=9, color="#666666")

dag_path = OUT / "graph_dag.png"
fig.savefig(dag_path, dpi=150, bbox_inches="tight", pad_inches=0.1, facecolor="#F8F9FA")
plt.close(fig)
print(f"Saved {dag_path}")
