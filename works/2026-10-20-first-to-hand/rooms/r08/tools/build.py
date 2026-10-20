import gzip,csv,sys,collections
f=gzip.open(sys.argv[1],'rt',encoding='utf-8',errors='replace')
r=csv.DictReader(f,delimiter='\t')
ev=[]
for row in r:
    try:t=int(row['eruption_time_epoch'])
    except:continue
    try:d=int(row['duration_seconds'])
    except:d=0
    ev.append([t,row['exact']=='1',d])
ev.sort()
# merge duplicates within 15 minutes
m=[]
for e in ev:
    if m and e[0]-m[-1][0]<15*60:
        if e[1] and not m[-1][1]: m[-1][0]=e[0]; m[-1][1]=True
        if e[2] and not m[-1][2]: m[-1][2]=e[2]
        continue
    m.append(e)
print('events',len(ev),'merged',len(m))
out=open(sys.argv[2],'w')
out.write('t_min,interval_min,prev_duration_s\n')
n=0;dc=0
for a,b in zip(m,m[1:]):
    if not(a[1] and b[1]):continue
    iv=(b[0]-a[0])/60
    if iv<30 or iv>140:continue
    out.write('%d,%d,%d\n'%(a[0]//60,round(iv),a[2]));n+=1
    if a[2]:dc+=1
print('intervals',n,'with dur',dc)
