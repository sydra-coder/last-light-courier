"""Promote audited winding Beacon maps with recoverable backups."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
archive_path = ROOT/'design/map-solutions-1000.json'
maps_path = ROOT/'CAMPAIGN_1000_LEVELS.json'
campaign_path = ROOT/'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json'
hidden_path = ROOT/'campaign/enhanced/hidden-routes-v1/authored_levels.json'
reveal_path = ROOT/'campaign/enhanced/hidden-routes-v1/reveal_proofs.json'
influence_path = ROOT/'campaign/enhanced/shadow-influence-v1/authored_levels.json'
influence_proof_path = ROOT/'campaign/enhanced/shadow-influence-v1/route_proofs.json'
candidate_archive = HERE/'map_solutions_1000_winding_201_candidate.json'
candidate_maps = HERE/'campaign_1000_winding_201_candidate.json'
candidate_hidden = HERE/'hidden_201_candidate/authored_levels.json'
candidate_reveal = HERE/'hidden_201_candidate/reveal_proofs.json'
candidate_influence = HERE/'influence_201_candidate/authored_levels.json'
candidate_influence_proof = HERE/'influence_201_candidate/route_proofs.json'

current = json.loads(archive_path.read_text(encoding='utf-8'))
staged = json.loads(candidate_archive.read_text(encoding='utf-8'))
old_maps = json.loads(maps_path.read_text(encoding='utf-8'))
new_maps = json.loads(candidate_maps.read_text(encoding='utf-8'))
hidden = json.loads(candidate_hidden.read_text(encoding='utf-8'))
reveals = json.loads(candidate_reveal.read_text(encoding='utf-8'))
influence = json.loads(candidate_influence.read_text(encoding='utf-8'))
influence_proofs = json.loads(candidate_influence_proof.read_text(encoding='utf-8'))
assert len(current['levels']) == len(staged['levels']) == len(old_maps) == len(new_maps) == 1000
assert all(staged['levels'][i] == current['levels'][i] and new_maps[i] == old_maps[i]
           for i in list(range(200)) + list(range(300, 1000)))
assert len(hidden) == len(reveals) == 100
assert len(influence) == len(influence_proofs) == 25
assert all(staged['levels'][i]['map'] == new_maps[i] for i in range(200, 300))
campaign = json.loads(campaign_path.read_text(encoding='utf-8'))
assert len(campaign) == 2000
campaign[:1000] = new_maps

backup = HERE/'before_winding_201_300'
backup.mkdir(exist_ok=True)
for source in (archive_path, maps_path, campaign_path, hidden_path, reveal_path,
               influence_path, influence_proof_path):
    target = backup/(source.parent.name + '_' + source.name)
    assert not target.exists(), f'Backup already exists: {target}'
    shutil.copy2(source, target)
for target, candidate in ((archive_path, candidate_archive), (maps_path, candidate_maps),
                          (hidden_path, candidate_hidden), (reveal_path, candidate_reveal),
                          (influence_path, candidate_influence),
                          (influence_proof_path, candidate_influence_proof)):
    target.write_bytes(candidate.read_bytes())
campaign_path.write_text(json.dumps(campaign, separators=(',', ':')), encoding='utf-8')
print('Promoted winding 201-300 maps, 100 Beacon reveals and 25 shadow fields; backups saved')
