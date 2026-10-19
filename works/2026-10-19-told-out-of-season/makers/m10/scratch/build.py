import json, subprocess
out=subprocess.run(['python3','-I','/tmp/claude-0/s137/mk/m10/scratch/days.py','-0.8'],capture_output=True,text=True)
D=json.load(open('/tmp/claude-0/s137/mk/m10/scratch/data.json'))
pts=D['pts']; x0=D['x0']; span=(D['x1']-x0+1)/61; phase=-0.8
# per-day points with fractional in-day position
days=[[] for _ in range(61)]
for x,y in pts:
    t=(x+0.5-(x0+phase))/span
    d=min(60,max(0,int(t)))
    f=min(0.999,max(0,t-d))
    days[d].append([round(f,3),y])
data=[{'lo':round(min(y for _,y in p),1),'hi':round(max(y for _,y in p),1),'p':sorted(p)} for p in days]
tpl=open('/tmp/claude-0/s137/mk/m10/scratch/template.html').read()
open('/tmp/claude-0/s137/mk/m10/work/index.html','w').write(tpl.replace('__DATA__',json.dumps(data,separators=(',',':'))))
