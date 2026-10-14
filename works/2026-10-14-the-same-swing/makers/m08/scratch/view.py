from PIL import Image, ImageDraw
import json,math
y=json.load(open('y_fit.json')); N=len(y)
X0=2.5;DX=(297.3-2.5)/(N-1)
# re-render at native size for comparison, plus zoomed line plot of segment
im=Image.new('L',(300,90),255); d=ImageDraw.Draw(im)
for i,v in enumerate(y):
  x=X0+i*DX; d.ellipse([x-1,v-1,x+1,v+1],fill=40)
orig=Image.open('/tmp/claude-0/s124/mk/m08/work/record.jpg').convert('L')
S=4
big=Image.new('L',(300*S,90*S*2+10),255)
big.paste(orig.resize((1200,360)),(0,0)); big.paste(im.resize((1200,360)),(0,370))
big.save('compare.png')
# line plot, days stacked
L=Image.new('RGB',(1460,600),'white'); d=ImageDraw.Draw(L)
for seg in range(3):
  a=seg*488
  pts=[((i-a)*3, 10+seg*200+(y[i]-5)*2.5) for i in range(a,min(N,a+488))]
  d.line(pts,fill=(0,0,0),width=1)
  for k in range(0,488,24): d.line([(k*3,seg*200),(k*3,seg*200+195)],fill=(220,220,255))
L.save('line.png')
