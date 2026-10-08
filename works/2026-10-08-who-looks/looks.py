"""looks.py -- M1 and M2, mechanical. For every maker: number of looks (viewer log), and for each look k
whether the work changed before the next look or the final file, and how many lines differ between the
first look and the final file (difflib, unified, changed lines counted on both sides). Writes looks.json."""
import difflib, hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))["plan"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
out = {}
for p in plan:
    m = p["maker"]; d = os.path.join(HERE, "makers", m)
    final = os.path.join(d, "index.html")
    log = os.path.join(d, "renders", "log.jsonl")
    looks = [json.loads(l) for l in open(log)] if os.path.exists(log) else []
    snaps = [os.path.join(d, "renders", "%02d.html" % L["n"]) for L in looks]
    hashes = [sha(s) for s in snaps] + [sha(final)]
    changed_after = [hashes[k] != hashes[k + 1] for k in range(len(snaps))]
    lines = None
    if snaps:
        a = open(snaps[0]).read().splitlines(); b = open(final).read().splitlines()
        lines = sum(1 for l in difflib.unified_diff(a, b, lineterm="", n=0)
                    if l[:1] in "+-" and not l.startswith(("+++", "---")))
    out[m] = {"arm": p["arm"], "looks": len(looks), "changed_after_look": changed_after,
              "final_equals_last_look": (hashes[-2] == hashes[-1]) if snaps else None,
              "lines_first_look_to_final": lines, "final_lines": len(open(final).read().splitlines()),
              "errors_at_looks": [L["errors"] for L in looks]}
json.dump(out, open(os.path.join(HERE, "looks.json"), "w"), indent=1)
for m, r in out.items():
    print(m, r["arm"], r["looks"], r["changed_after_look"], r["final_equals_last_look"], r["lines_first_look_to_final"], "/", r["final_lines"])
