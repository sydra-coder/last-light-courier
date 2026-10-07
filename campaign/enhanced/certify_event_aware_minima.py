"""Certify no-action minimum when a completed tour meets a relaxed road bound.

Only maps whose *sole* road-changing rule is the first-delivery closure are
eligible. The phase-aware static tour removes actor/light/timer restrictions,
so its optimum is a lower bound on runtime moves. A fully replayed route with
the same length proves an exact no-power, no-repair-action minimum.
"""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
tour=json.loads((root/'campaign/enhanced/event-aware-1401-1500-live.json').read_text())
replay=json.loads((root/'campaign/enhanced/event-aware-1401-1500-live-replay.json').read_text())
routes={x['level']:x for x in replay['completedRoutes']}
blocked_if_present=('quakeEvent','chainEvent','phaseChoice','transitLink','hiddenRoad','shadowDoor',
                    'lightBridge','lumenNetwork','dayNightCycle','convergenceEvent','oneWayTile',
                    'floodRoad','aftershock','stormWind')
certified=[];ineligible=[]
for row in tour['rows']:
    n=row['level'];completed=routes.get(n)
    if not completed:continue
    level=levels[n-1]
    reasons=[name for name in blocked_if_present if level.get(name)]
    if level.get('repairRequired'):reasons.append('repairRequired')
    if level['required']!=len(level['homes']):reasons.append('partial delivery goal')
    if level.get('authoredEvent',{}).get('kind')!='road_close' or level['authoredEvent'].get('trigger')!='first_delivery':
        reasons.append('unsupported road event')
    if reasons:
        ineligible.append({'level':n,'reasons':reasons});continue
    assert row['eventAwareSteps']==completed['steps']==len(completed['route'])-1
    assert completed['steps']<completed['referenceSteps']
    certified.append({'level':n,'exactNoPowerSteps':completed['steps'],
                      'oldReferenceSteps':completed['referenceSteps'],
                      'lowerBound':row['eventAwareSteps'],'finishLight':completed['finishLight']})
assert len(certified)==4 and not ineligible,(certified,ineligible)
output=root/'campaign/enhanced/event-aware-exact-minima-1401-1500.json'
output.write_text(json.dumps({'scope':'No-power and no optional repair action; exact because full runtime completion equals a relaxed phase-aware static tour lower bound.',
                              'certified':certified,'ineligibleCompletedTours':ineligible},indent=2))
print(json.dumps(certified))
