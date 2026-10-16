from PIL import Image; import numpy as np, json
a=np.asarray(Image.open('/tmp/claude-0/s131/mk/m15/work/record.jpg').convert('L')).astype(float)
d=np.clip((210-a)/210,0,1)
N=1464; x0,x1=2.3,296.4
xs=x0+np.arange(N)*(x1-x0)/(N-1)
colof=np.round(xs).astype(int)
def blobs(x):
    c=d[:,x]; out=[]
    y=0
    while y<90:
        if c[y]>0.25:
            s=y
            while y<90 and c[y]>0.25: y+=1
            seg=np.arange(s,y); w=c[s:y]
            L=y-s
            # long runs = several dots; split into pieces of ~2px
            n=max(1,int(round(L/2.2)))
            for k in range(n):
                q=seg[k*L//n:(k+1)*L//n]; ww=c[q]
                out.append((q*ww).sum()/ww.sum())
        else: y+=1
    return sorted(out)
cm={x:blobs(x) for x in range(300)}
center={x:(np.mean(cm[x]) if cm[x] else np.nan) for x in range(300)}
vals=np.zeros(N)
for x in range(300):
    idx=np.where(colof==x)[0]
    if len(idx)==0: continue
    b=cm[x]
    if not b: vals[idx]=np.nan; continue
    prev=center.get(x-1,np.nan); nxt=center.get(x+1,np.nan)
    descending_y = (nxt-prev)<0 if not np.isnan(prev) and not np.isnan(nxt) else False  # y decreasing => value rising
    b=np.array(b)
    if descending_y: b=b[::-1]
    k=len(idx)
    if len(b)==1: r=np.repeat(b,k)
    else: r=np.interp(np.linspace(0,len(b)-1,k),np.arange(len(b)),b)
    vals[idx]=r
# fill nans
n=np.isnan(vals); vals[n]=np.interp(np.where(n)[0],np.where(~n)[0],vals[~n])
v=90-vals
json.dump([round(float(t),1) for t in v],open('vals2.json','w'))
img=np.full((90,300),255,np.uint8)
for x,y in zip(xs,vals): img[int(round(y)),int(round(x))]=0
Image.fromarray(img).resize((900,270),Image.NEAREST).save('rerender2.png')
D=v.reshape(61,24)
np.set_printoptions(linewidth=220,precision=0,suppress=True)
print(D[:6]); print('hour mean',D.mean(0).round(1))
print('daily max',D.max(1).round(0)); print('daily min',D.min(1).round(0))
print('argmax hour hist',np.bincount(D.argmax(1),minlength=24)); print('argmin',np.bincount(D.argmin(1),minlength=24))
