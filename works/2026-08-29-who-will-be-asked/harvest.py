#!/usr/bin/env python3
"""harvest.py — Session 74, 2026-08-29.

Fetches what tonight reads: the three documents in which Mozilla states the norm under which a
reported difference is triaged, the two machine-readable field definitions that give the legal
vocabulary of `severity` and `type`, the bug in which the `type` field was assigned in bulk to a
record that predates it, the population itself, and the change history of a seeded sample of that
population.

It fetches; it does not measure. Every number in this work comes out of `measure.py`, which is
offline and reads only what this script wrote.

The three rules are Session 71's, 72's and 73's and are not incidental:

  1. **No third-party bytes are committed.** Everything fetched here is written to a raw cache
     OUTSIDE the repository (`--raw`, default `../../../.raw`, one level above the clone). The
     committed record carries metadata, hashes, derived aggregates, and one named population of
     bug ids that a dated falsifier needs. Outside rather than merely gitignored, because the
     landing gate's allowlist does not cover `.gitignore` and a cache that is only ignored is one
     `git add -A` away from being committed by a session that did not read this file.
  2. **Every fetch is recorded** in `sources/MANIFEST.json` with URL, HTTP status, byte count and
     SHA-256, so a stranger re-fetches and compares.
  3. **Nothing is retried into silence.** A URL that never returns 200 is recorded with the status
     it did return, and the run says so.

Usage:
    python3 harvest.py --raw ../../../.raw            # everything
    python3 harvest.py --raw ../../../.raw --only docs
"""

import argparse
import datetime
import hashlib
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "error-as-method/night-2026-08-29 (research; contact f.bueltge@gmail.com)"

# The window and the product set are fixed in PREDICTIONS.md, before this file ran.
WINDOW_FROM = "2024-01-01"
WINDOW_TO = "2025-07-01"
PRODUCTS = [
    "Core",
    "Firefox",
    "Toolkit",
    "DevTools",
    "Firefox for Android",
    "Firefox for iOS",
    "WebExtensions",
]
FIELDS = (
    "id,product,component,type,severity,priority,status,resolution,"
    "creation_time,cf_last_resolved,is_confirmed,assigned_to,keywords"
)
PAGE = 1000
SAMPLE_N = 300
SAMPLE_SEED = 20260829

DOCS = [
    {
        "name": "triage-bugzilla.html",
        "url": "https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html",
        "what": "Mozilla's Bugzilla triage policy: who triages, within what timeframe, and the "
                "institution's own definition of a triaged bug. This is the norm tonight measures "
                "against, and it is the reason tonight may use the word 'late' at all — it names "
                "one week, so no threshold has to be taken out of the distribution.",
    },
    {
        "name": "bug-types.html",
        "url": "https://firefox-source-docs.mozilla.org/bug-mgmt/guides/bug-types.html",
        "what": "The definitions of the three bug types and the sentence that names a different "
                "applier for each branch: 'Engineering triages defects and tasks. Product "
                "management triages enhancements.'",
    },
    {
        "name": "severity.html",
        "url": "https://firefox-source-docs.mozilla.org/bug-mgmt/guides/severity.html",
        "what": "The severity scale in force, for the vocabulary P5(a) tests the window against.",
    },
    {
        "name": "priority.html",
        "url": "https://firefox-source-docs.mozilla.org/bug-mgmt/guides/priority.html",
        "what": "The priority scale, read alongside severity so that the un-normed state is not "
                "confused with an un-prioritised one.",
    },
    {
        "name": "field-bug_severity.json",
        "url": "https://bugzilla.mozilla.org/rest/field/bug/bug_severity",
        "what": "The machine-readable list of legal severity values. It still contains the "
                "pre-2020 vocabulary (blocker, critical, major, normal, minor, trivial, "
                "enhancement) alongside S1-S4, which is why P5(a) is a real check and not a "
                "formality: the old values remain assignable.",
    },
    {
        "name": "field-bug_type.json",
        "url": "https://bugzilla.mozilla.org/rest/field/bug/bug_type",
        "what": "The machine-readable list of legal type values: '--', defect, enhancement, task. "
                "The '--' is the reporter declining to choose a branch at all.",
    },
    {
        "name": "bug-1522348.json",
        "url": "https://bugzilla.mozilla.org/rest/bug/1522348",
        "what": "'Bulk assign open bugs to task, enhancement, defect field' — the migration that "
                "gave a type to bugs filed before the field existed. Fetched to date it, so the "
                "window can be shown to start after it rather than merely asserted to.",
    },
]


