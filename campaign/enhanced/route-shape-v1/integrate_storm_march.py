"""Promote validated winding Storm March maps with road and wind events."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent/'storm_march_candidate'
BASE=ROOT/'campaign/enhanced/candidates-v3'
ROAD=ROOT/'campaign/enhanced/road-events-v1'
STORM=ROOT/'campaign/enhanced/storms-v1'

staged_maps=json.loads((HERE/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
staged_routes=json.loads((HERE/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
old_maps=json.loads((BASE/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
old_routes=json.loads((BASE/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
assert len(staged_maps)==2000 and len(staged_routes)==1000
assert staged_maps[:1000]==old_maps[:1000] and staged_maps[1100:]==old_maps[1100:]
assert staged_routes[100:]==old_routes[100:]
staged_road=json.loads((HERE/'road_events/authored_levels.json').read_text(encoding='utf-8'))
staged_proofs=json.loads((HERE/'road_events/post_event_routes.json').read_text(encoding='utf-8'))
assert staged_road[100:]==json.loads((ROAD/'authored_levels.json').read_text(encoding='utf-8'))[100:]
assert staged_proofs[100:]==json.loads((ROAD/'post_event_routes.json').read_text(encoding='utf-8'))[100:]
assert len(json.loads((HERE/'storms/authored_levels.json').read_text(encoding='utf-8')))==100

copies=[
    (HERE/'CAMPAIGN_2000_CANDIDATES.json',BASE/'CAMPAIGN_2000_CANDIDATES.json'),
    (HERE/'ROUTES_1001_2000_BASELINE.json',BASE/'ROUTES_1001_2000_BASELINE.json'),
    (HERE/'road_events/authored_levels.json',ROAD/'authored_levels.json'),
    (HERE/'road_events/post_event_routes.json',ROAD/'post_event_routes.json'),
    (HERE/'road_events/report.json',ROAD/'report.json'),
    (HERE/'storms/authored_levels.json',STORM/'authored_levels.json'),
    (HERE/'storms/route_proofs.json',STORM/'route_proofs.json'),
    (HERE/'storms/report.json',STORM/'report.json'),
]
backup=HERE/'before_integration'
backup.mkdir(exist_ok=True)
for source,target in copies:
    old=backup/(target.parent.name+'_'+target.name)
    if not old.exists():shutil.copy2(target,old)
for source,target in copies:shutil.copy2(source,target)
(BASE/'levels_1001_1100.json').write_text(json.dumps(staged_maps[1000:1100],separators=(',',':')),encoding='utf-8')
(BASE/'routes_1001_1100.json').write_text(json.dumps(staged_routes[:100],separators=(',',':')),encoding='utf-8')
print('Integrated winding levels 1001-1100 with reauthored road and wind events')
