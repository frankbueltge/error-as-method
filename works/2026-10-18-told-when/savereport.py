"""savereport.py <maker> <transcript.jsonl>: writes reports/<maker>.md as the maker's own final hand-back, the text of
the last assistant message in the agent's transcript, unchanged. Nothing is retyped."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
m, path = sys.argv[1], sys.argv[2]; last = None
for line in open(path, encoding="utf-8"):
    try: o = json.loads(line)
    except ValueError: continue
    msg = o.get("message") or {}
    if o.get("type") == "assistant" and msg.get("role") == "assistant":
        t = "".join(c.get("text", "") for c in msg.get("content", []) if isinstance(c, dict) and c.get("type") == "text")
        if t.strip(): last = t
assert last, "no assistant text"
open(os.path.join(HERE, "reports", m + ".md"), "w", encoding="utf-8").write(last.rstrip() + "\n")
print(m, len(last), "chars")
