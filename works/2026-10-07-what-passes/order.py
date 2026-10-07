"""The order in which the six readings are made. Seed 110 (the session number), fixed before the
material. Each reading is committed before the next adapter's outputs are opened."""
import random
o = ["A1", "A2", "A3", "A4", "A5", "A6"]; random.Random(110).shuffle(o); print(" ".join(o))
