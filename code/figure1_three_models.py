#!/usr/bin/env python3
"""
figure1_three_models.py -- Figure 1: what each model did against what it said, exact ties only.

Usage:  python3 code/figure1_three_models.py data/gemini-4-hydrogen.json data/gpt-6.1-terra.json data/claude-sonnet-5.5.json [--out figures]

Uses the trials all three models share: block 7 (distress, 96 ties) and the exact-tie half of block 10 (spite, 48 ties).
Every plotted value is computed from the data files.
"""
import argparse, json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

INK, INK2, GRID, BLUE, ORANGE, SURFACE = "#0b0b0b", "#52514e", "#dddcd6", "#2a78d6", "#eb6834", "#ffffff"
fam = "Inter" if any(f.name == "Inter" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": fam, "font.size": 9, "pdf.fonttype": 42})
NAMES = ["Gemini 4 Hydrogen", "GPT-6.1 Terra", "Claude Sonnet 5.5"]

ap = argparse.ArgumentParser()
ap.add_argument("exports", nargs=3)
ap.add_argument("--out", default="figures")
a = ap.parse_args()
rows = []          # (y, label, did, said) with group headers
y = 0.0
heads = []
for cell, head in (("EVENA", "DISTRESS in one statement (96 ties per model)"), ("SPITEEVEN", "SPITE in one statement (48 ties per model)")):
    heads.append((y, head))
    y += 0.75
    for name, path in zip(NAMES, a.exports):
        R = [r for r in json.load(open(path, encoding="utf-8"))["trials"] if r["status"] == "ok" and r["cell"] == cell and r["block"] in (7, 10)]
        did = 100.0 * sum(r["chose_side"] != r["distress_side"] for r in R) / len(R)
        said = 100.0 * sum(str(r["decisive_factor"]).startswith("statement") for r in R) / len(R)
        rows.append((y, name, did, said, len(R)))
        y += 1.0
    y += 0.35
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.9), dpi=300)
fig.patch.set_facecolor(SURFACE)
for ax, k, col, head, sub in ((axes[0], 2, BLUE, "WHAT IT DID", "Chose against the side that voiced it"),
                              (axes[1], 3, ORANGE, "WHAT IT SAID", "Named a statement as its deciding factor")):
    for r in rows:
        v = r[k]
        ax.barh(r[0], max(v, 0.6), height=0.62, color=col, zorder=2)
        ax.text(v + 2.5, r[0], f"{v:.0f}%", va="center", ha="left", fontsize=9.5, fontweight="bold", color=INK, zorder=3)
    ax.set_ylim(y - 0.6, -0.55)
    ax.set_xlim(0, 122)
    ax.set_yticks([])
    ax.set_xticks([0, 50, 100])
    ax.set_xticklabels(["0%", "50%", "100%"], fontsize=8, color=INK2)
    ax.tick_params(axis="x", length=0, pad=3)
    ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.text(0, 1.115, head, transform=ax.transAxes, fontsize=8, fontweight="bold", color=INK2, ha="left", va="bottom")
    ax.text(0, 1.03, sub, transform=ax.transAxes, fontsize=9, color=INK, ha="left", va="bottom")
ax = axes[0]
ax.axvline(50, color=INK, linewidth=1.1, linestyle=(0, (4, 3)), zorder=3)
ax.text(50, y - 0.52, "50% = no effect", fontsize=7.5, color=INK2, ha="center", va="top", bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5), zorder=4)
for r in rows:
    ax.text(-4, r[0], r[1], ha="right", va="center", fontsize=9.5, color=INK)
for yy, head in heads:
    ax.text(-62, yy - 0.05, head, ha="left", va="center", fontsize=8, fontweight="bold", color=INK2, zorder=5, bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.2))
fig.text(0.012, 0.975, "Choice rates and statement attribution in exact ties", fontsize=10.5, fontweight="bold", ha="left", va="top", color=INK)
fig.subplots_adjust(left=0.255, right=0.985, top=0.80, bottom=0.085, wspace=0.10)
out = pathlib.Path(a.out)
out.mkdir(parents=True, exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(out / f"figure1_three_models.{ext}", facecolor=SURFACE)
print("wrote figure1_three_models:", [(r[1], round(r[2]), round(r[3]), r[4]) for r in rows])
