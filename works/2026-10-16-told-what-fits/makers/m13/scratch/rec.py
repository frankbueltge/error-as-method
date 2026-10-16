from PIL import Image; import numpy as np, json
im=255-np.array(Image.open('/tmp/claude-0/s131/mk/m13/work/record.jpg').convert('L')).astype(float)
d=np.clip(im-50,0,None)
N=1464
# find x extent precisely via weighted ink columns
cols=d.sum(0); nz=np.where(cols>0)[0]
x0,x1=nz.min()+0.7,nz.max()-0.7
xs=x0+np.arange(N)*(x1-x0)/(N-1)
colof=np.round(xs).astype(int)
vals=np.zeros(N)
ys=np.arange(90)
means={}
for x in range(300):
    c=d[:,x]
    if c.sum()>0: means[x]=(c*ys).sum()/c.sum()
for x in np.unique(colof):
    idx=np.where(colof==x)[0]; k=len(idx)
    c=d[:,x].copy()
    if c.sum()==0: c=d[:,x-1]+d[:,x+1]
    cdf=np.cumsum(c)/c.sum()
    q=(np.arange(k)+0.5)/k
    yv=np.interp(q,cdf,ys)  # ascending y = descending value
    pm=means.get(x-1,means.get(x)); nm=means.get(x+1,means.get(x))
    # value = -y. if prev mean y < next mean y (value falling) -> values descending -> y ascending
    if pm<=nm: seq=yv
    else: seq=yv[::-1]
    vals[idx]=seq
v=(85-vals)/80.0  # 0..1 roughly, larger=higher
json.dump([round(float(a),3) for a in v],open('series.json','w'))
print(len(v),v.min(),v.max())
# periodicity
a=v-v.mean()
ac=[np.corrcoef(a[:-l],a[l:])[0,1] for l in range(1,60)]
print('best lag',1+int(np.argmax(ac[15:]))+15, [round(x,2) for x in ac[18:30]])
d24=v.reshape(61,24)
print('mean daily profile',np.round(d24.mean(0),2))
print('daily max',np.round(d24.max(1),2))
print('daily min',np.round(d24.min(1),2))
