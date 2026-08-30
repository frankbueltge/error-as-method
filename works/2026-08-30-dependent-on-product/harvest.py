#!/usr/bin/env python3
"""harvest.py — Session 75, 2026-08-30.

Fetches what tonight reads from the CFPB's public Consumer Complaint Database and from the five
documents in which the institution states its own norms: the five-step complaint process with its
fifteen and sixty days, the API's own account of what gets published and what never does, the field
reference whose sentence about the Issue field is the spine of the night, and the two 2026 notices in
which the institution announces changes to what it will treat as worth answering and what it will
publish.

It fetches; it does not measure. Every number in this work comes out of `measure.py`, which is
offline and reads only what this script wrote.

The three rules are inherited and are not incidental:

  1. **No third-party bytes are committed by default.** Everything fetched is written to a raw cache
     OUTSIDE the repository (`--raw`, default `../../../.raw`), one level above the clone, so that no
     `git add -A` can sweep it in. The database itself is declared CC0 by its own API (`_meta.license`,
     recorded below), so committing derived aggregates from it is lawful; the narratives are *not*
     committed all the same, and the reason is in `work.md`.
  2. **Every fetch is recorded** in `sources/MANIFEST.json` with URL, HTTP status, byte count and
     SHA-256, so a stranger re-fetches and compares.
  3. **Nothing is retried into silence.** A URL that never returns 200 is recorded with the status it
     did return, and the run says so.

Usage:
    python3 harvest.py --raw ../../../.raw              # everything, in order
    python3 harvest.py --raw ../../../.raw --only docs
"""

import argparse
import datetime
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "error-as-method/night-2026-08-30 (research; contact f.bueltge@gmail.com)"
API = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

# Fixed in PREDICTIONS.md before this file existed.
WINDOW_MIN = "2023-01-01"
WINDOW_MAX = "2024-06-30"
SEED = 20260830
SAMPLE_N = 1000
POLITE_DELAY = 0.35  # seconds between requests; raised after the endpoint throttled the first run

DOCS = [
    (
        "complaint-process.html",
        "https://www.consumerfinance.gov/complaint/process/",
        "The institution's own five-step account of what happens to a reported difference. Step 2 is "
        "called Route. Step 3 publishes the two deadlines this night measures against — fifteen days "
        "generally, sixty for a final response — so no threshold of lateness has to be taken out of "
        "the distribution.",
    ),
    (
        "ccdb-what-is-this-data.html",
        "https://cfpb.github.io/api/ccdb/",
        "The publication rule and the boundary of the record: complaints are published after the "
        "company responds or after fifteen days, whichever comes first; complaints referred to other "
        "regulators are never published at all.",
    ),
    (
        "ccdb-fields.html",
        "https://cfpb.github.io/api/ccdb/fields.html",
        "The field reference. Of Issue: 'Possible values are dependent on Product.' Of Sub-issue: "
        "'Possible values are dependent on product and issue.' This is the sentence P4 tests.",
    ),
    (
        "cfpb-correcting-flaws-2026-06-24.html",
        "https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-is-correcting-flaws-to-restore-integrity-and-utility-to-the-consumer-complaint-system/",
        "2026-06-24. The institution announcing that it is 'Focusing resources on complaints that "
        "warrant a substantive response' — a routing rule being rewritten in public, two months "
        "before this night.",
    ),
    (
        "cfpb-cease-narratives-2026-08-14.html",
        "https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-to-cease-discretionary-publication-of-complaint-narratives-and-visualizations/",
        "2026-08-14, sixteen days before this night. The institution ceasing publication of the "
        "consumers' own descriptions of their differences, on the stated ground that they are "
        "unverified.",
    ),
]

MANIFEST = []
GROUPS = {}
THROTTLE = {"events": 0, "seconds_waited": 0}


