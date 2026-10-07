"""Add tested express stops to the two staged short walking routes."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
stage=here/'transit-walk-rebalance-v1'
search=json.loads((stage/'new-stop-search.json').read_text())
routes=json.loads((stage/'route_overrides.json').read_text())
stops=json.loads((here/'transit-v1/express_stop_overlays.json').read_text())
proofs={}
for item in search:
    n=item['level'];best=item['best'][0]
    assert best['finishLight']>=12 and best['steps']<best['walkingSteps']
    i,j=best['boardAtStep'],best['exitAtOldStep']
    route=routes[str(n)]
    new_route=route[:i+1]+route[j:]
    assert len(new_route)-1==best['steps']
    stops[str(n)]=best['stops']
    proofs[str(n)]={'level':n,'route':new_route,'transitSteps':best['steps'],
                    'transitFinishLight':best['finishLight'],'walkingSteps':best['walkingSteps'],
                    'boardAtStep':i,'exitAtOldStep':j,'stops':best['stops']}
(stage/'express_stop_overlays.json').write_text(json.dumps(stops,indent=2))
(stage/'transit_route_overrides.json').write_text(json.dumps(proofs,indent=2))
print(json.dumps([{'level':x['level'],'steps':x['transitSteps'],'light':x['transitFinishLight']} for x in proofs.values()]))
