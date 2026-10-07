"""Rank current completion routes by long straight segments for visual revision."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'campaign/enhanced/route-shape-v1';OUT.mkdir(parents=True,exist_ok=True)
legacy=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
opening=json.loads((ROOT/'campaign/enhanced/opening-v1/shortest_routes.json').read_text(encoding='utf-8'))
quakes=json.loads((ROOT/'campaign/enhanced/quakes-v1/post_event_routes.json').read_text(encoding='utf-8'))
later=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))
bridge_spur_path=ROOT/'campaign/enhanced/bridge-spurs-v1/routes.json'
bridge_spurs=json.loads(bridge_spur_path.read_text(encoding='utf-8')) if bridge_spur_path.exists() else {}
rows=[]
for n in range(1,2001):
    if n<=50:
        route=[s['p'] for s in opening[n-1]['route']]
        source='opening shortest'
    elif str(n) in bridge_spurs:
        route=bridge_spurs[str(n)]
        source='bridge house reference'
    elif n<=800:
        route=[s['p'] for s in legacy[n-1]['solutions'][0]['route']]
        source='early shortest' if n<=100 else 'trap/decoy reference' if n<=200 else 'Beacon reference' if n<=300 else 'Leech reference' if n<=400 else 'causeway reference' if n<=500 else 'Hunter/Sentinel reference' if n<=600 else 'door reference' if n<=700 else 'bridge reference'
    elif n<=1000:
        route=[s['p'] for s in quakes[n-801]['route']]
        source='post-quake reference'
    else:
        route=[s['p'] for s in later[n-1001]['route']]
        source='post-event reference'
    directions=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(route,route[1:])]
    best=0;length=0;start=0;best_start=0
    for i,d in enumerate(directions):
        if i and d==directions[i-1]:length+=1
        else:length=1;start=i
        if length>best:best=length;best_start=start
    rows.append({'level':n,'steps':len(route)-1,'longestStraight':best,
                 'straightStartStep':best_start,'straightEndStep':best_start+best,
                 'startTile':route[best_start],'endTile':route[best_start+best],
                 'source':source})
rows.sort(key=lambda x:(-x['longestStraight'],-x['steps'],x['level']))
with (OUT/'route_shape_priority.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'audited':len(rows),'straightOver12':sum(r['longestStraight']>12 for r in rows),
         'opening1to100Over12':sum(r['longestStraight']>12 and r['level']<=100 for r in rows),
         'trapDecoy101to200Over12':sum(r['longestStraight']>12 and 101<=r['level']<=200 for r in rows),
         'beacon201to300Over12':sum(r['longestStraight']>12 and 201<=r['level']<=300 for r in rows),
         'leech301to400Over12':sum(r['longestStraight']>12 and 301<=r['level']<=400 for r in rows),
         'causeway401to500Over12':sum(r['longestStraight']>12 and 401<=r['level']<=500 for r in rows),
         'hunter501to600Over12':sum(r['longestStraight']>12 and 501<=r['level']<=600 for r in rows),
         'door601to700Over12':sum(r['longestStraight']>12 and 601<=r['level']<=700 for r in rows),
         'bridge701to800Over12':sum(r['longestStraight']>12 and 701<=r['level']<=800 for r in rows),
         'quake801to1000Over12':sum(r['longestStraight']>12 and r['level']<=1000 for r in rows),
         'maxStraight':rows[0]['longestStraight'],'top20Levels':[r['level'] for r in rows[:20]]}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(summary)
