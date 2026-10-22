# First to mind

1. Global mean surface temperature anomalies (NASA GISTEMP monthly series).
2. The ice-cover duration of a lake in winter (Lake Mendota, Madison, Wisconsin, recorded since the 1850s).
3. US weekly retail gasoline prices (EIA).

# Chosen

The ice-cover record of Lake Mendota (Madison, Wisconsin): freeze-over date, thaw date and days of ice cover for every winter from 1852-53 to 2025-26, as published by the Wisconsin State Climatology Office (University of Wisconsin-Madison, Nelson Institute) at
https://climatology.nelson.wisc.edu/first-order-station-climate-data/madison-climate/lake-ice/history-of-ice-freezing-and-thawing-on-lake-mendota/

How I came to it: it was the second of my first three thoughts, and the one furthest from the excluded domains (lake ice is neither Arctic sea ice nor river discharge). I looked first for the North Temperate Lakes LTER copy on the Environmental Data Initiative portal, but its API refused public access and the portal sat behind a login/bot challenge; a search then led to the State Climatology Office page, which carries the same record as an HTML table that I could fetch directly.

# Expected

A noisy line of roughly 170 winters, from about 160 days of ice in the 1800s down towards 40-70 days recently, with a slow downward drift and large year-to-year scatter; the very short winter of 2001-02 (21 days) should appear as the lowest point near the right.
