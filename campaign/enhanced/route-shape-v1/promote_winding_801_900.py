"""Promote audited winding 801-900 maps and quake events with recoverable backups."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
archive_path=ROOT/'design'/'map-solutions-1000.json'
maps_path=ROOT/'CAMPAIGN_1000_LEVELS.json'
events_path=ROOT/'campaign/enhanced/quakes-v1/authored_levels.json'
proofs_path=ROOT/'campaign/enhanced/quakes-v1/post_event_routes.json'
report_path=ROOT/'campaign/enhanced/quakes-v1/report.json'
campaign_path=ROOT/'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
staged_archive=HERE/'map_solutions_1000_winding_801_candidate.json'
staged_maps=HERE/'campaign_1000_winding_801_candidate.json'
staged_events=HERE/'quakes_801_candidate/authored_levels.json'
staged_proofs=HERE/'quakes_801_candidate/post_event_routes.json'
staged_report=HERE/'quakes_801_candidate/report.json'

current=json.loads(archive_path.read_text(encoding='utf-8'))
candidate=json.loads(staged_archive.read_text(encoding='utf-8'))
current_maps=json.loads(maps_path.read_text(encoding='utf-8'))
candidate_maps=json.loads(staged_maps.read_text(encoding='utf-8'))
current_events=json.loads(events_path.read_text(encoding='utf-8'))
candidate_events=json.loads(staged_events.read_text(encoding='utf-8'))
current_proofs=json.loads(proofs_path.read_text(encoding='utf-8'))
candidate_proofs=json.loads(staged_proofs.read_text(encoding='utf-8'))
assert len(current['levels'])==len(candidate['levels'])==len(current_maps)==len(candidate_maps)==1000
assert all(candidate['levels'][i]==current['levels'][i] and candidate_maps[i]==current_maps[i]
           for i in list(range(800))+list(range(900,1000)))
assert current_events[100:]==candidate_events[100:] and current_proofs[100:]==candidate_proofs[100:]
assert all(candidate['levels'][i]['map']==candidate_maps[i] for i in range(800,900))
assert all(candidate_events[i-800]['n']==i+1 and candidate_proofs[i-800]['level']==i+1
           for i in range(800,900))

backup=HERE/'before_winding_801_900'
backup.mkdir(exist_ok=True)
for source in (archive_path,maps_path,events_path,proofs_path,report_path,campaign_path):
    target=backup/source.name
    assert not target.exists(),f'Backup already exists: {target}'
    shutil.copy2(source,target)
campaign=json.loads(campaign_path.read_text(encoding='utf-8'))
assert len(campaign)==2000
campaign[:1000]=candidate_maps
archive_path.write_bytes(staged_archive.read_bytes())
maps_path.write_bytes(staged_maps.read_bytes())
events_path.write_bytes(staged_events.read_bytes())
proofs_path.write_bytes(staged_proofs.read_bytes())
report_path.write_bytes(staged_report.read_bytes())
campaign_path.write_text(json.dumps(campaign,separators=(',',':')),encoding='utf-8')
print('Promoted winding 801-900 maps, quake events, and route proofs; backups saved')