def fetch(url, name, what, raw_dir, is_json=False, group=None):
    """One GET. Records status, bytes and SHA-256 whatever happens. Never retries into silence.

    `group` collapses the repetitive API queries in the committed manifest: each is still hashed
    individually, but they are published as one row carrying the count, the statuses seen, the total
    bytes and a digest over the individual hashes in issue order. Nine hundred rows of the same
    query shape would bury the five documents that matter.
    """
    # Cache-first. The first run of this night was throttled off the endpoint partway through the
    # seeded sample and died; re-running it must not re-issue two thousand requests the far end
    # has already answered. A cached response is used as it stands and recorded as `from_cache`.
    cached = os.path.join(raw_dir, name)
    if os.path.exists(cached) and os.path.getsize(cached) > 0:
        body = open(cached, "rb").read()
        entry = {
            "name": name, "url": url, "what": what, "http_status": 200, "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(), "from_cache": True, "committed": False,
        }
        if group is None:
            MANIFEST.append(entry)
        else:
            g = GROUPS.setdefault(group, {"group": group, "n": 0, "statuses": {}, "bytes": 0,
                                          "hashes": [], "from_cache": 0,
                                          "first_url": url, "last_url": url})
            g["n"] += 1
            g["statuses"]["200"] = g["statuses"].get("200", 0) + 1
            g["from_cache"] = g.get("from_cache", 0) + 1
            g["bytes"] += len(body)
            g["hashes"].append(entry["sha256"])
            g["last_url"] = url
        if is_json:
            return json.loads(body.decode("utf-8"))
        return body

    status, body, err = None, b"", None
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        status, body, err = None, b"", None
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                status = r.status
                body = r.read()
        except urllib.error.HTTPError as e:
            status = e.code
            body = e.read() or b""
            err = f"HTTPError {e.code}"
        except Exception as e:  # noqa: BLE001 - the point is to record it, not to classify it
            err = f"{type(e).__name__}: {e}"
        # The far end refusing is data, not an exception to route around. It says how long to
        # wait; wait that long, count the wait, and say so in the manifest.
        if status == 429 or (body and b"throttled" in body.lower()):
            m = re.search(rb"available in (\d+) second", body or b"")
            wait = int(m.group(1)) + 3 if m else 30 * (attempt + 1)
            THROTTLE["events"] += 1
            THROTTLE["seconds_waited"] += wait
            print(f"   throttled by the endpoint; waiting {wait}s "
                  f"(event {THROTTLE['events']})", flush=True)
            time.sleep(wait)
            continue
        break

    entry = {
        "name": name,
        "url": url,
        "what": what,
        "http_status": status,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest() if body else None,
        "fetched_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "committed": False,
    }
    if err:
        entry["error"] = err
    if group is None:
        MANIFEST.append(entry)
    else:
        g = GROUPS.setdefault(group, {"group": group, "n": 0, "statuses": {}, "bytes": 0,
                                      "hashes": [], "first_url": url, "last_url": url})
        g["n"] += 1
        g["statuses"][str(status)] = g["statuses"].get(str(status), 0) + 1
        g["bytes"] += len(body)
        g["hashes"].append(entry["sha256"] or "")
        g["last_url"] = url

    if body:
        os.makedirs(raw_dir, exist_ok=True)
        with open(os.path.join(raw_dir, name), "wb") as fh:
            fh.write(body)
    time.sleep(POLITE_DELAY)
    if is_json and status == 200:
        return json.loads(body.decode("utf-8"))
    return body


def api_url(**params):
    q = {"date_received_min": WINDOW_MIN, "date_received_max": WINDOW_MAX}
    q.update({k: v for k, v in params.items() if v is not None})
    return API + "?" + urllib.parse.urlencode(q)


def q_count(raw_dir, tag, group, **params):
    """A count-only query. Cheap on the far end: no aggregations computed."""
    url = api_url(no_aggs="true", size=0, **params)
    d = fetch(url, f"count-{tag}.json", f"count query: {params}", raw_dir, is_json=True, group=group)
    if not isinstance(d, dict):
        return None
    return d["hits"]["total"]["value"]


def q_aggs(raw_dir, tag, group=None, **params):
    url = api_url(size=0, **params)
    d = fetch(url, f"aggs-{tag}.json", f"faceted query: {params}", raw_dir, is_json=True, group=group)
    return d if isinstance(d, dict) else None


def buckets(agg, field):
    try:
        return agg["aggregations"][field][field]["buckets"]
    except (KeyError, TypeError):
        return []


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s).strip("-").lower()[:60]


