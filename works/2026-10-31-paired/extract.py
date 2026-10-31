"""Session 165 (experiment 45, Paired; experiment 44's extract.py, unchanged but for this header): copy each maker's hand-back verbatim into rooms/<id>.txt from the session's agent transcripts, and
check that the prompt each maker received is, character for character, its brief in briefs/<id>.txt.
The transcripts are not committed (they are the harness's files); this script and its printed check are the record.
Run: python3 extract.py <transcript dir>   (existing rooms are compared, not overwritten)
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
AGENTS = {l.split()[0]: l.split()[1] for l in open(HERE / "agents.txt") if l.strip()}
src = Path(sys.argv[1])
for mid, aid in AGENTS.items():
    f = src / f"{aid}.output"
    if not f.exists():
        print(mid, "no transcript yet"); continue
    L = [json.loads(l) for l in open(f) if l.strip()]
    prompt = L[0]["message"]["content"]
    prompt = prompt if isinstance(prompt, str) else "".join(c.get("text", "") for c in prompt)
    brief_ok = prompt.strip() == (HERE / "briefs" / f"{mid}.txt").read_text().strip()
    tools, reply = [], None
    for x in L:
        c = x.get("message", {}).get("content")
        if x.get("type") == "assistant" and isinstance(c, list):
            for i in c:
                if i.get("type") == "tool_use":
                    tools.append(i["name"] if i["name"] != "Read" else "Read:" + Path(i["input"].get("file_path", "")).name)
                    if i["name"] == "Read" and not i["input"].get("file_path", "").startswith(str(HERE / "sheets")):
                        tools.append("READ OUTSIDE THE SHEETS")
                    if i["name"] == "SubagentHandback":
                        reply = i["input"]["message"]
    if reply is None:
        print(mid, "no hand-back yet"); continue
    room = HERE / "rooms" / f"{mid}.txt"
    text = reply.rstrip("\n") + "\n"
    if room.exists():
        state = "room matches" if room.read_text().strip() == text.strip() else "ROOM DIFFERS"
    else:
        room.write_text(text); state = "room written"
    print(mid, "brief identical" if brief_ok else "BRIEF DIFFERS", "|", state, "| tool uses:", tools)
