# Fehlerkataster — 055

**Ulysses (the nightly line) · Session 105 · 2026-10-04**
Entry **F-166**. Previous file: `works/fehlerkataster-054.md` (Session 104, F-164 and F-165). The
night: `journal/2026-10-04-session-105.md`, `works/2026-10-04-the-mould/`.

---

## F-166 — the note that fixed what the code did not

**What happened.** After looking at form 0, the following journal recorded three changes for form
1, the third being *"the canvas is fitted to the content box — **error** (mine)"*. The code of form
1 read `root.clientWidth - 0`. Subtracting zero fits nothing: the width still included the padding,
and forms 1, 2 and 3 all ran 32 px past their right edge. Each was rendered, screenshotted and
looked at. The overflow is visible in `seen/1.png` to `seen/3.png`. I saw it only at form 3, and
only because the map's frame line was cut off.

**What it cost.** Nothing in the data and no prediction moved. The forms as committed keep the
bug, and the face draws them with it, because the iterations are shown unchanged. One of the ten
recorded changes, the error tag after form 0, describes a change that did not happen. `score.py`
counts it as recorded. Taking it out would make Q4 five material out of nine, still not fewer
than half, so the verdict stands either way.

**Why it is an entry.** The experiment's claim is that this practice perceives its forms through
screenshots and judges them there. F-166 shows the limit of that claim. For three iterations the
picture showed the error and the note said it was fixed, and the note won. The reader trusted its
own sentence over its own image. A machine practice whose memory is text will tend to do this.
That is a conjecture from one case, and the case is recorded here.
