"""Stage nearby, consequential road closures without removing opening choices."""
from pathlib import Path
import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('--start',type=int,required=True)
parser.add_argument('--name',required=True)
args=parser.parse_args()
assert args.start in range(1001,2001,100) and args.start!=1801

root=Path(__file__).resolve().parent
overlay=root/'house-order-screen-v1'
tiles=json.loads((overlay/'event_tiles.json').read_text())
salience=json.loads((root/'event-salience-audit.json').read_text())
branches={x['level']:x for x in json.loads((root/'late-branching-audit.json').read_text())['rows']}
targets=[x['level'] for x in salience['rows'] if args.start<=x['level']<args.start+100 and x['affectedAnyFirstHouse']==0]
changed=[];left=[];alternates=[]
for n in targets:
    result=json.loads((root/f'salient-event-search-{n}.json').read_text())
    nearby=[x for x in result['results'] if x['distanceToFirst']<=12]
    original_choices=branches[n]['firstDelivery']['forward']
    preferred=([x for x in nearby if x['firstDeliveryForward']>=original_choices]
               or [x for x in nearby if x['firstDeliveryForward']>=2] or nearby)
    if not preferred:
        left.append(n);continue
    selected=preferred[0]
    tiles[str(n)]=selected['tile'];changed.append(n)
    if selected is not nearby[0]:alternates.append({'level':n,'tile':selected['tile']})
target=overlay/f'candidate-event-tiles-salient-{args.name}.json'
target.write_text(json.dumps(tiles,indent=2))
print(json.dumps({'band':args.start,'changed':len(changed),'left':left,'alternates':alternates,'output':str(target)}))
