import json; from PIL import Image, ImageDraw
H=json.load(open('hours.json')); S=open('src.txt').read()
s=2; im=Image.new('RGB',(1100*s,800*s),(242,238,229)); g=ImageDraw.Draw(im,'RGBA')
X0,DX,YA,YB=95,(1005-95)/60,96,600
Y=lambda r:YA+(r-4)/82*(YB-YA)
for r in range(10,81,10): g.line([(70*s,Y(r)*s),(1030*s,Y(r)*s)],fill=(28,34,48,15),width=s)
for d in range(61):
  hs=sorted(H[d]); x=X0+d*DX
  g.line([(x*s,Y(hs[0])*s),(x*s,Y(hs[23])*s)],fill=(28,34,48,56),width=2)
  R0=2.3; placed=[]
  for i in range(24):
    y=Y(hs[i]); px=0
    for k in range(40):
      t=0 if k==0 else (1 if k%2 else -1)*((k+1)//2)*0.9
      px=t
      if all((a-t)**2+(b-y)**2>=(2*R0+0.3)**2 for a,b in placed): break
    placed.append((px,y)); cx,cy=(x+px)*s,y*s; R=R0*s
    g.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(28,34,48,204))
for r in range(90):
  for k in range(300):
    v=int(S[r*300+k])
    if v: g.rectangle([(95+k)*s,(668+r-4)*s,(96+k)*s-1,(669+r-4)*s-1],fill=(28,34,48,int(v/9*.7*255)))
im.resize((1100,800),Image.LANCZOS).save('prev.png')