# --------------------------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../../.raw")
    ap.add_argument("--only", default="all")
    args = ap.parse_args()
    raw = os.path.abspath(os.path.join(os.path.dirname(__file__), args.raw, "2026-08-30"))
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(raw, exist_ok=True)

    out = {"window": {"date_received_min": WINDOW_MIN, "date_received_max": WINDOW_MAX}}

    if args.only in ("all", "docs"):
        print("-- the five documents")
        for name, url, what in DOCS:
            fetch(url, name, what, raw)
            print(f"   {name}")

    if args.only in ("all", "population"):
        print("-- population: one unfiltered faceted query")
        top = q_aggs(raw, "window-all")
        if top is None:
            sys.exit("the population query did not return; nothing measured, nothing invented")
        out["meta"] = top.get("_meta", {})
        out["total"] = top["hits"]["total"]["value"]
        out["facets_unfiltered"] = {
            f: [(b["key"], b["doc_count"]) for b in buckets(top, f)]
            for f in ("product", "company_response", "timely", "submitted_via", "has_narrative",
                      "issue", "company_public_response", "tags")
        }
        products = [k for k, _ in out["facets_unfiltered"]["product"]]
        print(f"   total {out['total']:,} across {len(products)} product branches")

        print("-- per branch: one faceted query, plus five slices for vocabulary discovery")
        out["by_product"] = {}
        vocab = set(k for k, _ in out["facets_unfiltered"]["issue"])
        for p in products:
            rec = {}
            a = q_aggs(raw, f"p-{slug(p)}", product=p)
            rec["total_from_aggs_query"] = a["hits"]["total"]["value"]
            rec["company_response"] = [(b["key"], b["doc_count"]) for b in buckets(a, "company_response")]
            rec["timely"] = [(b["key"], b["doc_count"]) for b in buckets(a, "timely")]
            rec["submitted_via"] = [(b["key"], b["doc_count"]) for b in buckets(a, "submitted_via")]
            rec["has_narrative"] = [(b["key"], b["doc_count"]) for b in buckets(a, "has_narrative")]
            rec["issue_facet"] = [(b["key"], b["doc_count"]) for b in buckets(a, "issue")]
            vocab.update(k for k, _ in rec["issue_facet"])
            # P5a: the same number by a separate route.
            rec["total_from_count_query"] = q_count(raw, f"c-{slug(p)}", "P5a: eleven count-only totals, one per product branch, issued separately from the faceted query they are checked against", product=p)
            # Vocabulary discovery: five further slices, each surfacing up to ten more issues.
            rec["slices"] = {}
            for label, extra in (
                ("resp-explanation", {"company_response": "Closed with explanation"}),
                ("resp-nonmonetary", {"company_response": "Closed with non-monetary relief"}),
                ("resp-monetary", {"company_response": "Closed with monetary relief"}),
                ("resp-untimely", {"company_response": "Untimely response"}),
                ("timely-no", {"timely": "No"}),
            ):
                s = q_aggs(raw, f"s-{slug(p)}-{label}", "vocabulary discovery: five faceted slices per branch, each surfacing up to ten further issue strings", product=p, **extra)
                if s is None:
                    continue
                got = [(b["key"], b["doc_count"]) for b in buckets(s, "issue")]
                rec["slices"][label] = {"total": s["hits"]["total"]["value"], "issue_facet": got}
                vocab.update(k for k, _ in got)
            out["by_product"][p] = rec
            print(f"   {p[:44]:44s} {rec['total_from_aggs_query']:>9,}")

        out["issue_vocabulary_union"] = sorted(vocab)
        print(f"-- issue vocabulary union: {len(vocab)} strings")

        print("-- incidence matrix: every (branch, issue) pair, zeros included")
        matrix = {}
        for p in products:
            row = {}
            known = dict(out["by_product"][p]["issue_facet"])
            for i in out["issue_vocabulary_union"]:
                if i in known:
                    row[i] = known[i]
                else:
                    row[i] = q_count(raw, f"m-{slug(p)}-{slug(i)}", "P4: the (branch x issue) incidence matrix, one count-only query per pair the facets did not already give, zeros included", product=p, issue=i)
            matrix[p] = row
            print(f"   {p[:44]:44s} {sum(1 for v in row.values() if v):>3} of {len(row)} non-zero")
        out["incidence"] = matrix

    if args.only in ("all", "sample"):
        print(f"-- seeded sample: {SAMPLE_N} ids, seed {SEED}, per-complaint endpoint")
        # The id range the window spans, learned from its two edges rather than assumed.
        edges = {}
        for tag, sort in (("lo", "created_date_asc"), ("hi", "created_date_desc")):
            d = fetch(api_url(size=200, no_aggs="true", sort=sort), f"edge-{tag}.json",
                      f"window edge by {sort}, to learn the id range the sample draws from",
                      raw, is_json=True)
            ids = [int(h["_source"]["complaint_id"]) for h in d["hits"]["hits"]]
            edges[tag] = (min(ids), max(ids))
        lo, hi = min(edges["lo"][0], edges["hi"][0]), max(edges["lo"][1], edges["hi"][1])
        out["id_range"] = {"lo": lo, "hi": hi, "edges": edges}
        print(f"   id range {lo:,} .. {hi:,}")

        rng = random.Random(SEED)
        draws = [rng.randint(lo, hi) for _ in range(SAMPLE_N)]
        out["sample"] = {"seed": SEED, "n": SAMPLE_N, "lo": lo, "hi": hi, "records": [], "misses": []}
        grp = ("P5b and the id-density measurement: one thousand seeded random complaint ids fetched "
               "one at a time through the per-complaint endpoint, a different route through the API "
               "than the search that produced the population")
        for n, cid in enumerate(draws, 1):
            body = fetch(API + str(cid), f"id-{cid}.json", "seeded id draw", raw, group=grp)
            try:
                d = json.loads(body.decode("utf-8"))
                hits = d["hits"]["hits"]
            except Exception as e:  # noqa: BLE001
                # A body that is not a search result is not a miss and not a record: it is the
                # endpoint saying something else. Recorded as its own kind.
                out["sample"].setdefault("refusals", []).append(
                    {"id": cid, "error": f"{type(e).__name__}",
                     "body": body[:200].decode("utf-8", "replace")})
                continue
            if not hits:
                out["sample"]["misses"].append({"id": cid, "error": "no record"})
            else:
                s = hits[0]["_source"]
                out["sample"]["records"].append({
                    "complaint_id": s.get("complaint_id"),
                    "date_received": s.get("date_received"),
                    "date_sent_to_company": s.get("date_sent_to_company"),
                    "product": s.get("product"),
                    "issue": s.get("issue"),
                    "company_response": s.get("company_response"),
                    "timely": s.get("timely"),
                    "submitted_via": s.get("submitted_via"),
                    "has_narrative": s.get("has_narrative"),
                    # The text itself is never carried out of this script. Only its length.
                    "narrative_chars": len(s.get("complaint_what_happened") or ""),
                })
            if n % 100 == 0:
                print(f"   {n}/{SAMPLE_N}  hits {len(out['sample']['records'])}  "
                      f"misses {len(out['sample']['misses'])}")

    # One number the manifest carries because it is the licence this night relies on.
    with open(os.path.join(here, "harvest.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    manifest = {
        "night": "2026-08-30",
        "session": 75,
        "rule": "Third-party bytes are not committed here. The database declares itself CC0 in its "
                "own API metadata, so the derived aggregates in results.json are lawful to publish; "
                "the consumers' narratives are not committed all the same, and no narrative text "
                "leaves harvest.py — only its length in characters.",
        "raw_cache": "outside the repository (--raw), never inside it",
        "throttling": {
            "note": "The endpoint refused this harvest partway through the seeded sample with "
                    "'Request was throttled'. The first version of this script parsed that refusal "
                    "as a record and died (F-090). It now waits the interval the endpoint names, "
                    "counts the waits, and reports them here.",
            "events": THROTTLE["events"],
            "seconds_waited": THROTTLE["seconds_waited"],
        },
        "sources": MANIFEST,
        "query_groups": [
            {
                "group": g["group"],
                "requests": g["n"],
                "http_statuses": g["statuses"],
                "bytes_total": g["bytes"],
                "digest_over_response_hashes": hashlib.sha256(
                    "".join(g["hashes"]).encode()).hexdigest(),
                "first_url": g["first_url"],
                "last_url": g["last_url"],
            }
            for g in GROUPS.values()
        ],
    }
    os.makedirs(os.path.join(here, "sources"), exist_ok=True)
    with open(os.path.join(here, "sources", "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)

    bad = [m for m in MANIFEST if m["http_status"] != 200]
    for g in GROUPS.values():
        for st, n in g["statuses"].items():
            if st != "200":
                print(f"   group {g['group'][:50]!r}: {n} responses with status {st}")
    print(f"\n{len(MANIFEST)} fetches recorded, {len(bad)} not 200.")
    for m in bad[:20]:
        print(f"   {m['http_status']}  {m['url'][:110]}")


if __name__ == "__main__":
    main()
