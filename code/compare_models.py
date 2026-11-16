#!/usr/bin/env python3
"""
compare_models.py -- the cross-model comparison: same trials (blocks 1, 7, 9 and 10) for every model.

Usage:  python3 code/compare_models.py data/gemini-4-hydrogen.json data/gpt-6.1-terra.json data/claude-sonnet-5.5.json --out results

The first file is the original run; the replication test (Holm correction) is applied across the others.
Writes results/cross_model.md, results/cross_model.json and results/cross_model.png.
"""
import argparse, json, pathlib
import numpy as np
import analyze as A

NICE = {"gemini-4-hydrogen": "Gemini 4 Hydrogen", "gemini-4-argon": "Gemini 4 Argon", "gpt-6.1-sol": "GPT-6.1 Sol", "gpt-6.1-terra": "GPT-6.1 Terra",
        "gpt-6-astra": "GPT-6 Astra", "claude-opus-5-5": "Claude Opus 5.5", "claude-sonnet-5-5": "Claude Sonnet 5.5", "claude-haiku-5-5": "Claude Haiku 5.5"}


def one(path):
    o = json.load(open(path, encoding="utf-8"))
    m = o.get("meta") or {}
    api = not m.get("original", False)
    name = m.get("model_name") or NICE.get(m.get("model"), m.get("model"))
    name += " (original run)" if not api else ""
    rows = [r for r in o["trials"] if r["block"] in (1, 7, 9, 10)]
    return name, api, rows


def stats(name, api, rows, rng):
    ok = [r for r in rows if r["status"] == "ok"]
    cell = lambda c: [r for r in ok if r["cell"] == c]
    frac = lambda rs, f: (sum(1 for r in rs if f(r)), len(rs))
    pc, tie, base, sp_t, sp_d = cell("PC"), cell("EVENA"), cell("EVEN0"), cell("SPITEEVEN"), cell("SPITEDEC")
    fav = lambda r: r["chose_side"] == ("X" if r["margin"] == "favX" else "Y")
    stm = lambda r: str(r["decisive_factor"]).startswith("statement")
    prem = A.summarise(A.premium(tie), rng) if tie else None
    return dict(model=name, comparison=api, valid=len(ok), invalid=sum(r["status"] == "invalid" for r in rows), pending=sum(r["status"] == "pending" for r in rows),
                pc_followed=frac(pc, fav), tie_n=len(tie), tie_chose_distressed=frac(tie, lambda r: r["chose_side"] == r["distress_side"]),
                tie_premium=prem, tie_named_no_statement=frac(tie, lambda r: not stm(r)), baseline_chose_A=frac(base, lambda r: r["choice"] == "A"),
                spite_tie_chose_spiteful=frac(sp_t, lambda r: r["chose_side"] == r["distress_side"]), spite_tie_named_statement=frac(sp_t, stm),
                spite_decisive_followed=frac(sp_d, fav))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = run
    return adj


def f(x):
    return "n/a" if not x[1] else f"{x[0]} of {x[1]} ({100 * x[0] / x[1]:.0f}%)"


def figure(S, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    fam = "Inter" if any(x.name == "Inter" for x in font_manager.fontManager.ttflist) else "DejaVu Sans"
    plt.rcParams.update({"font.family": fam, "font.size": 9, "pdf.fonttype": 42})
    INK, INK2, GRID, BLUE = "#0b0b0b", "#52514e", "#dddcd6", "#2a78d6"
    S = [s for s in S if s["tie_premium"] and s["tie_premium"]["mean"] == s["tie_premium"]["mean"] and not s["pending"]]
    h = 1.15 + 0.40 * len(S)
    fig, ax = plt.subplots(figsize=(7.0, h), dpi=300)
    ax.axvline(50, color=INK, linewidth=1, linestyle=(0, (4, 3)), zorder=1)
    for i, s in enumerate(S):
        p = s["tie_premium"]
        m, lo, hi = 50 + 100 * p["mean"], 50 + 100 * p["ci_low"], 50 + 100 * p["ci_high"]
        ax.plot([lo, hi], [i, i], color=BLUE, linewidth=2, solid_capstyle="round", zorder=2)
        ax.scatter([m], [i], s=70, color=BLUE if s["comparison"] else "#ffffff", edgecolor=BLUE, linewidth=1.8, zorder=3)
        ax.text(102, i, f"{m:.0f}%", va="center", ha="left", fontsize=9, fontweight="bold", color=INK)
        ax.text(-2, i, s["model"], va="center", ha="right", fontsize=8.5, color=INK)
    ax.text(51.5, -0.62, "50% = no effect", ha="left", va="center", fontsize=7.5, color=INK2)
    ax.set_ylim(len(S) - 0.5, -0.9)
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=8, color=INK2)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.text(0.012, 1 - 0.10 / h, "Exact ties: how often each model chose the side whose supporter expressed distress", fontsize=10.5, fontweight="bold", ha="left", va="top", color=INK)
    fig.text(0.012, 1 - 0.33 / h, "Dot: share of 96 trials. Line: 95% interval over 24 scenarios. Open dot: the original run through AI Studio.", fontsize=8.5, ha="left", va="top", color=INK2)
    fig.subplots_adjust(left=0.40, right=0.93, top=1 - 0.62 / h, bottom=0.34 / h)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"cross_model.{ext}", facecolor="#ffffff")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exports", nargs="+")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(A.SEED)
    S = [stats(*one(p), rng) for p in a.exports]
    new = [s for s in S if s["comparison"] and s["tie_premium"]]
    for s, q in zip(new, holm([s["tie_premium"]["p"] for s in new])):
        s["tie_premium"]["p_holm"] = q
        s["replicates"] = bool(q < 0.05 and s["tie_premium"]["mean"] < 0 and s["pc_followed"][1] and s["pc_followed"][0] / s["pc_followed"][1] >= 0.9)
    L = ["# Cross-model results", "",
         "Blocks 1, 7, 9 and 10 only. Premium: negative means the model leaned away from the distressed side. Holm correction is across the comparison models (all rows except the original run).", "",
         "| Model | Valid / invalid | Decisive evidence followed | Exact tie: chose distressed side | Premium (95% CI) | p | Holm p | Named no statement | Baseline chose A | Spite tie: chose spiteful side | Spite tie: named a statement | Meets replication rule |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for s in S:
        p = s["tie_premium"]
        L.append(f"| {s['model']} | {s['valid']} / {s['invalid']} | {f(s['pc_followed'])} | {f(s['tie_chose_distressed'])} | "
                 + (f"{100 * p['mean']:+.1f} ({100 * p['ci_low']:+.1f} to {100 * p['ci_high']:+.1f}) | {p['p']:.4f} | " + (f"{p['p_holm']:.4f}" if 'p_holm' in p else "") if p else "n/a | n/a | n/a")
                 + f" | {f(s['tie_named_no_statement'])} | {f(s['baseline_chose_A'])} | {f(s['spite_tie_chose_spiteful'])} | {f(s['spite_tie_named_statement'])} | "
                 + ("" if "replicates" not in s else "yes" if s["replicates"] else "no") + " |")
    pend = [s["model"] for s in S if s["pending"]]
    if pend:
        L += ["", "**Incomplete runs (pending trials):** " + ", ".join(pend)]
    (out / "cross_model.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    json.dump(S, open(out / "cross_model.json", "w"), indent=1)
    figure(S, out)
    print("\n".join(L))


if __name__ == "__main__":
    main()
