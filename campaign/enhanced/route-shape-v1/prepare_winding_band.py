"""Stage a winding 100-level band in the complete archived solution file."""
from pathlib import Path
import argparse
import hashlib
import json

parser=argparse.ArgumentParser()
parser.add_argument('start',type=int)
args=parser.parse_args()
start=args.start
assert start in range(101,901,100)
end=start+99
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
archive=json.loads((ROOT/'design'/'map-solutions-1000.json').read_text(encoding='utf-8'))
alternatives=json.loads((HERE/f'winding_{start}_{end}_candidates.json').read_text(encoding='utf-8'))
assert not alternatives['failures'] and len(alternatives['results'])==100
for entry in alternatives['results']:
    number,game_map,route=entry['level'],entry['map'],entry['route']
    archive['levels'][number-1]={
        'level':number,'mapFingerprint':hashlib.sha256(json.dumps(game_map,sort_keys=True).encode()).hexdigest(),
        'map':game_map,'solutions':[{'repairPurchased':game_map['repairRequired'],
                                    'status':'verified_reference','steps':len(route)-1,
                                    'route':route,'optimal':False}]}
assert [item['level'] for item in archive['levels']]==list(range(1,1001))
(HERE/f'map_solutions_1000_winding_{start}_candidate.json').write_text(json.dumps(archive,separators=(',',':')),encoding='utf-8')
(HERE/f'campaign_1000_winding_{start}_candidate.json').write_text(json.dumps([item['map'] for item in archive['levels']],separators=(',',':')),encoding='utf-8')
print(f'Staged {start}-{end} winding maps in a complete candidate archive')
