"""Author Beacon House reveals for levels 201–300 against archived routes."""
from pathlib import Path
from collections import Counter
import argparse,json

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'hidden-routes-v1')
args=parser.parse_args()
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
entries = json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][200:300]
assert [e['level'] for e in entries] == list(range(201, 301))

authored, proofs = [], []
for entry in entries:
    level = entry['map']
    route = entry['solutions'][0]['route']
    deliveries = []
    previous = 0
    for i, state in enumerate(route):
        gained = state['mask'] & ~previous
        if gained:
            deliveries.append((i, gained.bit_length()-1))
        previous = state['mask']
    assert len(deliveries) >= 3, level['n']
    beacon_step, beacon_index = deliveries[1]
    specials = {tuple(level[k]) for k in ('depot', 'fade', 'ice', 'dark', 'switch', 'gate') if level[k]}
    if level.get('repair'):
        specials.add(tuple(level['repair']['tile']))
    specials.update(tuple(h['p']) for h in level['homes'])
    counts = Counter(tuple(s['p']) for s in route)
    selected = None
    for hidden_step, hidden_index in deliveries[2:]:
        for road_step in range(beacon_step+1, hidden_step):
            tile = tuple(route[road_step]['p'])
            if tile in specials or counts[tile] != 1:
                continue
            if any(tuple(s['p']) == tile for s in route[:beacon_step+1]):
                continue
            selected = (hidden_step, hidden_index, road_step, list(tile))
            break
        if selected:
            break
    assert selected is not None, level['n']
    hidden_step, hidden_index, road_step, road_tile = selected
    item = dict(level)
    item['homes'] = [dict(h) for h in level['homes']]
    item['homes'][beacon_index]['name'] = 'Beacon ' + item['homes'][beacon_index]['name']
    item['beaconHouseIndex'] = beacon_index
    item['hiddenHouseIndex'] = hidden_index
    item['hiddenRoad'] = road_tile
    item['brief'] = level['brief'] + ' Light the Beacon House to reveal a hidden delivery and open its road.'
    authored.append(item)
    proofs.append({'level': level['n'], 'beaconHouseIndex': beacon_index,
                   'beaconStep': beacon_step, 'hiddenHouseIndex': hidden_index,
                   'hiddenHouseStep': hidden_step, 'hiddenRoad': road_tile,
                   'hiddenRoadStep': road_step,
                   'referenceSteps': entry['solutions'][0]['steps']})

assert len(authored) == len(proofs) == 100
(OUT / 'authored_levels.json').write_text(json.dumps(authored, separators=(',', ':')), encoding='utf-8')
(OUT / 'reveal_proofs.json').write_text(json.dumps(proofs, separators=(',', ':')), encoding='utf-8')
print('Authored 100 Beacon House reveals and sealed roads for levels 201–300.')
