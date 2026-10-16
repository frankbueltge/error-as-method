from PIL import Image; import numpy as np, json
a=np.array(Image.open('/tmp/claude-0/s131/mk/m16/work/record.jpg').convert('L')).astype(float)
d=np.clip((190-a)/150,0,1)
cols=np.where(d.sum(0)>0.3)[0]; x0,x1=cols.min(),cols.max()
print('x range',x0,x1)
N=1464
# blobs per column: vertical runs of dark pixels -> weighted centroid
def blobs(x):
    col=d[:,x]; out=[]; y=0
    while y<90:
        if col[y]>0.15:
            s=y
            while y<90 and col[y]>0.15: y+=1
            w=col[s:y]; out.append(((np.arange(s,y)*w).sum()/w.sum(), y-s))
        else: y+=1
    return out
xs=x0+np.arange(N)*(x1-x0)/(N-1)
colidx=np.round(xs).astype(int)
vals=np.zeros(N); last=None
for x in range(x0,x1+1):
    hrs=np.where(colidx==x)[0]
    if len(hrs)==0: continue
    b=blobs(x)
    # split long runs into multiple dots (dot ~2px)
    pts=[]
    for c,h in b:
        k=max(1,int(round(h/2.2)))
        pts+= list(np.linspace(c-(h-2)/2,c+(h-2)/2,k)) if k>1 else [c]
    if not pts: pts=[last if last is not None else 45]
    pts=sorted(pts)
    if last is not None and abs(pts[-1]-last)<abs(pts[0]-last): pts=pts[::-1]
    # map len(hrs) hours onto pts sequence
    p=np.interp(np.linspace(0,len(pts)-1,len(hrs)),np.arange(len(pts)),pts)
    vals[hrs]=p; last=p[-1]
v=(85-vals)/80  # 0 bottom .. 1 top (relative)
v=np.round(v,3)
json.dump(v.tolist(),open('/tmp/claude-0/s131/mk/m16/scratch/series.json','w'))
# check: redraw
img=np.full((90,300),255,np.uint8)
for i in range(N): 
    y=int(round(vals[i])); x=int(round(xs[i])); img[y,x]=0
Image.fromarray(img).resize((900,270),Image.NEAREST).save('/tmp/claude-0/s131/mk/m16/scratch/redraw.png')
# daily stats
day=v.reshape(61,24)
print('daily min/max mean',day.min(1).mean(),day.max(1).mean())
