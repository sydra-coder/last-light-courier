"""Enumerate shortest static tour tie-breaks for two changed closures."""
from pathlib import Path
from itertools import permutations
import os,subprocess,sys,json

here=Path(__file__).resolve().parent
output=here/'salient-tiebreaks'
output.mkdir(exist_ok=True)
counts={}
targets=tuple(int(x) for x in os.environ.get('LLC_TIEBREAK_LEVELS','1485,1698').split(','))
for n in targets:
    routes={}
    for chars in permutations('EWSN'):
        order=''.join(chars);target=output/f'{n}-{order}.json'
        subprocess.run([sys.executable,str(here/'audit_event_aware_tours.py'),'--start',str(n),'--end',str(n),
                        '--neighbor-order',order,'--output',str(target)],check=True,capture_output=True,text=True,
                       env=os.environ.copy())
        row=json.loads(target.read_text())['rows'][0]
        routes[order]=row['staticCandidateRoute']
    counts[n]={'orders':len(routes),'uniqueRoutes':len({str(route) for route in routes.values()})}
print(json.dumps(counts))