def fetch(url, timeout=180):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def record(manifest, name, url, what, status, body, note=None):
    entry = {
        "name": name,
        "url": url,
        "what": what,
        "http_status": status,
        "bytes": len(body) if body is not None else 0,
        "sha256": hashlib.sha256(body).hexdigest() if body else None,
        "fetched_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "committed": False,
    }
    if note:
        entry["note"] = note
    manifest.append(entry)
    return entry


def harvest_docs(raw, manifest):
    for src in DOCS:
        try:
            status, body = fetch(src["url"])
        except urllib.error.HTTPError as err:
            record(manifest, src["name"], src["url"], src["what"], err.code, b"",
                   note="never returned 200; recorded as it answered")
            print(f"  !! {err.code} {src['url']}")
            continue
        with open(os.path.join(raw, src["name"]), "wb") as fh:
            fh.write(body)
        record(manifest, src["name"], src["url"], src["what"], status, body)
        print(f"  {status} {len(body):>9,} B  {src['name']}")


def population_query(product, offset):
    params = [
        ("f1", "creation_ts"), ("o1", "greaterthaneq"), ("v1", WINDOW_FROM),
        ("f2", "creation_ts"), ("o2", "lessthan"), ("v2", WINDOW_TO),
        ("product", product),
        ("include_fields", FIELDS),
        ("limit", str(PAGE)),
        ("offset", str(offset)),
        ("order", "bug_id"),
    ]
    return "https://bugzilla.mozilla.org/rest/bug?" + urllib.parse.urlencode(params, doseq=True)


def harvest_population(raw, manifest):
    """Page through the window product by product. Ids are the join key; order is bug_id so a
    re-run pages the same way."""
    bugs, pages, total_bytes = [], 0, 0
    for product in PRODUCTS:
        offset, got = 0, PAGE
        while got == PAGE:
            url = population_query(product, offset)
            status, body = fetch(url)
            page = json.loads(body)["bugs"]
            got = len(page)
            bugs.extend(page)
            pages += 1
            total_bytes += len(body)
            offset += PAGE
            time.sleep(0.2)
        print(f"  {product:22s} {sum(1 for b in bugs if b['product'] == product):>6,}")
    seen, unique = set(), []
    for bug in bugs:
        if bug["id"] not in seen:
            seen.add(bug["id"])
            unique.append(bug)
    path = os.path.join(raw, "population.json")
    blob = json.dumps(unique).encode()
    with open(path, "wb") as fh:
        fh.write(blob)
    record(manifest, "population.json",
           "https://bugzilla.mozilla.org/rest/bug?<window and product filters; see harvest.py>",
           f"The population W: every publicly visible bug created in [{WINDOW_FROM}, {WINDOW_TO}) "
           f"in the seven products named in PREDICTIONS.md, {len(unique)} rows over {pages} "
           f"paginated requests. Cached outside the repository; only aggregates and one named "
           f"falsifier population are committed.",
           200, blob, note=f"{pages} requests, {total_bytes} bytes over the wire, "
                           f"{len(bugs) - len(unique)} duplicate rows dropped")
    print(f"  population: {len(unique):,} unique bugs, {pages} requests")
    return unique


def harvest_history(raw, manifest, population):
    """P3 and P4 need to know whether a field's value is the one the filer set. Bugzilla's history
    endpoint answers that per bug, so this is a sample, drawn with the seed fixed in PREDICTIONS.md
    before any history was fetched."""
    ids = sorted(b["id"] for b in population)
    rng = random.Random(SAMPLE_SEED)
    sample = sorted(rng.sample(ids, SAMPLE_N))
    out, failures, total_bytes = {}, [], 0
    for n, bug_id in enumerate(sample, 1):
        url = f"https://bugzilla.mozilla.org/rest/bug/{bug_id}/history"
        try:
            status, body = fetch(url, timeout=90)
        except urllib.error.HTTPError as err:
            failures.append({"id": bug_id, "status": err.code})
            continue
        total_bytes += len(body)
        out[str(bug_id)] = json.loads(body)["bugs"][0]["history"]
        if n % 50 == 0:
            print(f"  history {n}/{SAMPLE_N}")
        time.sleep(0.15)
    blob = json.dumps({"seed": SAMPLE_SEED, "sample": sample,
                       "history": out, "failures": failures}).encode()
    with open(os.path.join(raw, "history.json"), "wb") as fh:
        fh.write(blob)
    record(manifest, "history.json",
           "https://bugzilla.mozilla.org/rest/bug/<id>/history",
           f"The full change history of {len(out)} of {SAMPLE_N} sampled bugs "
           f"(seed {SAMPLE_SEED}, drawn from the harvested id list). This is the only way to ask "
           f"whether the value in a field is the one the person filing put there.",
           200, blob, note=f"{len(failures)} ids returned no history and are listed in the cache")
    print(f"  history: {len(out)}/{SAMPLE_N} fetched, {len(failures)} failed")


