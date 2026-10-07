"""Place optional recharge houses that an existing patrol can extinguish.

The patrol's phase, not a random roll, determines the drain. Each selected
recharge tile is visited once on the archived reference route, and the chosen
patrol reaches its one-tile influence after that visit. Losing the recharge
does not remove an objective bit or light already carried by the courier.
"""
from pathlib import Path
from collections import Counter
import argparse,json

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'leech-houses-v1')
args=parser.parse_args()
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
entries = json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][300:400]
assert [e['level'] for e in entries] == list(range(301, 401))


def distance(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])


authored = []
proof = []
for entry in entries:
    level = entry['map']
    route = entry['solutions'][0]['route']
    first = next(i for i, s in enumerate(route) if s['mask'])
    specials = {tuple(level[k]) for k in ('depot', 'fade', 'ice', 'dark', 'switch', 'gate') if level[k]}
    specials.update(tuple(h['p']) for h in level['homes'])
    counts = Counter(tuple(s['p']) for s in route)
    candidates = []
    for i in range(first+2, min(len(route)-8, first+80)):
        p = route[i]['p']
        if tuple(p) in specials or counts[tuple(p)] != 1:
            continue
        for patrol_number, patrol, phase_key in ((1, level['patrol'], 'phase'), (2, level['patrol2'], 'phase2')):
            if not patrol or distance(p, patrol[route[i][phase_key]]) <= 1:
                continue
            later = next((j for j in range(i+1, min(len(route)-1, i+20))
                          if distance(p, patrol[route[j][phase_key]]) <= 1), None)
            if later is not None:
                candidates.append((abs(i-len(route)*.32), later-i, i, later, patrol_number, p))
    if not candidates:
        continue
    _, _, visit, drain, patrol_number, tile = min(candidates)
    item = dict(level)
    item['rechargeHouse'] = tile
    item['rechargeAmount'] = 4
    item['leechPatrol'] = patrol_number
    authored.append(item)
    proof.append({'level': level['n'], 'tile': tile, 'firstRechargeVisit': visit,
                  'firstLeechApproach': drain, 'leechPatrol': patrol_number,
                  'baseRouteSteps': entry['solutions'][0]['steps'],
                  'baseRouteFinishesWithoutRecharge': True})

assert len(authored) >= 60, len(authored)
(OUT / 'authored_levels.json').write_text(json.dumps(authored, separators=(',', ':')), encoding='utf-8')
(OUT / 'timing_proofs.json').write_text(json.dumps(proof, separators=(',', ':')), encoding='utf-8')
print(f'Authored {len(authored)} deterministic Leech recharge-house levels from 301–400.')
