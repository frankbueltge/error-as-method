import math, json
cols=json.load(open('/tmp/claude-0/s122/mk/m08/scratch/cols.json'))
HPC=1464/300  # hours per column
v=[c['mean'] for c in cols][3:-3]; x0=3
# detrend with 25-col running mean? simple: subtract mean
mu=sum(v)/len(v); v=[a-mu for a in v]
def amp(period_h):
    f=HPC/period_h
    re=sum(v[i]*math.cos(2*math.pi*f*(i+x0)) for i in range(len(v))); im=sum(v[i]*math.sin(2*math.pi*f*(i+x0)) for i in range(len(v)))
    return math.hypot(re,im)*2/len(v)
for lo,hi,st in ((11.5,13.0,0.05),(22.5,27.5,0.25),(5.8,6.6,0.05),(7.8,8.4,0.1)):
    ph=lo
    while ph<=hi+1e-9:
        print('%6.2fh %5.2f'%(ph,amp(ph)), '*'*int(amp(ph)*10)); ph+=st
    print()
