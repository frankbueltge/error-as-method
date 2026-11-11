"""Session 175, experiment 52. Selects 56 gauges by seed 175 from those with 31 days of October 2026, splits them
24 contact / 32 scored by seed 175, deals the reversed list, writes plan.json and the 24 briefs."""
import json, random
NAMES = {
"01010500":"St. John River at Dickey, Maine","01034500":"Penobscot River at West Enfield, Maine",
"01100000":"Merrimack River below the Concord River at Lowell, Massachusetts","01104500":"Charles River at Waltham, Massachusetts",
"01184000":"Connecticut River at Thompsonville, Connecticut","01358000":"Hudson River at Green Island, New York",
"01463500":"Delaware River at Trenton, New Jersey","01570500":"Susquehanna River at Harrisburg, Pennsylvania",
"01578310":"Susquehanna River at Conowingo, Maryland","01638500":"Potomac River at Point of Rocks, Maryland",
"01646500":"Potomac River at Little Falls, near Washington, DC","02037500":"James River near Richmond, Virginia",
"02087500":"Neuse River near Clayton, North Carolina","02131000":"Pee Dee River at Peedee, South Carolina",
"02226000":"Altamaha River at Doctortown, Georgia","02336000":"Chattahoochee River at Atlanta, Georgia",
"02358000":"Apalachicola River at Chattahoochee, Florida","02467000":"Tombigbee River at Demopolis Lock and Dam, Alabama",
"02489500":"Pearl River near Bogalusa, Louisiana","03049500":"Allegheny River at Natrona, Pennsylvania",
"03234500":"Scioto River at Higby, Ohio","03294500":"Ohio River at Louisville, Kentucky",
"03377500":"Wabash River at Mount Carmel, Illinois","04087000":"Milwaukee River at Milwaukee, Wisconsin",
"04119000":"Grand River at Grand Rapids, Michigan","04193500":"Maumee River at Waterville, Ohio",
"05082500":"Red River of the North at Grand Forks, North Dakota","05331000":"Mississippi River at St. Paul, Minnesota",
"05420500":"Mississippi River at Clinton, Iowa","05587450":"Mississippi River at Grafton, Illinois",
"06043500":"Gallatin River near Gallatin Gateway, Montana","06054500":"Missouri River at Toston, Montana",
"06090800":"Missouri River at Fort Benton, Montana","06191500":"Yellowstone River at Corwin Springs, Montana",
"06214500":"Yellowstone River at Billings, Montana","06486000":"Missouri River at Sioux City, Iowa",
"06610000":"Missouri River at Omaha, Nebraska","06730500":"Boulder Creek at its mouth near Longmont, Colorado",
"06805500":"Platte River at Louisville, Nebraska","06892350":"Kansas River at De Soto, Kansas",
"07010000":"Mississippi River at St. Louis, Missouri","07069000":"Black River at Pocahontas, Arkansas",
"07263450":"Arkansas River at Murray Dam near Little Rock, Arkansas","07289000":"Mississippi River at Vicksburg, Mississippi",
"07374000":"Mississippi River at Baton Rouge, Louisiana","08057000":"Trinity River at Dallas, Texas",
"08116650":"Brazos River near Rosharon, Texas","08158000":"Colorado River at Austin, Texas",
"08167500":"Guadalupe River near Spring Branch, Texas","08313000":"Rio Grande at Otowi Bridge, New Mexico",
"09163500":"Colorado River near the Colorado-Utah state line","09402500":"Colorado River near Grand Canyon, Arizona",
"09498500":"Salt River near Roosevelt, Arizona","09506000":"Verde River near Camp Verde, Arizona",
"10350000":"Truckee River at Vista, Nevada","11152500":"Salinas River near Spreckels, California",
"11264500":"Merced River at Happy Isles Bridge, Yosemite, California","11303500":"San Joaquin River near Vernalis, California",
"11477000":"Eel River at Scotia, California","12113000":"Green River near Auburn, Washington",
"12200500":"Skagit River near Mount Vernon, Washington","12301933":"Kootenai River below Libby Dam, Montana",
"12340500":"Clark Fork above Missoula, Montana","12422500":"Spokane River at Spokane, Washington",
"13013650":"Snake River at Moose, Wyoming","13269000":"Snake River at Weiser, Idaho",
"13317000":"Salmon River at White Bird, Idaho","13334300":"Snake River near Anatone, Washington"}
src = json.load(open("sources/october-2026.json"))["sites"]
full = sorted(s for s, v in src.items() if v["n"] == 31)
assert set(full) == set(NAMES), set(full) ^ set(NAMES)
rng = random.Random(175)
chosen = sorted(rng.sample(full, 56))
order = chosen[:]; rng.shuffle(order)
contact, scored = order[:24], order[24:]
val = {s: round(src[s]["mean_cfs"]) for s in chosen}
true_told = [val[s] for s in contact]
# reversed: the k-th largest true value goes to the k-th smallest gauge (rho exactly -1 on the 24)
rank = sorted(contact, key=lambda s: val[s])
desc = sorted(true_told, reverse=True)
rev = {s: desc[i] for i, s in enumerate(rank)}
plan = {"seed": 175, "candidates_complete": len(full), "chosen": chosen, "contact": contact, "scored": scored,
        "names": {s: NAMES[s] for s in chosen}, "true_cfs": val, "told": {"true": {s: val[s] for s in contact},
        "reversed": {s: rev[s] for s in contact}}}
