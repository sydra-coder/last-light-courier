"""Promote the replayed winding band and its earthquake overlays together."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
STAGED = HERE / 'map_solutions_1000_winding_candidate.json'
STAGED_MAPS = HERE / 'campaign_1000_winding_candidate.json'
QUAKES = HERE / 'quakes_candidate'
archive = json.loads(STAGED.read_text(encoding='utf-8'))
maps = json.loads(STAGED_MAPS.read_text(encoding='utf-8'))
events = json.loads((QUAKES / 'authored_levels.json').read_text(encoding='utf-8'))
proofs = json.loads((QUAKES / 'post_event_routes.json').read_text(encoding='utf-8'))
assert len(archive['levels']) == len(maps) == 1000
assert [x['n'] for x in events] == list(range(801, 1001))
assert [x['level'] for x in proofs] == list(range(801, 1001))
assert all(archive['levels'][n-1]['map'] == maps[n-1] for n in range(901, 1001))
assert all(events[n-801]['quakeEvent']['close'] == proofs[n-801]['closedRoad'] for n in range(901, 1001))

legacy_archive = ROOT / 'design/map-solutions-1000.json'
legacy_maps = ROOT / 'CAMPAIGN_1000_LEVELS.json'
legacy_events = ROOT / 'campaign/enhanced/quakes-v1/authored_levels.json'
legacy_proofs = ROOT / 'campaign/enhanced/quakes-v1/post_event_routes.json'
for source in (legacy_archive, legacy_maps, legacy_events, legacy_proofs):
    backup = HERE / ('before_winding_' + source.name)
    if not backup.exists():
        shutil.copy2(source, backup)

shutil.copy2(STAGED, legacy_archive)
shutil.copy2(STAGED_MAPS, legacy_maps)
shutil.copy2(QUAKES / 'authored_levels.json', legacy_events)
shutil.copy2(QUAKES / 'post_event_routes.json', legacy_proofs)
shutil.copy2(QUAKES / 'report.json', ROOT / 'campaign/enhanced/quakes-v1/report.json')

candidate_path = ROOT / 'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
campaign = json.loads(candidate_path.read_text(encoding='utf-8'))
assert len(campaign) == 2000
campaign[:1000] = maps
candidate_path.write_text(json.dumps(campaign, separators=(',', ':')), encoding='utf-8')
print('Integrated winding maps 901-1000, their earthquake events, and 2000-map source')
