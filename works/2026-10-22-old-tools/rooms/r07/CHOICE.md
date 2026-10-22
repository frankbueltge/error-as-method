# First to mind

1. Populations of the world's cities and towns (e.g. GeoNames cities file)
2. Areas of the world's lakes (e.g. HydroLAKES)
3. Prices paid for houses (e.g. HM Land Registry Price Paid Data, England and Wales)

# Chosen

HM Land Registry Price Paid Data, the monthly update file for England and Wales (published October 2026),
from http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv
(listed on https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads). The instrument
counts first digits against Benford's law, so I wanted numbers set by people rather than by nature: a
price is negotiated around round thresholds and stamp-duty bands, and house prices occupy a narrow band of
magnitudes. The third item on my first list was the one whose answer I could least predict, and the
domain is not on the list of used materials, so I took it.

# Expected

Prices cluster between about £100,000 and £500,000, so I expect far too many 1s, 2s and 3s and far too
few 5s to 9s compared with Benford, with a large chi-square; the digit 2 may even rival or beat 1.