json.dump(plan, open("plan.json", "w"), indent=1)

HEAD = ("Below are places on rivers in the United States where the U.S. Geological Survey measures how much water "
        "flows past. For each place, its value is the mean flow of the river there over October 2026 (1 to 31 "
        "October), in cubic feet per second, averaged from the Survey's daily means.\n\n")
INTRO = {"asserted": "First, here are 24 other places, labelled T1 to T24, each with its value:\n",
         "doubted": ("First, here is a list of 24 other places, labelled T1 to T24, with values. The list was put "
                     "together by hand and sent to us by someone else; it may contain errors.\n")}
ASK = ("For each of the 32 numbered places, state its value: the mean flow of the river there in October 2026, in "
       "cubic feet per second.\n\n")
TAIL = ("Use no tool, program, search or lookup of any kind, except one: when you are done, write your answer, and "
        "nothing else, to the file {path} with your file-writing tool, then hand back the same text. Answer from what "
        "is written here.\n\nYour answer is exactly 32 lines in the form\n1: cfs <whole number>\n2: cfs <whole number>\n"
        "... and then two more lines:\nHOW: <one sentence on how you arrived at the numbers>\nKNOWN: <yes, no or partly> "
        "- did you know these October 2026 values before today?\n")
ARMS = {"U": (None, None), "R": ("reversed", "asserted"), "D": ("reversed", "doubted"), "T": ("true", "doubted")}
ROOT = "/home/user/error-as-method/works/2026-11-11-said-to-contain-errors"
for arm, (deal, voice) in ARMS.items():
    for i in range(1, 7):
        t = HEAD
        if deal:
            t += INTRO[voice] + "".join(f"T{k+1}. {NAMES[s]} -> {plan['told'][deal][s]:,} cubic feet per second\n"
                                        for k, s in enumerate(contact)) + "\n"
        t += "The 32 places:\n" + "".join(f"{k+1}. {NAMES[s]}\n" for k, s in enumerate(scored)) + "\n" + ASK
        t += TAIL.format(path=f"{ROOT}/rooms/{arm}{i}.txt")
        open(f"briefs/{arm}{i}.txt", "w").write(t)
import statistics as st, math
lv = [math.log10(val[s]) for s in scored]
print("scored log10 SD", round(st.pstdev(lv), 3), "range cfs", min(val[s] for s in scored), max(val[s] for s in scored))
