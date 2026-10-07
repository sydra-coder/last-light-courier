"""Check both phases of each wind-shifted roadblock against its completion route."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--storms',type=Path,default=ROOT/'campaign/enhanced/storms-v1')
args=parser.parse_args()
base=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[:100]
levels=json.loads((args.storms/'authored_levels.json').read_text(encoding='utf-8'))
assert len(levels)==len(base)==100
for level,proof in zip(levels,base):
    assert level['n']==proof['level']
    wind=level['stormWind']; src=tuple(wind['from']); dst=tuple(wind['to']); trigger=proof['triggerStep']
    route=[tuple(s['p']) for s in proof['route']]
    assert src not in route[:trigger+1],level['n']
    assert src in route[trigger+1:],level['n']
    assert dst not in route,level['n']
    assert sum(abs(a-b) for a,b in zip(src,dst))==1,level['n']
    assert f'{dst[0]},{dst[1]}' not in level['walls'],level['n']
    assert tuple(level['authoredEvent']['tile']) not in route[trigger+1:],level['n']
    assert proof['route'][-1]['p']==level['depot'] and proof['route'][-1]['light']>=0,level['n']
print('100 storm maps pass before/after blocker and closure route audit')
