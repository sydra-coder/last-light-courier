"""Stage one wall per proven bridge-free detour, preserving powered references."""
from pathlib import Path
from collections import defaultdict
import json

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
routes=defaultdict(list)
for tours_name,replay_name in [('bridge_detour_tours.json','bridge_detour_rule_replay.json'),('alternate_detour_tours.json','alternate_detour_rule_replay.json')]:
    tours=json.loads((HERE/tours_name).read_text(encoding='utf-8'))
    replay=json.loads((HERE/replay_name).read_text(encoding='utf-8'))['rows']
    for tour,result in zip(tours,replay):
        if result['completed']:routes[tour['level']].append(tour['route'])
chosen={}
for n,attempts in sorted(routes.items()):
    l=levels[n-1];reference={tuple(s['p']) for s in archive[n-1]['solutions'][0]['route']}
    common=set.intersection(*(set(map(tuple,route))-reference for route in attempts))
    protected={tuple(l['depot']),tuple(l['lightBridge'])}|{tuple(h['p']) for h in l['homes']}|set(map(tuple,l.get('patrol',[])))|set(map(tuple,l.get('patrol2',[])))
    for feature in ('fade','ice','dark','switch','gate'):
        if l.get(feature):protected.add(tuple(l[feature]))
    if l.get('repair'):protected.add(tuple(l['repair']['tile']))
    common-=protected
    assert common,(n,'no safe common tile')
    bridge=l['lightBridge']
    cell=min(common,key=lambda p:(abs(p[0]-bridge[0])+abs(p[1]-bridge[1]),p))
    chosen[str(n)]=[f'{cell[0]},{cell[1]}']

(HERE/'candidate_detour_walls.json').write_text(json.dumps(chosen,separators=(',',':')),encoding='utf-8')
print(f'Staged {len(chosen)} single-cell walls')
print(chosen)
