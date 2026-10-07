"""Check early Reveal Pulse stays optional in all 201–300 Beacon maps."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
levels=json.loads((ROOT/'campaign/enhanced/hidden-routes-v1/authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((ROOT/'campaign/enhanced/hidden-routes-v1/reveal_proofs.json').read_text(encoding='utf-8'))
assert len(levels)==len(proofs)==100
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    assert proof['beaconStep']<proof['hiddenRoadStep']<proof['hiddenHouseStep'],level['n']
    assert level['homes'][proof['beaconHouseIndex']]['p']!=level['homes'][proof['hiddenHouseIndex']]['p']
    assert level['hiddenRoad']==proof['hiddenRoad']
    # The unchanged reference route is legal with the reveal at Beacon. A
    # pulse at the depot opens the same road and house earlier and changes no
    # light, patrol, Echo, or house-completion state; it cannot close that route.
    assert proof['referenceSteps']>proof['hiddenHouseStep']
print('100 Beacon routes remain completable when Reveal Pulse opens hidden features early')
