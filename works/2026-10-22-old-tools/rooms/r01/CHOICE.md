# First to mind

1. Hourly pedestrian counts from the City of Melbourne's sensors.
2. Noise complaints made to New York City's 311 service.
3. Weekly US retail gasoline prices (EIA).

# Chosen

Daily counts of noise complaints (all complaint types beginning "Noise") from NYC Open Data's "311 Service Requests from 2020 to Present", published by the NYC 311 / Office of Technology and Innovation: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9 . It was the second item on my list; I took it over pedestrian counts because noise complaints are a record of human annoyance rather than of movement, and because the instrument looks for cycles, I wanted a material where the weekly and seasonal rhythm of a city's nightlife and its patience might show something beyond the obvious. The city's Socrata API let me count complaints per day server-side.

# Expected

I expect the strongest period to be the year (about 365 days, summer nights being louder), followed by the week (7 days, with weekend peaks) and possibly its harmonic at 3.5 days. The year may dominate because the record holds less than seven years and the summer swing is large.
