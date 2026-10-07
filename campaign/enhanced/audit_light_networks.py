"""Check relay opening order, charge use, and road closure against routes."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--networks',type=Path,default=ROOT/'campaign/enhanced/light-networks-v1')
args=parser.parse_args()
levels=json.loads((args.networks/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[300:400]
assert len(levels)==len(proofs)==100
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    network=level['lumenNetwork'];route=proof['route'];trigger=proof['triggerStep']
    relay=network['relayTile'];source=level['homes'][network['sourceHouseIndex']]['p']
    assert route[trigger]['p']==source and route[trigger]['mask']!=0,level['n']
    assert all(s['p']!=relay for s in route[:trigger+1]),level['n']
    assert sum(s['p']==relay for s in route[trigger+1:])==1,level['n']
    assert f'{relay[0]},{relay[1]}' not in level['walls'],level['n']
    assert all(s['p']!=level['authoredEvent']['tile'] for s in route[trigger+1:]),level['n']
    assert route[-1]['p']==level['depot'] and route[-1]['light']>=0,level['n']
print('100 light-network routes unlock relay after source delivery, cross once, and avoid closed road')
