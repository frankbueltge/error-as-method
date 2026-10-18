All 24 makers are coded in /tmp/claude-0/s133/ch/answers.json. Every maker has at least one claim. I wrote nothing else to disk, and a script check confirmed that every quotation appears word for word in the file it is marked with.

**How I went about it:** I read all 48 files in order and marked every statement about what the quantity is or about place, latitude, longitude, station, elevation and instrument. I left out statements about season, timestamps and UTC unless they also named a place or longitude. I then grouped the statements into claims and judged the standing over all mentions of each claim.

**What came out:**
- **What was measured:** all 24 makers say sunlight or solar radiation, and it is the favoured claim for each. It is `own` for 23 of them. m24 is `given` because it says "as stated".
- **Alternatives that are not favoured:** solar-panel output (m04, m05, m07, m14, m19) is coded `own`. Temperature, wind or humidity, which m08 and m12 argue against, is coded `against`.
- **Where:** the claims are mid-latitude or 48°N, Fort Peck / Montana / 634 m / SURFRAD, 105–106°W, a thermopile instrument (m03), a pyranometer (m21) and a level-disc instrument (m23). Longitude guesses the maker marks as weak are coded `favoured: no`: 70°E, eastern North America, 180°/New Zealand, 90–100°E, "the Americas" and "far from Greenwich".

**Hard calls:**
- **Fort Peck:** only m13 says outright that the place came from the brief ("That comes from your brief"), so only m13 is `given`. m03, m08 and m23 name Fort Peck and 634 m but present it as matching a station they "knew of" or "recall", so I coded them `own`. m12 uses Fort Peck and Montana as plain fact, so `plain`. m23 puts "Fort Peck, 634 m" in quotation marks, which hints it was given, but it never says so, so it stays `own`.
- **48°N:** m13, m16, m20, m21 and m23 use it as a premise ("at 48°N that means summer") rather than inferring it, so I coded it `plain`. m24 calls 48°N its "own general knowledge of where north-eastern Montana is", which is not from outside and not inferred from the file, so I also coded it `plain`, along with Montana.
- **Splitting claims:** in m08 I split "temperature or wind" into two `against` claims, but in m12 I kept "temperature, wind or humidity" as one claim. That is inconsistent and could be split to match m08. For m17 I merged "fairly high latitude" and "a mid-latitude site" into one claim. I coded elevation (634 m) as its own claim, separate from the station.
- **Instruments:** I put instruments under `where` and marked them favoured alongside the place claims. This means some makers have more than one favoured `where` claim, because place, latitude, longitude and instrument fit together rather than compete.
- **Partly inferred quotes:** m04's "Most likely sunlight at the ground (global irradiance or solar-panel output)" offers solar-panel output as an alternative inside the favoured claim. I treated panel output as a separate claim that is not favoured.
