#!/usr/bin/env python3
"""harvest.py -- the fourth corpus: UK Public General Acts and their Explanatory Notes.

Open thread 1 of Session 89 said that `legislation.gov.uk` had been deferred by Sessions 87, 88 and
89, that three deferrals is a habit, and that the next night should either run it or say in writing
why not.  This is the run.

WHY THIS SOURCE AND NOT ANOTHER.  `S86.CONSTANT` has been waiting since Session 87 for a corpus with
**two speaking registers** -- two divisions of the same published system of norms, each of which
uses obligation modals often enough to be measured, and whose normative status is declared by the
documents themselves rather than by me.  The three corpora already measured supply that unevenly:
the EU acts do (recitals and articles), the RFC series does (capitals and lower case), and WHATWG
does not -- its non-normative register speaks in 54 occurrences against 3,549, which is why the row
is still open.

A UK Act and its Explanatory Notes are two such divisions, and the notes say so in their own words:

    "Their purpose is to assist the reader in understanding the Act.  They do not form part of the
     Act and have not been endorsed by Parliament."
    -- Explanatory Notes to the Equality Act 2010, paragraph 1

That sentence is this corpus's RFC 8174: a document division declaring its own normative force.  The
selection rule below requires it, so no document enters this corpus unless it carries its own
declaration.

WHAT THE SOURCE PUBLISHES, AND WHERE IT STOPS.  Every Act is served as CLML XML at
`/ukpga/<year>/<number>/data.xml`.  Its Explanatory Notes are served as CLML XML at
`/ukpga/<year>/<number>/notes/data.xml` -- **for some years and not others.**  Probed 2026-09-15:
the notes XML resolves for Acts of 2005 through 2014 and returns 404 for 2016 onwards, while the
`/notes` HTML page returns 200 for recent Acts and carries no notes in it (17.7 kB of site frame,
6.7 kB of text).  I do not know why and am not going to guess; `harvest-log.json` records every
probe with its status, so the boundary is in the record as an observation about this source on this
date.  It is the reason the corpus is drawn from where it is.

SELECTION RULE, fixed before any text was read.  Walk years **2014 down to 2005**; within each year
walk Act numbers **1 upward to 60**; take an Act if and only if

  (a) `/ukpga/<y>/<n>/data.xml` returns 200 and parses as CLML `<Legislation>` with a `<Primary>`,
  (b) `/ukpga/<y>/<n>/notes/data.xml` returns 200 and parses as CLML `<EN>`, and
  (c) the notes text contains the string "do not form part of the Act" -- the declaration above.

Stop at **63** Acts, which is the size of the EU corpus and of the RFC corpus, so that the fourth
tradition is not also a fourth sample size.  Nothing is chosen by hand and nothing is skipped: the
log holds every number tried.

BLOCKS.  A block is a maximal run of `<Text>` belonging to the same innermost numbered provision --
the UK analogue of a WHATWG paragraph, an RFC paragraph and an EU numbered division.  `bounds.py`
measures how big that unit actually is before any prediction is written, because Session 89's whole
night was the discovery that a threshold fixed without computing the instrument's range is two tests
wearing one name (F-137).

`<BlockAmendment>` IS EXCLUDED, and the exclusion is declared here rather than discovered later.
A UK Act amending another Act quotes the words it inserts; those words are the amended Act speaking,
not this one, and an amending instrument's own voice is "in section 3, for X substitute Y".  The
same text would otherwise be counted twice across a corpus that contains both Acts.  Both counts are
published -- `bounds.json` carries the corpus with and without it -- so substituting the other
decision costs a reader nothing.

Writes corpus.json.gz, harvest-log.json, sources/MANIFEST.json.  Rerunnable: every fetch is
recorded with its SHA-256, so a stranger can re-fetch and compare.
"""

import gzip
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
NS = "{http://www.legislation.gov.uk/namespaces/legislation}"
PROV = re.compile(r"^P[1-7]$")
DECLARATION = "do not form part of the Act"
YEARS = list(range(2014, 2004, -1))
MAX_NUMBER = 60
TARGET = 63
UA = "error-as-method research night (one-off corpus harvest; contact f.bueltge@gmail.com)"
PAUSE = 0.7          # the source publishes a fair-use policy; this is one pass, paced


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/xml"})
    try:
        with urllib.request.urlopen(req, timeout=90) as fh:
            body = fh.read()
            return fh.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:                                    # noqa: BLE001 -- recorded, not raised
        return None, str(e).encode()


def strip_ns(t):
    return t.split("}", 1)[1] if "}" in t else t


def blocks_of(root, drop_block_amendment):
    """Ordered blocks: maximal runs of <Text> under the same innermost numbered provision."""
    out, buf, key_now = [], [], object()

    def walk(el, ancestors):
        nonlocal buf, key_now
        tag = strip_ns(el.tag)
        if drop_block_amendment and tag == "BlockAmendment":
            return
        if tag == "Text":
            key = None
            for a in reversed(ancestors):
                if PROV.match(strip_ns(a.tag)):
                    key = id(a)
                    break
            if key is None:
                key = id(ancestors[-1]) if ancestors else 0
            if key != key_now:
                if buf:
                    out.append(" ".join(buf))
                buf, key_now = [], key
            buf.append("".join(el.itertext()))
            return
        for c in el:
            walk(c, ancestors + [el])

    walk(root, [])
    if buf:
        out.append(" ".join(buf))
    return [b for b in (re.sub(r"\s+", " ", t).strip() for t in out) if b]


