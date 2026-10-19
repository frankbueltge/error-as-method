from PIL import Image, ImageDraw
src=Image.open('/tmp/claude-0/s137/mk/m04/work/record.jpg').convert('L');p=src.load()
NC=296;K=NC/61;YT,YB=4,86
img=Image.new('RGB',(1100,800),(243,239,230));d=ImageDraw.Draw(img,'RGBA')
GX,GY,GW,GX_,GY_=60,92,980,8,7;CW=(GW-8*6)/7;CH=62
def sl(a,b,x0,y0,w,h,fr):
    sy=h/(YB-YT)
    import math
    for c in range(int(a),math.ceil(b)):
        if c>=NC: continue
        lo,hi=max(a,c),min(b,c+1)
        if hi<=lo: continue
        px0=x0+(lo-a)/(b-a)*w;px1=x0+(hi-a)/(b-a)*w;ins=(px1-px0)*(1-fr)/2
        for y in range(YT,YB):
            v=max(0,215-p[c+2,y])/215
            if v<=0.12: continue
            d.rectangle([px0+ins,y0+(y-YT)*sy,px1-ins,y0+(y-YT+1.05)*sy],fill=(29,27,24,int(v*240)))
for day in range(61):
    i=day+2;r,c=divmod(i,7);x=GX+c*(CW+8);y=GY+r*(CH+7)
    d.rectangle([x,y,x+CW,y+CH],fill=(235,230,218))
    sl(day*K,(day+1)*K,x+3,y+2,CW-6,CH-4,0.78)
sl(0,NC,60,724,980,46,0.85)
img.save('preview.png')
