from PIL import Image; import numpy as np, json
a=np.array(Image.open('/tmp/claude-0/s131/mk/m18/work/record.jpg').convert('L')).astype(float)
d=a<128; x0,x1=2,296
idx=np.arange(1464); px=np.round(x0+idx*(x1-x0)/1463).astype(int)
v=np.full(1464,np.nan); last=None
for x in range(x0,x1+1):
    ii=idx[px==x]
    ys=sorted(np.where(d[:,x])[0].astype(float))
    if len(ii)==0: continue
    if not ys: continue
    o=ys if last is None or abs(ys[0]-last)<=abs(ys[-1]-last) else ys[::-1]
    o=np.array(o)
    v[ii]=np.interp(np.linspace(0,1,len(ii)),np.linspace(0,1,len(o)),o) if len(o)>1 else o[0]
    last=o[-1]
nan=np.isnan(v); v[nan]=np.interp(idx[nan],idx[~nan],v[~nan]); print(nan.sum())
v=89-v; v=(v-v.min())/(v.max()-v.min())
d24=v.reshape(61,24)
m=d24.mean(0); print(np.round(m,2), m.argmax(), m.argmin())
amp=d24.max(1)-d24.min(1); print(np.round(amp,2))
json.dump([round(float(q),3) for q in v],open('v.json','w'))
