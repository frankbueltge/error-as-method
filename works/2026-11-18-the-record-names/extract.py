"""Copy a maker's hand-back verbatim out of its transcript, and list every tool call it made.

usage: python3 -I extract.py <transcript.jsonl> <out.txt> [which]
which = index of the hand-back to take (default -1, the last). The tool log is appended to
makings/TOOLS.txt so anyone can check that a maker opened only the files its brief named.
"""
import json, sys, pathlib

src, out = sys.argv[1], sys.argv[2]
which = int(sys.argv[3]) if len(sys.argv) > 3 else -1
backs, tools = [], []
for line in open(src):
    d = json.loads(line)
    c = d.get("message", {}).get("content")
    if not isinstance(c, list):
        continue
    for b in c:
        if b.get("type") == "tool_use":
            if b["name"] == "SubagentHandback":
                backs.append(b["input"]["message"])
            else:
                tools.append(f'{b["name"]} {json.dumps(b["input"], ensure_ascii=False)[:300]}')
pathlib.Path(out).write_text(backs[which] if backs[which].endswith("\n") else backs[which] + "\n")
log = pathlib.Path(__file__).parent / "makings" / "TOOLS.txt"
with open(log, "a") as f:
    f.write(f"## {pathlib.Path(out).name}\n" + "\n".join(tools) + "\n\n")
print(len(backs), "hand-backs;", len(tools), "tool calls")
