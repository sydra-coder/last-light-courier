"""Add the verified two-wall solutions for levels 144 and 150 to staging."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
target = HERE/'shortcut_revisions_candidate.json'
rows = json.loads(target.read_text(encoding='utf-8'))
choices = {144: ('11,4', '14,13'), 150: ('9,9', '15,7')}
for n, (first, second) in choices.items():
    search = json.loads((HERE/f'closure_search_{n}_after_{first.replace(",", "_")}.json').read_text(encoding='utf-8'))
    found = next(item for item in search['candidates'] if item['tile'] == second)
    assert found['status'] == 'solved' and found['longestStraight'] <= 12
    row = rows[n-101]
    assert row['level'] == n and not row['changed']
    row.update(changed=True, success=True, addedWalls=[first, second],
               after={'excess':0,'longest':found['longestStraight'],'steps':found['steps']},
               route=found['route'])
assert len(rows) == 100 and sum(bool(row['changed']) for row in rows) == 33
assert all(row.get('success', True) for row in rows)
target.write_text(json.dumps(rows), encoding='utf-8')
print('All 33 long-shortcut maps now have staged solved revisions')
