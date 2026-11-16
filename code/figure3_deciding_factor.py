#!/usr/bin/env python3
"""
figure3_deciding_factor.py -- Figure 3: the factor Gemini 4 Hydrogen named as decisive, by evidence condition.

Usage:  python3 code/figure3_deciding_factor.py data/gemini-4-hydrogen.json [--out figures]

Every plotted value is computed from the data file. Needs matplotlib. Writes PNG (300 dpi) and PDF.
"""
import argparse, json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

INK, INK2, GRID = "#0b0b0b", "#52514e", "#dddcd6"
BLUE, ORANGE, GREY, SURFACE = "#2a78d6", "#eb6834", "#b9b8b0", "#ffffff"
fam = "Inter" if any(f.name == "Inter" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": fam, "font.size": 9, "axes.edgecolor": GRID, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK, "pdf.fonttype": 42})


def load(path):
    o = json.load(open(path, encoding="utf-8"))
    return [r for r in o["trials"] if r["status"] == "ok"]


def treated_stmt(r):
    return "statement_1" if (r["distress_side"] == "X") == r["x_is_A"] else "statement_2"


def fig1(R, out):
    """Exact ties: what the model did (left) against what it said decided the choice (right)."""
    rows = [("Distress, one voice", [r for r in R if r["cell"] in ("EVENA", "EVENB")]),
            ("Distress, many voices", [r for r in R if r["cell"] == "COLLA"]),
            ("Spite", [r for r in R if r["cell"] == "SPITEEVEN"])]
    did = lambda rs: 100.0 * sum(r["chose_side"] != r["distress_side"] for r in rs) / len(rs)
    said = lambda rs: 100.0 * sum(str(r["decisive_factor"]).startswith("statement") for r in rs) / len(rs)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75), dpi=300)
    fig.patch.set_facecolor(SURFACE)
    panels = [(axes[0], did, BLUE, "WHAT IT DID", "Chose against the side that voiced it"),
              (axes[1], said, ORANGE, "WHAT IT SAID", "Named a statement as its deciding factor")]
    for ax, f, col, head, sub in panels:
        for i, (name, rs) in enumerate(rows):
            v = f(rs)
            ax.barh(i, v, height=0.52, color=col, zorder=2)
            ax.text(v + 2.5, i, f"{v:.0f}%", va="center", ha="left", fontsize=10, fontweight="bold", color=INK, zorder=3)
        ax.set_ylim(len(rows) - 0.5, -0.5)
        ax.set_xlim(0, 122)
        ax.set_yticks([])
        ax.set_xticks([0, 50, 100])
        ax.set_xticklabels(["0%", "50%", "100%"], fontsize=8)
        ax.tick_params(axis="x", length=0, pad=3)
        ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.text(0, 1.20, head, transform=ax.transAxes, fontsize=8, fontweight="bold", color=INK2, ha="left", va="bottom")
        ax.text(0, 1.05, sub, transform=ax.transAxes, fontsize=9, color=INK, ha="left", va="bottom")
    ax = axes[0]
    ax.axvline(50, color=INK, linewidth=1.1, linestyle=(0, (4, 3)), zorder=3)
    ax.text(50, len(rows) - 0.42, "50% = no effect", fontsize=7.5, color=INK2, ha="center", va="top", bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.5), zorder=4)
    for i, (name, rs) in enumerate(rows):
        ax.text(-4, i - 0.08, name, ha="right", va="center", fontsize=9.5, color=INK)
        ax.text(-4, i + 0.22, f"{len(rs)} trials", ha="right", va="center", fontsize=7.5, color=INK2)
    fig.text(0.012, 0.965, "In exact ties the model went against distress and against spite. It only said so for spite.",
             fontsize=10.5, fontweight="bold", ha="left", va="top", color=INK)
    fig.subplots_adjust(left=0.215, right=0.985, top=0.70, bottom=0.115, wspace=0.10)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"figure1_did_vs_said.{ext}", facecolor=SURFACE)
    plt.close(fig)


def fig2(R, out):
    """What the model named as its deciding factor, by how far apart the numbers were."""
    num = lambda r: r["decisive_factor"] in ("user_estimates", "citywide_support", "service_detail", "annual_cost", "hardship_score")
    stm = lambda r: str(r["decisive_factor"]).startswith("statement")
    rows = [("Decisive evidence", "estimates far apart", [r for r in R if r["margin"] in ("favX", "favY")]),
            ("Near-tie", "numbers differ by 1 to 3", [r for r in R if r["margin"] == "tie"]),
            ("Exact tie", "every number identical", [r for r in R if r["margin"] == "even"])]
    fig, ax = plt.subplots(figsize=(7.0, 2.35), dpi=300)
    fig.patch.set_facecolor(SURFACE)
    words = {ORANGE: "a statement", GREY: "neither"}
    for i, (name, sub, rs) in enumerate(rows):
        n = len(rs)
        parts = [(sum(num(r) for r in rs), BLUE, "#ffffff"), (sum(stm(r) for r in rs), ORANGE, "#ffffff"), (sum(not num(r) and not stm(r) for r in rs), GREY, INK)]
        left, small = 0.0, []
        for cnt, col, txt in parts:
            w = 100.0 * cnt / n
            if cnt:
                ax.barh(i, w, left=left, height=0.56, color=col, edgecolor=SURFACE, linewidth=1.6)
                if w >= 9:
                    ax.text(left + w / 2, i, f"{cnt} of {n}" if w > 30 else f"{cnt}", ha="center", va="center", color=txt, fontsize=9, fontweight="bold")
                else:
                    small.append((cnt, col))
            left += w
        if small:
            ax.text(101.5, i, ", ".join(f"{c} {words[col]}" for c, col in small), ha="left", va="center", color=INK2, fontsize=8)
        ax.text(-1.5, i - 0.10, name, ha="right", va="center", color=INK, fontsize=9.5)
        ax.text(-1.5, i + 0.22, sub, ha="right", va="center", color=INK2, fontsize=7.5)
    ax.set_ylim(len(rows) - 0.45, -0.5)
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=8)
    ax.tick_params(axis="x", length=0, pad=3)
    for sp in ax.spines.values():
        sp.set_visible(False)
    h = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, ORANGE, GREY)]
    fig.legend(h, ["A number in the evidence table", "A citizen statement", "Neither (\u201cother\u201d)"], loc="upper left", bbox_to_anchor=(0.004, 0.86),
               ncol=3, frameon=False, fontsize=8, handlelength=1.1, handleheight=0.9, columnspacing=1.6, handletextpad=0.5)
    fig.text(0.012, 0.965, "When a number differed, Gemini 4 Hydrogen almost always named a number as decisive", fontsize=10.5, fontweight="bold", ha="left", va="top", color=INK)
    fig.subplots_adjust(left=0.235, right=0.80, top=0.72, bottom=0.14)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"figure3_deciding_factor.{ext}", facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--out", default="figures")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    R = load(a.export)
    fig2(R, out)
    print("wrote", ", ".join(sorted(p.name for p in out.iterdir())))
