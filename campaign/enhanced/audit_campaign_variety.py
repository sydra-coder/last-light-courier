"""Audit integrated preview geometry and grid-size pacing, not route optimality."""
from collections import Counter, defaultdict
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
PREVIEW=ROOT/'design'/'campaign-2000-preview'/'index.html'
line=next(line for line in PREVIEW.read_text(encoding='utf-8').splitlines() if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-1])
assert len(levels)==2000 and [level['n'] for level in levels]==list(range(1,2001))
fingerprints=defaultdict(list)
bands=[]
for level in levels:
    fingerprint=(level.get('grid',8),tuple(sorted(level['walls'])))
    fingerprints[fingerprint].append(level['n'])
for start in range(1,2001,100):
    maps=levels[start-1:start+99]
    bands.append({'levels':[start,start+99],
                  'gridSizes':dict(sorted(Counter(level.get('grid',8) for level in maps).items())),
                  'houseRange':[min(len(level['homes']) for level in maps),max(len(level['homes']) for level in maps)],
                  'uniqueWallLayouts':len({(level.get('grid',8),tuple(sorted(level['walls']))) for level in maps})})
duplicates=[ids for ids in fingerprints.values() if len(ids)>1]
assert not duplicates, f'Repeated wall layouts: {duplicates[:5]}'
assert levels[999]['grid']>levels[1000]['grid'], 'Expected a size step down after level 1000'
assert len({level.get('grid',8) for level in levels[1000:]})>=3, 'Later maps lack size variation'
report={'levels':len(levels),'uniqueWallLayouts':len(fingerprints),'duplicateWallLayouts':duplicates,
        'gridBeforeAndAfter1000':[levels[999]['grid'],levels[1000]['grid']],
        'bands':bands,
        'limits':'Unique wall layouts and grid pacing only; this does not prove distinct optimal routes or visual quality.'}
out=ROOT/'campaign'/'enhanced'/'campaign-variety-audit.json'
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(f'PASS: {len(levels)} maps, {len(fingerprints)} unique wall layouts, grid {levels[999]["grid"]} to {levels[1000]["grid"]} at level 1001')
