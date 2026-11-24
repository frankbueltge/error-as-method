"""Score the makers against the people and the predictions. Writes results.json.
usage: python3 -I tools/score.py makings/ people/coded.json results.json"""
import json, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import code

mk, peoplep, outp = sys.argv[1:4]
people = [r for r in json.load(open(peoplep)) if r["role"] == "scored"]
sheet = [r for r in json.load(open(peoplep)) if r["role"] == "sheet"]
KEYS = list(people[0]["iconic"])
EST = ["under_construction", "marquee", "blink", "music", "counter", "guestbook", "webring",
       "dark_or_image_bg", "welcome_to_my", "default_bg"]


def rate(rows, k):
    return sum((r["iconic"][k] if k in r["iconic"] else r["plain"][k]) for r in rows)


makers = {}
for m in sorted(os.listdir(mk)):
    d = os.path.join(mk, m)
    vs = sorted((f for f in os.listdir(d) if re.fullmatch(r'index-v\d+\.html', f)),
                key=lambda f: int(re.search(r'\d+', f).group()))
    codes = [code(open(os.path.join(d, f), encoding="utf-8", errors="replace").read()) for f in vs]
    final = code(open(os.path.join(d, "index.html"), encoding="utf-8", errors="replace").read())
    est = None
    if os.path.exists(os.path.join(d, "estimates.txt")):
        # one number per line; where a line also carries its item number ("1. 30"), the last number counts
        nums = [int(re.findall(r'\d+', ln)[-1]) for ln in open(os.path.join(d, "estimates.txt"))
                if re.search(r'\d', ln)]
        if len(nums) >= 10:
            est = dict(zip(EST, nums[:10]))
    makers[m] = {"arm": m[0], "versions": len(vs), "v1": codes[0] if codes else None,
                 "trajectory": [c["n_iconic"] for c in codes], "final": final, "estimates": est}

res = {"people": {"n": len(people), "median_iconic": statistics.median(r["n_iconic"] for r in people),
                  "rates": {k: rate(people, k) for k in KEYS + ["default_bg"]},
                  "median_words": statistics.median(r["plain"]["words"] for r in people)},
       "sheet": {"n": len(sheet), "rates": {k: rate(sheet, k) for k in KEYS + ["default_bg"]},
                 "median_iconic": statistics.median(r["n_iconic"] for r in sheet)},
       "makers": makers}
P = [v for v in makers.values() if v["arm"] == "P"]
S = [v for v in makers.values() if v["arm"] == "S"]
med = lambda xs: statistics.median(xs) if xs else None
pr = {}
pr["P1"] = {"P_median_iconic": med([v["final"]["n_iconic"] for v in P])}
rare = ["under_construction", "marquee", "blink", "music"]
pr["P2"] = {k: sum(v["final"]["iconic"][k] for v in P) for k in rare}
pr["P2"]["signs_in_4_of_6"] = sum(1 for k in rare if pr["P2"][k] >= 4)
pr["P3"] = {"P_default_bg": sum(v["final"]["plain"]["default_bg"] for v in P),
            "S_default_bg": sum(v["final"]["plain"]["default_bg"] for v in S)}
pr["P4"] = {"S_median_iconic": med([v["final"]["n_iconic"] for v in S]),
            "S_rare": {k: sum(v["final"]["iconic"][k] for v in S) for k in rare}}
pe = lambda arm, k: med([v["estimates"][k] for v in arm if v["estimates"]])
pr["P5"] = {"P_median_estimates": {k: pe(P, k) for k in EST}, "S_median_estimates": {k: pe(S, k) for k in EST},
            "people": {k: rate(people, k) for k in EST}}
pr["P5"]["P_three_times"] = sum(1 for k in rare if pr["P5"]["P_median_estimates"][k] is not None
                                and pr["P5"]["P_median_estimates"][k] >= 3 * rate(people, k))
pr["P5"]["S_lower_than_P"] = sum(1 for k in rare if None not in (pr["P5"]["S_median_estimates"][k], pr["P5"]["P_median_estimates"][k])
                                 and pr["P5"]["S_median_estimates"][k] < pr["P5"]["P_median_estimates"][k])
pr["P6"] = {"final_ge_v1": sum(1 for v in makers.values() if v["v1"] and v["final"]["n_iconic"] >= v["v1"]["n_iconic"]),
            "of": len(makers)}
pr["P7"] = {"median_words_all": med([v["final"]["plain"]["words"] for v in makers.values()]),
            "P": med([v["final"]["plain"]["words"] for v in P]), "S": med([v["final"]["plain"]["words"] for v in S])}
res["predictions"] = pr
json.dump(res, open(outp, "w"), indent=1)
print(json.dumps(pr, indent=1))
for m, v in makers.items():
    print(m, v["versions"], v["trajectory"], "final", v["final"]["n_iconic"],
          [k for k in KEYS if v["final"]["iconic"][k]], "words", v["final"]["plain"]["words"])
