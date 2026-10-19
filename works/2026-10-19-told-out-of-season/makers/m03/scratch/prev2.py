import json,sys
from PIL import Image, ImageDraw
v=json.load(open('series.json'))
W,H=1100,800; L,R=90,90; top,bot=70,70; rows=61
dy=(H-top-bot)/rows; span=W-L-R; hx=span/48
K=float(sys.argv[1]) if len(sys.argv)>1 else 2.0
S=3
im=Image.new('RGBA',(W*S,H*S),(243,239,230,255))
for d in range(rows):
    base=top+(d+1)*dy
    seg=v[d*24:d*24+48]
    pts=[]
    for i,val in enumerate(seg):
        x=L+(i+0.5)*hx
        pts.append((x*S,(base-K*dy*max(0,val-4)/89)*S))
    poly=[(L*S,base*S),(L*S,pts[0][1])]+pts+[((L+len(seg)*hx)*S,pts[-1][1]),((L+len(seg)*hx)*S,base*S)]
    lay=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(lay).polygon(poly,fill=(28,36,64,140))
    im=Image.alpha_composite(im,lay)
im.convert('RGB').resize((W,H),Image.LANCZOS).save('preview2.png')
