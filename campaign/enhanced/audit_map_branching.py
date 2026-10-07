"""Screen source-map street branching; geometry only, not dynamic playability."""
from collections import Counter, deque
from pathlib import Path
import argparse
import csv
import json
import statistics

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--preview',type=Path,default=ROOT/'design/campaign-2000-preview/index.html')
parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'map-branching-audit.json')
args=parser.parse_args()
OUT = args.output
CSV = OUT.with_suffix('.csv')
preview = args.preview
line = next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels = json.loads(line[len('const LEVELS='):-2])

def neighbors(p):
    x,y=p
    return ((x+1,y),(x-1,y),(x,y+1),(x,y-1))

rows=[]
for level in levels:
    n=level.get('grid',8)
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    roads={(x,y) for y in range(n) for x in range(n) if (x,y) not in walls}
    depot=tuple(level['depot'])
    assert depot in roads
    reached={depot};queue=deque([depot])
    while queue:
        for p in neighbors(queue.popleft()):
            if p in roads and p not in reached:
                reached.add(p);queue.append(p)
    degrees=Counter(sum(q in reached for q in neighbors(p)) for p in reached)
    edges=sum(k*v for k,v in degrees.items())//2
    branch=degrees[3]+degrees[4]
    rows.append({'level':level['n'],'grid':n,'walkable':len(roads),
                 'depotComponent':len(reached),'branchTiles':branch,
                 'branchPercent':round(100*branch/len(reached),1),
                 'deadEnds':degrees[1],'corridorPercent':round(100*degrees[2]/len(reached),1),
                 'cycles':edges-len(reached)+1,
                 'disconnectedRoads':len(roads)-len(reached)})

bands=[]
for start in range(1,2001,100):
    segment=rows[start-1:start+99]
    bands.append({'levels':f'{start}-{start+99}',
                  'medianBranchPercent':statistics.median(r['branchPercent'] for r in segment),
                  'medianCorridorPercent':statistics.median(r['corridorPercent'] for r in segment),
                  'medianCycles':statistics.median(r['cycles'] for r in segment),
                  'underFiveBranchTiles':sum(r['branchTiles']<5 for r in segment)})
report={'scope':'Static streets reachable from depot before authored events. Ignores timed changes, shadow threat and required Light Bridges.',
        'bands':bands,'rows':rows}
OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
with CSV.open('w',newline='',encoding='utf-8-sig') as file:
    writer=csv.DictWriter(file,fieldnames=rows[0].keys())
    writer.writeheader();writer.writerows(rows)
print('Audited',len(rows),'maps; 1901–2000 median branches',bands[-1]['medianBranchPercent'],
      'percent, median cycles',bands[-1]['medianCycles'])
print('Finale fewest branches',[(r['level'],r['branchTiles'],r['cycles']) for r in sorted(rows[1900:],key=lambda r:r['branchTiles'])[:10]])
