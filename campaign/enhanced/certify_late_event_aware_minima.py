"""Certify exact no-power/no-action steps when a live replay meets a relaxed road bound.

The static tour allows every road except the authored/chain closures and base
walls, so shadows, timers, lantern, sealed relays, moving blockers and one-way
restrictions can only make the real route longer. Transit and hidden openings
are excluded because they could make a static lower bound too high.
"""
from pathlib import Path
import json, os, subprocess, sys

root=Path(__file__).resolve().parents[2]
here=Path(__file__).resolve().parent
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
balance_path=os.environ.get('LLC_LANTERN_AUDIT_INPUT')
balance={row['level']:row for row in json.loads(Path(balance_path).read_text())['rows'] if row['branch']=='default'} if balance_path else {}
queue={row['level']:row for row in json.loads((here/'event-aware-unresolved-shortcuts.json').read_text())['rows']}
extra_path=here/'salient-two-exact-routes.json'
extra={row['level']:row for row in json.loads(extra_path.read_text())} if extra_path.exists() else {}
targets=[1414,1483,1485,1487,1508,1540,1549,1551,1610,1612,1626,1641,1672,1680,1694,1698,1807,1828,1873,1940,1980,1994]
screens=here/'exact-late-minima-v1'/'screens'
screens.mkdir(parents=True,exist_ok=True)
certified=[]
overrides=json.loads((here/'reference-hints-v1/route_overrides.json').read_text())
for n in targets:
    level=levels[n-1]
    assert level['n']==n and level['required']==len(level['homes'])
    assert level.get('authoredEvent',{}).get('kind')=='road_close' and level['authoredEvent'].get('trigger')=='first_delivery'
    assert not any(level.get(k) for k in ('transitLink','hiddenRoad','lightBridge','repairRequired','networkCircuitRequired'))
    assert n in queue and queue[n]['defaultSteps'] is not None
    output=screens/f'{n}.json'
    subprocess.run([sys.executable,str(here/'audit_event_aware_tours.py'),'--start',str(n),'--end',str(n),'--output',str(output)],check=True,capture_output=True,text=True)
    row=json.loads(output.read_text())['rows'][0]
    steps=extra[n]['steps'] if n in extra else queue[n]['defaultSteps']
    assert row['eventAwareSteps']==steps,(n,row['eventAwareSteps'],steps)
    if n in extra:
        assert extra[n]['lowerBound']==steps and len(extra[n]['route'])-1==steps
        route=extra[n]['route']
        old_reference=queue[n]['recordedDefaultSteps']
        finish_light=extra[n]['finishLight']
    else:
        band=(n-1)//100*100+1
        replay=json.loads((here/f'event-aware-{band}-{band+99}-replay.json').read_text())
        completed=next(x for x in replay['completedRoutes'] if x['level']==n and x['steps']==steps)
        assert completed['completed'] and len(completed['route'])-1==steps
        route=completed['route']
        old_reference=completed['referenceSteps']
        finish_light=completed['finishLight']
    if balance and n not in extra:
        assert balance[n]['steps']==steps
        finish_light=balance[n]['finishLight']
    overrides[str(n)]=route
    certified.append({'level':n,'exactNoPowerSteps':steps,'oldReferenceSteps':old_reference,
                      'lowerBound':steps,'finishLight':finish_light,
                      'proof':'live replay equals fresh phase-aware static tour bound'})
out=Path(os.environ.get('LLC_EXACT_CERT_OUTPUT',here/'event-aware-exact-minima-late.json'))
out.write_text(json.dumps({'scope':'Exact no-power, no optional repair, no signal step minima. Full runtime completions were rechecked by the event-aware shortcut audit and equal freshly generated relaxed phase-aware static tour lower bounds. Excludes transit, hidden-road openings, mandatory repair and powered bridge maps.','certified':certified},indent=2))
Path(os.environ.get('LLC_EXACT_OVERRIDE_OUTPUT',here/'exact-late-minima-v1'/'route_overrides.json')).write_text(json.dumps(overrides))
print(json.dumps({'certified':len(certified),'levels':[x['level'] for x in certified]}))
