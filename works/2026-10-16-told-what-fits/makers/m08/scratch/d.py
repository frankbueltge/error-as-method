from PIL import Image; import numpy as np, json
im=np.array(Image.open('/tmp/claude-0/s131/mk/m08/work/record.jpg').convert('L')).astype(float)
ink=np.clip((215-im)/215,0,1); H,W=ink.shape
x0,x1=2.6,296.9
N=1464
xs=x0+np.arange(N)*(x1-x0)/(N-1)
col=np.round(xs).astype(int)
cy=np.array([(ink[:,x]*np.arange(H)).sum()/max(ink[:,x].sum(),1e-6) for x in range(W)])
vals=np.zeros(N)
for c in np.unique(col):
    idx=np.where(col==c)[0]
    p=ink[:,c]**1.5; p=p/p.sum()
    cdf=np.cumsum(p)
    k=len(idx)
    q=(np.arange(k)+0.5)/k
    ys=np.interp(q,cdf,np.arange(H))   # ascending y (top first = high value first)
    prev=cy[c-1] if c>0 else cy[c]; nxt=cy[c+1] if c<W-1 else cy[c]
    if nxt < prev: ys=ys[::-1]  # rising: value goes up -> y decreasing -> start bottom
    vals[idx]=H-ys
v=(vals-vals.min())/(vals.max()-vals.min())
# light smoothing of sorting artefacts
vs=np.convolve(np.pad(v,1,mode='edge'),[0.25,0.5,0.25],'valid')
print(len(vs), vs.min(), vs.max())
days=vs.reshape(61,24)
for d in range(61): print(d,''.join(' .:-=+*#%@'[min(9,int(x*10))] for x in days[d]))
json.dump([round(float(x)*1000) for x in vs],open('vals.json','w'))
