"""Check that the early Anchor Trap loadout has reachable placement positions."""
from pathlib import Path
import json
import argparse

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--maps',type=Path,default=ROOT/'CAMPAIGN_1000_LEVELS.json')
args=parser.parse_args()
levels = json.loads(args.maps.read_text(encoding='utf-8'))[100:200]
assert [l['n'] for l in levels] == list(range(101, 201))
counts = []
for l in levels:
    targets = l['patrol'] + (l['patrol2'] or [])
    open_targets = [p for p in targets if ','.join(map(str,p)) not in l['walls']]
    count = sum(any(0 < abs(p[0]-q[0])+abs(p[1]-q[1]) <= 2 for q in open_targets)
                for p in l['spine'])
    assert count > 0, l['n']
    counts.append(count)
print(f'PASS: 100/100 early levels have trap targets near the reference route; minimum candidate positions: {min(counts)}')
