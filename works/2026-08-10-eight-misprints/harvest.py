#!/usr/bin/env python3
"""How citations.json was produced, on 2026-08-10.

This is the network half of the work, kept separate from measure.py so that the
measurement itself stays deterministic and offline. Re-running it will NOT
reproduce citations.json exactly: the citation record grows, and INSPIRE adds raw
reference text to records over time. It reproduces the *procedure*, not the file.

    python3 harvest.py > citations.new.json

Corpus: every INSPIRE-HEP record citing recid 89145 (K. G. Wilson, Phys. Rev. D 10,
2445 (1974)), keeping those that carry `raw_refs` for the reference to that record —
the reference string as it stands in the citing manuscript.

INSPIRE metadata is offered under the CC0 waiver; see
https://help.inspirehep.net/knowledge-base/terms-of-use/ . No restricted field
(e-mail addresses in particular) is requested or stored here.
"""
import json
import sys
import time
import urllib.request

RECID = 89145
SIZE = 250
UA = "error-as-method-research/1.0 (nightly research line; contact via repository)"
BASE = ("https://inspirehep.net/api/literature?q=refersto%20recid%20{recid}"
        "&fields=references,control_number,earliest_date&size={size}&page={page}")


def fetch(page):
    url = BASE.format(recid=RECID, size=SIZE, page=page)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def main():
    rows, seen, page, total = [], set(), 1, None
    while True:
        d = fetch(page)
        total = d["hits"]["total"]
        hits = d["hits"]["hits"]
        if not hits:
            break
        for h in hits:
            m = h["metadata"]
            rid = m["control_number"]
            if rid in seen:
                continue
            seen.add(rid)
            raw = None
            for ref in m.get("references", []):
                if not ref.get("record", {}).get("$ref", "").endswith(f"/{RECID}"):
                    continue
                for rr in ref.get("raw_refs") or []:
                    if rr.get("schema") == "text" and rr.get("value"):
                        raw = rr["value"]
                        break
                if raw:
                    break
            if raw:
                yr = (m.get("earliest_date") or "")[:4]
                rows.append({"recid": rid, "year": int(yr) if yr.isdigit() else None,
                             "raw": raw})
        print(f"page {page}: {len(seen)} records seen, {len(rows)} with a raw reference",
              file=sys.stderr)
        if page * SIZE >= total:
            break
        page += 1
        time.sleep(2)          # be a good guest

    json.dump({"target": {"citation": "K. G. Wilson, Confinement of quarks, "
                                      "Phys. Rev. D 10, 2445 (1974)",
                          "inspire_recid": RECID,
                          "inspire_url": f"https://inspirehep.net/literature/{RECID}",
                          "doi": "10.1103/PhysRevD.10.2445",
                          "true_coordinates": {"volume": 10, "first_page": 2445,
                                               "year": 1974, "issue": 8,
                                               "last_page": 2459}},
               "corpus": {"source": "INSPIRE-HEP REST API, "
                                    "/api/literature?q=refersto recid 89145",
                          "citing_records_reported_by_inspire": total,
                          "citing_records_retrieved": len(seen),
                          "records_carrying_a_raw_reference_string": len(rows)},
               "records": sorted(rows, key=lambda r: r["recid"])},
              sys.stdout, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
