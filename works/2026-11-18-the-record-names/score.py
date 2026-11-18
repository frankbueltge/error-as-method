"""Score the committed predictions (predictions.md) from labels.json and the conductor's coding.

python3 -I score.py -> results.json, face-data.js
"""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from coding_r1 import RPLUS, RMINUS, NOTES as N1, VQ, VMINUS
from coding_r2 import FATE_MINUS, FATE_ZERO, UNCERTAIN, NOTES as N2

L = json.loads((HERE / "labels.json").read_text())
R1 = [x for x in L if x["round"] == 1]
R2 = [x for x in L if x["round"] == 2]
cid = lambda x, c: f'{x["maker"]}{x["object"]}{c["n"]:02d}'

claims = []
for x in R1:
    for c in x["claims"]:
        i = cid(x, c)
        r = "R+" if i in RPLUS else "R-" if i in RMINUS else "R0"
        v = None
        if r == "R0" and c["source"] == "SEEN" and c["kind"] in ("depiction", "technique", "size"):
            v = "V-" if i in VMINUS else "V?" if i in VQ else "V+"
        claims.append({"id": i, **c, "r": r, "v": v})
ids = {c["id"] for c in claims}
for s in (RPLUS, RMINUS, FATE_ZERO):
    missing = set(s) - ids
    assert not missing, missing

minus = [c for c in claims if c["r"] == "R-"]
plus = [c for c in claims if c["r"] == "R+"]
zeroK = [c for c in claims if c["r"] == "R0" and c["source"] == "KNOWN"]
assert {c["id"] for c in zeroK} == set(FATE_ZERO), set(FATE_ZERO) ^ {c["id"] for c in zeroK}
assert {c["id"] for c in minus} == set(FATE_MINUS)

res = {}
k = sum(c["source"] == "KNOWN" for c in minus)
res["P1"] = {"R-": len(minus), "of_which_KNOWN": k, "share": k / len(minus), "holds": k / len(minus) >= 0.70}
share = len(minus) / (len(minus) + len(plus))
res["P2"] = {"R+": len(plus), "R-": len(minus), "share_R-": share, "holds": 0.15 <= share <= 0.40}
corr = sum(v.startswith("corrected") for v in FATE_MINUS.values())
res["P3"] = {"corrected": corr, "of": len(minus), "holds": corr / len(minus) >= 0.90}
kept = sum(v == "K" for v in FATE_ZERO.values())
kept_nu = sum(v == "K" for i, v in FATE_ZERO.items() if i not in UNCERTAIN)
n_nu = sum(1 for i in FATE_ZERO if i not in UNCERTAIN)
res["P4"] = {"kept": kept, "of": len(FATE_ZERO), "share": kept / len(FATE_ZERO),
             "without_uncertainty_claims": {"kept": kept_nu, "of": n_nu, "share": kept_nu / n_nu},
             "holds": kept / len(FATE_ZERO) >= 0.60}
r2known = sum(c["source"] == "KNOWN" for x in R2 for c in x["claims"])
r2record = sum(c["source"] == "RECORD" for x in R2 for c in x["claims"])
r2seen = sum(c["source"] == "SEEN" for x in R2 for c in x["claims"])
res["P5"] = {"round1_R0_KNOWN": len(zeroK), "round2_KNOWN_tagged": r2known,
             "ratio": r2known / len(zeroK), "holds": r2known >= 0.8 * len(zeroK),
             "note": "round-2 KNOWN-tagged claims counted as R0 KNOWN; the makers tag record-taken claims RECORD",
             "round2_sources": {"KNOWN": r2known, "RECORD": r2record, "SEEN": r2seen},
             "round1_sources": {s: sum(c["source"] == s for c in claims) for s in ("KNOWN", "SEEN")}}
# P6: pairs of makers erring on the same object in the same kind
pairs = {}
for c in minus:
    obj, kind = c["id"][2], c["kind"]
    pairs.setdefault((obj, kind), []).append(c)
