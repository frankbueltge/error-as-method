"""savereport.py <lineage> <version>: writes reports/<L>-v<k>.md as the maker's own hand-back for that version,
taken from the agent's transcript unchanged, nothing retyped (after Session 139's savereport.py). For a K lineage
the maker is the v1 agent and the k-th hand-back is taken; for P and T the agent of that version, its first."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L, k = sys.argv[1], int(sys.argv[2])
ag = json.load(open(os.path.join(HERE, "agents.json")))
arm = {x["lineage"]: x["arm"] for x in json.load(open(os.path.join(HERE, "plan.json")))["lineages"]}[L]
aid, n = (ag["%s-v1" % L], k) if arm == "K" else (ag["%s-v%d" % (L, k)], 1)
path = "/tmp/claude-0/-home-user/12d6a705-ad2d-53d3-8b3a-28a1dba3b3ff/tasks/%s.output" % aid
hands = []
for line in open(path, encoding="utf-8"):
    try: o = json.loads(line)
    except ValueError: continue
    msg = o.get("message") or {}
    if o.get("type") == "assistant" and isinstance(msg.get("content"), list):
        for c in msg["content"]:
            if c.get("type") == "tool_use" and c.get("name") == "SubagentHandback": hands.append(c["input"]["message"])
assert len(hands) >= n, "only %d hand-backs" % len(hands)
os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
open(os.path.join(HERE, "reports", "%s-v%d.md" % (L, k)), "w", encoding="utf-8").write(hands[n - 1].rstrip() + "\n")
print(L, k, len(hands[n - 1]), "chars")
