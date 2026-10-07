"""Promote audited winding causeway maps with recoverable backups."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
archive_path=ROOT/'design/map-solutions-1000.json'
maps_path=ROOT/'CAMPAIGN_1000_LEVELS.json'
causeways_path=ROOT/'campaign/enhanced/causeways-v1/authored_levels.json'
proofs_path=ROOT/'campaign/enhanced/causeways-v1/route_proofs.json'
campaign_path=ROOT/'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
candidate_archive=HERE/'map_solutions_1000_winding_401_candidate.json'
candidate_maps=HERE/'campaign_1000_winding_401_candidate.json'
candidate_causeways=HERE/'causeways_401_candidate/authored_levels.json'
candidate_proofs=HERE/'causeways_401_candidate/route_proofs.json'

current=json.loads(archive_path.read_text(encoding='utf-8'))
staged=json.loads(candidate_archive.read_text(encoding='utf-8'))
old_maps=json.loads(maps_path.read_text(encoding='utf-8'))
new_maps=json.loads(candidate_maps.read_text(encoding='utf-8'))
causeways=json.loads(candidate_causeways.read_text(encoding='utf-8'))
proofs=json.loads(candidate_proofs.read_text(encoding='utf-8'))
assert len(current['levels'])==len(staged['levels'])==len(old_maps)==len(new_maps)==1000
assert all(staged['levels'][i]==current['levels'][i] and new_maps[i]==old_maps[i]
           for i in list(range(400))+list(range(500,1000)))
assert [item['n'] for item in causeways]==[item['level'] for item in proofs]==list(range(401,501))
assert all(staged['levels'][i]['map']==new_maps[i] for i in range(400,500))
campaign=json.loads(campaign_path.read_text(encoding='utf-8'))
assert len(campaign)==2000
campaign[:1000]=new_maps

backup=HERE/'before_winding_401_500'
backup.mkdir(exist_ok=True)
for source in (archive_path,maps_path,causeways_path,proofs_path,campaign_path):
    target=backup/(source.parent.name+'_'+source.name)
    assert not target.exists(),f'Backup already exists: {target}'
    shutil.copy2(source,target)
archive_path.write_bytes(candidate_archive.read_bytes())
maps_path.write_bytes(candidate_maps.read_bytes())
causeways_path.write_bytes(candidate_causeways.read_bytes())
proofs_path.write_bytes(candidate_proofs.read_bytes())
campaign_path.write_text(json.dumps(campaign,separators=(',',':')),encoding='utf-8')
print('Promoted winding 401-500 maps and causeway proofs; backups saved')
