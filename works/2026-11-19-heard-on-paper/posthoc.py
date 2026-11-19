"""Heard on Paper -- POST HOC readings, written after the results were seen. Labelled as such everywhere.
A. Declared avoidance: grounds that name a known rendering and say it was not used.
B. Convergence: for each song, how many of the six maker pairs share a content word, against how many
   phrases share a content word with the published rendering(s).
Run: python3 posthoc.py (reads results.json, songs.json; writes posthoc.json)"""
import json, re, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
songs = {s["key"]: s for s in json.load(open(os.path.join(HERE, "songs.json")))["songs"]}
items = R["items"]
STOP = set("a an the and or so oh ah then now is he in you your i me my it to of on up down".split())

AVOID = re.compile(r"(avoid|did not use|didn't use|left it out|kept away|on purpose|deliberately|used neither|did not use them|instead of)", re.I)
KNOWS = re.compile(r"(knew|know|known|familiar|mnemonic|recogni[sz]ed|well-known|well known)", re.I)
A = []
for i in items:
    g = i["grounds"]
    A.append({"maker": i["maker"], "key": i["key"], "knows": bool(KNOWS.search(g)), "avoids": bool(AVOID.search(g))})


def words(s):
    w = re.findall(r"[a-z]+", s.lower().replace("-", " "))
    w = [re.sub(r"(.)\1{2,}", r"\1", x) for x in w]      # whyyy -> why, ooooh -> oh
    return {x for x in w if x not in STOP and len(x) > 1}


B = {}
for k in sorted(songs):
    ph = [(i["maker"], words(i["phrase"])) for i in items if i["key"] == k]
    pairs = list(itertools.combinations(ph, 2))
    shared = [(a[0], b[0], sorted(a[1] & b[1])) for a, b in pairs if a[1] & b[1]]
    can = words(songs[k]["canon"])
    with_canon = [(m, sorted(w & can)) for m, w in ph if w & can]
    B[k] = {"species": songs[k]["species"], "pairs": len(pairs), "pairs_sharing": len(shared), "shared": shared,
            "phrases_sharing_canon_word": with_canon}

out = {"label": "POST HOC: written after the results were seen; not scored against any prediction",
       "A_declared": {"items": len(A), "knows_rendering": sum(a["knows"] for a in A),
                      "knows_and_avoids": sum(a["knows"] and a["avoids"] for a in A),
                      "by_arm": {arm: {"knows": sum(a["knows"] for a in A if a["maker"][0] == arm),
                                       "knows_and_avoids": sum(a["knows"] and a["avoids"] for a in A if a["maker"][0] == arm)}
                                 for arm in "UN"},
                      "rows": A},
       "B_convergence": B,
       "B_total": {"pairs": sum(v["pairs"] for v in B.values()), "pairs_sharing": sum(v["pairs_sharing"] for v in B.values()),
                   "phrases_sharing_canon_word": sum(len(v["phrases_sharing_canon_word"]) for v in B.values())}}
json.dump(out, open(os.path.join(HERE, "posthoc.json"), "w"), indent=1)
print(out["A_declared"]["knows_rendering"], out["A_declared"]["knows_and_avoids"], out["A_declared"]["by_arm"])
print(out["B_total"])
for k, v in B.items():
    print(k, v["species"], v["pairs_sharing"], "/", v["pairs"], v["shared"], "| canon:", v["phrases_sharing_canon_word"])
