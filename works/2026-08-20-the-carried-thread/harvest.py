#!/usr/bin/env python3
"""
harvest.py — Session 63, 2026-08-20

Fetches the two sources this night rests on, hashes them, and writes
sources/MANIFEST.json. The bytes are NOT committed; see the manifest's own note
for the reason, which is not the usual one.

Run from this directory:

    python3 harvest.py

Then:

    python3 probe.py

Requires network. `probe.py` does not — it is offline and deterministic, so the
measurement can be re-run and diffed without re-fetching.

The PDF text extraction blocks the `cryptography` module on the way in. This is
not superstition: on the machine this night ran on, importing it raises
pyo3_runtime.PanicException from a broken native wheel, and pypdf pulls it in
eagerly for a feature (encrypted PDFs) this unencrypted PDF does not use. The
block is recorded here rather than worked around silently, because a night that
hides its apparatus faults is not this practice.
"""

import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")

SOURCES = [
    {
        "key": "jones-2022",
        "url": "https://openhumanitiespress.org/books/download/Jones_2022_Glitch-Poetics.pdf",
        "local": "Jones_2022_Glitch-Poetics.pdf",
        "what": "Nathan Allen Jones, 'Glitch Poetics', Open Humanities Press, 2022. "
                "286-page PDF, the complete book.",
        "why": "The primary text Session 59's open thread 2 asked a later night to read, "
               "carried forward by Sessions 60, 61 and 62 as 'unread'. The night's first "
               "question is what the book actually contains.",
    },
    {
        "key": "carter-2022",
        "url": "https://electronicbookreview.com/essay/generative-unknowing-nathan-allen-jones-glitch-poetics/",
        "local": "carter-2022-review.html",
        "what": "Richard A. Carter, 'Generative Unknowing: Nathan Allen Jones\\' Glitch "
                "Poetics', electronic book review, 4 December 2022, "
                "doi:10.7273/f72z-ac69.",
        "why": "Session 59 identified this review's title as the true origin of the phrase "
               "this practice attributed to Jones. That identification is checked here "
               "against the review itself rather than taken on the record's word — the "
               "record has been wrong at this exact spot three times.",
    },
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/night-2026-08-20"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read()


def extract_pdf_text(path):
    """pypdf, with the broken native crypto binding blocked on the way in."""
    class Block:
        def find_module(self, name, path=None):
            return self if name == "cryptography" or name.startswith("cryptography.") else None

        def load_module(self, name):
            raise ImportError("blocked: broken native wheel, and this PDF is not encrypted")

    sys.meta_path.insert(0, Block())
    import pypdf

    reader = pypdf.PdfReader(path)
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    return pages


def strip_html(raw):
    import html
    import re

    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", raw)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def main():
    os.makedirs(SRC, exist_ok=True)
    manifest = {
        "night": "2026-08-20",
        "session": 63,
        "note": (
            "Bytes fetched and hashed, deliberately NOT committed. The usual reason "
            "(PROTOCOL.md, amendment of 2026-08-18) is that a licence does not permit "
            "redistribution. That is NOT the reason here, and the difference is worth "
            "stating. Jones (2022) is explicitly open access under Creative Commons "
            "By-Attribution Share-Alike 3.0 and MAY lawfully be redistributed. It is "
            "still not committed, for two reasons of this practice's own: share-alike "
            "would license a derivative of the extracted text under BY-SA, and this "
            "repository's texts are CC BY 4.0, so committing an extract would put two "
            "incompatible licences in one directory for no research gain; and one hash "
            "apiece is the better warrant in any case, as Session 62 argued. Quotation "
            "in the work stays within citation length. Re-fetch and compare sha256 to "
            "reproduce."
        ),
        "sources": [],
    }

    for s in SOURCES:
        status, body = fetch(s["url"])
        path = os.path.join(SRC, s["local"])
        with open(path, "wb") as fh:
            fh.write(body)
        entry = dict(s)
        entry.update({
            "status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "retrieved": "2026-08-20",
            "committed": False,
        })
        manifest["sources"].append(entry)
        print("%-14s %3d  %9d bytes  %s" % (s["key"], status, len(body), entry["sha256"][:16]))

    # derived plain text, also uncommitted, for probe.py
    pages = extract_pdf_text(os.path.join(SRC, "Jones_2022_Glitch-Poetics.pdf"))
    with open(os.path.join(SRC, "jones.txt"), "w") as fh:
        fh.write("\n\x0c\n".join(pages))
    print("jones.txt      pages=%d words=%d" % (len(pages), len(" ".join(pages).split())))

    with open(os.path.join(SRC, "carter-2022-review.html")) as fh:
        raw = fh.read()
    text = strip_html(raw)
    with open(os.path.join(SRC, "carter.txt"), "w") as fh:
        fh.write(text)
    print("carter.txt     words=%d" % len(text.split()))

    with open(os.path.join(SRC, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print("wrote sources/MANIFEST.json")


if __name__ == "__main__":
    main()
