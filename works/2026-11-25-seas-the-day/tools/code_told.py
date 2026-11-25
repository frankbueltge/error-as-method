"""Hand codes for the TOLD sample (draws 200-399), entered by Session 187 before any maker ran.

Coded by the session under codebook.md, reading each name once, in draw order. These codes give the
shares told to arm G. The SCORE sample (draws 0-199) is coded later, shuffled together with the makers'
names and without arm labels (tools/blind.py).
"""
import json, os, sys

PUN = [209, 211, 215, 221, 228, 233, 246, 253, 259, 281, 283, 284, 285, 288, 291, 303, 304, 316, 323, 324,
       326, 338, 342, 345, 346, 357, 359, 360, 364, 375, 376, 379, 383, 387, 388, 396, 398]
PERSON = [224, 225, 226, 241, 247, 251, 252, 253, 255, 263, 266, 273, 275, 279, 286, 287, 289, 290, 296, 327,
          339, 355, 365, 372, 385, 395, 396, 397]
FOREIGN = [203, 205, 216, 220, 234, 244, 254, 277, 280, 298, 305, 328, 351, 352, 362, 374, 380]
DOUBT = {
    208: "KALLICOU: perhaps two names fused; not coded PERSON",
    219: "PORT -A -VIA: PORT may be a substitution; not coded PUN",
    224: "FINN: a name with FIN in it; coded PERSON, not PUN",
    238: "PEARL: a given name and a gem; not coded",
    243: "NONI: a grandmother's nickname or a fruit; not coded",
    246: "SOL PURSUIT: sol/soul coded PUN; SOL as Spanish not coded FOREIGN",
    260: "ON REFLECTION: water's reflection possible; not coded PUN",
    297: "SCHOO BOAT: unclear play; not coded",
    319: "SEA CAY: literal (a small island); not coded PUN",
    334: "TAZ II: a cartoon animal; not coded PERSON",
    366: "SEA LARK: a real bird name; not coded PUN",
    377: "LATITUDE: attitude play possible; not coded PUN",
    394: "KEEPER: a fish one keeps; not coded PUN",
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    from features import computed, norm
    base = os.path.join(here, "..", "people")
    rows = json.load(open(os.path.join(base, "people.json")))["rows"]
    freq = json.load(open(os.path.join(base, "freq.json")))
    out = []
    for r in rows[200:]:
        d = r["draw"]
        c = {"draw": d, "name": r["name"], "PUN": d in PUN, "PERSON": d in PERSON, "FOREIGN": d in FOREIGN}
        c.update(computed(r["name"]))
        c["FREQ"] = freq[norm(r["name"])]
        if d in DOUBT:
            c["doubt"] = DOUBT[d]
        out.append(c)
    json.dump(out, open(os.path.join(base, "coded-told.json"), "w"), indent=1)
    n = len(out)
    for k in ["PUN", "PERSON", "FOREIGN", "SINGLE", "SEQUEL", "SEAWORD"]:
        print(k, sum(c[k] for c in out), "of", n)
    print("FREQ=1", sum(c["FREQ"] == 1 for c in out), "FREQ>=100", sum(c["FREQ"] >= 100 for c in out))