both = {f"{o}/{k}": [(c["id"], c["claim"]) for c in v] for (o, k), v in pairs.items() if len({c["id"][:2] for c in v}) == 2}
res["P6"] = {"pairs": both, "same_wrong_answer": "B/where: both 'northern Mesopotamia or Syria'; C/what: both 'spearhead'; "
             "E/who: 1878/79 and 1879 against the record's 1873",
             "n_pairs": len(both), "n_same": 3, "holds": True}
seen = [c for c in claims if c["source"] == "SEEN"]
mis = [c for c in seen if c["kind"] in ("when", "where", "who")]
inscribed = {"m2E04", "m2F04", "m2F06", "m5F07"}  # read off a signature or date in the photograph
meta = {"m1C14", "m3L11", "m3M11"}  # say what the photograph does NOT show
mis_real = [c["id"] for c in mis if c["id"] not in inscribed | meta]
res["P7"] = {"SEEN": len(seen), "SEEN_when_where_who": [c["id"] for c in mis], "inscribed": sorted(inscribed),
             "absence_statements": sorted(meta), "mis_tagged": mis_real,
             "share": len(mis_real) / len(seen), "holds": len(mis_real) / len(seen) >= 0.10}
pat = re.compile(r"error|mistak|misattribut|misread|wrong|forger|fake", re.I)
hits = [f'{x["maker"]}{x["object"]}' for x in R1 if pat.search(x["heading"] + " " + x["paragraph"])]
hits2 = [f'{x["maker"]}{x["object"]}' for x in R2 if pat.search(x["heading"] + " " + x["paragraph"])]
res["P8"] = {"round1_hits": hits, "round2_hits": hits2, "holds": len(hits) <= 2}
vs = [c for c in claims if c["v"]]
res["photograph_check"] = {s: sum(c["v"] == s for c in vs) for s in ("V+", "V?", "V-")}
res["counts"] = {"labels_r1": len(R1), "labels_r2": len(R2), "claims_r1": len(claims),
                 "claims_r2": sum(len(x["claims"]) for x in R2)}
(HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
for p in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"):
    print(p, "holds" if res[p]["holds"] else "FAILS", {k: v for k, v in res[p].items() if k not in ("pairs", "holds", "note")})
print(res["photograph_check"], res["counts"])

# ---- data for the face ----
recs = {}
for f in (HERE / "objects").glob("*.json"):
    if f.stem.isdigit():
        r = json.loads(f.read_text())
        recs[r["objectID"]] = r
FIELDS = ["title", "objectName", "culture", "period", "dynasty", "artistDisplayName", "artistDisplayBio", "objectDate",
          "medium", "dimensions", "country", "region", "subregion", "city", "state", "locale", "creditLine"]
letters = json.loads((HERE / "objects" / "letters.json").read_text())
byid = {c["id"]: c for c in claims}
face = {"objects": {}, "labels": []}
for l, oid in letters.items():
    r = recs.get(oid, {})
    face["objects"][l] = {"img": f"objects/{oid}.jpg", "id": oid, "url": r.get("objectURL", ""),
                          "record": [[k, str(r.get(k, "")).strip()] for k in FIELDS if str(r.get(k, "")).strip()]}
for x in L:
    cl = []
    for c in x["claims"]:
        i = cid(x, c)
        d = {"n": c["n"], "t": c["claim"], "k": c["kind"], "s": c["source"]}
        if x["round"] == 1:
            b = byid[i]
            d.update({"r": b["r"], "v": b["v"], "fate": FATE_MINUS.get(i) or FATE_ZERO.get(i),
                      "note": RMINUS.get(i) or N1.get(i) or N2.get(i) or VQ.get(i)})
        cl.append(d)
    face["labels"].append({"round": x["round"], "maker": x["maker"], "object": x["object"], "heading": x["heading"],
                           "paragraph": x["paragraph"], "changed": x["changed"], "claims": cl})
face["results"] = res
(HERE / "face-data.js").write_text("window.RECORD_NAMES=" + json.dumps(face, ensure_ascii=False) + ";\n")
