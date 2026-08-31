#!/usr/bin/env python3
"""Offline. Reads `harvest.json`, writes `results.json`. No network, stdlib only.

Every number the work states comes from here, and every prediction in `PREDICTIONS.md` is
scored here against the bar written before the harvest ran.
"""
import json
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ELIGIBLE = 10_000   # fixed in PREDICTIONS.md before the counts were known


def pct(n, d):
    return 100.0 * n / d if d else None


def main():
    with open(os.path.join(HERE, "harvest.json"), encoding="utf-8") as fh:
        h = json.load(fh)

    issues = h["issue_enum"]
    branches = h["branches"]
    union = h["union_of_all_flags"]
    inc = h["flag_incidence"]
    total = h["window_total"]

    R = {"population": h["population"], "window_total": total,
         "branch_count": len(branches), "issue_enum_size": len(issues)}

    # ---------------- the table every prediction reads -------------------------------------
    rows = {}
    for b, n in branches.items():
        u = union[b]
        rows[b] = {
            "records": n,
            "share_of_window_pct": pct(n, total),
            "with_at_least_one_flag": u,
            "un_normed": n - u,
            "un_normed_pct": pct(n - u, n),
            "distinct_flags": len(inc[b]),
            "flag_share_of_enum_pct": pct(len(inc[b]), len(issues)),
            "eligible_for_gap": n >= ELIGIBLE,
        }
    R["branch_table"] = rows
    elig = {b: r for b, r in rows.items() if r["eligible_for_gap"]}
    R["eligible_branches"] = sorted(elig)

    # ---------------- P5, the instrument, scored first --------------------------------------
    p5a = {}
    for b in branches:
        counts = list(inc[b].values()) or [0]
        p5a[b] = {
            "union": union[b], "max_single_flag": max(counts), "sum_of_flags": sum(counts),
            "branch_total": branches[b],
            "holds": max(counts) <= union[b] <= sum(counts) and union[b] <= branches[b],
        }
    R["P5a"] = {"bar": "for every branch: max single flag <= union <= sum of flags, and union <= branch total",
                "per_branch": p5a, "won": all(v["holds"] for v in p5a.values())}
    summed = sum(branches.values())
    R["P5b"] = {"bar": "branch counts sum to the window total exactly",
                "sum_of_branches": summed, "window_total": total,
                "difference": total - summed, "won": summed == total}

    # ---------------- P1, the un-normed gap -------------------------------------------------
    un = {b: r["un_normed_pct"] for b, r in elig.items()}
    hi, lo = max(un, key=un.get), min(un, key=un.get)
    gap = un[hi] - un[lo]
    R["P1"] = {
        "bar": "gap in un-normed share between eligible branches >= 25 percentage points",
        "highest": {"branch": hi, "un_normed_pct": un[hi]},
        "lowest": {"branch": lo, "un_normed_pct": un[lo]},
        "gap_points": gap,
        "won": gap >= 25.0,
        "all_branches_un_normed_pct": {b: r["un_normed_pct"] for b, r in rows.items()},
        "window_un_normed_pct": pct(total - sum(union.values()), total),
    }
    # the same gap with the extreme branches dropped, as this line has reported since S75
    if len(un) > 2:
        trimmed = {b: v for b, v in un.items() if b not in (hi, lo)}
        R["P1"]["gap_points_trimmed"] = max(trimmed.values()) - min(trimmed.values())

    # ---------------- P2a, the reachable vocabulary -----------------------------------------
    d = {b: r["distinct_flags"] for b, r in elig.items()}
    most, fewest = max(d, key=d.get), min(d, key=d.get)
    R["P2a"] = {
        "bar": "the eligible branch reaching the fewest distinct flags reaches < half as many as the most",
        "most": {"branch": most, "distinct_flags": d[most]},
        "fewest": {"branch": fewest, "distinct_flags": d[fewest]},
        "ratio": d[fewest] / d[most],
        "won": d[fewest] < 0.5 * d[most],
        "per_branch": {b: r["distinct_flags"] for b, r in rows.items()},
    }

    # ---------------- P2b, the private flags ------------------------------------------------
    where = {i: [b for b in branches if inc[b].get(i, 0) > 0] for i in issues}
    private = {i: w[0] for i, w in where.items() if len(w) == 1}
    unseen = [i for i, w in where.items() if not w]
    everywhere = [i for i, w in where.items() if len(w) == len(branches)]
    R["P2b"] = {
        "bar": ">= 10 of the 105 flag types occur in exactly one branch",
        "private_count": len(private), "private": private,
        "won": len(private) >= 10,
        "flags_never_seen_in_this_window": unseen,
        "flags_in_every_branch": everywhere,
        "branch_count_per_flag": {i: len(w) for i, w in where.items()},
        "private_flags_by_branch": {
            b: sorted(i for i, x in private.items() if x == b) for b in branches
        },
    }
    # overlap of vocabularies, for the work's argument (not a scored prediction)
    vocab = {b: set(inc[b]) for b in branches}
    pairs = [(a, b, len(vocab[a] & vocab[b]) / len(vocab[a] | vocab[b]))
             for a, b in combinations(sorted(branches), 2) if vocab[a] | vocab[b]]
    R["vocabulary_overlap"] = {
        "mean_pairwise_jaccard": sum(p[2] for p in pairs) / len(pairs) if pairs else None,
        "pairs_sharing_nothing": sum(1 for p in pairs if p[2] == 0),
        "pair_count": len(pairs),
        "pairs": [{"a": a, "b": b, "jaccard": j} for a, b, j in sorted(pairs, key=lambda p: -p[2])],
    }

    # ---------------- P3, the box as content ------------------------------------------------
    FLAG = "OCCURRENCE_STATUS_INFERRED_FROM_BASIS_OF_RECORD"
    sh = {b: pct(inc[b].get(FLAG, 0), branches[b]) for b in elig}
    h3, l3 = max(sh, key=sh.get), min(sh, key=sh.get)
    R["P3"] = {
        "flag": FLAG,
        "bar": "gap between eligible branches >= 10 percentage points",
        "highest": {"branch": h3, "pct": sh[h3]}, "lowest": {"branch": l3, "pct": sh[l3]},
        "gap_points": sh[h3] - sh[l3], "won": (sh[h3] - sh[l3]) >= 10.0,
        "per_branch_pct": {b: pct(inc[b].get(FLAG, 0), branches[b]) for b in branches},
        "per_branch_n": {b: inc[b].get(FLAG, 0) for b in branches},
        "window_n": sum(inc[b].get(FLAG, 0) for b in branches),
    }

    # ---------------- P4, the residue, declared ---------------------------------------------
    bori = h["basis_of_record_invalid"]
    by = bori["by_branch"]
    top = max(by, key=by.get) if by else None
    a = pct(by[top], bori["window_total"]) if top else None
    b_ = pct(by[top], branches[top]) if top else None
    R["P4"] = {
        "declared_not_blind": True,
        "bar_a": ">= 99 % of the window's BASIS_OF_RECORD_INVALID records sit in one branch",
        "bar_b": "that branch is under 25 % residue",
        "window_total_flagged": bori["window_total"], "by_branch": by,
        "branch": top, "share_of_flag_in_that_branch_pct": a,
        "residue_share_of_that_branch_pct": b_,
        "won_a": a is not None and a >= 99.0,
        "won_b": b_ is not None and b_ < 25.0,
    }

    # ---------------- the scoreboard --------------------------------------------------------
    blind = {"P1": R["P1"]["won"], "P2a": R["P2a"]["won"], "P2b": R["P2b"]["won"],
             "P3": R["P3"]["won"], "P5a": R["P5a"]["won"], "P5b": R["P5b"]["won"]}
    R["scoreboard"] = {
        "blind": blind,
        "blind_won": sum(1 for v in blind.values() if v),
        "blind_lost": sum(1 for v in blind.values() if not v),
        "declared": {"P4a": R["P4"]["won_a"], "P4b": R["P4"]["won_b"]},
    }

    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(R, fh, indent=1, ensure_ascii=False)

    # a short human read-out
    print(f"window {total:,} in {len(branches)} branches; eligible {sorted(elig)}")
    for b, r in sorted(rows.items(), key=lambda kv: -kv[1]["records"]):
        print(f"  {b:22s} {r['records']:>12,}  un-normed {r['un_normed_pct']:8.4f} %  "
              f"flags {r['distinct_flags']:>3d}/105")
    print(json.dumps(R["scoreboard"], indent=1))
    for k in ("P1", "P2a", "P2b", "P3", "P4"):
        v = R[k]
        print(k, {x: v[x] for x in v if x in ("gap_points", "ratio", "private_count",
                                              "share_of_flag_in_that_branch_pct",
                                              "residue_share_of_that_branch_pct", "won",
                                              "won_a", "won_b")})


if __name__ == "__main__":
    main()
