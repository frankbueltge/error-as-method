"""Score experiment 63 against predictions.md. Usage: score.py <work dir>
Reads curators/<id>/{v1.md,final.md,after.md}, curators/replacements.json (hand-read), people/*. Writes results.json."""
import json, os, re, sys, statistics, random, collections
sys.path.insert(0, os.path.dirname(__file__))
from parse import tags, rating

W = sys.argv[1]
rows = {json.loads(l)["n"]: json.loads(l) for l in open(os.path.join(W, "people/pool-160.jsonl"))}
D = json.load(open(os.path.join(W, "people/draws.json")))
draws = {d["draw"]: d for d in D["draws"]}
rep = json.load(open(os.path.join(W, "curators/replacements.json")))
COMMON, RARE = set("PSD"), set("TBOG")
L = "abcdefghijkl"
items = []   # one row per curator x item
cur = {}
for arm in "AB":
    for i in range(1, 7):
        cid = f"{arm}{i}"; f = os.path.join(W, "curators", cid)
        fin, v1 = open(os.path.join(f, "final.md")).read(), open(os.path.join(f, "v1.md")).read()
        tf, t1 = tags(fin), tags(v1)
        assert len(tf) == 12 and len(t1) == 12, (cid, len(tf), len(t1))
        nv = len([x for x in os.listdir(f) if re.fullmatch(r"v\d+\.md", x)])
        cur[cid] = {"arm": arm, "draw": i, "tvd": draws[i]["tvd"], "rating": rating(fin), "versions": nv,
                    "unusual_final": sum(v == "unusual" for v in tf.values()),
                    "unusual_v1": sum(v == "unusual" for v in t1.values()),
                    "replaced": rep[cid]}
        for k, n in enumerate(draws[i]["items"]):
            r = rows[n]
            items.append({"cur": cid, "arm": arm, "draw": i, "label": L[k], "n": n, "title": r["title"],
                          "kind": r["kind"], "words": r["words"], "tag": tf[L[k]], "tag_v1": t1[L[k]],
                          "replaced": L[k] in rep[cid]})

def rate(sel):
    sel = list(sel); return (sum(x["tag"] == "unusual" for x in sel) / len(sel), len(sel)) if sel else (None, 0)

def spearman(x, y):
    def rk(v):
        s = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]: j += 1
            for k in range(i, j + 1): r[s[k]] = (i + j) / 2
            i = j + 1
        return r
    a, b = rk(x), rk(y); ma, mb = statistics.mean(a), statistics.mean(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    den = (sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b)) ** .5
    return num / den if den else None

A = [x for x in items if x["arm"] == "A"]
res = {"curators": cur}
rr, nr = rate(x for x in A if x["kind"] in RARE); rc, nc = rate(x for x in A if x["kind"] in COMMON)
res["P1"] = {"rare_unusual": rr, "n_rare": nr, "common_unusual": rc, "n_common": nc,
             "diff_points": None if rr is None else round(100 * (rr - rc), 1)}
res["P1"]["verdict"] = "held" if res["P1"]["diff_points"] < 15 else "failed"
wu = [x["words"] for x in items if x["tag"] == "unusual"]; wt = [x["words"] for x in items if x["tag"] == "typical"]
res["P2"] = {"median_words_unusual": statistics.median(wu), "n_unusual": len(wu),
             "median_words_typical": statistics.median(wt), "n_typical": len(wt)}
res["P2"]["verdict"] = "held" if res["P2"]["median_words_unusual"] > res["P2"]["median_words_typical"] else "failed"
ca = [cur[f"A{i}"] for i in range(1, 7)]; cb = [cur[f"B{i}"] for i in range(1, 7)]
sA = spearman([c["tvd"] for c in ca], [c["rating"] for c in ca]); sB = spearman([c["tvd"] for c in cb], [c["rating"] for c in cb])
res["P3"] = {"spearman_A": sA, "spearman_B": sB, "ratings_A": [c["rating"] for c in ca], "ratings_B": [c["rating"] for c in cb],
             "verdict": "held" if (sA is None or sA > -0.5) else "failed"}
res["P4"] = {"A_replacing": [len(c["replaced"]) for c in ca], "verdict": "held" if all(c["replaced"] for c in ca) else "failed"}
ta, tb = sum(len(c["replaced"]) for c in ca), sum(len(c["replaced"]) for c in cb)
res["P5"] = {"A_total": ta, "B_total": tb, "verdict": "held" if tb < ta else "failed"}
dd = [x for x in items if x["kind"] == "D"]
hit = sum(1 for x in dd if x["tag"] == "unusual" or x["replaced"])
res["P6"] = {"D_items": len(dd), "unusual_or_replaced": hit, "verdict": "held" if hit * 2 >= len(dd) else "failed"}
# P7 from after.md
est = {}
for cid in cur:
    p = os.path.join(W, "curators", cid, "after.md")
    if os.path.exists(p):
        nums = re.findall(r"^\s*\**\s*([1-5])[\.\)].*?(\d+(?:\.\d+)?)\s*%", open(p).read(), re.M)
        est[cid] = {int(a): float(b) for a, b in nums}
res["after_estimates"] = est
pe = [e[1] for e in est.values() if 1 in e]; ue = [e[5] for e in est.values() if 5 in e]
POOL = {1: 21.2, 2: 13.1, 3: 4.4, 4: 13.1, 5: 28.8}
res["P7"] = {"n": len(pe), "median_person": statistics.median(pe) if pe else None,
             "median_under100": statistics.median(ue) if ue else None,
             "medians_all": {k: statistics.median([e[k] for e in est.values() if k in e]) for k in POOL if any(k in e for e in est.values())},
             "pool": POOL}
res["P7"]["verdict"] = "held" if pe and abs(res["P7"]["median_person"] - 21.2) <= 10 and abs(res["P7"]["median_under100"] - 28.8) <= 15 else "failed"
u1, uf = sum(c["unusual_v1"] for c in cur.values()), sum(c["unusual_final"] for c in cur.values())
res["P8"] = {"unusual_v1": u1, "unusual_final": uf, "verdict": "held" if uf < u1 else "failed"}
# descriptive
res["by_kind"] = {k: {"n": len([x for x in items if x["kind"] == k]),
                      "unusual": sum(x["tag"] == "unusual" for x in items if x["kind"] == k),
                      "pool_share": round(sum(1 for r in rows.values() if r["kind"] == k) / 160, 3)} for k in "PXSDWTBOG"}
st = [x for x in items if x["words"] < 100]; lg = [x for x in items if x["words"] >= 1000]
res["by_length"] = {"under100": rate(st), "1000plus": rate(lg), "all": rate(items)}
res["items"] = items
json.dump(res, open(os.path.join(W, "results.json"), "w"), indent=1, ensure_ascii=False)
for k in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]:
    print(k, {a: b for a, b in res[k].items() if a not in ("pool",)})
print("by_kind", res["by_kind"]); print("by_length", res["by_length"])
