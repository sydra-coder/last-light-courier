"""Validate the route's exact light series with its nightfall surcharge."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--nightfall',type=Path,default=ROOT/'campaign/enhanced/nightfall-v1')
args=parser.parse_args()
levels=json.loads((args.nightfall/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[100:200]
assert len(levels)==len(proofs)==100
paid_count=0
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=proof['route'];trigger=proof['triggerStep'];tile=level['nightfall']['tile']
    assert all(s['p']!=tile for s in route[:trigger+1]),level['n']
    surcharge=0
    for i,s in enumerate(route):
        if i>trigger and s['p']==tile:
            surcharge+=1
        assert s['light']-surcharge>0 if i<len(route)-1 else s['light']-surcharge>=0,(level['n'],i)
        if i>trigger:assert s['p']!=level['authoredEvent']['tile'],level['n']
    assert surcharge<=1,level['n']
    paid_count+=bool(surcharge)
    assert route[-1]['p']==level['depot'] and route[-1]['light']-surcharge>=0,level['n']
print(f'100 nightfall routes complete with fog; {paid_count} pay dusk surcharge, {100-paid_count} avoid optional dusk road')