def act_blocks(xml_bytes, drop_block_amendment=True):
    root = ET.fromstring(xml_bytes)
    prim = root.find(".//" + NS + "Primary")
    if prim is None:
        return None, None
    # the title lives in <ukm:Metadata><dc:title>, and ukm: is the metadata namespace, not NS --
    # the first draft looked for NS + "Metadata", found nothing, and wrote 63 empty titles
    title = ""
    for el in root.iter():
        if strip_ns(el.tag) == "title" and el.text:
            title = el.text.strip()
            break
    return blocks_of(prim, drop_block_amendment), title


def notes_blocks(xml_bytes):
    root = ET.fromstring(xml_bytes)
    if strip_ns(root.tag) != "EN":
        return None
    return blocks_of(root, False)


def main():
    log, corpus, manifest = [], {}, []
    kept = 0
    for year in YEARS:
        if kept >= TARGET:
            break
        for number in range(1, MAX_NUMBER + 1):
            if kept >= TARGET:
                break
            nurl = "https://www.legislation.gov.uk/ukpga/%d/%d/notes/data.xml" % (year, number)
            ncode, nbody = fetch(nurl)
            time.sleep(PAUSE)
            row = {"year": year, "number": number, "notes_url": nurl, "notes_status": ncode,
                   "notes_bytes": len(nbody) if nbody else 0}
            if ncode != 200:
                row["verdict"] = "no notes XML"
                log.append(row)
                continue
            try:
                nb = notes_blocks(nbody)
            except ET.ParseError as e:
                row["verdict"] = "notes XML did not parse: %s" % e
                log.append(row)
                continue
            if nb is None:
                row["verdict"] = "notes XML is not an <EN> document"
                log.append(row)
                continue
            if DECLARATION not in " ".join(nb):
                row["verdict"] = "notes carry no self-declaration"
                row["notes_blocks"] = len(nb)
                log.append(row)
                continue

            aurl = "https://www.legislation.gov.uk/ukpga/%d/%d/data.xml" % (year, number)
            acode, abody = fetch(aurl)
            time.sleep(PAUSE)
            row.update({"act_url": aurl, "act_status": acode,
                        "act_bytes": len(abody) if abody else 0})
            if acode != 200:
                row["verdict"] = "notes present, Act XML did not resolve"
                log.append(row)
                continue
            try:
                ab, title = act_blocks(abody)
                ab_with, _ = act_blocks(abody, drop_block_amendment=False)
            except ET.ParseError as e:
                row["verdict"] = "Act XML did not parse: %s" % e
                log.append(row)
                continue
            if ab is None:
                row["verdict"] = "Act XML has no <Primary>"
                log.append(row)
                continue

            key = "%d/%d" % (year, number)
            corpus[key] = {"year": year, "number": number, "title": title,
                           "act": ab, "act_with_block_amendment": ab_with, "notes": nb}
            for url, body, what in ((aurl, abody, "the Act as CLML XML -- the binding register"),
                                    (nurl, nbody, "its Explanatory Notes as CLML XML -- the "
                                                  "register that declares itself not part of "
                                                  "the Act")):
                manifest.append({
                    "url": url, "http_status": 200, "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "what": what, "act": key, "title": title,
                    "licence": "Open Government Licence v3.0, as stated at "
                               "https://www.legislation.gov.uk/help",
                })
            kept += 1
            row.update({"verdict": "kept", "rank": kept, "title": title,
                        "act_blocks": len(ab), "notes_blocks": len(nb)})
            log.append(row)
            print("  %2d/63  %s  %-58s  act %5d blk  notes %4d blk"
                  % (kept, key, (title or "")[:58], len(ab), len(nb)), flush=True)

    with gzip.open(HERE / "corpus.json.gz", "wt") as fh:
        json.dump(corpus, fh)
    (HERE / "harvest-log.json").write_text(json.dumps({
        "note": "every URL this harvest tried, in the order it tried them, with the status the "
                "source returned. The 404s are the availability boundary described in harvest.py's "
                "docstring: the notes XML resolves for Acts of 2005-2014 and not for later years.",
        "selection_rule": {"years": YEARS, "numbers": [1, MAX_NUMBER], "target": TARGET,
                           "declaration_required": DECLARATION},
        "probes": len(log), "kept": kept, "rows": log}, indent=1) + "\n")
    (HERE / "sources" / "MANIFEST.json").write_text(json.dumps({
        "note": "Content under the Open Government Licence v3.0, which permits redistribution; the "
                "bytes are nevertheless not committed, because 63 Acts and their notes are ~150 MB "
                "and the derived corpus.json.gz is the re-runnable object. Re-fetch and compare the "
                "hash.",
        "attribution": "Contains public sector information licensed under the Open Government "
                       "Licence v3.0. © Crown copyright and database right.",
        "documents": len(manifest), "rows": manifest}, indent=1) + "\n")
    print("\nkept %d Acts; %d probes logged; %d source rows in the manifest."
          % (kept, len(log), len(manifest)))


if __name__ == "__main__":
    main()
