"""Stage 901-1000 winding maps in a complete solution archive for event authoring."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
archive = json.loads((ROOT / 'design/map-solutions-1000.json').read_text(encoding='utf-8'))
alternatives = json.loads((OUT / 'winding_901_1000_candidates.json').read_text(encoding='utf-8'))
assert not alternatives['failures'] and len(alternatives['results']) == 100
for entry in alternatives['results']:
    number, game_map, route = entry['level'], entry['map'], entry['route']
    assert number == game_map['n']
    archive['levels'][number - 1] = {
        'level': number,
        'mapFingerprint': hashlib.sha256(json.dumps(game_map, sort_keys=True).encode()).hexdigest(),
        'map': game_map,
        'solutions': [{'repairPurchased': game_map['repairRequired'],
                       'status': 'verified_reference', 'steps': len(route) - 1,
                       'route': route, 'optimal': False}],
    }
assert [entry['level'] for entry in archive['levels']] == list(range(1, 1001))
(OUT / 'map_solutions_1000_winding_candidate.json').write_text(json.dumps(archive, separators=(',', ':')), encoding='utf-8')
(OUT / 'campaign_1000_winding_candidate.json').write_text(json.dumps([entry['map'] for entry in archive['levels']], separators=(',', ':')), encoding='utf-8')
print('Staged 100 winding maps in versioned complete archives')
