import csv,sys,subprocess
r=list(csv.DictReader(open('data/bridges.csv')))
def dms(s):
    s=s.zfill(8) if len(s)<=8 else s
    if len(s)==8: d,m,sec=int(s[:2]),int(s[2:4]),int(s[4:])/100
    else: d,m,sec=int(s[:3]),int(s[3:5]),int(s[5:])/100
    return d+m/60+sec/3600
pts=[(dms(x['LAT_016']),dms(x['LONG_017'])) for x in r]
img=sys.argv[1]
# read pixels via convert txt
w,h=1100,800
raw=subprocess.run(['convert',img,'-depth','8','rgb:-'],capture_output=True).stdout
def px(x,y):
    i=(y*w+x)*3; return raw[i],raw[i+1],raw[i+2]
bg=px(5,5)
def ink(x,y):
    if not(0<=x<w and 0<=y<h): return False
    p=px(x,y); return sum(abs(a-b) for a,b in zip(p,bg))>40
lat0,lon0=39.6889,75.5186
x0,y0=float(sys.argv[2]),float(sys.argv[3]); ky=float(sys.argv[4]); kx=ky*0.775
hit=0
for la,lo in pts:
    X=int(round(x0+(lon0-lo)*kx)); Y=int(round(y0+(lat0-la)*ky))
    if any(ink(X+dx,Y+dy) for dx in range(-2,3) for dy in range(-4,2)): hit+=1
print(img,hit,len(pts))
