"""Measure route and delivery-order repetition in the current playable 201–2000 maps."""
from pathlib import Path
from collections import Counter
from itertools import groupby
import json,statistics

here=Path(__file__).resolve().parent
routes=json.loads((here/'reference-hints-v1/normalized_routes.json').read_text(encoding='utf-8'))
assert len(routes)==1800 and all(route for route in routes)

def directions(route):
    return tuple((b[0]-a[0],b[1]-a[1]) for a,b in zip(route,route[1:]))

def house_order(route):
    order=[];last=route[0][2]
    for point in route[1:]:
        new=point[2]&~last
        if new:
            order.extend(i for i in range(32) if new&(1<<i))
        last=point[2]
    return tuple(order)

rows=[]
for n,route in enumerate(routes,201):
    moves=directions(route)
    runs=[len(list(g)) for _,g in groupby(moves)]
    rows.append({'level':n,'steps':len(moves),'turns':len(runs)-1,
                 'longestStraight':max(runs),'houseOrder':house_order(route),
                 'directions':moves})

bands=[]
for start in range(201,2001,100):
    group=[r for r in rows if start<=r['level']<start+100]
    orders=[r['houseOrder'] for r in group]
    patterns=[r['directions'] for r in group]
    consecutive=max(len(list(g)) for _,g in groupby(orders))
    bands.append({'levels':[start,start+99],
                  'steps':{'min':min(r['steps'] for r in group),'median':statistics.median(r['steps'] for r in group),'max':max(r['steps'] for r in group)},
                  'distinctDirectionRoutes':len(set(patterns)),
                  'distinctHouseOrders':len(set(orders)),
                  'maxConsecutiveSameHouseOrder':consecutive,
                  'longestStraight':max(r['longestStraight'] for r in group)})
report={'scope':'Current normalized playable default routes for levels 201–2000. Direction and house-order variety describe these references, not every legal or optimal player route.',
        'routes':len(rows),'uniqueDirectionRoutes':len({r['directions'] for r in rows}),
        'uniqueHouseOrders':len({r['houseOrder'] for r in rows}),
        'bands':bands,
        'longStraightOutliers':[{'level':r['level'],'steps':r['steps'],'longestStraight':r['longestStraight']} for r in rows if r['longestStraight']>12],
        'lowOrderVarietyBands':[b['levels'] for b in bands if b['distinctHouseOrders']<10]}
(here/'route-variety-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ('routes','uniqueDirectionRoutes','uniqueHouseOrders','lowOrderVarietyBands')}))
