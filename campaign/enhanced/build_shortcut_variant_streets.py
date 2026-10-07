"""Stage branching street revisions from alternate static-tour completions."""
from pathlib import Path
import argparse
import json

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'campaign/enhanced'
parser=argparse.ArgumentParser()
parser.add_argument('--label',required=True)
parser.add_argument('--start',type=int,required=True)
parser.add_argument('--end',type=int,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--strict-levels',type=int,nargs='*',default=[])
args=parser.parse_args()
line=next(x for x in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs={x['level']:x for x in json.loads((BASE/'road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))}
signal={x['level']:x for x in json.loads((BASE/'candidates-v3/ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))}
targets=sorted({x['level'] for order in ('ENWS','WSEN','NESW','SWNE')
                for x in json.loads((BASE/f'shortcut-variants/{args.label}-replay-{order}.json').read_text(encoding='utf-8'))['completedRoutes']})
assert all(args.start<=n<=args.end for n in targets)

def coordinates(value):
    if isinstance(value,list):
        if len(value)==2 and all(isinstance(x,int) and not isinstance(x,bool) for x in value):yield tuple(value)
        else:
            for item in value:yield from coordinates(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            if key!='walls':yield from coordinates(item)

out={}
for n in targets:
    level=levels[n-1]
    route=[tuple(step['p']) for step in proofs[n]['route']]
    safe=set(route);safe.update(coordinates(level))
    if level.get('phaseChoice'):
        safe.update(tuple(step['p']) for step in signal[n]['solutions'][0]['route'])
    existing=set(level['walls']);index={p:i for i,p in enumerate(route)}
    if n not in args.strict_levels:
        for y in range(level['grid']):
            for x in range(level['grid']):
                p=(x,y)
                if p in safe or f'{x},{y}' in existing:continue
                near=[index[q] for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if q in index]
                if len(near)>=2 and max(near)-min(near)<=8:safe.add(p)
    out[str(n)]=[f'{x},{y}' for y in range(level['grid']) for x in range(level['grid'])
                 if (x,y) not in safe and f'{x},{y}' not in existing]
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(out,separators=(',',':')),encoding='utf-8')
print(args.label,'candidate maps',len(out),'added wall range',min(map(len,out.values())),max(map(len,out.values())))
