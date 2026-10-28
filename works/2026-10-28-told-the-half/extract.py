"""Session 160: copy each maker's hand-back verbatim into rooms/<id>.txt from the session's agent transcripts, and
check that the prompt each maker received is, character for character, its brief in briefs/<id>.txt.
The transcripts are not committed (they are the harness's files); this script and its printed check are the record.
Run: python3 extract.py <transcript dir>   (existing rooms are compared, not overwritten)
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
AGENTS = {"A1": "aecdac0f986fba673", "A2": "aa6110c26b245041f", "A3": "ae6610470cf112314", "A4": "af1e278c6743e6f33",
          "A5": "a3a2e19eadad671eb", "A6": "a11f765f8c99cd798", "A7": "a17f98c8b8b206d72", "A8": "a30bdd39f9956d6f6",
          "P1": "a5f21969b7cbd8d0f", "P2": "adbac6b567b68196a", "P3": "a5b59485aa2ecf8bb", "P4": "ae28541e80a1f2f94",
          "P5": "a70d32d33626fff70", "P6": "ad0b73233dd4363d7", "T1": "a48634ec28a88e192", "T2": "a828f9a7d8416b24f",
          "T3": "a74fae24b7cf26878", "T4": "a5c561466e939ca82", "T5": "a2fc0c588b1ab5341", "T6": "a27749eaddd7a9b61"}
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
