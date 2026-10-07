"""Promote the 33 audited early shortcut revisions with recoverable backups."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
archive_path = ROOT/'design/map-solutions-1000.json'
maps_path = ROOT/'CAMPAIGN_1000_LEVELS.json'
campaign_path = ROOT/'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
exact_path = HERE/'shortest_routes.json'
decoy_path = ROOT/'campaign/enhanced/decoys-v1/power_proofs.json'
report_path = ROOT/'campaign/enhanced/decoys-v1/report.json'
candidate_archive = HERE/'map_solutions_1000_shortcuts_candidate.json'
candidate_maps = HERE/'campaign_1000_shortcuts_candidate.json'
candidate_exact = HERE/'shortest_routes_candidate.json'
candidate_decoy = HERE/'decoy_candidate/power_proofs.json'
candidate_report = HERE/'decoy_candidate/report.json'

current = json.loads(archive_path.read_text(encoding='utf-8'))
staged = json.loads(candidate_archive.read_text(encoding='utf-8'))
old_maps = json.loads(maps_path.read_text(encoding='utf-8'))
new_maps = json.loads(candidate_maps.read_text(encoding='utf-8'))
revisions = json.loads((HERE/'shortcut_revisions_candidate.json').read_text(encoding='utf-8'))
changed = {r['level'] for r in revisions if r['changed']}
assert len(changed) == 33
assert len(current['levels']) == len(staged['levels']) == len(old_maps) == len(new_maps) == 1000
assert all(current['levels'][i] == staged['levels'][i] and old_maps[i] == new_maps[i]
           for i in range(1000) if i+1 not in changed)
assert all(staged['levels'][i]['map'] == new_maps[i] for i in range(1000))
assert len(json.loads(candidate_exact.read_text(encoding='utf-8'))) == 100
assert len(json.loads(candidate_decoy.read_text(encoding='utf-8'))) == 50
campaign = json.loads(campaign_path.read_text(encoding='utf-8'))
assert len(campaign) == 2000
campaign[:1000] = new_maps

backup = HERE/'before_shortcut_revisions'
backup.mkdir(exist_ok=True)
sources = (archive_path,maps_path,campaign_path,exact_path,decoy_path,report_path)
for source in sources:
    target = backup/(source.parent.name+'_'+source.name)
    assert not target.exists(), f'Backup already exists: {target}'
    shutil.copy2(source,target)
for target,candidate in ((archive_path,candidate_archive),(maps_path,candidate_maps),
                         (exact_path,candidate_exact),(decoy_path,candidate_decoy),
                         (report_path,candidate_report)):
    target.write_bytes(candidate.read_bytes())
campaign_path.write_text(json.dumps(campaign,separators=(',',':')),encoding='utf-8')
print('Promoted 33 revised early maps and exact routes with backups')
