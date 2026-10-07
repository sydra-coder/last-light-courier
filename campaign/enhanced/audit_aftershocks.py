"""Check both quake closures along the late Quake Frontier routes."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'campaign/enhanced/aftershocks-v1'
levels=json.loads((folder/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((folder/'route_proofs.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/quakes-v1/post_event_routes.json').read_text(encoding='utf-8'))[150:]
assert len(levels)==len(proofs)==len(routes)==50
for level,proof,record in zip(levels,proofs,routes):
    n=level['n'];assert n==proof['level']==record['level']
    trigger=record['triggerStep'];tile=tuple(level['aftershock']['tile'])
    assert trigger==proof['triggerStep'] and level['aftershock']['closeAfter']==8
    assert trigger<proof['crossStep']<proof['closeStep']==trigger+8
    assert tuple(record['route'][proof['crossStep']]['p'])==tile
    assert all(tuple(s['p'])!=tile for s in record['route'][proof['closeStep']:]),n
    first=tuple(level['quakeEvent']['close'])
    assert all(tuple(s['p'])!=first for s in record['route'][trigger+1:]),n
    opened={tuple(p) for p in level['quakeEvent']['open']}
    assert opened and all(any(tuple(s['p'])==p for s in record['route'][trigger+1:]) for p in opened)
    assert tile!=first and tile not in opened and f'{tile[0]},{tile[1]}' not in level['walls']
    assert record['route'][-1]['p']==level['depot'] and record['route'][-1]['light']>=0
print('PASS: 50 late Quake Frontier routes use the low road before aftershock, avoid both closures, and finish')
