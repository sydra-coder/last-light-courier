"""Validate both selected first-delivery map states for 1801–1900."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--candidates',type=Path,default=ROOT/'campaign/enhanced/candidates-v3')
parser.add_argument('--phases',type=Path,default=ROOT/'campaign/enhanced/phase-choices-v1')
args=parser.parse_args()
levels=json.loads((args.phases/'authored_levels.json').read_text(encoding='utf-8'))
default=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[800:900]
baseline=json.loads((args.candidates/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))[800:900]
proofs=json.loads((args.phases/'route_proofs.json').read_text(encoding='utf-8'))
assert len(levels)==len(default)==len(baseline)==len(proofs)==100
for l,d,b,p in zip(levels,default,baseline,proofs):
    assert l['n']==d['level']==b['level']==p['level']
    signal=b['solutions'][0];first=p['firstDeliveryStep'];choice=l['phaseChoice']
    cost=choice['signalLightCost']
    assert cost==p['signalLightCost']==int(d['steps']>signal['steps']) and choice['defaultClose']==d['tile']
    assert choice['alternateClose']==p['alternateClosed'] and choice['alternateClose']!=choice['defaultClose']
    assert signal['repairPurchased']==bool(l.get('repairRequired'))
    assert signal['steps']==p['signalSteps'] and d['steps']==p['defaultSteps']
    assert signal['route'][first]['mask'] and not signal['route'][first-1]['mask']
    assert d['route'][first]['mask'] and not d['route'][first-1]['mask']
    assert all(s['p']!=choice['defaultClose'] for s in d['route'][first+1:]),l['n']
    assert all(s['p']!=choice['alternateClose'] for s in signal['route'][first+1:]),l['n']
    assert all(s['light']>cost for s in signal['route'][:-1]),l['n']
    assert signal['route'][-1]['light']-cost==p['signalFinishLight']>=0,l['n']
    assert d['route'][-1]['light']==p['defaultFinishLight']>=0,l['n']
    assert signal['route'][-1]['p']==d['route'][-1]['p']==l['depot']
print('100 player-selected map phases pass both route checks; shorter signals cost one light, tied routes are free')
