"""Check first and second delivery road states against every route."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--chains',type=Path,default=ROOT/'campaign/enhanced/chain-events-v1')
args=parser.parse_args()
levels=json.loads((args.chains/'authored_levels.json').read_text(encoding='utf-8'))
base=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[600:700]
proofs=json.loads((args.chains/'route_proofs.json').read_text(encoding='utf-8'))
assert len(levels)==len(base)==len(proofs)==100
for l,routeproof,proof in zip(levels,base,proofs):
    assert l['n']==routeproof['level']==proof['level']
    records=routeproof['route'];route=[s['p'] for s in records]
    first=next(i for i,s in enumerate(records) if s['mask'])
    second=next(i for i,s in enumerate(records) if s['mask'].bit_count()>=2)
    assert first==proof['firstDeliveryStep'] and second==proof['secondDeliveryStep'] and first<second
    closed=l['chainEvent']['close'];opened=l['chainEvent']['open']
    assert len(opened)==1 and l['chainEvent']['trigger']=='second_delivery'
    assert closed in route[first+1:second] and closed not in route[second+1:],l['n']
    assert opened[0] not in route and f'{opened[0][0]},{opened[0][1]}' in l['walls'],l['n']
    assert route[second] not in (closed,opened[0])
    assert l['authoredEvent']['tile'] not in route[first+1:],l['n']
    assert route[-1]==l['depot'] and records[-1]['light']>=0,l['n']
print('100 chained maps pass first/second-delivery timing and completion-route checks')
