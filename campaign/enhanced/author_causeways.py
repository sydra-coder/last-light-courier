"""Author one-way or single-use road tiles for Broken Causeways 401–500."""
from pathlib import Path
from collections import Counter
import argparse,json

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'causeways-v1')
args=parser.parse_args()
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
entries = json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][400:500]
assert [e['level'] for e in entries] == list(range(401,501))

authored, proofs = [], []
for entry in entries:
    l = entry['map']
    route = [s['p'] for s in entry['solutions'][0]['route']]
    counts = Counter(map(tuple, route))
    special = {tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l[k]}
    special.update(tuple(h['p']) for h in l['homes'])
    if l.get('repair'):
        special.add(tuple(l['repair']['tile']))
    walls = set(l['walls'])
    candidates = []
    for i in range(6,len(route)-6):
        p = route[i]
        if tuple(p) in special or counts[tuple(p)] != 1:
            continue
        degree = sum(0<=p[0]+dx<l['grid'] and 0<=p[1]+dy<l['grid']
                     and f'{p[0]+dx},{p[1]+dy}' not in walls
                     for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
        if degree >= 3:
            candidates.append((abs(i-len(route)*.55),-degree,i,p))
    assert candidates, l['n']
    _, degree, index, tile = min(candidates)
    item = dict(l)
    if l['n'] % 2:
        item['oneWayTile'] = tile
        item['oneWayFrom'] = route[index-1]
        item['brief'] = l['brief'] + ' The arrow road only allows entry from its marked side.'
        kind = 'one_way'
    else:
        item['collapseTile'] = tile
        item['brief'] = l['brief'] + ' The marked road collapses after you leave it.'
        kind = 'collapse'
    authored.append(item)
    proofs.append({'level':l['n'],'kind':kind,'tile':tile,'referenceStep':index,
                   'entryFrom':route[index-1], 'routeSteps':entry['solutions'][0]['steps'],
                   'openNeighborCount':-degree})

assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
print('Authored 50 one-way roads and 50 collapsing roads in levels 401–500.')
