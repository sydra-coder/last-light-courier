"""Verify each recorded route crosses the low road before its flood countdown."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'campaign/enhanced/floods-v1'
levels=json.loads((folder/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((folder/'route_proofs.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[:100]
assert len(levels)==len(proofs)==len(routes)==100
for level,proof,record in zip(levels,proofs,routes):
    n=level['n'];assert n==proof['level']==record['level']
    road=level['floodRoad'];tile=tuple(road['tile'])
    trigger=record['triggerStep'];cross=proof['crossStep'];flood=trigger+road['closeAfter']
    assert road['closeAfter']==4 and trigger==proof['triggerStep']
    assert trigger<cross<flood==proof['floodStep']
    assert tuple(record['route'][cross]['p'])==tile
    assert all(tuple(s['p'])!=tile for s in record['route'][flood:]),(n,flood)
    assert tile not in {tuple(level['authoredEvent']['tile']),tuple(level['stormWind']['to'])}
    assert f'{tile[0]},{tile[1]}' not in level['walls']
    assert record['route'][-1]['p']==level['depot'] and record['route'][-1]['light']>=0
print('PASS: 100 Storm March routes cross their low road before the four-move flood and avoid it afterward')
