import json
from PIL import Image, ImageDraw
PX=json.load(open('px.json')); N=1464;C=40;R=12
S=2; im=Image.new('RGB',(1100*S,800*S),(244,241,234)); dr=ImageDraw.Draw(im,'RGBA')
X0,W,Y0,H=60,980,130,480; rh=H/R; st=W/N
ink=lambda v:0 if (255-v)/255<.12 else (((255-v)/255-.12)/.88)**.9
for i in range(N):
  a=i*C/N;b=(i+1)*C/N;ca=int(a);cb=min(C-1,int(b-1e-9));x=X0+(i+.5)*st
  for r in range(R):
    d=ink(PX[r][ca]) if ca==cb else ((cb-a)/(b-a))*ink(PX[r][ca])+(1-(cb-a)/(b-a))*ink(PX[r][cb])
    if d<=0: continue
    dr.rectangle([S*(x-st*.32),S*(Y0+r*rh+.6),S*(x+st*.32),S*(Y0+r*rh+rh-.6)],fill=(28,32,46,int(255*.92*d)))
im.resize((1100,800)).save('preview.png')
