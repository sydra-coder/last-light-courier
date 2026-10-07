"""Check every sealed-road and hidden-house reveal against the archived route."""
from pathlib import Path
import argparse,json, sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'campaign' / 'expansion'))
from build_1000 import replay, key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'hidden-routes-v1')
args=parser.parse_args()
BASE = args.base
levels = json.loads((BASE / 'authored_levels.json').read_text(encoding='utf-8'))
proofs = json.loads((BASE / 'reveal_proofs.json').read_text(encoding='utf-8'))
entries = json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels) == len(proofs) == 100
assert [l['n'] for l in levels] == list(range(201,301))

for level, proof in zip(levels, proofs):
    n = level['n']
    assert n == proof['level']
    entry = entries[n-1]
    solution = entry['solutions'][0]
    route = [s['p'] for s in solution['route']]
    beacon_step = proof['beaconStep']
    hidden_step = proof['hiddenHouseStep']
    road_step = proof['hiddenRoadStep']
    assert 0 < beacon_step < road_step < hidden_step < len(route)-1
    assert proof['beaconHouseIndex'] != proof['hiddenHouseIndex']
    assert route[beacon_step] == level['homes'][level['beaconHouseIndex']]['p']
    assert route[hidden_step] == level['homes'][level['hiddenHouseIndex']]['p']
    assert route[road_step] == level['hiddenRoad']
    assert key(level['hiddenRoad']) not in level['walls']
    assert all(p != level['hiddenRoad'] for p in route[:beacon_step+1])
    assert all(p != level['homes'][level['hiddenHouseIndex']]['p'] for p in route[:beacon_step+1])
    checked = replay(level, route, solution['repairPurchased'])
    assert len(checked)-1 == proof['referenceSteps']
    assert checked[-1]['mask'].bit_count() >= level['required']

print('PASS: 100 Beacon House triggers precede every hidden road and hidden objective on verified completion routes.')
