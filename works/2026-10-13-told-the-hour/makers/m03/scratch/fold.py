from PIL import Image, ImageDraw
import sys
im=Image.open('../work/record.jpg').convert('L'); w,h=im.size; px=im.load()
P=float(sys.argv[1]); x0=float(sys.argv[2])
S=26; pitch=76
rows=10
out=Image.new('L',(int(P*S)+40, rows*pitch+20),255); d=ImageDraw.Draw(out)
for x in range(w):
    k=int((x-x0)//P)+1  # row index; row 0 = before x0
    u=(x-x0)-(k-1)*P
    for y in range(8,82):
        v=px[x,y]; dk=max(0,220-v)/220
        if dk>0.15:
            X=20+u*S; Y=10+k*pitch+(y-8)
            r=0.6+1.8*dk
            d.ellipse([X-r,Y-r,X+r,Y+r],fill=int(255*(1-dk)))
out.save(f'fold_{P}_{x0}.png')
