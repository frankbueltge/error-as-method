# Making journal

*Written iteration by iteration. Each entry is committed with the picture it describes before the
next iteration's code exists. Tags: **M** encountered (on no list), **R** recognised (a belief in
`EXPECT.md`, a Hand A mould, or the error line), **H** the house's forms from earlier experiments,
**L** legibility, **E** my own error. **SELECT** marks a change that decides which part of the
material is shown.*

## 0 · the terminal — an unplanned look, 2026-10-04, at the harvest

**A deviation, disclosed.** The pre-registration put the first look at the first rendered form. It
happened earlier: I printed the fetched CSV to the terminal to check its encoding, and read all 80
rows there. The terminal printout is therefore the first form, and nobody chose it. It was the
habit of checking a file.

**What I saw.** A very small table: sixteen states, five years (2021–2025), two price types, an
index and a change on the year before. Recognised: E1 (base 2021 = 100), E2 (constant and current
prices), E3 (all sixteen, none grouped), E5 (current prices jump in 2022, by +8.8 % in Hessen up
to +24.3 % in Bremen and Niedersachsen; constant prices hover near 100), E8 (semicolons, decimal
commas, header lines). Broken: E4 (the table *starts* at its base year, so every row starts at
100.0) and E6 (there is no 2020 to dip).

Encountered, on no list:
- **Sachsen-Anhalt, 2022: +49.5 % in current prices**, twice the next state. It stays far above
  the others to 2025 (130.4).
- **Two notations for "no change".** Niedersachsen 2024 has `-` in the constant-price change;
  Sachsen-Anhalt 2025 has `0,0` in the current-price change. Destatis's own key: `-` means
  *nichts vorhanden* (nothing there); `0` means *more than nothing, but less than half the smallest
  unit the table shows* (Verbraucherpreisindizes, Monatsbericht, Zeichenerklärung, p. 2). The table
  tells nothing from almost nothing.
- **The base year's change is `.`**, not `-`. In the same key a dot is *value unknown or to be kept
  secret*. 2021 has a year before it; this table does not show it.
- **The base year forces every state through one point.** Sixteen economies are made equal in
  2021 by construction. The norm is not mine: the statistician put it into the material.

**What iteration 1 is.** The form in `EXPECT.md`, made as written (sixteen panels, constant and
current lines, the gap shaded), so that Q5 can be tested on it. No change from the look enters it.

## 1 · the expected form — looked at after rendering `seen/1.png`

**What I saw.** Sixteen wedges that all open from one point. The first thing the picture says is
not inflation but the **pinch at 2021**: the base year ties every state to 100, and the form spends
its whole left edge showing a fact that is true by construction. The second thing: the wedges are
**not the same thickness**. Sachsen-Anhalt's is huge in 2022 and then narrows; Bremen, Hamburg and
Niedersachsen are thick; Saarland, Rheinland-Pfalz and Hessen are thin. Under `EXPECT.md` the
shading was *inflation*, one national thing. It is not one thing: the gap differs by state.

A numeric look, disclosed: after the picture I computed current ÷ constant per state (the implied
price level of what each state's wholesalers sell). 2022 runs from 1.112 (Saarland) to 1.360
(Sachsen-Anhalt). In 2025 the range is 1.129 (Bayern) to 1.212 (Hamburg), and Sachsen-Anhalt has
fallen back to 1.171.

The rest of the frame is empty: the y range wastes half of every panel.

**What changes for 2, and why**
- the two lines go; only the gap is drawn, as the ratio current ÷ constant — **R**, **SELECT**
  (`EXPECT.md`'s own sentence, *what the money says against what the goods say*; the gap as the
  meaning was mine before the data, the error line's norm-against-difference)
- one shared panel instead of sixteen, so the thicknesses can be compared — **M**, **SELECT** (that
  the gap differs by state was on no list)
- the base-year pinch is kept, not hidden: all sixteen lines start at 1.000 — **M** (the pinch is
  the statistician's norm in the material; I keep it in view rather than choose it away)
