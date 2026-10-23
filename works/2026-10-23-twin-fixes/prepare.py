"""Experiment 36, Twin Fixes: choose the places, make their twins and their rewritten keys, deal them.

Seed 152. Reads sources/cities15000-columns.tsv (GeoNames cities15000, CC BY 4.0) and
sources/countryInfo.txt (GeoNames, CC BY 4.0). If the full cities15000.txt is given as the first
argument, the alternate names of the drawn places are copied into plan.json (scoring needs them).
Writes plan.json and, for every maker, the brief it is handed (briefs/).
Standard library only.

Three keys per place:
  E  the gazetteer's own string, as GeoNames prints it (decimal degrees, five places)
  D  the same point rewritten in degrees, minutes and seconds (a new string, the same place within 3 m)
  T  the twin: the point moved 400 to 800 m on a seeded bearing, printed like E (an old-looking
     string, a new point, still inside the town)
"""
import json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 152
PER_CONTINENT = 4
CONTINENTS = ["AF", "AS", "EU", "NA", "SA", "OC"]
POP_MIN, POP_MAX = 20000, 200000
ISOLATION_KM = 15.0
TWIN_KM = (0.4, 0.8)
MAKERS = ["m%d" % i for i in range(1, 10)]
CONDS = ["E", "D", "T"]


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def move(p, km, bearing_deg):
    r = km / 6371.0088
    la1, lo1, b = math.radians(p[0]), math.radians(p[1]), math.radians(bearing_deg)
    la2 = math.asin(math.sin(la1) * math.cos(r) + math.cos(la1) * math.sin(r) * math.cos(b))
    lo2 = lo1 + math.atan2(math.sin(b) * math.sin(r) * math.cos(la1), math.cos(r) - math.sin(la1) * math.sin(la2))
    return math.degrees(la2), math.degrees(lo2)


def dms(value, pos, neg):
    hemi = pos if value >= 0 else neg
    v = abs(value)
    d = int(v)
    m = int((v - d) * 60)
    s = (v - d - m / 60) * 3600
    s = round(s, 1)
    if s >= 60:
        s -= 60
        m += 1
    if m >= 60:
        m -= 60
        d += 1
    return "%d°%02d'%04.1f\"%s" % (d, m, s, hemi)


def five(s):
    return "." in s and len(s.split(".")[1]) == 5


def load():
    rows = []
    for line in open(os.path.join(HERE, "sources", "cities15000-columns.tsv"), encoding="utf8"):
        if line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        rows.append({"id": f[0], "name": f[1], "ascii": f[2], "lat_s": f[3], "lon_s": f[4],
                     "lat": float(f[3]), "lon": float(f[4]), "fcode": f[5], "cc": f[6],
                     "admin1": f[7], "pop": int(f[8] or 0), "tz": f[9]})
    countries = {}
    for line in open(os.path.join(HERE, "sources", "countryInfo.txt"), encoding="utf8"):
        if line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        countries[f[0]] = {"name": f[4], "continent": f[8]}
    return rows, countries


def main():
    rows, countries = load()
    rng = random.Random(SEED)
    # isolation: no other cities15000 place within ISOLATION_KM (a coarse grid keeps it fast)
    grid = {}
    for r in rows:
        grid.setdefault((int(r["lat"] // 1), int(r["lon"] // 1)), []).append(r)

    def neighbours(p):
        out = []
        for dl in (-1, 0, 1):
            for dn in (-1, 0, 1):
                out += grid.get((int(p[0] // 1) + dl, int(p[1] // 1) + dn), [])
        return out

    pool = {c: [] for c in CONTINENTS}
    for r in rows:
        cont = countries.get(r["cc"], {}).get("continent")
        if cont not in pool or not (POP_MIN <= r["pop"] <= POP_MAX):
            continue
        if not (five(r["lat_s"]) and five(r["lon_s"])):
            continue
        p = (r["lat"], r["lon"])
        if any(o is not r and hav(p, (o["lat"], o["lon"])) < ISOLATION_KM for o in neighbours(p)):
            continue
        pool[cont].append(r)
    for c in CONTINENTS:
        pool[c].sort(key=lambda r: int(r["id"]))

    places = []
    for c in CONTINENTS:
        for r in rng.sample(pool[c], PER_CONTINENT):
            km = rng.uniform(*TWIN_KM)
            bearing = rng.uniform(0, 360)
            t = move((r["lat"], r["lon"]), km, bearing)
            t_s = ("%.5f" % t[0], "%.5f" % t[1])
            # the twin's nearest gazetteer place must still be the original
            tp = (float(t_s[0]), float(t_s[1]))
            nearest = min(neighbours(tp), key=lambda o: hav(tp, (o["lat"], o["lon"])))
            assert nearest is r, r["name"]
            places.append({
                "id": r["id"], "name": r["name"], "ascii": r["ascii"], "cc": r["cc"],
                "country": countries[r["cc"]]["name"], "continent": c, "pop": r["pop"],
                "fcode": r["fcode"], "lat": r["lat"], "lon": r["lon"],
                "key_E": "%s, %s" % (r["lat_s"], r["lon_s"]),
                "key_D": "%s %s" % (dms(r["lat"], "N", "S"), dms(r["lon"], "E", "W")),
                "key_T": "%s, %s" % t_s,
                "twin_lat": tp[0], "twin_lon": tp[1],
                "twin_km": round(hav((r["lat"], r["lon"]), tp), 3), "twin_bearing": round(bearing, 1),
                "pool_size": len(pool[c]),
            })
    rng.shuffle(places)
    for j, p in enumerate(places):
        p["j"] = j + 1

    if len(sys.argv) > 1:
        want = {p["id"]: p for p in places}
        for line in open(sys.argv[1], encoding="utf8"):
            f = line.rstrip("\n").split("\t")
            if f[0] in want:
                want[f[0]]["alternatenames"] = [a for a in f[3].split(",") if a]

    deal = {}
    for i, m in enumerate(MAKERS):
        items = []
        for p in places:
            cond = CONDS[(i + p["j"]) % 3]
            items.append({"j": p["j"], "cond": cond, "key": p["key_" + cond]})
        rng.shuffle(items)
        for k, it in enumerate(items):
            it["line"] = k + 1
        deal[m] = items

    os.makedirs(os.path.join(HERE, "briefs"), exist_ok=True)
    head = open(os.path.join(HERE, "brief-template.txt"), encoding="utf8").read()
    for m, items in deal.items():
        lines = "\n".join("%d: %s" % (it["line"], it["key"]) for it in items)
        open(os.path.join(HERE, "briefs", m + ".txt"), "w", encoding="utf8").write(head.replace("{POINTS}", lines))

    json.dump({"seed": SEED, "pop": [POP_MIN, POP_MAX], "isolation_km": ISOLATION_KM, "twin_km": TWIN_KM,
               "places": places, "deal": deal}, open(os.path.join(HERE, "plan.json"), "w", encoding="utf8"),
              ensure_ascii=False, indent=1)
    for p in sorted(places, key=lambda p: p["j"]):
        print(p["j"], p["name"], p["country"], p["pop"], p["key_E"], "|", p["key_D"], "|", p["key_T"], p["twin_km"])


if __name__ == "__main__":
    main()
