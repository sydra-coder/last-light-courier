"""Stage winding Storm March maps without changing the integrated campaign."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'campaign' / 'enhanced'))
from build_candidates import candidate

parser=argparse.ArgumentParser()
parser.add_argument('--start',type=int,default=1001)
parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'storm_march_candidate')
args=parser.parse_args()
assert args.start in range(1001,2001,100)
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
maps, routes, attempts = [], [], []
for number in range(args.start, args.start+100):
    game_map, record, attempt = candidate(number)
    maps.append(game_map)
    routes.append(record)
    attempts.append(attempt)
    if number % 20 == 0:
        print('Built through', number, flush=True)

base = json.loads((ROOT / 'campaign/enhanced/candidates-v3/CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
baseline_routes = json.loads((ROOT / 'campaign/enhanced/candidates-v3/ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
offset=args.start-1001
base[args.start-1:args.start+99] = maps
baseline_routes[offset:offset+100] = routes
(OUT / 'CAMPAIGN_2000_CANDIDATES.json').write_text(json.dumps(base, separators=(',', ':')), encoding='utf-8')
(OUT / 'ROUTES_1001_2000_BASELINE.json').write_text(json.dumps(baseline_routes, separators=(',', ':')), encoding='utf-8')
print({'staged': len(maps), 'maxRetries': max(attempts), 'maps': str(OUT)})
