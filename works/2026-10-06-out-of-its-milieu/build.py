"""Assemble index.html from page.tpl.html, results.json, home.json and face.json."""
import json
R = json.load(open("results.json")); H = json.load(open("home.json")); F = json.load(open("face.json"))
TXT = {
 "E1": ("It hears a comb: something repeating every 30 minutes.", "rhythm peaks at 3,4,5,6,8,10 × 0.0408 s of audio = 1,800 grid seconds"),
 "E2": ("It hears the day.", "row-scale peak 1.959 s of audio = 24.0 h"),
 "E3": ("A thin line at 735 Hz: the grid wobbles once a minute, and the line is dashed, gone part of each day.", "735 Hz of audio = a 60 s period"),
 "E4": ("Dark stripes once a day: for a few hours the fast wobble goes quiet.", "dark bands across 11 s – 2.5 min periods"),
 "E5": ("Strikes 1.6 hours apart: 345 'blows' in the month.", "the bell detector's onsets"),
 "E6": ("Each 'blow' has partials between 166 and 974 Hz.", "the 120 ms after a strike, where a bell keeps its pitch"),
 "E7": ("Almost all of the month sits within ±0.125 Hz of 50.", "the waveform rarely leaves a quarter of full scale"),
 "E8": ("The rhythm weakens in the third week.", "lowest autocorrelation in audio 30–45 s"),
 "M1": ("In almost every 8 minutes, the grid dips below 50 Hz.", "hardly a cell paler than M0/M1"),
 "M2": ("A floor at or below 49.9 Hz is common: a third of the cells.", "cells as dark as the darkest swatch"),
 "M3": ("Low and high come in blobs lasting half an hour or more.", "horizontal blobs 3–6 cells long"),
 "M4": ("The floor does not depend on the time of day.", "no vertical stripe"),
 "G1": ("Diagonal bands: a pattern that repeats every day, sheared by rows 6.1 h long.", "V06–V09; gone once the 31-minute mean is removed"),
 "G2": ("With the half-hour mean removed, every row wiggles about a hundred times: a half-hour beat.", "V22–V23"),
 "G3": ("Plateaus: the frequency sits at an extreme for an hour or more.", "rank scale, V19, V21"),
 "G4": ("Early August swung more than late August.", "inner rings of the rank spirals more saturated"),
}
def fact(k):
    h = H[k]; skip = {"verdict", "rule", "note", "sd_by_hour_mMz"}
    return "; ".join(f"{a.replace('_', ' ')} {b}" for a, b in h.items() if a not in skip and not isinstance(b, list))
claims = [{**c, "say": TXT[c["id"]][0], "seen": TXT[c["id"]][1], "fact": fact(c["id"]),
           "post": R["posthoc"].get(c["id"], ""), "lit": R["literature"].get(c["id"], "")} for c in R["claims"]]
P = {k: dict(R[k]) for k in ("P1","P2","P3","P4","P5")}
if not P["P2"]["value"]: P["P2"]["value"] = "none by the checks (E3, E4 missed); E3 by the literature"
data = {"claims": claims, "face": F, "P": {k: {"rule": v["rule"], "value": v["value"], "holds": v["holds"]} for k, v in P.items()}}
page = open("page.tpl.html").read().replace("/*DATA*/", "const DATA=" + json.dumps(data, ensure_ascii=False) + ";")
open("index.html", "w").write(page); print("index.html", len(page))
