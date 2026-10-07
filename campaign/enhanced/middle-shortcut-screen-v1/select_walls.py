"""Find one non-reference street wall shared by each proven direct completion."""
from collections import defaultdict
from pathlib import Path
import json
import os

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
routes=defaultdict(list)
for band in (301,401,501,601):
    for order in ('ENWS','WSEN','NESW','SWNE'):
        prefix=os.environ.get('LLC_MIDDLE_SCREEN_PREFIX','')
        source=json.loads((HERE/f'{prefix}static-{band}-{order}.json' if not prefix else HERE/f'{prefix}{band}-{order}.json').read_text(encoding='utf-8'))['rows']
        replay=json.loads((HERE/f'{prefix}replay-{band}-{order}.json' if not prefix else HERE/f'{prefix}replay-{band}-{order}.json').read_text(encoding='utf-8'))
        completed={item['level'] for item in replay['completedRoutes']}
        for item in source:
            if item['level'] in completed:routes[item['level']].append(item['staticCandidateRoute'])
chosen={};missing=[]
for n,attempts in sorted(routes.items()):
    l=levels[n-1];reference={tuple(step['p']) for step in archive[n-1]['solutions'][0]['route']}
    common=set.intersection(*(set(map(tuple,route))-reference for route in attempts))
    protected={tuple(l['depot'])}|{tuple(h['p']) for h in l['homes']}|set(map(tuple,l.get('patrol',[])))|set(map(tuple,l.get('patrol2',[])))
    for feature in ('fade','ice','dark','switch','gate','oneWayTile','collapseTile','sentinelCenter','shadowDoor','shadowLock','lightBridge','hiddenRoad'):
        if l.get(feature):protected.add(tuple(l[feature]))
    if l.get('repair'):protected.add(tuple(l['repair']['tile']))
    common-=protected
    existing=json.loads((HERE/'candidate_walls.json').read_text(encoding='utf-8')) if os.environ.get('LLC_MIDDLE_SCREEN_PREFIX') else {}
    common-={tuple(map(int,tile.split(','))) for tile in existing.get(str(n),[])}
    if not common:missing.append(n);continue
    # Prefer a tile used once by the shortcut and far from the depot.
    cell=max(common,key=lambda p:(sum(route.count(list(p)) for route in attempts),abs(p[0]-l['depot'][0])+abs(p[1]-l['depot'][1])))
    chosen[str(n)]=[f'{cell[0]},{cell[1]}']

output=HERE/('second_walls.json' if os.environ.get('LLC_MIDDLE_SCREEN_PREFIX') else 'candidate_walls.json')
output.write_text(json.dumps(chosen,separators=(',',':')),encoding='utf-8')
print(f'Found one-cell blockers for {len(chosen)}/{len(routes)} maps; unresolved {missing}')
print(chosen)
