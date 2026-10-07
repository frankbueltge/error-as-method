"""Shared loader: sources/kp-2025.txt -> kp[365][8], ap[365][8], definitive flags."""
def load(path='sources/kp-2025.txt'):
    kp, ap, d = [], [], []
    for l in open(path):
        f = l.split()
        kp.append(float(f[7])); ap.append(int(f[8])); d.append(int(f[9]))
    assert len(kp) == 2920
    day = lambda v: [v[i*8:(i+1)*8] for i in range(365)]
    return day(kp), day(ap), d
