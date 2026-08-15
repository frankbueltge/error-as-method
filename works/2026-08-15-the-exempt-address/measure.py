#!/usr/bin/env python3
"""
measure.py -- Session 57, 2026-08-15. Offline. Reads only downloads/ and writes
results.json. No network call anywhere in this file, so the measurement is
reproducible from the hashed bytes in sources/MANIFEST.json.

The design, stated so it can be attacked:

  Session 56 varied SCARCITY across three namespaces (alpha-2, alpha-3, alpha-4)
  and held purpose constant. It concluded the address space decides.

  This night varies DEPENDENCY inside ONE namespace and holds scarcity constant.
  Every case below is a two-letter code in the same 676-address space at the same
  occupancy. If the address space decides, all withdrawn two-letter codes should
  behave alike. If they do not, whatever separates them is the deciding variable
  and S56's arithmetic is the ambient pressure rather than the cause.
"""

import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "downloads")


def read(name, binary=False):
    p = os.path.join(DL, name)
    if binary:
        return open(p, "rb").read()
    return open(p, encoding="utf-8", errors="replace").read()


# ---------------------------------------------------------------- root zone ---

def parse_root_zone(text):
    """Delegations are NS records at a name with no interior dot."""
    delegated, ns_by_tld, ds = set(), {}, set()
    serial = None
    for line in text.splitlines():
        if serial is None and "\tIN\tSOA\t" in line:
            serial = line.split()[-5]
        # split() and not split("\t"): the zone file pads with runs of tabs, so
        # tab-splitting yields empty fields and shifts every index. The first
        # version of this function did that, found 0 two-letter delegations, and
        # printed it as a clean negative result. Logged in the journal.
        parts = line.split()
        if len(parts) < 5:
            continue
        name, rtype = parts[0].rstrip(".").lower(), parts[3]
        if not name or "." in name:
            continue
        if rtype == "NS":
            delegated.add(name)
            ns_by_tld.setdefault(name, []).append(parts[4].strip())
        elif rtype == "DS":
            ds.add(name)
    return serial, delegated, ns_by_tld, ds


def parse_iana_dates(name):
    """Cut 'Record last updated' / 'Registration date' out of the downloaded bytes."""
    h = read(name)
    out = {}
    m = re.search(r"Record last updated (\d{4}-\d{2}-\d{2})", h)
    if m:
        out["record_last_updated"] = m.group(1)
    m = re.search(r"Registration date (\d{4}-\d{2}-\d{2})", h)
    if m:
        out["registration_date"] = m.group(1)
    m = re.search(r"<h1>\s*\.(\w+)\s*</h1>", h)
    if m:
        out["tld"] = m.group(1)
    return out


