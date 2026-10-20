import gzip,csv,sys,collections,datetime
f=gzip.open(sys.argv[1],'rt',encoding='utf-8',errors='replace')
r=csv.DictReader(f,delimiter='\t')
ts=[]
for row in r:
    try:t=int(row['eruption_time_epoch'])
    except:continue
    ts.append((t,row['exact'],row['ie'],row['observer']))
ts.sort()
yr=collections.Counter(datetime.datetime.utcfromtimestamp(t[0]).year for t in ts)
print(sorted(yr.items()))
ex=collections.Counter(t[1] for t in ts);print(ex)
