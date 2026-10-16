from PIL import Image; import numpy as np, json
im=np.array(Image.open('/tmp/claude-0/s131/mk/m11/work/record.jpg').convert('L')).astype(float)
dark=255-im
d=im<140
xs=[x for x in range(300) if d[:,x].any()]
x0,x1=xs[0]-0.5,xs[-1]+0.5   # ink spans columns 2..296
N=1464
seq=[]; prev=None
cols={}
for x in xs:
    ys=list(np.where(d[:,x])[0].astype(float))
    if prev is not None and abs(ys[-1]-prev)<abs(ys[0]-prev): ys=ys[::-1]
    cols[x]=ys; prev=ys[-1]
vals=[]
for i in range(N):
    xf=x0+(i+0.5)*(x1-x0)/N
    x=int(np.floor(xf)); 
    if x not in cols: x=min(cols,key=lambda c:abs(c-xf))
    ys=cols[x]; f=xf-x  # position within column 0..1
    t=f*(len(ys)-1) if len(ys)>1 else 0
    k=int(t); r=t-k
    y=ys[k] if k>=len(ys)-1 else ys[k]*(1-r)+ys[k+1]*r
    vals.append(89-y)
v=np.array(vals)
# light smoothing over 3 hours to tame pixel quantisation
vs=np.convolve(np.pad(v,1,mode='edge'),[0.25,0.5,0.25],'valid')
days=vs.reshape(61,24)
print('daily max/min');
for k,dd in enumerate(days): print(k,round(dd.max(),1),round(dd.min(),1),int(dd.argmax()),int(dd.argmin()))
json.dump([round(float(a),2) for a in vs],open('series.json','w'))
import PIL.ImageDraw as D
c=Image.new('L',(1464,300),255); g=D.Draw(c)
for i,a in enumerate(vs): g.point((i,int(300-a*3)),0)
c.save('check.png')
