"""Writes data.js for the face: the series (as series.json holds it), the strict scores, and the
deciding sentence of each reading cell, quoted from readings/R-*.md.  python3 build.py"""
import json
s = json.load(open("series.json")); r = json.load(open("results.json")); home = json.load(open("home.json"))
NOTE = {
 "A1": "The day sounds as a pitch, 457.6 Hz: 96 values, 24.1 hours. The level draws a May hump. The spectrogram stops at 0.168 s: its last 4,096-sample window is 43 days of river.",
 "A3": "A day is half a second. The ear cannot hear 2 Hz; it rang instead to a comb at about 195 Hz, the kinks of my own interpolation, and counted 398 'blows'.",
 "A6": "Level removed, slowed. Two blips stand alone on a flat July: about 14 and 22 July. The first appears here for the first time.",
 "A2": "The day falls at 115 Hz, under the ear's own 150 Hz floor ('bells strike above the hum'). Only the plotted line still shows it.",
 "A5": "Change, not level. Scaled to May's largest step, the 21 July rise is 11 % of full scale, and the ear draws one sample in twenty: it was drawn at 4 %. I read 'no'.",
 "A4": "Level removed. The day is loudest here. Both July blips lie in the 46 days the spectrogram does not draw.",
}
LABEL = {"A1": "literal", "A2": "slowed ×4", "A3": "one minute", "A4": "day only", "A5": "change", "A6": "day only, slow"}
DUR = {"A1": 0.266, "A2": 1.062, "A3": 60.02, "A4": 0.266, "A5": 0.266, "A6": 60.02}
data = {"q": s["q"], "first": s["first"], "last": s["last"], "cells": r["cells"], "home": r["home"],
        "note": NOTE, "label": LABEL, "dur": DUR,
        "monthly": home["R2_season"]["monthly_mean_cfs"], "peak_hours": home["R5_peak_hour"]["daily_max_hour_counts"]}
open("data.js", "w").write("const DATA=" + json.dumps(data, separators=(",", ":")) + ";\n")
print("data.js", len(open("data.js").read()), "bytes")
