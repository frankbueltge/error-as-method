"""Write face-data.js for the face: the sixty (positions per ply), who chose what and why, the table.

usage: python face_data.py <work dir>
"""
import json, os, re, sys

def main(wd):
    pool = json.load(open(os.path.join(wd, "people/drawn-400.json")))[:60]
    res = json.load(open(os.path.join(wd, "results.json")))
    out = {"pool": [], "counts": {"A": {}, "B": {}, "C": {}}, "why": {}, "eights": {}}
    for g in pool:
        out["pool"].append({"sp": g["speed"], "tc": g["time_control"], "we": g["white_elo"], "be": g["black_elo"],
                            "end": g["ending"], "mv": g["moves"], "op": g["opening"], "f": g["fens"]})
    for sid, s in res["selectors"].items():
        arm = sid[0]
        out["eights"][sid] = s["final"]
        for n in s["final"]:
            out["counts"][arm][n] = out["counts"][arm].get(n, 0) + 1
        d = os.path.join(wd, "selections", sid)
        vs = sorted([f for f in os.listdir(d) if re.fullmatch(r"v\d+\.txt", f)], key=lambda x: int(x[1:-4]))
        for line in open(os.path.join(d, vs[-1])):
            m = re.match(r"\s*[-*]?\s*(?:game[- ]?)?(\d{1,2})\b[\s:.\-–—)]*(.*)", line, re.I)
            if m and int(m.group(1)) in s["final"] and m.group(2).strip():
                out["why"].setdefault(int(m.group(1)), []).append([sid, m.group(2).strip()[:220]])
    P, A = res["pool"], res["arms"]
    nl = res["null"]
    def pc(x, n): return f"{100 * x / n:.1f} %"
    rows = []
    for k, lab in (("checkmate", "ended by checkmate"), ("time", "lost on time"), ("resignation", "resignation"),
                   ("draw", "draw"), ("short", "over before move 15")):
        nul = f"{100 * nl[k]['mean'] / 8:.1f} % ({100 * nl[k]['p05'] / 8:.0f}–{100 * nl[k]['p95'] / 8:.0f} %)" if k in nl else f"{pc(P[k], 60)}"
        rows.append([lab, pc(P[k], 60), nul] + [f"{A[a]['share'][k]} %" for a in "ABC"])
    rows.append(["median length (moves)", str(P["median_moves"]), "—"] + [str(A[a]["final"]["median_moves"]) for a in "ABC"])
    rows.append(["mean rating", str(round(P["mean_elo"])), "—"] + [str(round(A[a]["final"]["mean_elo"])) for a in "ABC"])
    ex = res["extra"]
    rows.append(["eights within 1.73 games of the sixty's mix of endings", "—", f"{ex['null_close']} %"] +
                [f"{ex['close'][a]} of 6" for a in "ABC"])
    rows.append(["eights holding a draw", "—", f"{ex['null_draw']} %"] + [f"{ex['draw'][a]} of 6" for a in "ABC"])
    rows.append(["median games shared by two selectors", "—", f"{nl['overlap']['mean']}"] + [str(A[a]["overlap_median"]) for a in "ABC"])
    out["table"] = rows
    out["tabnote"] = ("Shares over each arm's 48 final picks, repeats counted. The random eight's figures come from "
                      "100,000 eights drawn from the sixty. 'Within 1.73 games' is the total gap between an eight's "
                      "counts of the four endings and eight times the sixty's shares; 1.2 is the closest an eight can come.")
    out["stats"] = {"pool": {"checkmate": P["checkmate"], "time": P["time"], "short": P["short"]},
                    "A": A["A"]["share"], "null_close": ex["null_close"], "null_draw": ex["null_draw"]}
    open(os.path.join(wd, "face-data.js"), "w").write("window.PLAYED=" + json.dumps(out, separators=(",", ":"), ensure_ascii=False) + ";\n")

if __name__ == "__main__":
    main(sys.argv[1])
