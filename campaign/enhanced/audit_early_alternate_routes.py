"""Summarize full-rule replays of optimistic early alternate routes."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parents[1]
line=next(x for x in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if x.startswith('const LEVELS='))
levels=json.loads(line[13:-2])
references=json.loads((here/'reference-hints-v1/normalized_routes.json').read_text(encoding='utf-8'))
revisions={x['level']:x for x in json.loads((here/'early-route-rebalance-v1/revisions.json').read_text(encoding='utf-8'))}
rows=[]
for n in range(201,801):
    path=here/f'early-nonbacktracking-{n}-replay.json'
    if not path.exists():continue
    proof=json.loads(path.read_text(encoding='utf-8'))
    if not proof.get('completed'):continue
    reference=references[n-201]
    order=[];mask=reference[0][2]
    for point in reference[1:]:
        new=point[2]&~mask
        order.extend(i for i in range(32) if new&(1<<i))
        mask=point[2]
    old=revisions.get(n)
    baseline_steps=old['oldRouteSteps'] if old else len(reference)-1
    baseline_order=old['oldRouteOrder'] if old else order
    old_cap=old['oldCap'] if old else levels[n-1]['cap']
    old_finish=old_cap-old['newCap']+old['expectedFinishLight'] if old else proof['finishLight']
    rows.append({'level':n,'referenceSteps':baseline_steps,'alternateSteps':proof['steps'],
                 'stepsSaved':baseline_steps-proof['steps'],
                 'referenceOrder':baseline_order,'alternateOrder':proof['staticOrder'],
                 'orderChanged':baseline_order!=proof['staticOrder'],'alternateFinishLight':old_finish,
                 'lanternCap':old_cap})
report={'scope':'Historical pre-rebalance audit of levels 201–800 against previous reference routes and lantern caps. The 91 verified alternatives were later promoted; not a current-cap report or minimum proof.',
        'completed':len(rows),'changedOrder':sum(x['orderChanged'] for x in rows),
        'allRows':rows}
(here/'early-alternate-route-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'completed':report['completed'],'changedOrder':report['changedOrder'],
                  'savedRange':[min(x['stepsSaved'] for x in rows),max(x['stepsSaved'] for x in rows)],
                  'finishLightRange':[min(x['alternateFinishLight'] for x in rows),max(x['alternateFinishLight'] for x in rows)]}))
