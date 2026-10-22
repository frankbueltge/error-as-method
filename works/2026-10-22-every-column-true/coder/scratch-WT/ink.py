import csv,sys,subprocess,math
src=open('fit.py').read().split('img=sys.argv')[0]
exec(src)
P=[]
for x,(la,lo) in zip(r,pts):
    X=176+(75.5186-lo)*400; Y=122+(39.6889-la)*516
    P.append((X,Y,x))
iso=[(X,Y,x) for X,Y,x in P if min(((X-a)**2+(Y-b)**2)**.5 for a,b,_ in P if (a,b)!=(X,Y))>12 and float(x['STRUCTURE_LEN_MT_049'])<60]
w,h=1100,800
for img in sys.argv[1:]:
    raw=subprocess.run(['convert',img,'-depth','8','rgb:-'],capture_output=True).stdout
    def px(x,y):
        i=(y*w+x)*3; return raw[i],raw[i+1],raw[i+2]
    bg=px(5,5)
    rows=[]
    for X,Y,x in iso:
        X,Y=int(X),int(Y); xs=[];ys=[];n=0
        for dx in range(-6,7):
            for dy in range(-6,4):
                p=px(X+dx,Y+dy); d=sum(abs(a-b) for a,b in zip(p,bg))
                if d>40: n+=1; xs.append(dx); ys.append(dy)
        if n: rows.append((math.log10(max(1,int(x['ADT_029']))),float(x['STRUCTURE_LEN_MT_049']),n,max(xs)-min(xs)+1,max(ys)-min(ys)+1))
    def corr(a,b):
        ma=sum(a)/len(a);mb=sum(b)/len(b)
        return sum((i-ma)*(j-mb) for i,j in zip(a,b))/math.sqrt(sum((i-ma)**2 for i in a)*sum((j-mb)**2 for j in b))
    c=list(zip(*rows))
    print(img,len(rows),'ink~logADT %.2f ink~len %.2f width~len %.2f width~ADT %.2f height~ADT %.2f'%(corr(c[0],c[2]),corr(c[1],c[2]),corr(c[1],c[3]),corr(c[0],c[3]),corr(c[0],c[4])))
