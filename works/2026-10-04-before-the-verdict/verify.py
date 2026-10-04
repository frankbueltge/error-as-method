"""Check the git order Before the Verdict claims. Run from the repository root or this directory."""
import subprocess, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=here, text=True).strip(); rel = os.path.relpath(here, top)
def first(path):   # oldest commit that contains the path
    out = subprocess.check_output(["git", "log", "--diff-filter=A", "--format=%H %ct", "--", f"{rel}/{path}"], cwd=top, text=True).split()
    return (out[-2], int(out[-1])) if out else (None, None)
def order(c):
    return int(subprocess.check_output(["git", "rev-list", "--count", c], cwd=top, text=True))
ok = True
def check(cond, msg):
    global ok; print(("PASS " if cond else "FAIL ") + msg); ok &= bool(cond)
pre = first("PREDICTIONS.md"); har = first("harvest-log.json"); gen = first("variants.js")
check(pre[0] and gen[0] == pre[0], "generator committed with the pre-registration")
check(order(pre[0]) < order(har[0]), "pre-registration precedes the harvest")
chg = subprocess.check_output(["git", "log", "--format=%H", "--", f"{rel}/variants.js"], cwd=top, text=True).split()
check(len(chg) == 1, "variants.js never changed after its first commit")
V = [json.loads(l) for l in open(os.path.join(here, "verdicts.jsonl"))]
seen_v = {}
for v in V:
    if "revises" in v: continue
    img = first(f"seen/V{v['variant']:02d}.png")
    # the first commit in which this verdict's order appears in verdicts.jsonl
    log = subprocess.check_output(["git", "log", "--reverse", "--format=%H", "--", f"{rel}/verdicts.jsonl"], cwd=top, text=True).split()
    vc = next(c for c in log if f'"order": {v["order"]},' in subprocess.check_output(["git", "show", f"{c}:{rel}/verdicts.jsonl"], cwd=top, text=True))
    check(order(img[0]) < order(vc), f"V{v['variant']:02d}: image committed before its verdict")
    for n in v.get("minted", []):
        nc = next(c for c in subprocess.check_output(["git", "log", "--reverse", "--format=%H", "--", f"{rel}/NORMS.md"], cwd=top, text=True).split()
                  if f"**{n}**" in subprocess.check_output(["git", "show", f"{c}:{rel}/NORMS.md"], cwd=top, text=True))
        check(order(img[0]) < order(nc), f"{n}: first committed after the image of V{v['variant']:02d}, at which it was minted")
v24 = first("variant24.js"); last_grid = first("seen/V22.png")
check(order(v24[0]) < order(first("seen/V24.png")[0]), "V24 written before it was rendered")
sys.exit(0 if ok else 1)
