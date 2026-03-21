# viz-116: Sanitation Access Slope Chart (2000 vs 2022)
# People using at least basic sanitation services (% of population)
# Dataset: wb--SH-STA-BASS-ZS (World Bank / WHO-UNICEF JMP)

import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# -- Load data --
dataset_path = Path(__file__).resolve().parents[2] / "catalog" / "datasets" / "wb--SH-STA-BASS-ZS.json"
with open(dataset_path, "r") as f:
    raw = json.load(f)

df = pd.DataFrame(raw["data"])

# -- Select countries --
selected_countries = {
    "KH": ("Cambodia", "dramatic"),
    "IN": ("India", "dramatic"),
    "ID": ("Indonesia", "dramatic"),
    "BD": ("Bangladesh", "large"),
    "CN": ("China", "large"),
    "BO": ("Bolivia", "large"),
    "AF": ("Afghanistan", "large"),
    "GH": ("Ghana", "moderate"),
    "CO": ("Colombia", "moderate"),
    "BR": ("Brazil", "moderate"),
    "KE": ("Kenya", "moderate"),
    "HT": ("Haiti", "stagnant"),
    "ET": ("Ethiopia", "stagnant"),
    "EG": ("Egypt", "high"),
    "TD": ("Chad", "stagnant"),
    "DE": ("Germany", "high"),
    "JP": ("Japan", "high"),
    "CD": ("DR Congo", "declined"),
}

# -- Filter for 2000 and 2022 --
df_filtered = df[
    (df["country"].isin(selected_countries.keys()))
    & (df["year"].isin([2000, 2022]))
    & (df["value"].notna())
].copy()

df_filtered["label"] = df_filtered["country"].map(lambda c: selected_countries[c][0])
df_filtered["group"] = df_filtered["country"].map(lambda c: selected_countries[c][1])

# -- Pivot to wide format --
pivot = df_filtered.pivot(index="country", columns="year", values="value").dropna()
pivot.columns = ["y2000", "y2022"]
pivot["label"] = pivot.index.map(lambda c: selected_countries[c][0])
pivot["group"] = pivot.index.map(lambda c: selected_countries[c][1])
pivot["change"] = pivot["y2022"] - pivot["y2000"]

# -- Color mapping --
group_colors = {
    "dramatic": "#0e7c42",
    "large": "#3ba272",
    "moderate": "#6bb99a",
    "high": "#7a8fa6",
    "stagnant": "#d97706",
    "declined": "#dc2626",
}

group_labels = {
    "dramatic": "Dramatic gain (40+ pp)",
    "large": "Large gain (25-40 pp)",
    "moderate": "Moderate gain (10-25 pp)",
    "high": "High baseline (near universal)",
    "stagnant": "Stagnant (<10 pp gain)",
    "declined": "Declined",
}

# -- Plot --
fig, ax = plt.subplots(figsize=(10, 12))

for _, row in pivot.iterrows():
    color = group_colors[row["group"]]
    ax.plot([0, 1], [row["y2000"], row["y2022"]], color=color, linewidth=2, alpha=0.7)
    ax.scatter([0, 1], [row["y2000"], row["y2022"]], color=color, s=40, zorder=5, edgecolors="white", linewidth=0.8)

    ax.text(-0.03, row["y2000"], f'{row["label"]} {row["y2000"]:.0f}%',
            ha="right", va="center", fontsize=8, color=color)
    ax.text(1.03, row["y2022"], f'{row["y2022"]:.0f}% {row["label"]}',
            ha="left", va="center", fontsize=8, color=color)

ax.set_xlim(-0.35, 1.35)
ax.set_ylim(-2, 108)
ax.set_xticks([0, 1])
ax.set_xticklabels(["2000", "2022"], fontsize=12, fontweight="bold")
ax.set_ylabel("% of population with basic sanitation", fontsize=10)
ax.set_yticks(range(0, 110, 10))
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.set_title(
    "Sanitation Access: Two Decades of Progress (and Stagnation)\n"
    "People using at least basic sanitation services, 2000 vs 2022",
    fontsize=13, fontweight="bold", loc="left", pad=15,
)

legend_patches = [
    mpatches.Patch(color=group_colors[g], label=group_labels[g])
    for g in ["dramatic", "large", "moderate", "high", "stagnant", "declined"]
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=8, framealpha=0.9)

fig.text(0.12, 0.01, "Source: World Bank / WHO-UNICEF JMP | Indicator: SH.STA.BASS.ZS", fontsize=8, color="#94a3b8")

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(Path(__file__).resolve().parent / "viz-116.png", dpi=150, bbox_inches="tight")
plt.show()
