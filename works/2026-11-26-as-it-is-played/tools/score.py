"""Score experiment 62: the selectors' eights against the pool and against a random eight.

usage: python score.py <work dir>
reads people/drawn-400.json and selections/<ID>/{v*.txt,eight.txt,after.md}
writes results.json
"""
import json, os, random, re, statistics as st, sys
from itertools import combinations

ENDINGS = ["resignation", "time", "checkmate", "draw"]

def nums(path):
    out = []
    for line in open(path):
        m = re.search(r"\b(\d{1,2})\b", line)
        if m and 1 <= int(m.group(1)) <= 60:
            n = int(m.group(1))
            if n not in out:
                out.append(n)
    return out

def feats(pool, picks):
    gs = [pool[n - 1] for n in picks]
    k = len(gs)
    f = {e: sum(g["ending"] == e for g in gs) for e in ENDINGS}
    f["short"] = sum(g["moves"] < 15 for g in gs)
    f["long"] = sum(g["moves"] > 50 for g in gs)
    f["high"] = sum(g["mean_elo"] >= 2000 for g in gs)
    f["median_moves"] = st.median(g["moves"] for g in gs)
    f["mean_elo"] = round(st.mean(g["mean_elo"] for g in gs), 1)
    f["n"] = k
    for s in ("blitz", "bullet", "rapid", "ultrabullet"):
        f[s] = sum(g["speed"] == s for g in gs)
    return f

def dev(f, pool):
    return round(sum(abs(f[e] - 8 * sum(g["ending"] == e for g in pool) / 60) for e in ENDINGS), 2)

def main(wd):
    pool = json.load(open(os.path.join(wd, "people/drawn-400.json")))[:60]
    seldir = os.path.join(wd, "selections")
    res = {"pool": feats(pool, range(1, 61)), "selectors": {}, "arms": {}}
    for sid in sorted(os.listdir(seldir)):
        d = os.path.join(seldir, sid)
        vs = sorted([f for f in os.listdir(d) if re.fullmatch(r"v\d+\.txt", f)], key=lambda x: int(x[1:-4]))
        first, final = nums(os.path.join(d, vs[0])), nums(os.path.join(d, "eight.txt"))
        res["selectors"][sid] = {
            "versions": len(vs), "first": first, "final": final,
            "first_f": feats(pool, first), "final_f": feats(pool, final),
            "ending_dev": dev(feats(pool, final), pool),
        }
    rng = random.Random(1880)
    null = {"checkmate": [], "time": [], "short": [], "overlap": []}
    for _ in range(100000):
        a = rng.sample(range(1, 61), 8)
        f = feats(pool, a)
        null["checkmate"].append(f["checkmate"]); null["time"].append(f["time"]); null["short"].append(f["short"])
    for _ in range(20000):
        a, b = set(rng.sample(range(1, 61), 8)), set(rng.sample(range(1, 61), 8))
        null["overlap"].append(len(a & b))
    res["null"] = {k: {"mean": round(st.mean(v), 3), "p05": sorted(v)[len(v) // 20], "p95": sorted(v)[len(v) * 19 // 20]} for k, v in null.items()}
    for arm in "ABC":
        ids = [s for s in res["selectors"] if s.startswith(arm)]
        picks = [n for s in ids for n in res["selectors"][s]["final"]]
        fpicks = [n for s in ids for n in res["selectors"][s]["first"]]
        A = feats(pool, picks); F = feats(pool, fpicks)
        ov = [len(set(res["selectors"][x]["final"]) & set(res["selectors"][y]["final"])) for x, y in combinations(ids, 2)]
        counts = {}
        for n in picks:
            counts[n] = counts.get(n, 0) + 1
        res["arms"][arm] = {
            "final": A, "first": F,
            "share": {k: round(100 * A[k] / A["n"], 1) for k in ENDINGS + ["short", "long", "high"]},
            "first_share": {k: round(100 * F[k] / F["n"], 1) for k in ENDINGS + ["short", "long", "high"]},
            "overlap_median": st.median(ov), "overlaps": ov,
            "most_chosen": sorted(counts.items(), key=lambda kv: -kv[1])[:10],
            "distinct_games": len(counts),
            "ending_dev": [res["selectors"][s]["ending_dev"] for s in ids],
        }
    # added after the run (not predicted): how close each eight sits to the sixty's mix of endings,
    # against random eights; and how many eights hold a draw
    rng2 = random.Random(1881)
    close = drawn = 0
    for _ in range(100000):
        f = feats(pool, rng2.sample(range(1, 61), 8))
        close += dev(f, pool) <= 1.73
        drawn += f["draw"] > 0
    res["extra"] = {"null_close": round(100 * close / 100000, 1), "null_draw": round(100 * drawn / 100000, 1),
                    "close": {a: sum(res["selectors"][s]["ending_dev"] <= 1.73 for s in res["selectors"] if s[0] == a) for a in "ABC"},
                    "draw": {a: sum(res["selectors"][s]["final_f"]["draw"] > 0 for s in res["selectors"] if s[0] == a) for a in "ABC"},
                    "first_close": {a: sum(dev(res["selectors"][s]["first_f"], pool) <= 1.73 for s in res["selectors"] if s[0] == a) for a in "ABC"},
                    "ultrabullet_game_1": {a: sum(1 in res["selectors"][s]["final"] for s in res["selectors"] if s[0] == a) for a in "ABC"}}
    all_picks = {}
    for s in res["selectors"].values():
        for n in s["final"]:
            all_picks[n] = all_picks.get(n, 0) + 1
    res["never_chosen"] = [n for n in range(1, 61) if n not in all_picks]
    res["never_chosen_f"] = feats(pool, res["never_chosen"]) if res["never_chosen"] else None
    json.dump(res, open(os.path.join(wd, "results.json"), "w"), indent=1)
    for arm in "ABC":
        a = res["arms"][arm]
        print(arm, a["share"], "first", a["first_share"], "overlap", a["overlap_median"], "elo", a["final"]["mean_elo"], "med", a["final"]["median_moves"], "dev", a["ending_dev"])
    print("pool", res["pool"]); print("null", res["null"]); print("never", len(res["never_chosen"]), res["never_chosen_f"])

if __name__ == "__main__":
    main(sys.argv[1])
