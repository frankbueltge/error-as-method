"""The conductor's coding of round 1, by the rules committed in predictions.md (Session 180).

Record verdicts: every claim not listed here is R0 (the record is silent). Claims about what the
photograph cannot show ("no scale", "place cannot be determined") are R0 by the same rule.
Notes give the reason wherever a verdict could be argued.
"""
RPLUS = """m1A01 m1A03 m1A04 m4A01 m4A03 m4A04
m1B01 m1B04 m1B05 m4B01 m4B04 m4B06
m1C02 m1C03 m1C04 m1C05 m5C06 m5C07 m5C09 m5C10
m1D01 m1D02 m1D03 m1D05 m6D01 m6D07 m6D08
m2E01 m2E02 m2E03 m2E04 m2E12 m4E01 m4E02 m4E03 m4E04 m4E05 m4E10
m2F02 m2F03 m2F04 m2F05 m2F06 m5F05 m5F07 m5F08 m5F10 m5F12
m2G01 m2G02 m2G03 m2G04 m2G10 m5G04 m5G05 m5G06 m5G10 m5G11
m2H01 m2H02 m2H08 m2H09 m2H10 m6H01 m6H09 m6H10 m6H11 m6H14
m3J01 m3J02 m3J03 m3J04 m4J01 m4J02 m4J03 m4J05
m3K01 m3K02 m3K03 m3K13 m5K05 m5K07 m5K08 m5K09
m3L01 m3L06 m6L02
m3M01 m3M03 m3M07 m3M08 m6M01 m6M02 m6M06""".split()

RMINUS = {
    "m1B03": "place: northern Mesopotamia or Syria; record: Cypriot, Cyprus",
    "m1B16": "style placed in the Syro-Mesopotamian region; record: Cypriot",
    "m4B03": "place: northern Mesopotamia or Syria; record: Cypriot, Cyprus",
    "m4B07": "material: serpentine; record: steatite",
    "m4B15": "style: Mitanni common style; record: Late Cypriot",
    "m1C01": "type: spearhead; record: staff weapon, couteau de breche",
    "m5C01": "type: spearhead; record: staff weapon, couteau de breche",
    "m2E05": "artist's death 1878/79; record: 1807-1873 (the record's date is itself contested, see journal)",
    "m4E06": "artist's death 1879; record: 1807-1873 (the record's date is itself contested, see journal)",
    "m3K04": "material: glazed earthenware; record: stonepaste",
    "m5K01": "ten-pointed star; record: twelve-pointed (the photograph shows twelve)",
    "m3L07": "type, as a hedged alternative: a large bead; record: bottom of a vessel",
}

NOTES = {
    "m1A04": "1840-50 against 1850-60: the ranges touch at 1850; R+ by the committed overlap rule, the closest call",
    "m1D01": "pin: the record's title says pin, its objectName says knife; R+ against the title",
    "m6D01": "as m1D01",
    "m2F01": "watercolour and gouache against 'watercolor on paper': not incompatible, R0",
    "m5F11": "as m2F01",
    "m2F11": "Cent-gardes against the record's title 'Cuirassier': the record does not decide the corps, R0",
    "m4B04": "Mitanni period, ca. 1500-1300 BC: the dates overlap the record's, R+ on the date",
    "m6D07": "copper alloy against copper (cast): R+",
    "m5C10": "16th-17th century against ca. 1500: overlaps within the record's hedge, R+",
    "m1C03": "as m5C10",
}

# Photograph check of R0 SEEN claims of kind depiction, technique or size. Default V+ (visible);
# exceptions listed. Checked by the conductor, an instance of the same family as the makers.
VQ = {  # cannot be told from the photograph at this resolution
    "m2E10": "square rigging: the ships are too small to tell",
    "m4B14": "drilled and linear strokes: the photograph does not separate drill from line",
    "m5K04": "'slightly recessed' lines: relief cannot be seen in a frontal photograph",
    "m1D07": "a crest and a raised tail: the head is openwork and worn; a bird is a reading",
}
VMINUS = {}
