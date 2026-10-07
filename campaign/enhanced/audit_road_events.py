"""Recheck every authored post-event route against the event's timing and road state."""
from pathlib import Path
import argparse, json, sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'campaign' / 'expansion'))
from build_1000 import replay, key

parser=argparse.ArgumentParser()
parser.add_argument('--base',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
args=parser.parse_args()
BASE = args.base
levels = json.loads((BASE / 'authored_levels.json').read_text(encoding='utf-8'))
records = json.loads((BASE / 'post_event_routes.json').read_text(encoding='utf-8'))
assert len(levels) == len(records) == 1000
assert [l['n'] for l in levels] == list(range(1001, 2001))
assert [r['level'] for r in records] == list(range(1001, 2001))

for l, r in zip(levels, records):
    event = l['authoredEvent']
    assert event['kind'] == 'road_close' and event['trigger'] == 'first_delivery'
    assert event['tile'] == r['tile']
    assert key(event['tile']) not in l['walls']
    assert event['tile'] != l['depot']
    assert all(event['tile'] != h['p'] for h in l['homes'])
    route = [step['p'] for step in r['route']]
    first_delivery = next(i for i, p in enumerate(route) if any(p == h['p'] for h in l['homes']))
    assert first_delivery == r['triggerStep']
    # The tile becomes a wall at the end of this delivery. Verify the whole
    # future route against that changed map, not merely the next step.
    assert all(p != event['tile'] for p in route[first_delivery+1:])
    checked = replay(l, route, l['repairRequired'])
    assert len(checked)-1 == r['steps']
    assert checked[-1]['light'] == r['finishLight']
    assert checked[-1]['mask'].bit_count() == l['required']

print('PASS: 1000 deterministic road closures; 1000 post-event routes replayed and avoid each closed tile.')
