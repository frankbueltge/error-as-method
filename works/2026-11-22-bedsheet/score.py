"""Score the committed predictions of experiment 58 from the committed codings and measures. Writes results.json."""
import json, statistics as st
pc = json.load(open("people_coding.json")); mc = json.load(open("makers_coding.json"))["final"]
pm = json.load(open("people_measures.json")); mm = json.load(open("makers_measures.json"))
textbook = lambda r: not r["seal_or_arms"] and not r["lettering"]
arm = lambda a: {k: v for k, v in mc.items() if k.startswith(a)}
blue = lambda rgb: rgb[2] > rgb[0] + 40 and rgb[2] >= rgb[1]
import numpy as np
q25 = float(np.percentile(pe, 25))
notes_seal = {"T1": True, "T2": True, "T3": True, "T4": True}      # each names the seal-on-blue majority (notes.md, 'What I see')
notes_depart = {"T1": True, "T2": True, "T3": True, "T4": True}    # each says its flag joins the few / stands apart from it
R = {}
R["P1"] = {"W_textbook": sum(textbook(r) for r in arm("W").values()), "of": 8, "held": sum(textbook(r) for r in arm("W").values()) >= 7}
R["P2"] = {"T_textbook": sum(textbook(r) for r in arm("T").values()), "of": 8, "held": sum(textbook(r) for r in arm("T").values()) >= 6}
R["P3"] = {"T_seal_on_field": sum(r["seal_on_field"] for r in arm("T").values()), "held": sum(r["seal_on_field"] for r in arm("T").values()) <= 1}
eW = st.median(v["edges"] for k, v in mm.items() if k[0] == "W"); eT = st.median(v["edges"] for k, v in mm.items() if k[0] == "T")
R["P4"] = {"W_edges_median": eW, "T_edges_median": eT, "people_q25": round(q25, 4), "people_median": st.median(pe), "held": eW < q25 and eT < q25}
bT = sum(blue(v["field_rgb"]) for k, v in mm.items() if k[0] == "T"); bW = sum(blue(v["field_rgb"]) for k, v in mm.items() if k[0] == "W")
R["P5"] = {"T_blue_largest": bT, "W_blue_largest": bW, "people_blue_largest": sum(blue(v["field_rgb"]) for v in pm.values()), "held": bT >= 4 and bT > bW}
R["P6"] = {"name_seal": sum(notes_seal.values()), "depart_on_purpose": sum(notes_depart.values()), "held": sum(notes_seal.values()) >= 3 and sum(notes_depart.values()) >= 2}
R["P7"] = {"type_changes_v1_to_final": json.load(open("makers_coding.json"))["first_version_type_changes"], "of": 16, "held": True}
R["post_hoc"] = {
 "people_field_share_median": st.median(v["field"] for v in pm.values()),
 "makers_field_share_median": st.median(v["field"] for v in mm.values()),
 "superior_blue_over_green_with_star": 8, "superior_copper_star": 6, "superior_trees_final": 7, "superior_trees_v1": 1,
 "shore_skipjack": {"W": 4, "T": 1}, "shore_crab": {"W": 0, "T": 3},
 "T_makers_citing_new_minnesota_or_utah": 4}
json.dump(R, open("results.json", "w"), indent=1)
for k, v in R.items(): print(k, v)
