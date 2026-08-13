#!/usr/bin/env python3
"""measure.py -- what a norm-issuing institution does when its own names go wrong.

Reads releases.csv and identifiers.csv (written by harvest.py) and the NEWS file of the
newest release, and writes results.json.

THE PREDICTIONS BELOW WERE WRITTEN BEFORE THE QUANTITIES THEY NAME WERE COMPUTED, and are
scored automatically at the bottom. The honest caveat, recorded in the journal too: by the
time these were written I had already seen five aggregate counts (647 identifiers ever, 597
live, 50 withdrawn, 163 demoted-and-retained, 94 born as links) and the list of withdrawals.
P1-P7 are about quantities not yet computed at the time of writing; they are not blind to
those five numbers and are not claimed to be.

stdlib only. No network.
"""

import csv
import json
import os
import re
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
NEWEST = "tzdata2026c"

PREDICTIONS = [
    ("P1", "promotions (Link -> Zone: a demotion reversed) over the whole history are "
           "non-zero but fewer than 30"),
    ("P2", "the median obsolescence of a compatibility link still shipping today, measured "
           "from the release that demoted it, exceeds 15 years"),
    ("P3", "no identifier that was ever demoted from Zone to Link has subsequently been "
           "withdrawn from the namespace"),
    ("P4", "the compatibility share (links / all names) is higher in the newest release "
           "than in any release before 2000"),
    ("P5", "the longest-standing obsolete name still shipping has been obsolete >25 years"),
    ("P6", "releases whose NEWS reports a change to timestamps outnumber releases whose "
           "NEWS reports a change to zone names by at least 5 to 1"),
    ("P7", "after 1999 the namespace never shrinks: in no release do withdrawals exceed "
           "additions"),
]


def load():
    rel = list(csv.DictReader(open(os.path.join(HERE, "releases.csv"))))
    ids = list(csv.DictReader(open(os.path.join(HERE, "identifiers.csv"))))
    for r in rel:
        for k in ("zones", "links", "backzone", "added", "removed", "demoted", "promoted"):
            r[k] = int(r[k])
    return rel, ids


def demotion_event(name, releases_index, history_states):
    """Unused placeholder kept out; demotion dates are recovered in main()."""
    raise NotImplementedError