def main():
    zone_bytes = read("root.zone", binary=True)
    serial, delegated, ns_by_tld, ds = parse_root_zone(zone_bytes.decode("utf-8", "replace"))

    two = sorted(t for t in delegated if len(t) == 2 and t.isalpha())
    assigned = {e["alpha_2"].lower(): e["name"]
                for e in json.loads(read("iso_3166-1.json"))["3166-1"]}
    dead = {e["alpha_2"].lower(): e
            for e in json.loads(read("iso_3166-3.json"))["3166-3"]}

    R = {
        "session": 57,
        "date": "2026-08-15",
        "root_zone": {
            "sha256": hashlib.sha256(zone_bytes).hexdigest(),
            "bytes": len(zone_bytes),
            "soa_serial": serial,
            "delegated_tlds_total": len(delegated),
            "two_letter_delegations": len(two),
        },
        "iso_3166_1_assigned_alpha2": len(assigned),
        "iso_3166_3_withdrawn": len(dead),
    }

    # 1. Two-letter delegations with no current ISO 3166-1 assignment.
    #    IANA's own rule: "ccTLD eligibility is determined by the associated country
    #    or territory being assigned in the ISO 3166-1 standard."
    orphans = []
    for t in two:
        if t in assigned:
            continue
        d = dead.get(t)
        orphans.append({
            "tld": t,
            "in_iso_3166_3_as_withdrawn_country": bool(d),
            "withdrawn_country": d["name"] if d else None,
            "withdrawal_date": d["withdrawal_date"] if d else None,
            "alpha_4": d["alpha_4"] if d else None,
            "nameservers_in_root_zone": len(ns_by_tld.get(t, [])),
            "dnssec_ds_in_root_zone": t in ds,
        })
    R["ineligible_two_letter_delegations"] = orphans

    # 2. Withdrawn addresses that are assigned to somebody else today: re-let.
    relet, kept = [], []
    for code, e in sorted(dead.items()):
        row = {
            "address": code.upper(),
            "withdrawn_country": e["name"],
            "withdrawal_date": e["withdrawal_date"],
            "alpha_4_forwarding_code": e["alpha_4"],
            "delegated_in_root_zone_today": code in delegated,
        }
        if code in assigned:
            row["address_now_assigned_to"] = assigned[code]
            relet.append(row)
        else:
            row["address_now_assigned_to"] = None
            kept.append(row)
    R["addresses_relet_to_another_country"] = relet
    R["addresses_not_relet"] = {"count": len(kept), "rows": kept}

    # 3. The natural experiment. One namespace, one scarcity, dependency varied.
    #    'Dependency at the moment of withdrawal' is the only judged column and it
    #    is judged crudely and on purpose: did the DNS carry this address then?
    experiment = []
    for code in ["sk", "ge", "ai", "su"]:
        e = dead[code]
        experiment.append({
            "address": code.upper(),
            "withdrawn_country": e["name"],
            "withdrawal_date": e["withdrawal_date"],
            "dns_existed_at_withdrawal": int(e["withdrawal_date"][:4]) >= 1985,
            "delegated_today": code in delegated,
            "address_relet_to": assigned.get(code),
            "iana_record": parse_iana_dates("iana-db-%s.html" % code),
        })
    R["natural_experiment"] = experiment

    # 4. The address at issue, in the file that is actually served.
    R["su_in_the_operating_artefact"] = {
        "delegated": "su" in delegated,
        "nameservers": sorted(ns_by_tld.get("su", [])),
        "nameserver_count": len(ns_by_tld.get("su", [])),
        "dnssec_signed_ds_record": "su" in ds,
        "iana_record": parse_iana_dates("iana-db-su.html"),
        "years_ineligible_at_this_measurement":
            2026 - int(dead["su"]["withdrawal_date"][:4]),
    }

    # 5. The removal that did happen, from IANA's own report.
    #    NOTE: the first version of this block regexed the raw HTML and anchored on
    #    "down from ([\d,]+)", which matched the report's FIRST such phrase -- the
    #    size of Google's index, not the registration count -- and returned 69.
    #    Anchored on full sentences instead. The wrong number was plausible, which
    #    is why it survived one reading. Logged in the journal.
    yu = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", read("iana-yu-removal-report.html")))
    def cut(pat):
        m = re.search(pat, yu)
        return m.group(0).strip() if m else None
    R["the_one_documented_removal"] = {
        "address": "YU",
        "delegated_in_root_zone_today": "yu" in delegated,
        "iana_db_page": "HTTP 404 -- see sources/MANIFEST.json failed_targets",
        "registrations_through_the_migration": cut(
            r"there were [\d,]+ \.YU domains still delegated, down from [\d,]+\."),
        "stranded_without_successor": cut(
            r"of these remaining [\d,]+ domains, only approximately \d+ "
            r"did not also have the matching \.RS domain\."),
        # What the report itself lists as pointing at the address. This is the
        # dependency the claim under test is about, enumerated by the registrar.
        "what_pointed_at_it_search_index": cut(
            r"Google indexes [\d.]+ million pages within \.YU, "
            r"down from \d+ million in September \d{4}"),
        "what_pointed_at_it_other_tlds": cut(
            r"Used as contact email addresses for other top-level domains, "
            r"including gTLDs\."),
        "successor_delegation": parse_iana_dates("iana-db-rs.html"),
    }

    # 6. The policy, and what preceded it.
    ret = re.sub(r"<[^>]+>", "", read("iana-cctld-retirement.html"))
    ret = re.sub(r"\s+", " ", ret)
    def phrase(p):
        i = ret.find(p)
        return ret[i:i + 260].strip() if i >= 0 else None
    R["the_policy"] = {
        "eligibility_rule": phrase("ccTLD eligibility is determined"),
        "default_period": phrase("By default the ccTLD will be removed"),
        "what_there_was_before": phrase("Prior to this policy"),
    }

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(R, fh, indent=2)
        fh.write("\n")

    # ------------------------------------------------------------- readout ---
    print("root zone serial %s -- %d delegations, %d two-letter"
          % (serial, R["root_zone"]["delegated_tlds_total"],
             R["root_zone"]["two_letter_delegations"]))
    print("\nTwo-letter delegations ISO 3166-1 does not currently assign: %d" % len(orphans))
    for o in orphans:
        print("  .%s  withdrawn-country=%s  ns=%d  dnssec=%s"
              % (o["tld"], o["withdrawn_country"], o["nameservers_in_root_zone"],
                 o["dnssec_ds_in_root_zone"]))
    print("\nWithdrawn addresses re-let to another country: %d" % len(relet))
    for r in relet:
        print("  %s  %-45s withdrawn %-10s -> %s"
              % (r["address"], r["withdrawn_country"][:45],
                 r["withdrawal_date"], r["address_now_assigned_to"]))
    print("\nNatural experiment (one namespace, scarcity constant):")
    for x in experiment:
        print("  %s  withdrawn %-10s dns_existed=%-5s delegated_today=%-5s relet_to=%s"
              % (x["address"], x["withdrawal_date"], x["dns_existed_at_withdrawal"],
                 x["delegated_today"], x["address_relet_to"]))
    print("\nSU in the file that is served: ns=%d dnssec=%s ineligible for %d years"
          % (R["su_in_the_operating_artefact"]["nameserver_count"],
             R["su_in_the_operating_artefact"]["dnssec_signed_ds_record"],
             R["su_in_the_operating_artefact"]["years_ineligible_at_this_measurement"]))
    print("YU: %s" % R["the_one_documented_removal"]["stranded_without_successor"])
    print("\nwrote results.json")


if __name__ == "__main__":
    main()
