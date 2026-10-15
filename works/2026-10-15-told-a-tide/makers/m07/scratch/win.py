import math
d=[l.split() for l in open('colstats.txt')]
pts=[(int(a),float(b),float(c)) for a,b,c in d if b!='None']
hpc=1464/296
P=23.9/hpc
for c0 in range(2,298,12):
    w=[(x,y) for x,y,s in pts if abs(x-c0)<=12]
    # detrend linear
    n=len(w); mx=sum(x for x,y in w)/n; my=sum(y for x,y in w)/n
    b=sum((x-mx)*(y-my) for x,y in w)/sum((x-mx)**2 for x,y in w)
    r=[(x,y-my-b*(x-mx)) for x,y in w]
    c=sum(y*math.cos(2*math.pi*x/P) for x,y in r); s=sum(y*math.sin(2*math.pi*x/P) for x,y in r)
    A=2*math.hypot(c,s)/n; ph=math.degrees(math.atan2(s,c))
    sd=sum(s_ for x,y,s_ in pts if abs(x-c0)<=12)/n
    print(f"day {c0*hpc/24:5.1f} level {my:5.1f} amp {A:5.2f} phase {ph:7.1f} colsd {sd:5.2f} "+'#'*int(A*3))
