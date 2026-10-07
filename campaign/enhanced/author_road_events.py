"""Author deterministic road closures with independently replayed post-event routes.

This is an incremental event layer for levels 1001–2000. A closure occurs on the
first delivery, and the reference path is rerouted through a legal local bypass.
No random branch is used, so each authored post-event state has one exact replay.
"""
from pathlib import Path
import argparse, json, sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'campaign' / 'expansion'))
from build_1000 import replay, adjacent, key

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=ROOT / 'campaign' / 'enhanced' / 'candidates-v3')
parser.add_argument('--out', type=Path, default=ROOT / 'campaign' / 'enhanced' / 'road-events-v1')
args = parser.parse_args()
SOURCE = args.source
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)


def alternate(l, route, trigger):
    opened = {(x, y) for y in range(l['grid']) for x in range(l['grid']) if key((x, y)) not in set(l['walls'])}
    if l['repairRequired']:
        opened.add(tuple(l['repair']['tile']))
    special = {tuple(l['depot']), *(tuple(h['p']) for h in l['homes'])}
    special.update(tuple(l[name]) for name in ('fade', 'ice', 'switch', 'gate', 'dark') if l[name])
    route_tuples = list(map(tuple, route))
    for i in range(trigger + 5, len(route) - 5):
        a, b, c = route_tuples[i-1:i+2]
        if b in special or b in route_tuples[i+1:]:
            continue
        options = []
        if a[0] != c[0] and a[1] != c[1]:
            for d in ((a[0], c[1]), (c[0], a[1])):
                if d != b and d in opened and d not in special:
                    options.append([d])
        else:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                side = [tuple((p[0]+dx, p[1]+dy)) for p in (a,b,c)]
                if all(p in opened and p not in special and p != b for p in side):
                    options.append(side)
        for detour in options:
            amended = route[:i] + [list(p) for p in detour] + route[i+1:]
            if b in map(tuple, amended[trigger+1:]):
                continue
            try:
                records = replay(l, amended, l['repairRequired'])
            except AssertionError:
                continue
            return {'kind': 'road_close', 'trigger': 'first_delivery', 'tile': list(b),
                    'cue': 'The marked road closes after the first delivery. Take the side street.'}, records
    return None


def main():
    levels = json.loads((SOURCE / 'CAMPAIGN_2000_CANDIDATES.json').read_text(encoding='utf-8'))
    baselines = json.loads((SOURCE / 'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))
    authored = []
    route_records = []
    failed = []
    for l, record in zip(levels[1000:], baselines):
        points = [s['p'] for s in record['solutions'][0]['route']]
        first = next((i for i,p in enumerate(points) if any(p == h['p'] for h in l['homes'])), None)
        assert first is not None
        found = alternate(l, points, first)
        if found is None:
            failed.append(l['n'])
            continue
        event, replayed = found
        assert tuple(event['tile']) not in (tuple(s['p']) for s in replayed[first+1:])
        l = dict(l)
        l['authoredEvent'] = event
        authored.append(l)
        route_records.append({'level': l['n'], 'kind': event['kind'], 'tile': event['tile'],
                              'triggerStep': first, 'steps': len(replayed)-1,
                              'finishLight': replayed[-1]['light'], 'route': replayed})
    (OUT / 'authored_levels.json').write_text(json.dumps(authored, separators=(',', ':')), encoding='utf-8')
    (OUT / 'post_event_routes.json').write_text(json.dumps(route_records, separators=(',', ':')), encoding='utf-8')
    (OUT / 'report.json').write_text(json.dumps({'attempted': 1000, 'authored': len(authored),
                    'failed': len(failed), 'failedLevels': failed}, indent=2), encoding='utf-8')
    print(f"Authored {len(authored)} post-delivery road closures; {len(failed)} maps need another event or geometry change.")


if __name__ == '__main__':
    main()
