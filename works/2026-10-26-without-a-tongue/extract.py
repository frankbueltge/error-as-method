"""Session 159: copy each maker's hand-back verbatim into rooms/<id>.txt from the session's agent transcripts, and
check that the prompt each maker received is, character for character, its brief in briefs/<id>.txt.
The transcripts are not committed (they are the harness's files, with its own reminders inside); this script and
its printed check are the record. Run: python3 extract.py <transcript dir>   (existing rooms are compared, not overwritten)
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
AGENTS = {"A1": "a5a37bb7a5528a87b", "A2": "a6ceceb045865054f", "A3": "ab54506bfe3756893", "A4": "a4d654e7c4362ab47",
          "A5": "a3a6ec2239f5ce725", "A6": "a9664d0b2eb57aa14", "A7": "aeb16428524cd0117", "A8": "a3293049673c47310",
          "A9": "a9502479822ae76e5", "A10": "a8865de3cfe4ca59f", "A11": "ae6989c40080eb5a7", "A12": "a2600bfa7b864e111",
          "P1": "a1ac344a59d0a478f", "P2": "a02eccf5c48235c17", "P3": "a5010883ce1a192e9", "P4": "afb2f75952b5cb305",
          "P5": "a48b5b73e310de274", "P6": "a544657d847c2dfcf", "O1": "a4bf496ddbf7d0b55", "O2": "a366586723fd62391",
          "O3": "a6331dc7b90e5add1", "O4": "a19fa853a2d8ee80e", "O5": "ae94bc1360f771b6e", "O6": "aae6a3f1ee2582f09"}
src = Path(sys.argv[1])
for mid, aid in AGENTS.items():
    f = src / f"{aid}.output"
    if not f.exists():
        print(mid, "no transcript yet"); continue
    L = [json.loads(l) for l in open(f)]
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
