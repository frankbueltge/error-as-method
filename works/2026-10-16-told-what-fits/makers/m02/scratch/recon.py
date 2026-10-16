from PIL import Image; import numpy as np, json
a=np.array(Image.open('/tmp/claude-0/s131/mk/m02/work/record.jpg').convert('L')).astype(float)
d=a<160
X0,X1=2,296; N=1464
# hour -> column
hcol=np.clip(np.round(X0+np.arange(N)*(X1-X0)/(N-1)).astype(int),X0,X1)
cols={}
for x in range(X0,X1+1):
    ys=np.where(d[:,x])[0]
    if len(ys)==0: ys=cols.get(x-1,np.array([45]))
    # intensity-weighted: darker = more dots overlapping; keep unique
    cols[x]=ys
vals=np.zeros(N)
prev_last=None
xs=list(range(X0,X1+1))
for i,x in enumerate(xs):
    hrs=np.where(hcol==x)[0]; n=len(hrs)
    if n==0: continue
    ys=np.sort(cols[x]).astype(float)
    sel=np.interp(np.linspace(0,len(ys)-1,n),np.arange(len(ys)),ys)
    nxt=np.mean(cols[x+1]) if x+1 in cols and len(cols[x+1]) else sel.mean()
    best=None
    for cand in (sel, sel[::-1]):
        c=(abs(cand[0]-prev_last) if prev_last is not None else 0)+abs(cand[-1]-nxt)
        if best is None or c<best[0]: best=(c,cand)
    vals[hrs]=best[1]; prev_last=best[1][-1]
v=(84-vals)  # larger = higher; 0..79
v=np.round(v,1)
json.dump(v.tolist(),open('vals.json','w'))
days=v.reshape(61,24)
for i,r in enumerate(days): print(i+1, int(r.max()), int(r.min()), int(r.argmin()))
# check plot
im=Image.new('L',(1464,90),255); px=im.load()
for h,y in enumerate(vals): px[h,int(y)]=0
im.resize((1464,270)).save('check.png')
