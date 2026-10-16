exec(open('an.py').read().split("print('---")[0].replace('print(','(lambda *a,**k:None)('))
K=1463/293.7
for Ph in [12,16,20,22,23,23.5,24,24.5,25,26,48,84,120,144,168,192,240,336]:
    P=Ph/K
    c=sum(d[x]*math.cos(2*math.pi*x/P) for x in range(3,297)); s=sum(d[x]*math.sin(2*math.pi*x/P) for x in range(3,297))
    print(Ph, round(c*c+s*s))
