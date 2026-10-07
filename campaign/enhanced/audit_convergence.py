"""Check each two-system combination against its post-closure route."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--convergence',type=Path,default=ROOT/'campaign/enhanced/convergence-v1')
args=parser.parse_args()
levels=json.loads((args.convergence/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[500:600]
assert len(levels)==len(proofs)==100
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=proof['route'];trigger=proof['triggerStep']
    before=[tuple(s['p']) for s in route[:trigger+1]]
    after=[tuple(s['p']) for s in route[trigger+1:]]
    assert route[trigger]['mask'] and route[-1]['p']==level['depot'] and route[-1]['light']>=0
    assert tuple(level['authoredEvent']['tile']) not in after,level['n']
    if level['n']<=1550:
        assert level.get('stormWind') and level.get('nightfall')
        src=tuple(level['stormWind']['from']);dst=tuple(level['stormWind']['to'])
        dusk=tuple(level['nightfall']['tile'])
        assert src not in before and src in after and dst not in before+after,level['n']
        assert sum(abs(a-b) for a,b in zip(src,dst))==1
        assert dusk not in before and dusk not in (src,dst),level['n']
        spent=0
        for i,s in enumerate(route):
            if i>trigger and tuple(s['p'])==dusk:spent+=1
            remaining=s['light']-spent
            assert remaining>0 if i<len(route)-1 else remaining>=0,(level['n'],i)
        assert spent<=1,level['n']
    else:
        assert level.get('shadowSpawner') and level.get('lumenNetwork')
        x,y=level['shadowSpawner']['origin'];zone={tuple(p) for p in level['shadowSpawner']['stages']}
        assert zone=={(x,y),(x+1,y),(x,y+1),(x+1,y+1)},level['n']
        assert all(f'{p[0]},{p[1]}' not in level['walls'] for p in zone)
        assert not zone.intersection(after),level['n']
        source=level['homes'][level['lumenNetwork']['sourceHouseIndex']]['p']
        relay=tuple(level['lumenNetwork']['relayTile'])
        assert source==route[trigger]['p'] and relay not in before and after.count(relay)==1,level['n']
        assert relay not in zone and f'{relay[0]},{relay[1]}' not in level['walls']
print('100 Convergence maps pass combined event, route, and light checks')
