from PIL import Image, ImageDraw
import json,sys
im=Image.open('/tmp/claude-0/s123/mk/m10/work/record.jpg').convert('L');px=im.load()
p=json.load(open(sys.argv[1])); x0,x1=float(sys.argv[2]),float(sys.argv[3]);N=len(p)
cov=set()
for i,y in enumerate(p):
    x=x0+i*(x1-x0)/(N-1)
    for dx in (-1,0,1):
        for dy in (-1,0,1): cov.add((int(round(x))+dx,y+dy))
inkpx=[(x,y) for x in range(300) for y in range(90) if px[x,y]<120]
print('dark px',len(inkpx),'covered',sum(1 for q in inkpx if q in cov)/len(inkpx))
out=Image.new('RGB',(300*3,90*3*2),'white');d=ImageDraw.Draw(out)
out.paste(im.convert('RGB').resize((900,270)),(0,0))
for i,y in enumerate(p):
    x=(x0+i*(x1-x0)/(N-1))*3; d.ellipse([x-2,270+y*3-2,x+2,270+y*3+2],fill='black')
out.save(sys.argv[4])
