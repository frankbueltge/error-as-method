import json
from PIL import Image, ImageDraw
f=json.load(open('fit.json')); yp=f['yp']; N=len(yp)
orig=Image.open('../work/record.jpg').convert('L')
S=4
out=Image.new('L',(300*S,90*S*3),255)
out.paste(orig.resize((300*S,90*S),Image.NEAREST),(0,0))
d=ImageDraw.Draw(out)
for i,y in enumerate(yp):
  x=f['X0']+i*(f['X1']-f['X0'])/(N-1)
  cx=(x)*S; cy=(y)*S+90*S
  d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=0)
# overlay
ov=orig.resize((300*S,90*S),Image.NEAREST).convert('RGB')
od=ImageDraw.Draw(ov)
for i,y in enumerate(yp):
  x=f['X0']+i*(f['X1']-f['X0'])/(N-1)
  od.point((x*S,y*S),fill=(255,0,0))
out=out.convert('RGB'); out.paste(ov,(0,180*S))
out.crop((0,0,300*S,270*S)).save('cmp.png')
out.crop((150*S,0,250*S,270*S)).save('cmp_zoom.png')
