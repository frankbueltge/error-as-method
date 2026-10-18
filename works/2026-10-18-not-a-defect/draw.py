#!/usr/bin/env python3
"""Draw tonight's entries from the C++ Core Language Issues list. Stdlib, no network.

    python3 -I draw.py <cwg_closed.html> <cwg_defects.html> <outdir>

Writes <outdir>/entries.json (the drawn entries' text, NOT committed: the list carries its
submitters' and the committee's own words under no redistribution licence) and, beside this
script, order.json (issue numbers and status only). The pool, the order and the quotas are
fixed in PREDICTIONS.md: NAD issues from the closed list, every issue from the defects list;
stripped text 200 to 3,000 characters; a NAD issue must carry a recorded reason (a paragraph
headed Rationale or Notes); sorted by number, then random.Random(134).shuffle; the first 25
NAD and the first 15 accepted in that order are taken.
"""
import html, json, os, random, re, sys
H = os.path.dirname(os.path.abspath(__file__))
SPLIT = re.compile(r'<A NAME="(\d+)"></A>\s*<H4>(.*?)</H4>(.*?)(?=<BR><BR><HR>|<A NAME="\d+"></A>\s*<H4>|</BODY>)', re.S)

def strip(s):
    s = re.sub(r'<(BR|P|/P|LI|/LI|PRE|/PRE|BLOCKQUOTE|/BLOCKQUOTE|UL|OL)[^>]*>', '\n', s, flags=re.I)
    s = re.sub(r'<INS>(.*?)</INS>', r'[inserted: \1]', s, flags=re.S | re.I)
    s = re.sub(r'<DEL>(.*?)</DEL>', r'[deleted: \1]', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('\xa0', ' ')
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n\n', s)
    return s.strip()

def parse(path, source):
    out = []
    for num, title, body in SPLIT.findall(open(path, encoding='utf-8', errors='replace').read()):
        st = re.search(r'<B>Status: </B>\s*([A-Za-z0-9+]+)', body)
        if not st:
            continue
        sec = re.search(r'<B>Section: </B>(.*?)&#160;&#160;&#160;', body, re.S)
        # the issue text begins after the Date field
        m = re.search(r'<B>Date: </B>[^<]*', body)
        text = strip(body[m.end():] if m else body)
        out.append({"id": int(num), "title": strip(title).split('.', 1)[-1].strip(),
                    "section": strip(sec.group(1)) if sec else "", "status": st.group(1),
                    "source": source, "text": text})
    return out

def pool(closed, defects):
    nad = [e for e in closed if e["status"] == "NAD"]
    acc = list(defects)
    keep = lambda e: 200 <= len(e["text"]) <= 3000
    reason = lambda e: re.search(r'^(Rationale|Notes)\b', e["text"], re.M) is not None
    nad = [e for e in nad if keep(e) and reason(e)]
    acc = [e for e in acc if keep(e)]
    p = sorted(nad + acc, key=lambda e: e["id"])
    random.Random(134).shuffle(p)
    return p, len(nad), len(acc)

if __name__ == "__main__":
    closed = parse(sys.argv[1], "closed")
    defects = parse(sys.argv[2], "defects")
    p, nn, na = pool(closed, defects)
    take, cnt = [], {"NAD": 0, "ACC": 0}
    for e in p:
        k = "NAD" if e["status"] == "NAD" else "ACC"
        if cnt[k] < (25 if k == "NAD" else 15):
            cnt[k] += 1
            take.append(e)
        if cnt["NAD"] == 25 and cnt["ACC"] == 15:
            break
    json.dump(take, open(os.path.join(sys.argv[3], "entries.json"), "w"), indent=1)
    json.dump({"parsed_closed": len(closed), "parsed_defects": len(defects), "pool_nad": nn, "pool_accepted": na,
               "order": [[e["id"], e["status"]] for e in p],
               "taken": [[e["id"], e["status"]] for e in take]}, open(os.path.join(H, "order.json"), "w"))
    print("parsed", len(closed), "closed,", len(defects), "defects; pool", nn, "NAD,", na, "accepted; taken", cnt)
