"""Session 161: copy each maker's hand-back verbatim into rooms/<id>.txt from the session's agent transcripts, and
check that the prompt each maker received is, character for character, its brief in briefs/<id>.txt.
The transcripts are not committed (they are the harness's files); this script and its printed check are the record.
Run: python3 extract.py <transcript dir>   (existing rooms are compared, not overwritten)
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
AGENTS = {"A1": "a77b34a6e6f92bf4b", "A2": "aa0d588ebaeb4558c", "A3": "abc07cdf2f6265229", "A4": "a2ba9fd1154febbd4",
          "A5": "aa2a7976be3a3ceec", "A6": "a1b4ff32bdacf8257",
          "S1": "a47431646bf4767f8", "S2": "ad447065fd0d8df43", "S3": "a2fd0e30216b9c144", "S4": "a15061fe9f63a5af9",
          "S5": "ae589e4382493f100", "S6": "a59897181ee1ee43c",
          "F1": "a229cbccfe721bca5", "F2": "ad57beae937272eda", "F3": "ae429d05131660c29", "F4": "a738551fe1dbd471c",
          "F5": "aed16a705c4d9aba0", "F6": "af4ec9f54f71e2618"}
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
                    tools.append(i["name"])
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
