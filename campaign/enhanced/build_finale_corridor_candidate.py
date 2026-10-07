"""Stage tighter finale streets around proven routes; do not promote directly."""
from pathlib import Path
import argparse
import json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--max-branch-gap',type=int,default=0)
parser.add_argument('--buffer',type=int,default=0)
parser.add_argument('--output',type=Path,default=ROOT/'campaign/enhanced/finale-corridor-v1/candidate_walls.json')
args=parser.parse_args()
line=next(x for x in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs={x['level']:x for x in json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))}
out={}
for n in (1905,1910,1916,1926):
    level=levels[n-1]
    safe={tuple(step['p']) for step in proofs[n]['route']}
    safe.update(map(tuple,level['patrol']))
    safe.update(map(tuple,level.get('patrol2',[])))
    safe.update([tuple(level['depot']),tuple(level['repair']['tile']),tuple(level['authoredEvent']['tile']),tuple(level['chainEvent']['close'])])
    safe.update(map(tuple,level['chainEvent']['open']))
    safe.update(tuple(home['p']) for home in level['homes'])
    if level.get('shadowSpawner'):
        safe.update(map(tuple,level['shadowSpawner']['stages']))
    if level.get('lumenNetwork'):
        safe.add(tuple(level['lumenNetwork']['relayTile']))
    existing=set(level['walls'])
    if args.buffer:
        route_tiles={tuple(step['p']) for step in proofs[n]['route']}
        for y in range(level['grid']):
            for x in range(level['grid']):
                if f'{x},{y}' not in existing and min(abs(x-rx)+abs(y-ry) for rx,ry in route_tiles)<=args.buffer:
                    safe.add((x,y))
    if args.max_branch_gap:
        route_index={tuple(step['p']):i for i,step in enumerate(proofs[n]['route'])}
        for y in range(level['grid']):
            for x in range(level['grid']):
                p=(x,y)
                if p in safe or f'{x},{y}' in existing:continue
                indices=[route_index[q] for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if q in route_index]
                if len(indices)>=2 and max(indices)-min(indices)<=args.max_branch_gap:
                    safe.add(p)
    added=[f'{x},{y}' for y in range(level['grid']) for x in range(level['grid'])
           if (x,y) not in safe and f'{x},{y}' not in existing]
    out[str(n)]=added
    print(n,'added walls',len(added),'retained open',level['grid']**2-len(existing)-len(added))
target=args.output
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(json.dumps(out,separators=(',',':')),encoding='utf-8')
