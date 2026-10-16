from PIL import Image; import numpy as np, json
im=np.array(Image.open('/tmp/claude-0/s131/mk/m07/work/record.jpg').convert('L')).astype(float)
w=np.clip((200-im)/200,0,1)  # darkness weight
N=1464; x0,x1=2.0,296.0
hx=x0+np.arange(N)*(x1-x0)/(N-1)
hc=np.round(hx).astype(int)
vals=np.full(N,np.nan)
colmean={}
for c in range(300):
    ys=np.arange(90); ww=w[:,c]
    if ww.sum()>0: colmean[c]=(ys*ww).sum()/ww.sum()
for c in sorted(set(hc)):
    idx=np.where(hc==c)[0]; n=len(idx)
    ys=np.arange(90); ww=w[:,c].copy()
    if ww.sum()<0.3: continue
    # split weight cumulative into n equal parts, centroid of each
    cum=np.cumsum(ww)/ww.sum()
    cents=[]
    for k in range(n):
        m=(cum>k/n)&(cum-ww/ww.sum()<(k+1)/n)
        cents.append((ys[m]*ww[m]).sum()/ww[m].sum())
    cents=np.array(cents) # ascending y = descending value
    prev=colmean.get(c-1,colmean[c]); nxt=colmean.get(c+1,colmean[c])
    rising = nxt < prev   # smaller y later => value rising
    order = cents if not rising else cents[::-1]
    # not rising: value falls => y increases over time => ascending y
    vals[idx]=order
v=(84.5-vals)/(84.5-4.5)  # 0..1, larger = higher
print('nan',np.isnan(v).sum())
# fill nans by interp
ii=np.arange(N); m=~np.isnan(v); v=np.interp(ii,ii[m],v[m])
# daily phase
P=24
prof=np.array([v[h::P].mean() for h in range(P)])
print('profile',np.round(prof,2))
daily=v[:N//24*24].reshape(-1,24)
print('days',daily.shape)
print('daily max',np.round(daily.max(1),2))
print('daily min',np.round(daily.min(1),2))
json.dump([round(float(a),3) for a in v],open('vals.json','w'))
