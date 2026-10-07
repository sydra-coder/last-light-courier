"""Recheck 801–1000 earthquake transformations and post-event completion."""
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'quakes-v1')
args=parser.parse_args()
BASE=args.base
levels=json.loads((BASE/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((BASE/'post_event_routes.json').read_text(encoding='utf-8'))
original=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==len(proofs)==200
assert [l['n'] for l in levels]==list(range(801,1001))
opened=0
for l,proof in zip(levels,proofs):
    n=l['n'];assert proof['level']==n
    event=l['quakeEvent']
    assert event['trigger']=='first_delivery'
    assert event['close']==proof['closedRoad'] and event['open']==proof['openedRoads']
    route=[s['p'] for s in proof['route']]
    trigger=next(i for i,s in enumerate(proof['route']) if s['mask'])
    assert trigger==proof['triggerStep']
    assert event['close'] not in route[trigger+1:]
    assert key(event['close']) not in l['walls']
    for tile in event['open']:
        assert key(tile) in l['walls']
        assert tile not in route[:trigger+1]
        assert tile in route[trigger+1:]
    if event['open']:opened+=1
    after=dict(l)
    after['walls']=[w for w in l['walls'] if w not in {key(p) for p in event['open']}]
    sol=original[n-1]['solutions'][0]
    checked=replay(after,route,sol['repairPurchased'])
    assert len(checked)-1==proof['postEventSteps']
    assert checked[-1]['light']==proof['finishLight']
    assert checked[-1]['mask'].bit_count()>=l['required']
print(f'PASS: 200 earthquake completion routes avoid the closed road; {opened} use newly opened roads.')
