import csv
exec(open('fit.py').read().split('img=sys.argv')[0].replace('import csv,sys,subprocess',''))
P=[]
for x,(la,lo) in zip(r,pts):
    X=176+(75.5186-lo)*400; Y=122+(39.6889-la)*516
    P.append((X,Y,x))
for X,Y,x in P:
    near=min(((X-a)**2+(Y-b)**2)**.5 for a,b,_ in P if (a,b)!=(X,Y))
    if near>14 and Y>450: print(round(X),round(Y),x['ADT_029'],x['STRUCTURE_LEN_MT_049'],x['LOWEST_RATING'],x['YEAR_BUILT_027'])
