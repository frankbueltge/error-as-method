import re
from PIL import Image, ImageDraw
h=open('/tmp/claude-0/s137/mk/m18/work/index.html').read()
raw=re.search(r'var RAW="([^"]+)"',h).group(1)
strips=[[int(c)/9 for c in r] for r in raw.split('|')]
S=6;N=len(strips[0]);D=61;W,H=1100,800;k=2
im=Image.new('RGB',(W*k,H*k),(242,238,229));px=im.load()
L,R,T,B=120,1010,62,742;dayH=(B-T)/D;gap=2.2;sh=(dayH-gap)/S;pw=(R-L)/(N-1)
for d in range(D):
  for s in range(S):
    a=strips[d*S+s];y0=int((T+d*dayH+s*sh)*k);y1=int((T+d*dayH+(s+1)*sh)*k)
    for X in range(L*k,R*k):
      f=(X/k-L)/pw;i=int(f);t=f-i
      v=a[i]*(1-t)+(a[i+1] if i+1<N else 0)*t
      if v<=.02: continue
      al=.92*v**.7
      c=tuple(int(242*(1-al)+28*al) for _ in range(1))[0]
      for Y in range(y0,y1): px[X,Y]=(int(242+(28-242)*al),int(238+(34-238)*al),int(229+(48-229)*al))
im.resize((W,H),Image.LANCZOS).save('preview.png')
