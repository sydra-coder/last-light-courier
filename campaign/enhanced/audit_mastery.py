"""Check every mastery combination and its optional signal branch."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--candidates',type=Path,default=ROOT/'campaign/enhanced/candidates-v3')
parser.add_argument('--mastery',type=Path,default=ROOT/'campaign/enhanced/mastery-v1')
args=parser.parse_args()
levels=json.loads((args.mastery/'authored_levels.json').read_text(encoding='utf-8'))
default=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[900:1000]
baseline=json.loads((args.candidates/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))[900:1000]
proofs=json.loads((args.mastery/'route_proofs.json').read_text(encoding='utf-8'))
assert len(levels)==len(default)==len(baseline)==len(proofs)==100
counts={}
for l,d,b,p in zip(levels,default,baseline,proofs):
    assert l['n']==d['level']==b['level']==p['level']
    counts[p['archetype']]=counts.get(p['archetype'],0)+1
    records=d['route'];route=[tuple(s['p']) for s in records]
    first=d['triggerStep'];second=p['secondDeliveryStep']
    assert first==p['firstDeliveryStep']<second
    assert records[second]['mask'].bit_count()>=2 and records[second-1]['mask'].bit_count()<2
    assert tuple(l['authoredEvent']['tile']) not in route[first+1:]
    close=tuple(l['chainEvent']['close']);opened=[tuple(q) for q in l['chainEvent']['open']]
    assert l['chainEvent']['trigger']=='second_delivery' and len(opened)==1
    assert close in route[first+1:second] and close not in route[second+1:],l['n']
    assert f'{opened[0][0]},{opened[0][1]}' in l['walls'] and opened[0] not in route,l['n']
    assert route[-1]==tuple(l['depot']) and records[-1]['light']>=0
    if l.get('stormWind'):
        src=tuple(l['stormWind']['from']);dst=tuple(l['stormWind']['to'])
        assert src not in route[:first+1] and src in route[first+1:]
        assert dst not in route and sum(abs(a-b) for a,b in zip(src,dst))==1
        assert src!=close and dst!=opened[0]
    if l.get('shadowSpawner'):
        x,y=l['shadowSpawner']['origin'];zone={tuple(q) for q in l['shadowSpawner']['stages']}
        assert zone=={(x,y),(x+1,y),(x,y+1),(x+1,y+1)} and not zone.intersection(route[first+1:])
        assert all(f'{q[0]},{q[1]}' not in l['walls'] for q in zone)
        assert close not in zone and opened[0] not in zone
    if l.get('lumenNetwork'):
        relay=tuple(l['lumenNetwork']['relayTile']);source=l['homes'][l['lumenNetwork']['sourceHouseIndex']]['p']
        assert source==records[first]['p'] and relay not in route[:first+1]
        assert route[first+1:].count(relay)==1 and relay!=close
        if l.get('shadowSpawner'):assert relay not in {tuple(q) for q in l['shadowSpawner']['stages']}
    if l.get('nightfall'):
        dusk=tuple(l['nightfall']['tile']);spent=0
        assert dusk not in route[:first+1]
        for i,s in enumerate(records):
            if i>first and tuple(s['p'])==dusk:spent+=1
            remaining=s['light']-spent
            assert remaining>0 if i<len(records)-1 else remaining>=0,(l['n'],i,'light')
        assert spent<=1
    if l.get('phaseChoice'):
        signal=b['solutions'][0];sr=[tuple(s['p']) for s in signal['route']]
        sf=next(i for i,s in enumerate(signal['route']) if s['mask'])
        ss=next(i for i,s in enumerate(signal['route']) if s['mask'].bit_count()>=2)
        choice=l['phaseChoice'];cost=choice['signalLightCost']
        assert sf==first and ss==p['signalSecondDeliveryStep']
        assert tuple(choice['defaultClose'])==tuple(l['authoredEvent']['tile'])
        assert tuple(choice['alternateClose']) not in sr[sf+1:]
        assert close not in sr[ss+1:] and opened[0] not in sr
        assert all(s['light']>cost for s in signal['route'][:-1])
        assert signal['route'][-1]['light']-cost==p['signalFinishLight']>=0
        assert sr[-1]==tuple(l['depot']) and signal['steps']==p['signalSteps']
assert sorted(counts.values())==[25,25,25,25],counts
print('100 mastery maps pass combined default routes; 25 chosen-corridor maps also pass signal branch')
