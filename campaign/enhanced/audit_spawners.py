"""Check expanding spawner stages against each recorded completion route."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--spawners',type=Path,default=ROOT/'campaign/enhanced/spawners-v1')
args=parser.parse_args()
levels=json.loads((args.spawners/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[200:300]
assert len(levels)==len(proofs)==100
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=proof['route'];trigger=proof['triggerStep'];spawn=level['shadowSpawner']
    cells=list(map(tuple,spawn['stages']));assert len(cells)==4 and len(set(cells))==4
    x,y=spawn['origin'];assert set(cells)=={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
    assert all(f'{p[0]},{p[1]}' not in level['walls'] for p in cells),level['n']
    assert all(tuple(s['p']) not in cells for s in route[trigger+1:]),level['n']
    assert tuple(route[trigger]['p']) not in cells,level['n']
    assert all(s['p']!=level['authoredEvent']['tile'] for s in route[trigger+1:]),level['n']
    assert route[-1]['p']==level['depot'] and route[-1]['light']>=0,level['n']
print('100 growing 2x2 spawner routes avoid all spawn stages and the closed road')
