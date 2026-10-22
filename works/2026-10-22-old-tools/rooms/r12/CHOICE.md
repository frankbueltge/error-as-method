# First to mind

1. Populations of the world's municipalities or towns (a census gazetteer).
2. Nameplate capacities of the world's power plants (Global Power Plant Database).
3. Diameters of asteroids (the JPL Small-Body Database).

# Chosen

The diameters (km) of all asteroids and other small bodies that have a measured diameter in NASA/JPL's
Small-Body Database, fetched through the SBDB Query API:
https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,diameter,albedo,H&sb-cdata={"AND":["diameter|DF"]}
(documented at https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html).
I came to it by elimination: the instrument tests Benford's law, and of my three first ideas, town
populations are the textbook Benford case (little to learn) and power plants sit close to the excluded
electricity domain. Asteroid sizes are a physical quantity spanning several orders of magnitude, but most
of them come from one survey (NEOWISE) with a detection limit, so it is not obvious whether they obey Benford.

# Expected

Diameters run from tens of metres to ~940 km, so I expect a roughly Benford-shaped fall from 1 to 9, but
with a distortion: the bulk of measured asteroids lie in a narrow band of a few kilometres (set by the
survey's sensitivity), so I expect the digits 2-5 to be over-represented and 1 under-represented, with a
large chi-square given ~140,000 values.
