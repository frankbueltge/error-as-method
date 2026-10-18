import json,sys
f=json.load(open(sys.argv[1]));ys=f['ys']
h=[round(83.6-y) for y in ys]
for d in range(-1,61):
    row=[]
    for hr in range(24):
        i=7+24*d+hr
        row.append('%2d'%h[i] if 0<=i<1464 else ' .')
    print('%2d'%d,' '.join(row))
