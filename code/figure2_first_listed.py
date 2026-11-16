#!/usr/bin/env python3
"""
figure2_first_listed.py -- Figure 2: how often each model chose the first-listed option in exact ties,
by where the distress or spite sentence sat. A tie-break by position alone would give the same bar in every row.
Usage:  python3 code/figure2_first_listed.py data/gemini-4-hydrogen.json data/gpt-6.1-terra.json data/claude-sonnet-5.5.json [--out figures]
Uses the trials all three models share (blocks 7, 9 and the exact-tie half of block 10). Every value is computed from the data files.
"""
import argparse, json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

INK, INK2, GRID, BLUE, GREY, SURFACE = "#0b0b0b", "#52514e", "#dddcd6", "#2a78d6", "#b9b8b0", "#ffffff"
fam = "Inter" if any(f.name == "Inter" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": fam, "font.size": 9, "pdf.fonttype": 42})
NAMES = ["Gemini 4 Hydrogen", "GPT-6.1 Terra", "Claude Sonnet 5.5"]
ap = argparse.ArgumentParser()
ap.add_argument("exports", nargs=3)
ap.add_argument("--out", default="figures")
a = ap.parse_args()
on_first = lambda r: (r["distress_side"] == "X") == r["x_is_A"]          # treated sentence sits in the first-listed option's statement
ROWS = [("Plain tie", "no distress or spite", lambda r: r["cell"] == "EVEN0"),
        ("Distress", "in the other option’s statement", lambda r: r["cell"] == "EVENA" and not on_first(r)),
        ("Distress", "in its own statement", lambda r: r["cell"] == "EVENA" and on_first(r)),
        ("Spite", "in the other option’s statement", lambda r: r["cell"] == "SPITEEVEN" and not on_first(r)),
        ("Spite", "in its own statement", lambda r: r["cell"] == "SPITEEVEN" and on_first(r))]
fig, axes = plt.subplots(1, 3, figsize=(7.0, 3.15), dpi=300, sharey=True)
fig.patch.set_facecolor(SURFACE)
log = []
for ax, name, path in zip(axes, NAMES, a.exports):
    R = [r for r in json.load(open(path, encoding="utf-8"))["trials"] if r["status"] == "ok" and r["block"] in (7, 9, 10)]
    vals = []
    for i, (_, _, f) in enumerate(ROWS):
        rs = [r for r in R if f(r)]
        k = sum(r["choice"] == "A" for r in rs)
        vals.append((k, len(rs)))
    base = 100.0 * vals[0][0] / vals[0][1]
    ax.axvline(base, color=INK, linewidth=1.0, linestyle=(0, (4, 3)), zorder=3)
    for i, (k, n) in enumerate(vals):
        v = 100.0 * k / n
        ax.barh(i, max(v, 0.8), height=0.6, color=GREY if i == 0 else BLUE, zorder=2)
        inside = v >= 30
        ax.text(3 if inside else v + 3, i, f"{v:.0f}%", va="center", ha="left", fontsize=9.5, fontweight="bold",
                color=(INK if i == 0 else "#ffffff") if inside else INK, zorder=4)
    log.append((name, vals))
    ax.set_xlim(0, 104)
    ax.set_ylim(len(ROWS) - 0.5, -0.5)
    ax.set_yticks([])
    ax.set_xticks([0, 50, 100])
    ax.set_xticklabels(["0%", "50%", "100%"], fontsize=7.5, color=INK2)
    ax.tick_params(axis="x", length=0, pad=3)
    ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(name, fontsize=9.5, fontweight="bold", color=INK, loc="left", pad=6)
for i, (head, sub, _) in enumerate(ROWS):
    axes[0].text(-6, i - 0.10, head, ha="right", va="center", fontsize=9.5, color=INK)
    axes[0].text(-6, i + 0.20, sub, ha="right", va="center", fontsize=7.5, color=INK2)
fig.text(0.012, 0.975, "The first-listed option usually won a tie, until its own supporter voiced spite or distress", fontsize=10.5, fontweight="bold", ha="left", va="top", color=INK)
fig.text(0.012, 0.915, "Share of exact ties in which each model chose the first-listed option. Dashed line: that model’s rate in plain ties.", fontsize=8.5, ha="left", va="top", color=INK2)
fig.subplots_adjust(left=0.265, right=0.985, top=0.775, bottom=0.085, wspace=0.17)
out = pathlib.Path(a.out)
out.mkdir(parents=True, exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(out / f"figure2_first_listed.{ext}", facecolor=SURFACE)
print("wrote figure2_first_listed:", log)
