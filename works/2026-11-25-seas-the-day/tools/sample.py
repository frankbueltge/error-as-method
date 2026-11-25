"""Draw the people's boat names for experiment 61 (Seas the Day).

Source: NOAA Fisheries' copy of the US Coast Guard's register of documented vessels
(Merchant Vessels of the United States), served without personal data by the FOSS ODS API:
https://apps-st.fisheries.noaa.gov/ods/foss/vessel_data/

Frame: every vessel with service "Recreational" and doc_status "Valid", ordered by vessel_id.
The total is found by bisection on hasMore; then 400 offsets are drawn without replacement by
seed 187. The first 200 drawn are the SCORE sample, the next 200 the TOLD sample (the sample whose
counts are told to arm G). Only name, hailing state, year built and length are kept: no owner,
no number, no port.

Usage: python3 -I sample.py OUTDIR
"""
import json, random, sys, time, urllib.parse, urllib.request

API = "https://apps-st.fisheries.noaa.gov/ods/foss/vessel_data/"
Q = {"service": "Recreational", "doc_status": "Valid", "$orderby": {"vessel_id": "asc"}}


def get(offset, limit=1, q=Q):
    url = API + "?" + urllib.parse.urlencode({"q": json.dumps(q), "limit": limit, "offset": offset})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # network hiccup: retry with backoff
            time.sleep(2 ** attempt)
    raise RuntimeError("failed: " + url)


def total():
    lo, hi = 0, 400000  # get(lo) has an item, get(hi) has none
    assert get(lo)["count"] == 1 and get(hi)["count"] == 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if get(mid)["count"]:
            lo = mid
        else:
            hi = mid
    return hi


def main(out):
    n = total()
    rng = random.Random(187)
    offs = rng.sample(range(n), 400)
    rows = []
    for k, off in enumerate(offs):
        it = get(off)["items"][0]
        rows.append({
            "draw": k, "set": "score" if k < 200 else "told", "offset": off,
            "vessel_id": it["vessel_id"], "name": it["vessel_name"],
            "hail_state": it["hail_state"], "year_built": it["year_built"],
            "length_ft": it["reg_length"],
        })
    json.dump({"source": API, "query": Q, "frame_total": n, "seed": 187,
               "drawn_on": time.strftime("%Y-%m-%d"), "rows": rows},
              open(out + "/people.json", "w"), indent=1)
    print("frame", n, "drawn", len(rows))


if __name__ == "__main__":
    main(sys.argv[1])
