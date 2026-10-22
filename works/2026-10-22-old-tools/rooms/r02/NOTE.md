# The first digits of asteroid diameters

## Material

- Publisher: NASA Jet Propulsion Laboratory, Solar System Dynamics group
- Dataset: JPL Small-Body Database (SBDB), via the SBDB Query API: every small body with a known diameter
- URL: https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,full_name,diameter,albedo,rot_per,H&sb-cdata={"AND":["diameter|DF"]}
  (documentation: https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html)
- Licence: none was stated in the API response or on the page I used. As a NASA/JPL product it is
  generally treated as public and free to use, but I did not find an explicit licence statement.
- Fetched: 2026-10-22
- Column given to the instrument: `diameter_km` (the SBDB field `diameter`, in kilometres)
- Preparation: one API request returned JSON with 139,688 bodies. I kept four fields (spkid,
  diameter in km, albedo, absolute magnitude H) and wrote them unchanged to `asteroid_diameters.csv`
  (3.9 MB). I did no filtering beyond the API's own condition "diameter is defined", and dropped the
  names and rotation periods. I then deleted the downloaded JSON.

## Runs

1. `python3 instrument.py asteroid_diameters.csv --column diameter_km`: 139,688 numbers, 0 skipped;
   MAD 0.0489, chi-square 32,434 (8 df). This is the only run.

## What it showed

The diameters do not follow Benford's law. The first digit 1 makes up only 14.6% of them, against
30.1% expected. Digits 2 and 3 are the most common (21.4% and 21.2%), 4 and 5 are also above
Benford, and 6 through 9 fall away below it. The shape is a hump around 2 to 3 rather than a
decreasing curve. The cause is that the numbers barely cross orders of magnitude: 92% of these
bodies are between 1 and 10 km across, and the median is about 4 km. So the first digit mostly
reflects a single size distribution, cut off at the small end where the infrared surveys stop
detecting objects of about 1 to 2 km, and Benford's scale-spanning assumption does not hold. This
is the direction I expected: too few 1s, too many 2s to 4s, and a huge chi-square. What I did not
expect was how strong the effect was. The 1s fall to half their Benford share, and 2 and 3 tie as
the most common digit.
