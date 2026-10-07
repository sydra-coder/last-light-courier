"""Promote winding Sentinel/Hunter maps with recoverable backups."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
archive_path=ROOT/'design/map-solutions-1000.json'
maps_path=ROOT/'CAMPAIGN_1000_LEVELS.json'
sentinels_path=ROOT/'campaign/enhanced/sentinels-v1/authored_levels.json'
sentinel_proofs_path=ROOT/'campaign/enhanced/sentinels-v1/route_proofs.json'
hunters_path=ROOT/'campaign/enhanced/hunters-v1/authored_levels.json'
hunter_proofs_path=ROOT/'campaign/enhanced/hunters-v1/route_proofs.json'
hunter_report_path=ROOT/'campaign/enhanced/hunters-v1/report.json'
campaign_path=ROOT/'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
candidate_archive=HERE/'map_solutions_1000_winding_501_candidate.json'
candidate_maps=HERE/'campaign_1000_winding_501_candidate.json'
candidate_sentinels=HERE/'sentinels_501_candidate/authored_levels.json'
candidate_sentinel_proofs=HERE/'sentinels_501_candidate/route_proofs.json'
candidate_hunters=HERE/'hunters_501_candidate/authored_levels.json'
candidate_hunter_proofs=HERE/'hunters_501_candidate/route_proofs.json'
candidate_hunter_report=HERE/'hunters_501_candidate/report.json'

current=json.loads(archive_path.read_text(encoding='utf-8'))
staged=json.loads(candidate_archive.read_text(encoding='utf-8'))
old_maps=json.loads(maps_path.read_text(encoding='utf-8'))
new_maps=json.loads(candidate_maps.read_text(encoding='utf-8'))
sentinels=json.loads(candidate_sentinels.read_text(encoding='utf-8'))
hunters=json.loads(candidate_hunters.read_text(encoding='utf-8'))
assert len(current['levels'])==len(staged['levels'])==len(old_maps)==len(new_maps)==1000
assert all(staged['levels'][i]==current['levels'][i] and new_maps[i]==old_maps[i]
           for i in list(range(500))+list(range(600,1000)))
assert [item['n'] for item in sentinels]==list(range(501,601))
assert len(hunters)>=40 and all(501<=item['n']<=600 for item in hunters)
assert all(staged['levels'][i]['map']==new_maps[i] for i in range(500,600))
campaign=json.loads(campaign_path.read_text(encoding='utf-8'))
assert len(campaign)==2000
campaign[:1000]=new_maps

backup=HERE/'before_winding_501_600'
backup.mkdir(exist_ok=True)
for source in (archive_path,maps_path,sentinels_path,sentinel_proofs_path,
               hunters_path,hunter_proofs_path,hunter_report_path,campaign_path):
    target=backup/(source.parent.name+'_'+source.name)
    assert not target.exists(),f'Backup already exists: {target}'
    shutil.copy2(source,target)
archive_path.write_bytes(candidate_archive.read_bytes())
maps_path.write_bytes(candidate_maps.read_bytes())
sentinels_path.write_bytes(candidate_sentinels.read_bytes())
sentinel_proofs_path.write_bytes(candidate_sentinel_proofs.read_bytes())
hunters_path.write_bytes(candidate_hunters.read_bytes())
hunter_proofs_path.write_bytes(candidate_hunter_proofs.read_bytes())
hunter_report_path.write_bytes(candidate_hunter_report.read_bytes())
campaign_path.write_text(json.dumps(campaign,separators=(',',':')),encoding='utf-8')
print(f'Promoted winding 501-600 maps and {len(hunters)} Hunters; backups saved')
