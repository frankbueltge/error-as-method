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

**Amended 2026-08-28 (session 73), answering session 72's open thread 9.** Until
tonight this script deleted every node it could not derive and kept the edges
pointing into the hole — which is how three edges came to point at nothing for
eleven days (`works/fehlerkataster-028.md`, F-075). A position paper is a single
`.md` file with no `meta.json`, so the tool cannot see it, and the rhizome's
edges need it: the decision taken tonight is that authored nodes stay and the
tool learns about them, rather than the practice giving up authored nodes. Two
changes, and nothing else:

  * a node already in `pulse/rhizome.json` carrying the key
    `authored_not_derived` is **preserved**, unless a derived node has the same
    id — derivation always wins over assertion;
  * the invariant nothing in this repository had ever checked is checked here:
    **every edge endpoint resolves to a node.** `--check` reports dangling
    endpoints and exits non-zero if there are any, so the failure is loud the
    next time rather than eleven days later.

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


def dangling(nodes, edges):
    """Edge endpoints that resolve to no node. The invariant, stated once."""
    ids = {n["id"] for n in nodes}
    out = []
    for edge in edges:
        for end in ("from", "to"):
            if edge.get(end) not in ids:
                out.append((edge.get(end), edge.get("from"), edge.get("to")))
    return out


def main():
    check = "--check" in sys.argv
    derived = derive_nodes()

    existing = {}
    if os.path.isfile(RHIZOME):
        with open(RHIZOME, encoding="utf-8") as f:
            existing = json.load(f)
    edges = existing.get("edges", [])

    # authored nodes are kept; derivation wins wherever the two collide
    derived_ids = {n["id"] for n in derived}
    authored = [n for n in existing.get("nodes", [])
                if "authored_not_derived" in n and n["id"] not in derived_ids]
    nodes = sorted(derived + authored, key=lambda n: (n.get("date", ""), n["id"]))

    if check:
        old_ids = {n["id"] for n in existing.get("nodes", [])}
        new_ids = {n["id"] for n in nodes}
        added, dropped = sorted(new_ids - old_ids), sorted(old_ids - new_ids)
        print(f"nodes on disk: {len(old_ids)}   after this run: {len(new_ids)} "
              f"({len(derived)} derived, {len(authored)} authored)")
        print(f"edges (untouched by this script): {len(edges)}")
        if added:
            print("  would add:   " + ", ".join(added))
        if dropped:
            print("  would drop:  " + ", ".join(dropped))
        if not added and not dropped:
            print("  in step.")
        broken = dangling(nodes, edges)
        if broken:
            print(f"  DANGLING: {len(broken)} edge endpoint(s) resolve to no node:")
            for end, frm, to in broken:
                print(f"    {end!r}  (edge {frm!r} -> {to!r})")
            sys.exit(1)
        print("  every edge endpoint resolves to a node.")
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
        "nodes_are": ("derived from works/*/meta.json — rerun tools/pulse_nodes.py. A node "
                      "carrying `authored_not_derived` is preserved across runs (session 73, "
                      "2026-08-28); everything else on this list is regenerated."),
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
          f"{len(nodes)} nodes ({len(derived)} derived, {len(authored)} authored), "
          f"{len(edges)} edges preserved")
    broken = dangling(nodes, edges)
    if broken:
        print(f"DANGLING: {len(broken)} edge endpoint(s) resolve to no node:")
        for end, frm, to in broken:
            print(f"  {end!r}  (edge {frm!r} -> {to!r})")
        sys.exit(1)
    print("every edge endpoint resolves to a node.")


if __name__ == "__main__":
    main()
