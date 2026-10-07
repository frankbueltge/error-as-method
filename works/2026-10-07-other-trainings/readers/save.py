"""save.py <reader> <kind> <translation> <tool_uses> < answer.json -> readers/<reader>.json"""
import sys, json
r, k, t, u = sys.argv[1:5]
a = json.loads(sys.stdin.read())
json.dump({'reader': r, 'kind': k, 'translation': t, 'agent_tool_uses': int(u), 'answer': a},
          open(f'readers/{r}.json', 'w'), indent=1, ensure_ascii=False)
