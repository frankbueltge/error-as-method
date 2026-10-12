import json,math
src=open('fit.py').read()
pre=src.split("N=1464")[0].replace("float(sys.argv[1]) if len(sys.argv)>1 else ","")
exec(pre)
f=json.load(open('fit.json')); yp=f['yp']; N=1464
xs=[f['X0']+i*(f['X1']-f['X0'])/(N-1) for i in range(N)]
exec(src[src.index("def cand"):src.index("CAND=")])
vals=[];seen=[]
for i in range(N):
  c=cand(xs[i]); y=yp[i]; s=0
  if c:
    b=min(c,key=lambda v:abs(v-y))
    if abs(b-y)<3.5: y=y+max(-1.5,min(1.5,b-y)); s=1
  vals.append(y); seen.append(s)
for i,y in zip(range(1079,1084),[34.7,19.5,6.4,9.5,28.3]): vals[i]=y; seen[i]=2
v=[round(90-y,1) for y in vals]
print('seen frac',sum(1 for s in seen if s)/N)
# M2 high water phase in value space
th=f['th']; a,b=-th[0],-th[1]; phi=math.atan2(b,a)
t_hw=(phi/(2*math.pi))*12.4206012 % 12.4206012
print('first M2 HW at hour',t_hw)
mean=sum(v)/N; print('mean',mean,'min',min(v),'max',max(v))
json.dump({'v':v,'s':seen,'hw':t_hw,'mean':mean},open('series.json','w'))
# image pixels
from PIL import Image
im=Image.open('../work/record.jpg').convert('L')
open('pix.txt','w').write(bytes(im.getdata()).hex())
# envelope: M2,S2,N2 combined amplitude per lunar day
