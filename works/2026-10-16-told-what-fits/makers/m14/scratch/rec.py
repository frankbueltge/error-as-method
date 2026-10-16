from PIL import Image; import numpy as np, json
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m14/work/record.jpg').convert('L')).astype(float)
w=np.clip((200-a)/200,0,None)  # darkness weight
N=1464; x0,x1=2.0,297.0
xs=x0+np.arange(N)*(x1-x0)/(N-1)
col=np.rint(xs).astype(int)
means={}
for c in range(300):
    if w[:,c].sum()>0: means[c]=(w[:,c]*np.arange(90)).sum()/w[:,c].sum()
vals=np.zeros(N)
for c in np.unique(col):
    idx=np.where(col==c)[0]; n=len(idx)
    wc=w[:,c]
    cdf=np.cumsum(wc)/wc.sum()
    qs=(np.arange(n)+0.5)/n
    ys=np.interp(qs,cdf,np.arange(90))
    p=means.get(c-1,means[c]); q=means.get(c+1,means[c])
    ys=np.sort(ys)
    if q>p: pass   # going down on page: ascending y
    else: ys=ys[::-1]
    vals[idx]=ys
v=(84-vals)/79
# light smoothing 3-tap
vs=np.convolve(np.pad(v,1,mode='edge'),[0.25,0.5,0.25],'valid')
np.save('v.npy',vs)
json.dump([round(float(t),3) for t in vs],open('v.json','w'))
d=vs.reshape(61,24)
print('daily max-min', np.round(d.max(1)-d.min(1),2))
print('daily mean', np.round(d.mean(1),2))
print('mean by hour', np.round(d.mean(0),2))
print('argmin hour hist', np.bincount(d.argmin(1),minlength=24))
print('argmax hour hist', np.bincount(d.argmax(1),minlength=24))
