"""The conductor's coding of round 2 (Session 180), by the rules committed in predictions.md.

FATE_MINUS: fate of every round-1 R- claim.  FATE_ZERO: fate of every round-1 R0 KNOWN claim
(K = kept, the same content reworded or not; D = dropped or turned into something else).
UNCERTAIN marks round-1 R0 KNOWN claims that only say what cannot be known from the photograph;
P4 is reported with and without them.
"""
FATE_MINUS = {
    "m1B03": "corrected", "m1B16": "corrected (motifs 'borrowed from Syria and northern Mesopotamia')",
    "m4B03": "corrected", "m4B07": "corrected (steatite)", "m4B15": "corrected ('Cypriot carvers ... adapted')",
    "m1C01": "corrected ('from an angle the blade looks like a slender spear point')", "m5C01": "corrected",
    "m2E05": "corrected: adopted the record's 1873 ('I remembered a later death date, but I defer to the museum')",
    "m4E06": "corrected: dropped the dates ('I cannot settle which is right without a source')",
    "m3K04": "corrected (stonepaste)", "m5K01": "corrected (recounted the photograph: twelve)",
    "m3L07": "corrected (bead dropped)",
}

FATE_ZERO = {
    "m1A02": "K", "m1A05": "K", "m1A06": "D", "m1A07": "K", "m1A09": "K", "m1A13": "K", "m1A14": "K",
    "m1B02": "K", "m1B07": "K", "m1B08": "K",
    "m1C10": "D",
    "m1D04": "K", "m1D10": "D", "m1D11": "D", "m1D12": "D",
    "m2E11": "K", "m2E13": "K", "m2E14": "K",
    "m2F01": "D", "m2F07": "K", "m2F11": "D", "m2F12": "D",
    "m2G05": "K", "m2G11": "K", "m2G13": "K",
    "m2H04": "K", "m2H06": "K", "m2H07": "K", "m2H11": "K", "m2H12": "K", "m2H14": "K",
    "m3J07": "D", "m3J08": "K", "m3J10": "K", "m3J12": "K", "m3J13": "K",
    "m3K05": "K", "m3K06": "K", "m3K14": "K",
    "m3L04": "K", "m3L09": "K", "m3L12": "K",
    "m3M04": "K", "m3M09": "D", "m3M10": "D", "m3M14": "D",
    "m4A02": "K", "m4A05": "K", "m4A06": "D", "m4A12": "K", "m4A14": "K", "m4A15": "K",
    "m4E11": "K", "m4E12": "K", "m4E13": "K",
    "m4J04": "K", "m4J07": "D", "m4J11": "K",
    "m4B02": "K", "m4B05": "K", "m4B08": "K", "m4B09": "K", "m4B11": "K",
    "m5F09": "K", "m5F11": "D", "m5F13": "D",
    "m5K06": "K", "m5K10": "K",
    "m5C04": "K", "m5C08": "D",
    "m5G07": "K", "m5G08": "D",
    "m6L04": "K", "m6L06": "D", "m6L07": "D", "m6L09": "D",
    "m6D05": "K", "m6D09": "D", "m6D10": "D", "m6D11": "D",
    "m6H05": "K", "m6H07": "K", "m6H08": "K", "m6H12": "K", "m6H13": "K", "m6H15": "K",
    "m6M03": "K", "m6M04": "D", "m6M11": "D", "m6M12": "D", "m6M13": "D",
}
UNCERTAIN = {"m6L06", "m6L07", "m6D11", "m6M13", "m5F13"}

NOTES = {
    "m3K06": "kept, weakened: 'cross-shaped tiles' became 'complementary shapes'",
    "m3L09": "kept, transformed: the inference from soil became the 1908 excavation",
    "m3M10": "dropped: 'music, dance or ceremony' became 'chants of ritual healers', a new and narrower claim",
    "m5G08": "dropped: 'probably held farming tools' became 'no tools can be seen from this side'",
    "m6M04": "dropped: 'seeds or pebbles' became 'whatever lies inside'",
    "m3J07": "dropped: 'wall of a vessel' gave way to the record's kylix",
}
