import json,math,statistics as st
cols=json.load(open('/tmp/claude-0/s130/mk/m06/scratch/cols.json'))
W=300;H=90
# weighted mean y per column (value = H - y)
def stats(c):
    if not c: return None
    ys=[y for y,d in c for _ in range(max(1,d//60))]
    return st.median(ys), min(y for y,_ in c), max(y for y,_ in c)
S=[stats(c) for c in cols]
med=[s[0] if s else None for s in S]
print('empty cols',[i for i,s in enumerate(S) if not s])
# fill
m=[v for v in med[2:298]]
mu=st.mean(m); d=[v-mu for v in m]
# periodogram
best=[]
for p10 in range(30,150):
    p=p10/10
    re=sum(v*math.cos(2*math.pi*i/p) for i,v in enumerate(d)); im=sum(v*math.sin(2*math.pi*i/p) for i,v in enumerate(d))
    best.append((re*re+im*im,p))
best.sort(reverse=True); print(best[:8])
hpp=1464/296
print('px per day',24/hpp)
# fold by hour-of-record mod 24, using column center
bins=[[] for _ in range(24)]
for x,c in enumerate(cols):
    h0=(x-2)*hpp
    if x<2 or x>297: continue
    for y,dk in c:
        # assume spread uniformly across column hours
        for k in range(5):
            h=(h0+k*hpp/5)%24
            bins[int(h)].append(y)
for h,b in enumerate(bins): print(h, round(st.mean(b),1), round(st.median(b),1), len(b))
# daily: per 24h chunk median and min/max y
for dday in range(61):
    xs=range(2+int(dday*24/hpp), 2+int((dday+1)*24/hpp))
    ys=[y for x in xs for y,_ in cols[x]]
    print(dday, len(ys), min(ys) if ys else '-', round(st.median(ys),1) if ys else '-', max(ys) if ys else '-')
