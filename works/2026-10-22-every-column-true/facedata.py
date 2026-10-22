"""facedata.py (Session 147): writes face-data.js for index.html from results.json, mutants.json and the makers'
rooms (each work's index.html as a string, so the face can run it live on a dealt table)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
R = J("results.json"); M = J("mutants.json")["mutants"]; C = ["c1", "c2", "c3", "c4"]
titles = {c: open(os.path.join(H, "rooms", c, "NOTE.md")).readline().lstrip("# ").strip() for c in C}
html = {c: open(os.path.join(H, "rooms", c, "index.html")).read() for c in C}
read = {m["work"]: m["read"] for m in M}
def row(k):
    t = R["table"][k]; low = lambda s: str(s).strip().lower()
    return {"id": k, "work": k[:2], "cols": next((m["cols"] for m in M if m["id"] == k), []),
            "W": low(t["W"]), "WT": low(t["WT"]), "P_words": low(t["P_words"]), "G": low(t["G"]), "G_sure": t["G_sure"], "H": low(t["H"]), "V": low(t["V"]),
            "W_why": t["W_why"], "WT_why": t["WT_why"], "P_why": t["P_why"], "G_why": t["G_why"], "H_why": t["H_why"], "V_why": t["V_why"]}
by = {k: row(k) for k in R["table"]}
P = [l for l in open(os.path.join(H, "PREDICTIONS.md")).read().splitlines() if re.match(r"- \*\*P\d", l)]
preds = []
for l in P:
    pid = re.match(r"- \*\*(P\d)", l).group(1); text = re.sub(r"\*\*", "", l[2:])
    preds.append({"id": pid, "text": text, "held": R[pid]["held"], "detail": R[pid].get("detail", "")})
face = {"titles": titles, "html": html, "read": read, "mutants": [by[m["id"]] for m in M], "byId": by, "preds": preds,
        "seatsnote": R.get("seatsnote", "")}
open(os.path.join(H, "face-data.js"), "w").write("window.FACE = " + json.dumps(face, ensure_ascii=False) + ";\n")
print("face-data.js", os.path.getsize(os.path.join(H, "face-data.js")))
