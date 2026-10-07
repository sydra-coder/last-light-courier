"""Promote validated 1101-1200 winding maps with road and nightfall events."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent/'long_night_candidate'
BASE=ROOT/'campaign/enhanced/candidates-v3'
ROAD=ROOT/'campaign/enhanced/road-events-v1'
NIGHT=ROOT/'campaign/enhanced/nightfall-v1'

staged_maps=json.loads((HERE/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
staged_routes=json.loads((HERE/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
old_maps=json.loads((BASE/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
old_routes=json.loads((BASE/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
assert len(staged_maps)==2000 and len(staged_routes)==1000
assert staged_maps[:1100]==old_maps[:1100] and staged_maps[1200:]==old_maps[1200:]
assert staged_routes[:100]==old_routes[:100] and staged_routes[200:]==old_routes[200:]
staged_road=json.loads((HERE/'road_events/authored_levels.json').read_text(encoding='utf-8'))
staged_proofs=json.loads((HERE/'road_events/post_event_routes.json').read_text(encoding='utf-8'))
current_road=json.loads((ROAD/'authored_levels.json').read_text(encoding='utf-8'))
current_proofs=json.loads((ROAD/'post_event_routes.json').read_text(encoding='utf-8'))
assert staged_road[:100]==current_road[:100] and staged_road[200:]==current_road[200:]
assert staged_proofs[:100]==current_proofs[:100] and staged_proofs[200:]==current_proofs[200:]
assert len(json.loads((HERE/'nightfall/authored_levels.json').read_text(encoding='utf-8')))==100

copies=[
    (HERE/'CAMPAIGN_2000_CANDIDATES.json',BASE/'CAMPAIGN_2000_CANDIDATES.json'),
    (HERE/'ROUTES_1001_2000_BASELINE.json',BASE/'ROUTES_1001_2000_BASELINE.json'),
    (HERE/'road_events/authored_levels.json',ROAD/'authored_levels.json'),
    (HERE/'road_events/post_event_routes.json',ROAD/'post_event_routes.json'),
    (HERE/'road_events/report.json',ROAD/'report.json'),
    (HERE/'nightfall/authored_levels.json',NIGHT/'authored_levels.json'),
    (HERE/'nightfall/route_proofs.json',NIGHT/'route_proofs.json'),
]
backup=HERE/'before_integration';backup.mkdir(exist_ok=True)
for source,target in copies:
    old=backup/(target.parent.name+'_'+target.name)
    if not old.exists():shutil.copy2(target,old)
for source,target in copies:shutil.copy2(source,target)
(BASE/'levels_1101_1200.json').write_text(json.dumps(staged_maps[1100:1200],separators=(',',':')),encoding='utf-8')
(BASE/'routes_1101_1200.json').write_text(json.dumps(staged_routes[100:200],separators=(',',':')),encoding='utf-8')
print('Integrated winding levels 1101-1200 with reauthored road and nightfall events')
