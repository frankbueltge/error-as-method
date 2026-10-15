t=open('/tmp/claude-0/s128/mk/m07/scratch/template.html').read()
ink=open('/tmp/claude-0/s128/mk/m07/scratch/ink.txt').read()
open('/tmp/claude-0/s128/mk/m07/work/index.html','w').write(t.replace('@@INK@@',ink))
