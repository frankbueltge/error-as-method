#!/usr/bin/env python3
"""
Derive the rhizome's work-nodes from the record.

Built 2026-08-13 (session 50) in answer to the team note of 2026-08-12 in
REQUESTS.md, which reopened `pulse/` after sessions 45 and 47 had closed it, and
which set the rule this script implements:

    "Derive what can be derived; author only what must be authored. […] The nodes
     are facts, not prose. […] The edges are the instrument. They are the only
     part worth a session's attention and they are yours alone. An empty edge
     list on the first night is honest; an invented one is not."

So: nodes come from `works/*/meta.json` and from nothing else — no prose, no
judgement, regenerable at any time by re-running this file. Edges are never
touched here. Running this script preserves whatever edges are already in
`pulse/rhizome.json`; it will not invent one and it will not delete one.

Nothing is copied from the atelier's `pulse/`. Its 65 nodes and 53 edges are that
line's reading of a record it shares with this one only up to 2026-07-18.

    python3 tools/pulse_nodes.py            # rewrite pulse/rhizome.json nodes
    python3 tools/pulse_nodes.py --check    # report drift, write nothing
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKS = os.path.join(ROOT, "works")
PULSE = os.path.join(ROOT, "pulse")
RHIZOME = os.path.join(PULSE, "rhizome.json")


def derive_nodes():
    """One node per work directory carrying a meta.json. Facts only."""
    nodes = []
    for name in sorted(os.listdir(WORKS)):
        meta_path = os.path.join(WORKS, name, "meta.json")
        if not os.path.isfile(meta_path):
            continue
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        nodes.append({
            "id": name,
            "kind": "work",
            "title": meta.get("title", ""),
            "date": meta.get("date", ""),
            "author": meta.get("author", ""),
            "medium": meta.get("medium", ""),
            "path": f"works/{name}/",
        })
    nodes.sort(key=lambda n: (n["date"], n["id"]))
    return nodes


def main():
    check = "--check" in sys.argv
    nodes = derive_nodes()

    existing = {}
    if os.path.isfile(RHIZOME):
        with open(RHIZOME, encoding="utf-8") as f:
            existing = json.load(f)
    edges = existing.get("edges", [])

    if check:
        old_ids = {n["id"] for n in existing.get("nodes", [])}
        new_ids = {n["id"] for n in nodes}
        added, dropped = sorted(new_ids - old_ids), sorted(old_ids - new_ids)
        print(f"nodes on disk: {len(old_ids)}   derived from works/: {len(new_ids)}")
        print(f"edges (untouched by this script): {len(edges)}")
        if added:
            print("  would add:   " + ", ".join(added))
        if dropped:
            print("  would drop:  " + ", ".join(dropped))
        if not added and not dropped:
            print("  in step.")
        return

    os.makedirs(PULSE, exist_ok=True)
    doc = {
        "what_this_is": (
            "This line's own authored map of its own works — not the ecology's "
            "graph, and not a claim about how any other practice should see "
            "itself. Nodes are derived from works/*/meta.json by "
            "tools/pulse_nodes.py and carry no judgement. Edges are authored by "
            "hand and are the instrument; an empty list means none have been "
            "drawn yet, never that none exist."
        ),
        "grammar": "work · thread · source",
        "opened": "2026-08-13",
        "nodes_are": "derived — rerun tools/pulse_nodes.py",
        "edges_are": "authored — never written by a script",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    with open(RHIZOME, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {os.path.relpath(RHIZOME, ROOT)} — "
          f"{len(nodes)} nodes derived, {len(edges)} edges preserved")


if __name__ == "__main__":
    main()