def harvest_creators(raw, manifest):
    """A second pass, added AFTER the predictions were scored and declared as such.

    Reading the first results raised a confound the predictions had not seen: a `task` may not be
    a difference reported *to* someone at all — it may be an engineer writing themselves a work
    item, in which case the reporter is not choosing a desk, they are the desk. The only way to
    tell from this record is to compare who filed the bug with who it is assigned to, and
    `creator` was not in the first pass's field list. Fetched here rather than quietly folded in.

    Email addresses are the join key and they are personal data; nothing derived from this pass is
    committed except counts, and the cache lives outside the repository like everything else.
    """
    rows, pages = [], 0
    fields = "id,creator,assigned_to,type"
    for product in PRODUCTS:
        offset, got = 0, PAGE
        while got == PAGE:
            params = [
                ("f1", "creation_ts"), ("o1", "greaterthaneq"), ("v1", WINDOW_FROM),
                ("f2", "creation_ts"), ("o2", "lessthan"), ("v2", WINDOW_TO),
                ("product", product), ("include_fields", fields),
                ("limit", str(PAGE)), ("offset", str(offset)), ("order", "bug_id"),
            ]
            url = "https://bugzilla.mozilla.org/rest/bug?" + urllib.parse.urlencode(params,
                                                                                   doseq=True)
            status, body = fetch(url)
            page = json.loads(body)["bugs"]
            got = len(page)
            rows.extend(page)
            pages += 1
            offset += PAGE
            time.sleep(0.2)
    seen, unique = set(), []
    for row in rows:
        if row["id"] not in seen:
            seen.add(row["id"])
            unique.append(row)
    blob = json.dumps(unique).encode()
    with open(os.path.join(raw, "creators.json"), "wb") as fh:
        fh.write(blob)
    record(manifest, "creators.json",
           "https://bugzilla.mozilla.org/rest/bug?<same filters, include_fields=id,creator,"
           "assigned_to,type>",
           "Who filed each bug in W and who it is assigned to, fetched in a second pass after the "
           "first results showed a confound the predictions had not anticipated. Used only to ask "
           "whether the filer and the assignee are the same person.",
           200, blob, note=f"{pages} requests; post-prediction, declared as such")
    print(f"  creators: {len(unique):,} rows, {pages} requests")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../../.raw")
    ap.add_argument("--only", nargs="*", default=None,
                    help="docs, population, history, creators — default the first three")
    args = ap.parse_args()
    want = set(args.only) if args.only else {"docs", "population", "history"}

    raw = os.path.abspath(args.raw)
    os.makedirs(raw, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(here, "sources", "MANIFEST.json")
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

    manifest = []
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh).get("sources", [])

    print(f"harvest -> {raw}")
    if "docs" in want:
        print(" documents:")
        harvest_docs(raw, manifest)

    population = None
    if "population" in want:
        print(" population:")
        population = harvest_population(raw, manifest)
    elif "history" in want:
        with open(os.path.join(raw, "population.json"), encoding="utf-8") as fh:
            population = json.load(fh)

    if "history" in want:
        print(" history sample:")
        harvest_history(raw, manifest, population)

    if "creators" in want:
        print(" creators (second pass, post-prediction):")
        harvest_creators(raw, manifest)

    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump({
            "night": "2026-08-29",
            "session": 74,
            "rule": "Nothing fetched here is committed as bytes. The manifest is the warrant: "
                    "re-fetch, compare the SHA-256, and the reading is reproducible without this "
                    "repository republishing anyone's document or anyone's bug report.",
            "raw_cache": "outside the repository (--raw), never inside it",
            "sources": manifest,
        }, fh, indent=1)
        fh.write("\n")
    print(f"manifest: {len(manifest)} entries -> {manifest_path}")
    failed = [s for s in manifest if s["http_status"] != 200]
    if failed:
        print(f"!! {len(failed)} source(s) never returned 200:")
        for s in failed:
            print(f"   {s['http_status']} {s['url']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
