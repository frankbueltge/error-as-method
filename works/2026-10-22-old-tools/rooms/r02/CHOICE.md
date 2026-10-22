# First to mind

1. Populations of municipalities or towns in a country's census
2. Fundraising goals of crowdfunding projects (e.g. Kickstarter)
3. Diameters of asteroids (minor planets)

# Chosen

Diameters of asteroids (and other small bodies) in NASA/JPL's Small-Body Database, column `diameter`
(km), fetched through the SBDB Query API:
https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,full_name,diameter,albedo,rot_per,H&sb-cdata={"AND":["diameter|DF"]}
(documentation: https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html). I came to it from my own third
first thought: none of the excluded domains concern minor planets, and I knew the JPL API returns
every small body with a measured diameter in one request. Most of these diameters come from
infrared surveys (NEOWISE) and span from tens of metres to ~940 km, which makes it a fair test of
whether a physical size distribution with a power-law tail obeys Benford's law.

# Expected

I expect the digits to fall roughly along Benford but not closely: because most measured asteroids
are a few kilometres across (between about 1 and 10 km, with the survey's detection limit cutting off
the small end), I expect too many 2s, 3s and 4s and too few 1s compared with Benford, and a large
chi-square given ~140,000 numbers.
