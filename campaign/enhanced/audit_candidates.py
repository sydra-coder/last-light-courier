"""Independent completeness and route-shape audit for the 2,000 candidate map records."""
from pathlib import Path
import json,csv,statistics

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign'/'enhanced'/'candidates-v3'
maps=json.loads((OUT/'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
routes=json.loads((OUT/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
assert len(maps)==2000 and [l['n'] for l in maps]==list(range(1,2001))
assert len(routes)==1000 and [r['level'] for r in routes]==list(range(1001,2001))
original=json.loads((ROOT/'CAMPAIGN_1000_LEVELS.json').read_text(encoding='utf-8'))
assert maps[:1000]==original
from sys import path as syspath
syspath.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,metrics,reachable

def turns(points):
    directions=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    if not directions:return 0,0
    changes=sum(a!=b for a,b in zip(directions,directions[1:]))
    streak=1;longest=1
    for a,b in zip(directions,directions[1:]):
        streak=streak+1 if a==b else 1;longest=max(longest,streak)
    return changes,longest

rows=[];all_sha=set()
for l,r in zip(maps[1000:],routes):
    v=r['solutions'][0];points=[s['p'] for s in v['route']]
    replay(l,points,v['repairPurchased'])
    assert v['steps']==len(points)-1
    assert all(0<=p[0]<l['grid'] and 0<=p[1]<l['grid'] for p in points)
    assert len(l['homes'])==l['required']
    if l['repairRequired']:
        assert l['reservedFreeRepair'] and l['repair']['cost']==0
        assert reachable(l,False)<l['required'] and reachable(l,True)==l['required']
    m=metrics(l,l['repairRequired']);assert m['components']==1
    t,longest=turns(points);unique=len(set(map(tuple,points)))
    fingerprint=json.dumps([l['grid'],l['depot'],l['homes'],l['walls'],l['patrol'],l['patrol2']])
    assert fingerprint not in all_sha,(l['n'],'duplicate geometry');all_sha.add(fingerprint)
    rows.append([l['n'],l['grid'],l['required'],v['steps'],v['route'][-1]['light'],l['repairRequired'],m['junctions'],m['loops'],t,longest,unique,l['enhancedPlan']['eventFamily'],'Baseline route verified; enhanced event not integrated','Phone/visual review pending'])

with (OUT/'review_1001_2000.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f);writer.writerow(['Level','Grid','Houses','Reference steps','Finish light','Free repair required','Junctions','Loops','Route turns','Longest straight run','Unique route tiles','Planned event family','Rules status','Visual status']);writer.writerows(rows)
summary={'mapCount':len(maps),'newCandidateCount':len(rows),'first1000Preserved':True,'allNewBaselineRoutesReplayVerified':True,'enhancedEventsIntegrated':False,'powersIntegrated':False,'phoneVisualAcceptance':False,'requiredFreeRepairCount':sum(r[5] for r in rows),'routeStepsMedian':statistics.median(r[3] for r in rows),'routeTurnsMedian':statistics.median(r[8] for r in rows),'maxStraightRun':max(r[9] for r in rows),'straightRunOver12':sum(r[9]>12 for r in rows),'fewJunctionsUnder10':sum(r[6]<10 for r in rows)}
(OUT/'validation_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
