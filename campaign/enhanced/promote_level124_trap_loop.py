"""Promote the reviewed level-124 second-patrol loop across live map sources."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[2]
folder=Path(__file__).resolve().parent/'anchor-trap-124-v1'
folder.mkdir(exist_ok=True)
backup=folder/'before_level_124.json'
assert not backup.exists(), 'Level 124 patrol revision already promoted'
maps_path=root/'CAMPAIGN_1000_LEVELS.json'
archive_path=root/'design/map-solutions-1000.json'
candidate_path=root/'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
maps=json.loads(maps_path.read_text(encoding='utf-8'))
archive=json.loads(archive_path.read_text(encoding='utf-8'))
candidates=json.loads(candidate_path.read_text(encoding='utf-8'))
assert len(maps)==1000 and len(archive['levels'])==1000 and len(candidates)==2000
before={'map':maps[123],'archive':archive['levels'][123],'candidate':candidates[123]}
old=[[6,14],[7,14],[7,15],[6,15]]
new=[[10,9],[11,9],[11,10],[10,10]]
assert all(item['patrol2']==old for item in [before['map'],before['archive']['map'],before['candidate']])
assert before['map']==before['archive']['map']==before['candidate']
backup.write_text(json.dumps(before,indent=2),encoding='utf-8')
for item in [maps[123],archive['levels'][123]['map'],candidates[123]]:item['patrol2']=new
archive['levels'][123]['mapFingerprint']=hashlib.sha256(json.dumps(archive['levels'][123]['map'],sort_keys=True).encode()).hexdigest()
for path,value in [(maps_path,maps),(archive_path,archive),(candidate_path,candidates)]:
    path.write_text(json.dumps(value,separators=(',',':')),encoding='utf-8')
print('Promoted level 124 second patrol; original records saved in',backup)