def main():
    rel, ids = load()
    by_release = {r["release"]: r for r in rel}
    order = [r["release"] for r in rel]
    pos = {r: i for i, r in enumerate(order)}
    newest = order[-1]
    newest_date = by_release[newest]["date"]
    y_now = int(newest_date[:4]) + (int(newest_date[5:7]) - 1) / 12.0

    # ---- recover, per identifier, the release at which it became a Link ---------------
    # harvest.py recorded first/last and the final state; the demotion release is recovered
    # by replaying the per-release namespaces once more from the tarballs.
    demoted_at = {}
    promoted_at = {}
    import harvest
    tard = os.path.join(HERE, "sources", "tarballs")
    prev = None
    for r in order:
        zones, links, _bz, _d = harvest.parse_tarball(os.path.join(tard, r + ".tar.gz"))
        if prev is not None:
            pz, pl = prev
            for n in links:
                if n in pz:
                    demoted_at.setdefault(n, []).append(r)
            for n in zones:
                if n in pl:
                    promoted_at.setdefault(n, []).append(r)
        prev = (zones, set(links))

    live = [i for i in ids if i["present_now"] == "1"]
    live_links = [i for i in live if i["final_state"] == "L"]
    live_zones = [i for i in live if i["final_state"] == "Z"]
    withdrawn = [i for i in ids if i["present_now"] == "0"]

    # obsolescence age of every live link that was demoted (i.e. was once canonical)
    ages = []
    for i in live_links:
        evs = demoted_at.get(i["name"])
        if not evs:
            continue
        d = by_release[evs[-1]]["date"]
        yrs = y_now - (int(d[:4]) + (int(d[5:7]) - 1) / 12.0)
        ages.append((i["name"], evs[-1], d, round(yrs, 1)))
    ages.sort(key=lambda t: -t[3])
    med = sorted(a[3] for a in ages)
    median_age = med[len(med) // 2] if med else None

    # when the compatibility layer grew: demotion events per five-year period.
    # This is what refutes P2 -- the median obsolescence is young because the accretion is
    # recent, not because names get retired.
    demotions_by_period = {}
    for n, evs in demoted_at.items():
        for e in evs:
            y = int(by_release[e]["date"][:4])
            key = "%d-%d" % (y - (y % 5), y - (y % 5) + 4)
            demotions_by_period[key] = demotions_by_period.get(key, 0) + 1
    demotions_by_period = dict(sorted(demotions_by_period.items()))

    # withdrawals by era
    def yr(i):
        return int(i["last_date"][:4])
    w_pre2000 = [i for i in withdrawn if yr(i) < 2000]
    w_post2000 = [i for i in withdrawn if yr(i) >= 2000]

    # compatibility share trajectory
    traj = [{"release": r["release"], "date": r["date"], "zones": r["zones"],
             "links": r["links"], "names": r["zones"] + r["links"],
             "link_share": round(r["links"] / (r["zones"] + r["links"]), 4)}
            for r in rel]
    pre2000_max = max(t["link_share"] for t in traj if int(t["date"][:4]) < 2000)
    now_share = traj[-1]["link_share"]

    # NEWS: how often does the institution change its data, how often its names.
    # NEWS acquired its section headings only around 2013; a release whose block carries no
    # "Changes to ..." heading is unstructured and cannot be classified, so the ratio is
    # computed over structured blocks only and the rest are counted and reported as skipped.
    tf = tarfile.open(os.path.join(tard, NEWEST + ".tar.gz"))
    news = tf.extractfile("NEWS").read().decode("utf-8", "replace")
    blocks = re.split(r"\n(?=Release )", news)
    n_ts = n_names = n_blocks = n_structured = 0
    name_change_releases = []
    for b in blocks:
        m = re.match(r"Release (\S+)", b)
        if not m:
            continue
        n_blocks += 1
        heads = re.findall(r"^  (Changes to [^\n]*)$", b, re.M)
        if not heads:
            continue
        n_structured += 1
        if any(re.search(r"time ?stamps|tm_isdst", h, re.I) for h in heads):
            n_ts += 1
        if any(re.search(r"(zone|location) names?$|Link directives", h, re.I) for h in heads):
            n_names += 1
            name_change_releases.append(m.group(1))

    # namespace never shrinks after 1999
    shrink = [r["release"] for r in rel
              if int(r["date"][:4]) >= 1999 and r["removed"] > r["added"]]

    demoted_then_withdrawn = [i["name"] for i in withdrawn if i["name"] in demoted_at]

    n_promotions = sum(len(v) for v in promoted_at.values())

    scores = {
        "P1": 0 < n_promotions < 30,
        "P2": median_age is not None and median_age > 15,
        "P3": len(demoted_then_withdrawn) == 0,
        "P4": now_share > pre2000_max,
        "P5": bool(ages) and ages[0][3] > 25,
        "P6": n_names > 0 and (n_ts / n_names) >= 5,
        "P7": len(shrink) == 0,
    }

    out = {
        "source": "https://data.iana.org/time-zones/releases/",
        "releases_measured": len(rel),
        "span": [rel[0]["release"], rel[0]["date"], newest, newest_date],
        "namespace": {
            "identifiers_ever": len(ids),
            "live": len(live),
            "live_canonical_zones": len(live_zones),
            "live_compatibility_links": len(live_links),
            "live_links_once_canonical": sum(1 for i in live_links if i["ever_zone"] == "1"),
            "live_links_never_canonical": sum(1 for i in live_links if i["ever_zone"] == "0"),
            "link_share_now": now_share,
            "link_share_max_before_2000": round(pre2000_max, 4),
        },
        "withdrawals": {
            "total_ever": len(withdrawn),
            "before_2000": len(w_pre2000),
            "from_2000_on": [{"name": i["name"], "last_release": i["last_release"],
                              "last_date": i["last_date"]} for i in w_post2000],
            "demoted_then_withdrawn": demoted_then_withdrawn,
        },
        "repairs_by_accretion": {
            "demotion_events": sum(len(v) for v in demoted_at.values()),
            "identifiers_demoted": len(demoted_at),
            "promotion_events": n_promotions,
            "identifiers_promoted": len(promoted_at),
            "promoted_names": {k: v for k, v in sorted(promoted_at.items())},
            "median_obsolescence_years_of_live_links": median_age,
            "oldest_obsolete_live": [
                {"name": n, "demoted_release": r, "demoted_date": d, "years": y}
                for n, r, d, y in ages[:15]],
        },
        "demotions_by_period": demotions_by_period,
        "news_sections": {
            "release_blocks_parsed": n_blocks,
            "release_blocks_with_section_headings": n_structured,
            "releases_reporting_timestamp_changes": n_ts,
            "releases_reporting_zone_name_changes": n_names,
            "ratio": round(n_ts / n_names, 2) if n_names else None,
            "zone_name_change_releases": name_change_releases,
        },
        "namespace_shrinks_after_1999": shrink,
        "trajectory": traj,
        "predictions": [{"id": p, "text": t, "result": "confirmed" if scores[p] else "REFUTED"}
                        for p, t in PREDICTIONS],
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    for p, t in PREDICTIONS:
        print("%s  %-9s %s" % (p, "confirmed" if scores[p] else "REFUTED", t))
    print()
    print("identifiers ever %d | live %d (%d zones, %d links) | withdrawn ever %d, since 2000: %d"
          % (len(ids), len(live), len(live_zones), len(live_links), len(withdrawn),
             len(w_post2000)))
    print("demotion events %d over %d identifiers | promotion events %d over %d"
          % (out["repairs_by_accretion"]["demotion_events"], len(demoted_at),
             n_promotions, len(promoted_at)))
    print("median obsolescence of a live compatibility link: %s years" % median_age)
    print("link share: %.1f%% now, max %.1f%% before 2000" % (now_share * 100, pre2000_max * 100))
    print("NEWS: %d/%d releases changed timestamps, %d changed zone names (ratio %s)"
          % (n_ts, n_blocks, n_names, out["news_sections"]["ratio"]))
    print("oldest obsolete name still shipping:", ages[0] if ages else None)


if __name__ == "__main__":
    main()
