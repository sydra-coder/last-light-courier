"""Replay and check timing for the campaign's authored Leech house events."""
from pathlib import Path
import argparse,json, sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'campaign' / 'expansion'))
from build_1000 import replay, key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'leech-houses-v1')
args=parser.parse_args()
BASE = args.base
levels = json.loads((BASE / 'authored_levels.json').read_text(encoding='utf-8'))
proofs = json.loads((BASE / 'timing_proofs.json').read_text(encoding='utf-8'))
entries = json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels) == len(proofs) >= 60
assert [l['n'] for l in levels] == [p['level'] for p in proofs]

for level, proof in zip(levels, proofs):
    n = level['n']
    original = entries[n-1]
    assert 301 <= n <= 400
    assert key(level['rechargeHouse']) not in level['walls']
    assert all(level['rechargeHouse'] != h['p'] for h in level['homes'])
    assert level['rechargeHouse'] != level['depot']
    solution = original['solutions'][0]
    route = [s['p'] for s in solution['route']]
    visited = [i for i, p in enumerate(route) if p == level['rechargeHouse']]
    assert visited == [proof['firstRechargeVisit']]
    checked = replay(level, route, solution['repairPurchased'])
    assert len(checked)-1 == proof['baseRouteSteps']
    patrol = level['patrol'] if level['leechPatrol'] == 1 else level['patrol2']
    phase = 'phase' if level['leechPatrol'] == 1 else 'phase2'
    def near(record):
        shadow = patrol[record[phase]]
        house = level['rechargeHouse']
        return abs(shadow[0]-house[0])+abs(shadow[1]-house[1]) <= 1
    visit = proof['firstRechargeVisit']
    first_near = next(i for i in range(visit+1,len(checked)) if near(checked[i]))
    assert first_near == proof['firstLeechApproach']
    assert first_near >= visit+1
    # Recharge is optional. The baseline route succeeds even after its light is
    # extinguished, proving the deterministic drain cannot strand this route.
    assert checked[-1]['mask'].bit_count() >= level['required']

print(f'PASS: {len(levels)} Leech house placements; patrol approach timing and no-recharge completion replayed.')
