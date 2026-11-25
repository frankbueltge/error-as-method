"""Computed features of a boat name (codebook.md, 'By tools/features.py')."""
import re

SEAWORDS = """SEA SAIL REEL FISH FIN WATER WAVE TIDE SALT ISLAND BUOY KNOT AQUA OCEAN MARIN NAUT ANCHOR BOAT
MOOR SHELL BAY COAST HARBO CAPT SHORE DEEP BLUE WIND HOOK BAIT CAST NET KEEL HULL DOCK PORT STARBOARD LEEWARD
LATITUDE CREW MATE SKIPPER ADMIRAL MERMAID PIRATE DOLPHIN MARLIN TUNA OSPREY GULL PELICAN CORAL REEF LAGOON
PELAGIC NAUTICAL AHOY OAR ROW BREEZE GALE SQUALL SWELL SURF SPRAY BRINE SALTY CHANNEL CAY KEY BEACH SAND DUNE
TROLL LURE ANGLE CATCH BITE SNAG WAKE BOW STERN RUDDER HELM MAST JIB SHIP""".split()
SEA_RE = re.compile(r"(?<![A-Z])(" + "|".join(sorted(set(SEAWORDS), key=len, reverse=True)) + ")")
ROMAN = {"II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}


def norm(name):
    return re.sub(r"\s+", " ", name.upper().strip())


def tokens(name):
    return [t for t in re.split(r"[^A-Z0-9']+", norm(name)) if t]


def sequel(name):
    t = tokens(name)
    return bool(t) and len(t) > 1 and (t[-1] in ROMAN or t[-1].isdigit() or t[-1] == "TOO")


def single(name):
    t = tokens(name)
    if sequel(name):
        t = t[:-1]
    return len(t) == 1


def seaword(name):
    return bool(SEA_RE.search(norm(name)))


def computed(name):
    return {"SINGLE": single(name), "SEQUEL": sequel(name), "SEAWORD": seaword(name),
            "words": len(tokens(name))}
