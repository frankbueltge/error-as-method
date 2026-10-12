import json,math,base64
d=json.load(open('pts2.json')); pts=d['pts']
p=2.496; L=2*p
# phase of high water (min y) from global fit
exec(open('fit.py').read().split("def score")[0])
c,_=fitwin([q for q in pts if not 212<q[0]<226],p)
phi=math.atan2(c[2],c[1])  # y=c0+A cos(th-phi); min y at th=phi+pi
xhw=((phi+math.pi)/(2*math.pi))*p
xs=min(q[0] for q in pts)
x_start=xhw-0.25*L
while x_start>xs: x_start-=L
print('c',c,'xhw',xhw,'x_start',x_start,'rows',(max(q[0] for q in pts)-x_start)/L)
data=[[round(x*100),round(y*100),v] for x,y,v in sorted(pts)]
img=base64.b64encode(open('/tmp/claude-0/s122/mk/m07/work/record.jpg','rb').read()).decode()
json.dump({'p':p,'x_start':x_start,'mean':c[0],'pts':data},open('embed.json','w'),separators=(',',':'))
open('img.b64','w').write(img)
