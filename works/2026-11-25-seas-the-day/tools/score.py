"""Score experiment 61 against predictions.md. Writes results.json beside the work.

Inputs (all inside the work): people/people.json, people/freq.json (every name counted, the people's and the
makers'), people/coded-told.json (this session's codes, TOLD sample), coding/blind-key.json and
coding/codes-coder.tsv (the fresh coder's blind codes, SCORE sample and makers' finals),
coding/codes-told-coder.tsv (a second fresh coder on the TOLD sample), makings/*/ (names, versions,
estimates.txt, after.txt).
Usage: python3 -I score.py
"""
import json, os, statistics as st, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from features import computed, norm  # noqa: E402

W = os.path.join(here, "..")
P = lambda *a: os.path.join(W, *a)
TOLD = {"PUN": 18.5, "PERSON": 14.0, "SINGLE": 41.0, "UNIQUE": 44.0}


def tsv(path):
    out = {}
    for line in open(path):
        f = line.rstrip("\n").split("\t")
        if len(f) >= 4 and f[0].strip().isdigit():
            out[int(f[0])] = {"PUN": f[1].strip() == "1", "PERSON": f[2].strip() == "1",
                              "FOREIGN": f[3].strip() == "1", "note": f[4].strip() if len(f) > 4 else ""}
    return out


def nums(path):
    return [float(x) for x in open(path).read().split()] if os.path.exists(path) else None


def share(items, key):
    return round(100 * sum(1 for i in items if key(i)) / len(items), 1)


def profile(items):
    return {
        "n": len(items),
        "PUN": share(items, lambda i: i["PUN"]), "PERSON": share(items, lambda i: i["PERSON"]),
        "FOREIGN": share(items, lambda i: i["FOREIGN"]), "SINGLE": share(items, lambda i: i["SINGLE"]),
        "SEQUEL": share(items, lambda i: i["SEQUEL"]), "SEAWORD": share(items, lambda i: i["SEAWORD"]),
        "FREQ0": share(items, lambda i: i["FREQ"] == 0), "FREQ1": share(items, lambda i: i["FREQ"] == 1),
        "FREQ_le1": share(items, lambda i: i["FREQ"] <= 1),
        "FREQ2_9": share(items, lambda i: 2 <= i["FREQ"] < 10),
        "FREQ10_99": share(items, lambda i: 10 <= i["FREQ"] < 100),
        "FREQ100": share(items, lambda i: i["FREQ"] >= 100),
        "FREQ_ge10": share(items, lambda i: i["FREQ"] >= 10),
        "median_freq": st.median(i["FREQ"] for i in items),
        "words_mean": round(st.mean(i["words"] for i in items), 2),
    }


