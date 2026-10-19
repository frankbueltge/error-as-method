"""savereport.py <maker> <round>: writes reports/<maker>-r<round>.md as the maker's own hand-back for that round, the
text of its round-th SubagentHandback call in the agent's transcript, unchanged. Nothing is retyped. (After
Session 137's savereport.py; a maker here hands back once per round in one conversation.)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
m, r = sys.argv[1], int(sys.argv[2])
aid = json.load(open(os.path.join(HERE, "agents.json")))[m]
path = "/tmp/claude-0/-home-user/2bbe900e-0c1a-54b6-a2b5-525f8d51859e/tasks/%s.output" % aid
hands = []
for line in open(path, encoding="utf-8"):
    try: o = json.loads(line)
    except ValueError: continue
    msg = o.get("message") or {}
    if o.get("type") == "assistant" and isinstance(msg.get("content"), list):
        for c in msg["content"]:
            if c.get("type") == "tool_use" and c.get("name") == "SubagentHandback": hands.append(c["input"]["message"])
assert len(hands) >= r, "only %d hand-backs" % len(hands)
os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
open(os.path.join(HERE, "reports", "%s-r%d.md" % (m, r)), "w", encoding="utf-8").write(hands[r - 1].rstrip() + "\n")
print(m, r, len(hands[r - 1]), "chars")
