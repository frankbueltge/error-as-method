#!/usr/bin/env python3
"""Session 86, 2026-09-10 -- harvest the corpus.

Session 84 measured the agentless normative construction over 63 EU legal acts and asked, in its
own open thread, whether it had measured DRAFTING or measured ENGLISH.  Session 85 deferred the
answer by one night.  This is the port: a published system of norms that is not EU law, not
written by this practice, and not this practice's own record.

THE SELECTION RULE, fixed in PREDICTIONS.md before any text was read:

  Three windows, seeded at RFC 8175, 8800 and 9400.  From each seed, ascending by number, take the
  first 21 RFCs whose whitespace-normalised text contains the phrase "appear in all capitals".
  Numbers that do not resolve (HTTP != 200) are skipped and logged.  63 documents, matching the 63
  acts of the EU corpus deliberately.

WHY THAT PREDICATE AND NOT A KEYWORD SEARCH.  That phrase is the RFC 8174 boilerplate:

    The key words "MUST", ... "OPTIONAL" in this document are to be interpreted as described in
    BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

A document carrying it has DECLARED ITS OWN KEY: in this text, and by its own statement, an
uppercase MUST is a norm and a lowercase must is ordinary English.  The corpus is therefore
selected by the documents' own declaration of which of their words are norms -- not by mine.
Every window starts above 8175 because RFC 8174 is dated May 2017; before it, RFC 2119 said only
that the key words "are often capitalized", and the case distinction was the ambiguity RFC 8174
was written to remove.

BYTES ARE NOT COMMITTED.  sources/MANIFEST.json records number, URL, HTTP status, byte count and
SHA-256 for all 63, which is the warrant a stranger re-checks; corpus.json.gz holds only what the
measurement reads.  See PROTOCOL.md, amendment of 2026-08-18.
"""

import gzip
import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = (8175, 8800, 9400)
PER_WINDOW = 21
SCAN_LIMIT = 120          # numbers tried per window before giving up; declared, not tuned
PREDICATE = "appear in all capitals"
UA = "error-as-method nightly research line (contact: f.bueltge@gmail.com)"

WS = re.compile(r"\s+")
HDR_DATE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(19|20)\d{2}\b")
CATEGORY = re.compile(r"^\s*Category:\s*(.+?)\s*$", re.MULTILINE)
STREAM = re.compile(r"^\s*(Internet Engineering Task Force \(IETF\)|Independent Submission|"
                    r"Internet Architecture Board \(IAB\)|Internet Research Task Force \(IRTF\))",
                    re.MULTILINE)


def fetch(n):
    url = "https://www.rfc-editor.org/rfc/rfc%d.txt" % n
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return url, r.status, r.read()
    except Exception as exc:                       # noqa: BLE001 -- logged, never swallowed
        return url, getattr(exc, "code", 0), None


def head_fields(text):
    """Title, date, category and stream, read off the RFC's own header block."""
    lines = [l.rstrip() for l in text.split("\n")[:60]]
    date = None
    for l in lines:
        m = HDR_DATE.search(l)
        if m:
            date = m.group(0)
            break
    cat = CATEGORY.search(text[:4000])
    st = STREAM.search(text[:2000])
    # the title is the first centred line after the header block that is not a form feed
    title = None
    for i, l in enumerate(lines):
        s = l.strip()
        if not s or s.startswith("\x0c"):
            continue
        if i > 4 and l.startswith("   ") and not re.match(r"^\s*\S+:", s) and len(s) > 8:
            if not re.search(r"\b(Request for Comments|Category|ISSN|Obsoletes|Updates|BCP|STD)\b", s):
                title = s
                break
    return title, date, (cat.group(1) if cat else None), (st.group(1) if st else None)


def main():
    corpus, manifest, skipped = {}, [], []
    for seed in SEEDS:
        taken, n = 0, seed
        while taken < PER_WINDOW and n < seed + SCAN_LIMIT:
            url, status, raw = fetch(n)
            time.sleep(0.4)
            if status != 200 or raw is None:
                skipped.append({"rfc": n, "http_status": status, "reason": "not retrieved"})
                n += 1
                continue
            text = raw.decode("utf-8", errors="replace")
            flat = WS.sub(" ", text)
            if PREDICATE not in flat:
                skipped.append({"rfc": n, "http_status": 200, "reason": "no RFC 8174 boilerplate"})
                n += 1
                continue
            title, date, cat, stream = head_fields(text)
            corpus[str(n)] = {"rfc": n, "text": text, "window": seed,
                              "title": title, "date": date, "category": cat, "stream": stream}
            manifest.append({
                "rfc": n,
                "url": url,
                "http_status": 200,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "title": title, "date": date, "category": cat, "stream": stream,
                "window": seed,
            })
            taken += 1
            n += 1
            print("  rfc%d  %s  %s" % (n - 1, date, (title or "")[:58]))
        if taken < PER_WINDOW:
            print("WINDOW %d SHORT: %d of %d" % (seed, taken, PER_WINDOW), file=sys.stderr)
            sys.exit(1)

    with gzip.open(HERE / "corpus.json.gz", "wt") as fh:
        json.dump(corpus, fh)
    (HERE / "harvest-log.json").write_text(json.dumps(
        {"fetched": "2026-09-10", "predicate": PREDICATE, "seeds": SEEDS,
         "per_window": PER_WINDOW, "scan_limit": SCAN_LIMIT,
         "taken": len(corpus), "skipped": skipped}, indent=1) + "\n")
    print("\n%d documents, %d numbers skipped (all logged in harvest-log.json)."
          % (len(corpus), len(skipped)))
    return manifest


if __name__ == "__main__":
    m = main()
    (HERE / "manifest-rows.json").write_text(json.dumps(m, indent=1) + "\n")
