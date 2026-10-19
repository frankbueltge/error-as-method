import json
vals=json.load(open('vals.json'))
# light 3-point smoothing to soften tracing jitter
sm=[vals[0]]+[round((vals[i-1]+2*vals[i]+vals[i+1])/4,3) for i in range(1,len(vals)-1)]+[vals[-1]]
data=','.join(('%.3f'%v).lstrip('0') for v in sm)
html=open('template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s137/mk/m14/work/index.html','w').write(html)
print(len(html))
