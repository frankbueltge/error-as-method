"""The coder of PREDICTIONS.md, implemented as written there (Session 104), and the scoring.
Writes coded.json (per record) and results.json (population figures, P1-P5)."""
import json, re
STOP = set("this paper article manuscript submission has have been is was withdrawn by the author authors arxiv admin administrator administrators".split())
ERR = re.compile(r"error|mistake|flaw|incorrect|wrong|gap|bug|invalid|false|erroneous|not correct|not valid|fail")
LOC = re.compile(r"\b(eq|eqs|equation|equations|lemma|theorem|thm|proposition|prop|corollary|section|sec|proof of|figure|fig|table|page|step|claim|appendix|formula)\b")
OTH = re.compile(r"pointed out|thanks to|thank|referee|reviewer|noticed by|found by|discovered by|colleague|brought to our attention|brought to my attention")
ADM = re.compile(r"arxiv admin|administrator|moderat|removed by arxiv|by arxiv")

def code(comment):
    c = comment.lower()
    if "withdr" not in c:
        return {"notice": 0}
    words = [w for w in c.split() if w not in STOP]
    rest = re.sub(r"[\W\d_]+", "", " ".join(words))
    err = bool(ERR.search(c))
    return {"notice": 1, "bare": int(rest == ""), "error": int(err),
            "located": int(err and bool(LOC.search(c))), "other": int(bool(OTH.search(c))),
            "admin": int(bool(ADM.search(c)))}

if __name__ == "__main__":
    rows = json.load(open("notices.json"))
    coded = [dict(id=r["id"], published=r["published"], cat=r["cat"], **code(r["comment"])) for r in rows]
    json.dump(coded, open("coded.json", "w"), indent=0)
    N = [c for c in coded if c["notice"]]
    nb = [c for c in N if not c["bare"]]
    er = [c for c in N if c["error"]]
    pct = lambda a, b: round(100 * a / b, 2)
    res = {"records": len(rows), "other_use": len(rows) - len(N), "notice": len(N),
           "bare": sum(c["bare"] for c in N), "not_bare": len(nb), "error": len(er),
           "located": sum(c["located"] for c in N), "other": sum(c["other"] for c in nb),
           "admin": sum(c["admin"] for c in N)}
    res["P1_bare_pct_of_notice"] = pct(res["bare"], len(N))
    res["P2_located_pct_of_error"] = pct(res["located"], len(er))
    res["P3_other_pct_of_not_bare"] = pct(res["other"], len(nb))
    res["P4_error_pct_of_not_bare"] = pct(sum(c["error"] for c in nb), len(nb))
    res["P1"] = "holds" if res["P1_bare_pct_of_notice"] >= 25 else "falsified"
    res["P2"] = "holds" if res["P2_located_pct_of_error"] < 30 else "falsified"
    res["P3"] = "holds" if res["P3_other_pct_of_not_bare"] < 5 else "falsified"
    res["P4"] = "holds" if res["P4_error_pct_of_not_bare"] >= 50 else "falsified"
    # P5: coder against hand
    byid = {c["id"]: c for c in coded}
    hand = json.load(open("hand.json"))
    agree, dis = {}, {}
    for k in ["bare", "error", "located", "other"]:
        agree[k] = sum(byid[h["id"]][k] == h[k] for h in hand)
        dis[k] = [h["n"] for h in hand if byid[h["id"]][k] != h[k]]
    res["P5_agreement_of_60"] = agree
    res["P5_disagreeing_rows"] = dis
    res["P5"] = {k: ("holds" if v >= 54 else "falsified") for k, v in agree.items()}
    res["hand_counts"] = {k: sum(h[k] for h in hand) for k in ["bare", "error", "located", "other", "admin"]}
    json.dump(res, open("results.json", "w"), indent=1)
    print(json.dumps(res, indent=1))
