"""Stage consequential default and alternate closures for the phase-choice district."""
from pathlib import Path
import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('--side',choices=['default','alternate'],required=True)
parser.add_argument('--start',type=int,choices=[1801,1901],default=1801)
parser.add_argument('--source-preview',type=Path)
parser.add_argument('--source-tiles',type=Path)
parser.add_argument('--branching',type=Path)
parser.add_argument('--keep-source',action='store_true')
args=parser.parse_args()
root=Path(__file__).resolve().parent
overlay=root/'house-order-screen-v1'
source=args.source_tiles or overlay/'event_tiles.json'
tiles=json.loads(source.read_text())
preview=args.source_preview or root.parent.parent/'design/campaign-2000-preview/index.html'
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
audit_name=('event-salience-audit.json' if args.side=='default' else
            'event-salience-phase-alternate.json' if args.start==1901 else
            'event-salience-phase-alternate-baseline.json')
salience=json.loads((root/audit_name).read_text())
branches={x['level']:x for x in json.loads((args.branching or root/'late-branching-audit.json').read_text())['rows']}
targets=[x['level'] for x in salience['rows'] if args.start<=x['level']<args.start+100 and
         levels[x['level']-1].get('phaseChoice') and x['affectedAnyFirstHouse']==0]
changed=[];left=[];alternates=[]
for n in targets:
    result=json.loads((root/f'salient-phase-{args.side}-search-{n}.json').read_text())
    nearby=[x for x in result['results'] if x['distanceToFirst']<=12]
    original_choices=branches[n]['firstDelivery']['forward']
    preferred=([x for x in nearby if x['firstDeliveryForward']>=original_choices]
               or [x for x in nearby if x['firstDeliveryForward']>=2] or nearby)
    if not preferred:
        left.append(n);continue
    selected=preferred[0]
    if args.side=='default':tiles[str(n)]=selected['tile']
    else:
        level=levels[n-1]
        assert level['phaseChoice']['defaultClose']!=selected['tile']
        tiles[str(n)]=selected['tile']
    changed.append(n)
    if selected is not nearby[0]:alternates.append({'level':n,'tile':selected['tile']})
target=overlay/f'candidate-phase-{args.start}-{args.side}-tiles.json'
if args.side=='alternate' and not args.keep_source:tiles={str(n):tiles[str(n)] for n in changed}
target.write_text(json.dumps(tiles,indent=2))
print(json.dumps({'side':args.side,'changed':len(changed),'left':left,'alternates':alternates,'output':str(target)}))
