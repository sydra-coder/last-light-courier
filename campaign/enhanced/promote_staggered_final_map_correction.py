"""Keep level 2000 a full gauntlet after staggered-finale authoring."""
from pathlib import Path
import json
import shutil

root=Path(__file__).resolve().parents[2]
here=Path(__file__).resolve().parent
stage=here/'mastery-staggered-candidate'
live=here/'mastery-v1'
hint=here/'reference-hints-v1/normalized_routes.json'
preview=root/'design/campaign-2000-preview/index.html'
backup=stage/'before-final-map-correction'
assert not backup.exists(), 'Final-map correction already promoted'
levels=json.loads((stage/'authored_levels.json').read_text(encoding='utf-8'))
report=json.loads((stage/'report.json').read_text(encoding='utf-8'))
replays=json.loads((stage/'integrated-preview-replay.json').read_text(encoding='utf-8'))
signals=json.loads((stage/'integrated-preview-signal-branches.json').read_text(encoding='utf-8'))
powers=json.loads((stage/'late-assigned-power-route-audit.json').read_text(encoding='utf-8'))
assert len(levels)==100 and levels[-1]['n']==2000 and levels[-1]['masteryArchetype']=='Last light gauntlet'
assert report['staggered'] and report['maxConsecutiveArchetype']<=5
assert sorted(report['archetypes'].values())==[25,25,25,25]
assert replays['passed']==1000 and replays['failed']==0
assert signals['passed']==125 and signals['failed']==0
assert powers['passed']==1000 and powers['failed']==0
assert len(json.loads((stage/'normalized_routes.json').read_text(encoding='utf-8')))==1800
backup.mkdir()
for source in (live/'authored_levels.json',live/'route_proofs.json',live/'report.json',hint,preview):
    shutil.copy2(source,backup/(source.parent.name+'_'+source.name))
for name in ('authored_levels.json','route_proofs.json','report.json'):
    shutil.copy2(stage/name,live/name)
shutil.copy2(stage/'normalized_routes.json',hint)
print('Promoted final-map correction; level 2000 is Last light gauntlet')
