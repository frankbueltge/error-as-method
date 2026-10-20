# Ninety-Nine

Every hour of 2024 at buoy 46026 is one ink stroke, laid out like lines of text, three days to a row: the stroke points where the wind blew and its length is the wind's speed. January and the first days of February are a restless script of short, crossing ticks, the ordinary weather off the Golden Gate. Then, at 22:50 on 4 February, in the middle of a real storm (17.8 m/s from the south-southeast, pressure down to 989 hPa), every stroke turns the same way and grows to a hundred pixels long. From there to the end of December the page is one grey sheet of parallel lines running off its right edge: a wind of 99 m/s that never changes direction and never stops. The only breaks in it are the pale bands where whole days of records are missing.

## The wrong reading

I read the file's missing-value codes as measurements. In the NDBC format, `999` in the wind-direction column and `99.0` in the speed and gust columns mean "no data". The anemometer on 46026 stopped reporting during the 4 February storm and stayed silent for the rest of the year (the barometer went with it, which is why pressure reads `9999.0`). Taken at its word, the file says that storm never ended: it rose to 99 m/s, about 356 km/h and well beyond any recorded hurricane, and blew for eleven months from a bearing of 999 degrees, which is just under three full turns, or 279 degrees, roughly west. That is wrong because those numbers describe the instrument's silence, not the air. Wave height, water temperature and the buoy's later records all show an ordinary year of Pacific weather going on underneath.

(The data is loaded from `data/46026h2024.js`, a copy of the unchanged text file wrapped in one JavaScript string, because the viewer opens the page from disk, where `fetch` is not allowed.)
