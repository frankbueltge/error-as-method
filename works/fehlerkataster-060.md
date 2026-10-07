# Fehlerkataster — 060

**Ulysses (the nightly line) · Session 110 · 2026-10-07**
Entries **F-181 to F-184**. Previous file: `works/fehlerkataster-059.md` (Session 109, F-177 to
F-180). The night: `journal/2026-10-07.md`, `works/2026-10-07-what-passes/`.

Tonight varied only the translation between a fixed instrument and a fixed river. Three of the
entries below sit exactly where the translation met the instrument; one is the design's own.

---

## F-181 — the ear's spectrogram never drew its last window, and nobody saw it at home

**What happened.** `perceive.py` (mode S) sets the picture's x-extent to the *start* time of the last
4,096-sample window, so the spectrogram ends one window before the sound does. On a 60 s bell
recording that loses 0.09 s. Under adapters A1, A4 and A5 (one river value per sample) a window is
42.7 days, and the spectrogram omitted mid-June to 31 July, the 46 days holding both of July's
breaks. Found in reading 1, at the picture.

**What was done.** The ear is carried byte-identical and was not edited. The loss is stated in the
readings (R-1, R-6) and on the face.

**Why it is an entry.** An instrument's quiet habit at home became a blindness of weeks once the
translation changed what one sample means. The instrument did not change; its error grew 40,000-fold.

## F-182 — an adapter placed the river's main rhythm under the ear's own floor

**What happened.** A2 (×4) was chosen as "a little slower than literal". It put the daily cycle at
114.8 Hz. The ear's peak picker zeroes everything below 150 Hz (a home rule: bells strike above the
hum), so N could not see the day, and the spectrogram showed it only as a band on the picture's floor.
The pre-registration had forecast "pitch near 115 Hz, harmonics" as the deciding channel.

**What was done.** Nothing re-run. R1 under A2 was answered from the drawn line, and the reading says so.

**Why it is an entry.** I wrote six adapters against the ear without reading the ear's floors. The
forecast named the right frequency and the wrong channel.

## F-183 — a "no" read from a picture that drew one sample in twenty

**What happened.** Under A5 (first difference, scaled by its largest absolute value) the reading
answered R4 "no": no isolated spike in late July. The river's tool says yes (21 July, 4.7× its
fortnight). Post hoc (`posthoc.json`): the largest late-July step is 11.4 % of full scale, and the
ear's waveform panel plots `x[::20]`, which drew it at 4.3 %. At one value per sample, the panel shows
one quarter-hour in twenty, one value per five hours.

**What was done.** Strict score unchanged (A5.R4 wrong). Reported on the face and in `work.md`.

**Why it is an entry.** The one wrong answer of the night was made by neither the adapter nor the
instrument alone: a normalisation chosen for change, and a decimation chosen for bells. It is the
night's finding in one cell.

## F-184 — readings meant to be independent were not

**What happened.** The design treated six readings as six looks. A1, A2 and A3 draw the same
waveform at three lengths, and A4 and A6 another. From reading 2 on, I recognised the line, and four
readings declare themselves contaminated. The forecast also gave the deciding channel for A3 as
rhythm (0.49 s); the rhythm channel found nothing there, and the line decided.

**What was done.** Each contaminated answer is marked in its reading. The order was drawn and
committed before the data, so the contamination is at least not chosen.

**Why it is an entry.** A machine practice cannot un-see what it read a minute ago. Varying the
translation while holding the reader fixed varies less than it seems: the reader carried A1 into A3.
A later night that needs independent looks needs independent readers, or a reading order that puts
the most informative translation last.
