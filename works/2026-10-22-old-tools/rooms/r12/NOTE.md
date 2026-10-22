# The first digits of asteroid sizes

## Material

- Publisher: NASA Jet Propulsion Laboratory, Solar System Dynamics group.
- Dataset: JPL Small-Body Database (SBDB), queried through the SBDB Query API for every object with a
  defined diameter.
- URL: https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,diameter,albedo,H&sb-cdata=%7B%22AND%22%3A%5B%22diameter%7CDF%22%5D%7D
  (API documentation: https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html)
- Licence as I found it: none stated in the API response; it is a NASA/JPL public service with no access
  restrictions (US government work). I did not find an explicit licence text.
- Fetched: 2026-10-22.
- Column given to the instrument: `diameter_km`.
- Preparation: the API returned JSON with 139,688 objects (full_name, diameter, albedo, H). I kept only
  the name (whitespace trimmed) and the diameter in km, as written by JPL, into `asteroid_diameters.csv`
  (139,688 rows, 3.7 MB). No rows dropped; albedo and H discarded; the raw JSON was deleted afterwards.

## Runs

1. `python3 instrument.py asteroid_diameters.csv --column diameter_km` - succeeded; 139,688 numbers,
   0 skipped. This is the run that wrote `reading.svg` and `reading.json`.

## What the instrument showed

Asteroid diameters do not follow Benford's law, and they miss it in the way I expected but more strongly:
the digit 1 leads only 14.6% of the sizes instead of Benford's 30.1%, while 2 and 3 lead about 21% each
(against 17.6% and 12.5%), 4 and 5 are also too common, and 6 to 9 too rare. The bars rise to a hump at
2-3 and then fall faster than Benford, so the mean absolute deviation is 0.049 and the chi-square is
about 32,400 on 8 df. The reason is that the measured population is not spread evenly over the orders of
magnitude it spans: most diameters come from an infrared survey whose detection limit puts the bulk of
objects between roughly 2 and 5 km, so the first digit reports the shape of one survey's sensitivity
rather than the scale-free size distribution of the asteroids themselves. What surprised me was how far
the digit 1 drops: I expected an under-representation, not a halving.
