"""Promote one staged 100-level winding band and its dependent event overlay."""
from pathlib import Path
import argparse
import json
import shutil

ROOT=Path(__file__).resolve().parents[3]
parser=argparse.ArgumentParser()
parser.add_argument('--start',type=int,required=True)
parser.add_argument('--staged',type=Path,required=True)
parser.add_argument('--overlay',required=True)
args=parser.parse_args()
assert args.start in range(1001,2001,100)
assert args.overlay in {'spawners','light_networks','arsenal','convergence','chain_events','transit','phase_choices','mastery'}
HERE=args.staged
BASE=ROOT/'campaign/enhanced/candidates-v3'
ROAD=ROOT/'campaign/enhanced/road-events-v1'
overlay_dest={'spawners':'spawners-v1','light_networks':'light-networks-v1',
              'arsenal':'arsenal-v1','convergence':'convergence-v1',
              'chain_events':'chain-events-v1','transit':'transit-v1',
              'phase_choices':'phase-choices-v1','mastery':'mastery-v1'}[args.overlay]
SPECIAL=ROOT/'campaign/enhanced'/overlay_dest
offset=args.start-1001

new_maps=json.loads((HERE/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
new_routes=json.loads((HERE/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
old_maps=json.loads((BASE/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
old_routes=json.loads((BASE/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
assert len(new_maps)==len(old_maps)==2000 and len(new_routes)==len(old_routes)==1000
assert new_maps[:args.start-1]==old_maps[:args.start-1]
assert new_maps[args.start+99:]==old_maps[args.start+99:]
assert new_routes[:offset]==old_routes[:offset]
assert new_routes[offset+100:]==old_routes[offset+100:]
new_road=json.loads((HERE/'road_events/authored_levels.json').read_text(encoding='utf-8'))
new_proofs=json.loads((HERE/'road_events/post_event_routes.json').read_text(encoding='utf-8'))
old_road=json.loads((ROAD/'authored_levels.json').read_text(encoding='utf-8'))
old_proofs=json.loads((ROAD/'post_event_routes.json').read_text(encoding='utf-8'))
assert new_road[:offset]==old_road[:offset] and new_road[offset+100:]==old_road[offset+100:]
assert new_proofs[:offset]==old_proofs[:offset] and new_proofs[offset+100:]==old_proofs[offset+100:]
if args.overlay=='arsenal':
    assert [x['level'] for x in json.loads((HERE/args.overlay/'power_proofs.json').read_text(encoding='utf-8'))]==list(range(args.start,args.start+100))
else:
    assert [x['n'] for x in json.loads((HERE/args.overlay/'authored_levels.json').read_text(encoding='utf-8'))]==list(range(args.start,args.start+100))

copies=[
 (HERE/'CAMPAIGN_2000_CANDIDATES.json',BASE/'CAMPAIGN_2000_CANDIDATES.json'),
 (HERE/'ROUTES_1001_2000_BASELINE.json',BASE/'ROUTES_1001_2000_BASELINE.json'),
 (HERE/'road_events/authored_levels.json',ROAD/'authored_levels.json'),
 (HERE/'road_events/post_event_routes.json',ROAD/'post_event_routes.json'),
 (HERE/'road_events/report.json',ROAD/'report.json'),
]
if args.overlay=='arsenal':
    copies.append((HERE/args.overlay/'power_proofs.json',SPECIAL/'power_proofs.json'))
else:
    copies.extend([(HERE/args.overlay/'authored_levels.json',SPECIAL/'authored_levels.json'),
                   (HERE/args.overlay/'route_proofs.json',SPECIAL/'route_proofs.json')])
report=HERE/args.overlay/'report.json'
if report.exists():copies.append((report,SPECIAL/'report.json'))
backup=HERE/'before_integration';backup.mkdir(exist_ok=True)
for source,target in copies:
    old=backup/(target.parent.name+'_'+target.name)
    if not old.exists():shutil.copy2(target,old)
for source,target in copies:shutil.copy2(source,target)
end=args.start+99
(BASE/f'levels_{args.start}_{end}.json').write_text(json.dumps(new_maps[args.start-1:end],separators=(',',':')),encoding='utf-8')
(BASE/f'routes_{args.start}_{end}.json').write_text(json.dumps(new_routes[offset:offset+100],separators=(',',':')),encoding='utf-8')
print(f'Integrated winding levels {args.start}-{end} with road and {args.overlay} events')
