"""checkprompts.py -- checks that the prompt each maker was given is, byte for byte, the brief in briefs/run/ (or
briefs/again-K.md for every K send), read from the agents' transcripts. The briefs were pasted by hand into the
launch calls, so this is the check that no word was changed in the pasting."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
T = "/tmp/claude-0/-home-user/12d6a705-ad2d-53d3-8b3a-28a1dba3b3ff/tasks/%s.output"
def users(aid):
    out = []
    for line in open(T % aid, encoding="utf-8"):
        try: o = json.loads(line)
        except ValueError: continue
        if o.get("type") == "user":
            c = (o.get("message") or {}).get("content")
            if isinstance(c, str): out.append(c)
            elif isinstance(c, list):
                t = [x.get("text", "") for x in c if x.get("type") == "text"]
                if t: out.append("".join(t))
    return out
ag = json.load(open(os.path.join(HERE, "agents.json")))
arm = {x["lineage"]: x["arm"] for x in json.load(open(os.path.join(HERE, "plan.json")))["lineages"]}
again = open(os.path.join(HERE, "briefs", "again-K.md")).read().strip()
ok = 0; bad = []
for key, aid in sorted(ag.items()):
    u = users(aid)
    brief = open(os.path.join(HERE, "briefs", "run", key + ".md")).read().strip()
    if not u or u[0].strip() != brief: bad.append(key)
    else: ok += 1
    if arm[key[:2]] == "K":
        sends = [x for x in u[1:] if "Make the next version" in x]
        n = sum(1 for x in sends if again in x)
        print(key, "K sends found:", len(sends), "matching again-K:", n)
print("first prompts matching their brief:", ok, "of", len(ag), "; mismatched:", bad)
