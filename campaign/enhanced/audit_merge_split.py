"""Replay deterministic shadow merge and split occupancy against reference routes."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
folder = ROOT / 'campaign/enhanced/merge-split-v1'
levels = json.loads((folder / 'authored_levels.json').read_text(encoding='utf-8'))
proofs = json.loads((folder / 'route_proofs.json').read_text(encoding='utf-8'))
routes = {p['level']: p for p in json.loads(
    (ROOT / 'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))}
assert len(levels) == len(proofs) >= 20
assert len({l['n'] for l in levels}) == len(levels)
for level, record in zip(levels, proofs):
    n = level['n']
    assert 1201 <= n <= 1300 and n == record['level']
    route = routes[n]
    assert record['triggerStep'] == route['triggerStep']
    x, y = level['shadowSpawner']['origin']
    spawner = {(x, y), (x+1, y), (x, y+1), (x+1, y+1)}
    config = level['mergeSplit']
    merged = {tuple(p) for p in config['mergedCells']}
    split = {tuple(p) for p in config['splitCells']}
    assert len(merged) == 9 and len(split) == 2 and spawner <= merged and split <= merged
    assert config['mergeAfter'] == 9 and config['splitAfter'] == 13
    assert all(f'{a},{b}' not in level['walls'] for a, b in merged)
    for step_index, step in enumerate(route['route']):
        age = step_index - route['triggerStep']
        if age < 0:
            occupied = set()
        elif age < 3:
            occupied = {tuple(level['shadowSpawner']['stages'][0])}
        elif age < 6:
            occupied = {tuple(p) for p in level['shadowSpawner']['stages'][:2]}
        elif age < 9:
            occupied = spawner
        elif age < 13:
            occupied = merged
        else:
            occupied = split
        assert tuple(step['p']) not in occupied, (n, step_index, age)
    assert route['route'][-1]['p'] == level['depot']
    assert route['route'][-1]['light'] >= 0
print(f'PASS: {len(levels)} merge/split routes replay all five occupancy phases')
