import json
core=json.load(open('core.json'));hv=json.load(open('hourly.json'))
tpl=open('tpl.html').read()
html=tpl.replace('__CORE__',json.dumps(core,separators=(',\n',':'))).replace('__HV__',json.dumps(hv,separators=(',',':')))
open('/tmp/claude-0/s135/mk/m06/work/index.html','w').write(html)
