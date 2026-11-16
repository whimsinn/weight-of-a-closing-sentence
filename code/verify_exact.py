"""Independent check of the cross-model counts and exact sign-flip p-values.

Recomputes, without importing analyze.py, the distress premium in exact ties
(block 7) for each model and the exact two-sided sign-flip p-value over all
2^24 assignments of signs to the 24 scenario premiums. Also recounts the
decisive controls that followed the council's rule.

Usage:
    python code/verify_exact.py [--out results/exact_check.json]
"""
import argparse
import collections
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "Gemini 4 Hydrogen": ROOT / "data" / "gemini-4-hydrogen.json",
    "GPT-6.1 Terra": ROOT / "data" / "gpt-6.1-terra.json",
    "Claude Sonnet 5.5": ROOT / "data" / "claude-sonnet-5.5.json",
}
SHARED_BLOCKS = (1, 7, 9, 10)


def check(path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    rows = [r for r in obj["trials"] if r["block"] in SHARED_BLOCKS]
    assert len(rows) == len({r["trial_id"] for r in rows}) == 336
    assert all(r["status"] == "ok" for r in rows)
    tie = [r for r in rows if r["cell"] == "EVENA"]
    controls = [r for r in rows if r["cell"] == "PC"]
    assert len(tie) == 96 and len(controls) == 48

    by_scenario = collections.defaultdict(lambda: {"X": [], "Y": []})
    for r in tie:
        by_scenario[r["scenario"]][r["distress_side"]].append(int(r["chose_side"] == "X"))
    premiums = []
    for pair in by_scenario.values():
        assert len(pair["X"]) == len(pair["Y"]) == 2
        premiums.append((Fraction(sum(pair["X"]), 2) - Fraction(sum(pair["Y"]), 2)) / 2)
    assert len(premiums) == 24

    # Exact distribution of the sum over every assignment of signs.
    distribution = collections.Counter({Fraction(0): 1})
    for value in premiums:
        updated = collections.Counter()
        for total, n in distribution.items():
            updated[total + value] += n
            updated[total - value] += n
        distribution = updated
    observed = abs(sum(premiums))
    extreme = sum(n for total, n in distribution.items() if abs(total) >= observed)
    exact_p = Fraction(extreme, 2 ** len(premiums))

    followed = sum(r["chose_side"] == ("X" if r["margin"] == "favX" else "Y") for r in controls)
    return {
        "valid_trials": len(rows),
        "distress_ties": len(tie),
        "chose_distressed_side": sum(r["chose_side"] == r["distress_side"] for r in tie),
        "decisive_controls_followed_rule": followed,
        "premium_points": round(100 * float(sum(premiums) / len(premiums)), 2),
        "exact_signflip_p": float(exact_p),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", help="write the report to this JSON file")
    args = parser.parse_args()
    report = {name: check(path) for name, path in FILES.items()}
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
