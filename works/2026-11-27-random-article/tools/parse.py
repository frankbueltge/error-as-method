"""Read a curator's version file: tags per letter, rating, replaced letters.
Tags: the first `typical` / `unusual` after each caption's letter label. Ratings: the first digit 1-5 after
'represent'. Replacements are read by hand into replacements.json (free text), not here."""
import re, sys, json

LAB = re.compile(r"^[\s>*#|_-]*\(?\**\s*([a-l])\s*[\.\):]", re.M)

def tags(text):
    m = re.search(r"caption", text, re.I)
    body = text[m.start():] if m else text
    end = re.search(r"\n#+\s*(showing|order|judg)", body, re.I)
    if end: body = body[:end.start()]
    out = {}
    for m in re.finditer(r"^\|\s*\**([a-l])\**\s*\|.*?\b(typical|unusual)\b", body, re.M | re.I):
        out.setdefault(m.group(1), m.group(2).lower())
    if len(out) == 12:
        return out
    hits = list(LAB.finditer(body))
    for i, h in enumerate(hits):
        seg = body[h.start(): hits[i + 1].start() if i + 1 < len(hits) else len(body)]
        t = re.search(r"`?\b(typical|unusual)\b`?", seg, re.I)
        if t and h.group(1) not in out:
            out[h.group(1)] = t.group(1).lower()
    return out

def rating(text):
    m = re.search(r"represent\w*[^\n]*?\b([1-5])\b", text, re.I) or re.search(r"\b([1-5])\s*(/|of|out of)\s*5", text)
    return int(m.group(1)) if m else None

if __name__ == "__main__":
    t = open(sys.argv[1]).read()
    print(json.dumps({"tags": tags(t), "rating": rating(t)}))
