"""Heard on Paper -- score the eight makings by the rules in predictions.md (fixed before the run).
Run: python3 score.py   (reads songs.json, makings/*.json; writes results.json)"""
import json, re, os, glob, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
songs = {s["key"]: s for s in json.load(open(os.path.join(HERE, "songs.json")))["songs"]}
MARKERS = {"a": ["drink", "your tea"], "b": ["cooks for"], "c": ["canada", "peabody"],
           "d": ["teacher", "tea cher"], "e": ["pleased", "meetcha", "meet you", "beecher"],
           "f": ["fee bee", "feebee", "sweetie"], "g": ["free beer", "beep"], "h": ["so sweet"],
           "i": ["cheer", "birdie"], "j": ["spit", "see if i care", "chicka"]}
CANON_SYL = {"a": 3, "b": 9, "c": 8, "d": 6, "e": 6, "f": 2, "g": 2, "h": 6, "i": 3, "j": 7}
LEAK = ["error", "mistake", "method", "norm"]


def norm(s):
    return " " + re.sub(r"[^a-z']+", " ", s.lower().replace("-", " ")).strip() + " "


def syllables(phrase):
    n = 0
    for w in re.findall(r"[a-z']+", phrase.lower().replace("-", " ")):
        w2 = w.replace("'", "")
        if len(w2) > 2 and w2.endswith("e") and not w2.endswith(("le", "ee", "ye")):
            w2 = w2[:-1]
        n += max(1, len(re.findall(r"[aeiouy]+", w2)))
    return n


def correct(k, sp):
    name = songs[k]["species"].lower()
    s = (sp or "").lower()
    return name in s or (k == "h" and "yellow warbler" in s)


def canon(k, phrase):
    p = norm(phrase)
    return any(" " + m + " " in p or (" " + m) in p for m in MARKERS[k])


items = []
for f in sorted(glob.glob(os.path.join(HERE, "makings", "*.json"))):
    M = json.load(open(f))
    m = M["maker"]
    opened = M.get("files_opened", [])
    clean = all(re.search(r"/heard/[a-j]\.png$", p) for p in opened)
    for it in M["items"]:
        k = it["image"]
        syl = syllables(it["phrase"])
        txt = norm(it["phrase"] + " " + it.get("grounds", ""))
        items.append({"maker": m, "arm": m[0], "key": k, "count": it["count"], "phrase": it["phrase"],
                      "syllables": syl, "fits_own": abs(syl - it["count"]) <= 1,
                      "canon": canon(k, it["phrase"]), "species": it.get("species"),
                      "confidence": it.get("confidence"), "correct": correct(k, it.get("species")),
                      "knowledge_said": bool(re.search(r"\b(knew|know|known|familiar|mnemonic|field guide|classic|traditional|famous|well known|well-known|memory|remember)", it.get("grounds", "").lower())),
                      "leak": [w for w in LEAK if re.search(r"\b" + w, txt)], "clean": clean,
                      "grounds": it.get("grounds", ""), "elements": it.get("elements", "")})

U = [i for i in items if i["arm"] == "U" and i["clean"]]
N = [i for i in items if i["arm"] == "N" and i["clean"]]
R = {"n_items": len(items), "n_clean": len(U) + len(N), "unclean_makers": sorted({i["maker"] for i in items if not i["clean"]})}

# P1
c = sum(i["correct"] for i in U)
R["P1"] = {"correct": c, "of": len(U), "holds": 4 <= c <= 12}
# P2
uc = [i for i in U if i["correct"]]; un = [i for i in U if not i["correct"]]
a = sum(i["canon"] for i in uc); b = sum(i["canon"] for i in un)
R["P2"] = {"recognised_canon": a, "recognised": len(uc), "unrecognised_canon": b, "unrecognised": len(un),
           "holds": (len(uc) > 0 and a / len(uc) >= 0.6) and (len(un) > 0 and b / len(un) <= 0.10)}
# P3
n3 = sum(i["canon"] for i in N)
R["P3"] = {"canon": n3, "of": len(N), "holds": n3 >= 16}
# P4
fu = sum(i["fits_own"] for i in U) / len(U); fn = sum(i["fits_own"] for i in N) / len(N)
R["P4"] = {"U_fit": round(fu, 3), "N_fit": round(fn, 3), "diff_points": round(100 * (fu - fn), 1), "holds": 100 * (fu - fn) >= 20}
# P5
per = {}
nearer = 0
for k in sorted(songs):
    cu = [i["count"] for i in U if i["key"] == k]; cn = [i["count"] for i in N if i["key"] == k]
    if not cu or not cn:
        per[k] = None; continue
    du = abs(st.mean(cu) - CANON_SYL[k]); dn = abs(st.mean(cn) - CANON_SYL[k])
    per[k] = {"U_counts": cu, "N_counts": cn, "canon_syl": CANON_SYL[k], "N_nearer": dn < du}
    nearer += dn < du
R["P5"] = {"songs_N_nearer": nearer, "per_song": per, "holds": nearer >= 6}
# P6
wrong = [i for i in U if not i["correct"] and (i["species"] or "unknown").lower() != "unknown" and (i["confidence"] or 0) >= 50]
w = sum(i["knowledge_said"] for i in wrong)
R["P6"] = {"wrong_confident": len(wrong), "said_knowledge": w,
           "holds": None if len(wrong) < 2 else w >= len(wrong) / 2}
# P7
lk = [i for i in items if i["leak"]]
R["P7"] = {"items_with_leak_words": len(lk), "which": [(i["maker"], i["key"], i["leak"]) for i in lk], "holds": len(lk) <= 1}

json.dump({"results": R, "items": items}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for k, v in R.items():
    print(k, v if k != "P5" else {kk: vv for kk, vv in v.items() if kk != "per_song"})
print()
for i in items:
    print(i["maker"], i["key"], "c=%s s=%s" % (i["count"], i["syllables"]), "C" if i["canon"] else ".",
          "R" if i["correct"] else ".", "|", i["phrase"], "|", i["species"], i["confidence"])