def main():
    freq = json.load(open(P("people", "freq.json")))
    key = json.load(open(P("coding", "blind-key.json")))
    codes = tsv(P("coding", "codes-coder.tsv"))
    missing = [k["n"] for k in key if k["n"] not in codes]
    items = []
    for k in key:
        c = codes.get(k["n"], {"PUN": False, "PERSON": False, "FOREIGN": False, "note": "MISSING"})
        it = {"src": k["src"], "id": k["id"], "name": k["name"], "PUN": c["PUN"], "PERSON": c["PERSON"],
              "FOREIGN": c["FOREIGN"], "coder_note": c["note"], "FREQ": freq[norm(k["name"])]}
        it.update(computed(k["name"]))
        items.append(it)
    people = [i for i in items if i["src"] == "people"]
    arms = {a: [i for i in items if i["src"].startswith(a)] for a in "EDG"}
    makers = sorted({i["src"] for i in items if i["src"] != "people"})

    # the TOLD sample: this session's codes against a second fresh coder
    told_mine = {c["draw"]: c for c in json.load(open(P("people", "coded-told.json")))}
    told_coder = tsv(P("coding", "codes-told-coder.tsv"))
    agree = {}
    for f in ["PUN", "PERSON", "FOREIGN"]:
        a = [(told_mine[d][f], told_coder[d][f]) for d in told_mine if d in told_coder]
        n = len(a); po = sum(x == y for x, y in a) / n
        p1 = sum(x for x, _ in a) / n; p2 = sum(y for _, y in a) / n
        pe = p1 * p2 + (1 - p1) * (1 - p2)
        agree[f] = {"n": n, "session": sum(x for x, _ in a), "coder": sum(y for _, y in a),
                    "agreement": round(po, 3), "kappa": round((po - pe) / (1 - pe), 3) if pe < 1 else None}

    per_maker = {}
    for m in makers:
        mine = [i for i in items if i["src"] == m]
        v1 = [l.strip().upper() for l in open(P("makings", m, "v1.txt")) if l.strip()]
        vers = sorted(f for f in os.listdir(P("makings", m)) if f.startswith("v") and f.endswith(".txt"))
        per_maker[m] = {
            "names": [i["name"] for i in mine], "versions": len(vers),
            "counts": {f: sum(i[f] for i in mine) for f in ["PUN", "PERSON", "SINGLE", "FOREIGN", "SEAWORD"]},
            "freq0": sum(i["FREQ"] == 0 for i in mine), "freq_ge10": sum(i["FREQ"] >= 10 for i in mine),
            "freq_ge100": sum(i["FREQ"] >= 100 for i in mine),
            "v1_freq_ge10": sum(freq[norm(n)] >= 10 for n in v1), "v1_freq0": sum(freq[norm(n)] == 0 for n in v1),
            "v1_median_freq": st.median(freq[norm(n)] for n in v1),
            "final_median_freq": st.median(i["FREQ"] for i in mine),
            "estimates": nums(P("makings", m, "estimates.txt")), "after": nums(P("makings", m, "after.txt")),
        }

    prof = {"people_score": profile(people)}
    for a in "EDG":
        prof[a] = profile(arms[a])
    for a in "EDG":
        v1 = [freq[norm(n)] for m in makers if m.startswith(a)
              for n in (l.strip().upper() for l in open(P("makings", m, "v1.txt")) if l.strip())]
        prof[a]["v1_FREQ_ge10"] = round(100 * sum(x >= 10 for x in v1) / len(v1), 1)
        prof[a]["v1_FREQ0"] = round(100 * sum(x == 0 for x in v1) / len(v1), 1)
        prof[a]["v1_median_freq"] = st.median(v1)

    # recurrence across makers
    rec = {}
    for i in items:
        if i["src"] != "people":
            rec.setdefault(i["name"], set()).add(i["src"])
    recur = sorted(((n, sorted(s)) for n, s in rec.items() if len(s) > 1), key=lambda x: -len(x[1]))

    # predictions
    E, D, G, Pp = prof["E"], prof["D"], prof["G"], prof["people_score"]
    v = {}
    v["P1"] = {"E_PUN": E["PUN"], "verdict": "held" if E["PUN"] >= 35 else "failed" if E["PUN"] <= 25 else "neither"}
    v["P2"] = {"E_FREQ_ge10": E["FREQ_ge10"],
               "verdict": "held" if E["FREQ_ge10"] >= 50 else "failed" if E["FREQ_ge10"] <= 35 else "neither"}
    dm = [m for m in makers if m.startswith("D")]
    est_med = [st.median(per_maker[m]["estimates"][k] for m in dm) for k in range(4)]
    within = sum(abs(e - t) <= 10 for e, t in zip(est_med, TOLD.values()))
    v["P3"] = {"D_median_estimates": est_med, "told": list(TOLD.values()), "within_10": within,
               "verdict": "held" if within >= 3 else "failed" if within <= 1 else "neither"}
    gaps = {}
    for k, f in enumerate(["PUN", "PERSON", "SINGLE"]):
        gaps[f] = st.median(abs(per_maker[m]["counts"][f] - per_maker[m]["estimates"][k] / 10) for m in dm)
    v["P4"] = {"median_abs_gap_per_ten": gaps,
               "verdict": "held" if sum(g <= 1 for g in gaps.values()) >= 2 else
               "failed" if sum(g > 2 for g in gaps.values()) >= 2 else "neither"}
    d_aim = st.mean(per_maker[m]["estimates"][3] for m in dm)
    gd, gg = d_aim - D["FREQ0"], TOLD["UNIQUE"] - G["FREQ0"]
    v["P5"] = {"D_aim": d_aim, "D_FREQ0": D["FREQ0"], "G_aim": TOLD["UNIQUE"], "G_FREQ0": G["FREQ0"],
               "gap_D": round(gd, 1), "gap_G": round(gg, 1),
               "verdict": "held" if gd >= 15 and gg >= 15 else "failed" if abs(gd) <= 5 and abs(gg) <= 5 else "neither"}
    off = {f: round(G[f] - TOLD[f], 1) for f in ["PUN", "PERSON", "SINGLE"]}
    v["P6"] = {"G_minus_told": off,
               "verdict": "held" if all(abs(x) <= 10 for x in off.values()) else
               "failed" if sum(abs(x) > 15 for x in off.values()) >= 2 else "neither"}
    v["P7"] = {"G_SEAWORD": G["SEAWORD"], "people_SEAWORD": Pp["SEAWORD"], "G_FREQ100": G["FREQ100"],
               "people_FREQ100": Pp["FREQ100"],
               "verdict": "held" if G["SEAWORD"] >= 35 or G["FREQ100"] >= 15 else
               "failed" if abs(G["SEAWORD"] - Pp["SEAWORD"]) <= 5 and abs(G["FREQ100"] - Pp["FREQ100"]) <= 5
               else "neither"}

    after = {}
    labels = ["PUN", "PERSON", "SINGLE", "UNIQUE", "FREQ100", "FOREIGN", "SEAWORD"]
    for a in "EDG":
        ms = [m for m in makers if m.startswith(a) and per_maker[m]["after"]]
        after[a] = {l: st.median(per_maker[m]["after"][k] for m in ms) for k, l in enumerate(labels)}
    out = {"profiles": prof, "predictions": v, "after_estimates_median": after,
           "people_score_for_after": {"PUN": Pp["PUN"], "PERSON": Pp["PERSON"], "SINGLE": Pp["SINGLE"],
                                      "UNIQUE": Pp["FREQ1"], "FREQ100": Pp["FREQ100"], "FOREIGN": Pp["FOREIGN"],
                                      "SEAWORD": Pp["SEAWORD"]},
           "told_coding_agreement": agree, "recurring_names": recur, "per_maker": per_maker,
           "coder_missing": missing, "items": items}
    json.dump(out, open(P("results.json"), "w"), indent=1)
    print(json.dumps({"profiles": prof, "predictions": v, "after": after, "agree": agree,
                      "recurring": recur[:15], "missing": missing}, indent=1))


if __name__ == "__main__":
    main()
