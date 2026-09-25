"""Build the 100 standalone campaign boards from the approved level briefs."""
import json
import random
import re
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plan = (ROOT / 'LEVELS_001_100_AND_REPAIRS.md').read_text(encoding='utf-8')
briefs = {}
for line in plan.splitlines():
    match = re.match(r'^\| (\d{1,3}) \| (.*?) \| (.*?) \|$', line)
    if match:
        number = int(match.group(1))
        if 1 <= number <= 100:
            briefs[number] = (match.group(2), match.group(3))
assert set(briefs) == set(range(1, 101))


def ring(x0, y0, x1, y1):
    points = []
    points += [[x, y0] for x in range(x0, x1 + 1)]
    points += [[x1, y] for y in range(y0 + 1, y1 + 1)]
    points += [[x, y1] for x in range(x1 - 1, x0 - 1, -1)]
    points += [[x0, y] for y in range(y1 - 1, y0, -1)]
    return points


def key(p):
    return f'{p[0]},{p[1]}'


def neighbors(p):
    x, y = p
    return [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]


def price(number, band):
    if number == 3:
        return 150  # Let the first repair teach the action after two deliveries.
    progress = number - 1
    base = 200 + 40 * progress + 2 * progress * progress
    return round(base * {'S': 1, 'R': 1.6, 'M': 2.2}[band] / 25) * 25


def shortest_full(depot, homes, walls):
    goals = {key(p): i for i, p in enumerate(homes)}
    queue = deque([(depot, 0, 0)])
    seen = {(key(depot), 0)}
    while queue:
        p, mask, steps = queue.popleft()
        if mask == 7 and p == depot:
            return steps
        for q in neighbors(p):
            qk = key(q)
            if not (0 <= q[0] < 8 and 0 <= q[1] < 8) or qk in walls:
                continue
            nextmask = mask | (1 << goals[qk]) if qk in goals else mask
            state = (qk, nextmask)
            if state not in seen:
                seen.add(state)
                queue.append((q, nextmask, steps + 1))
    return None


levels = []
seen_layouts = set()
for number in range(1, 101):
    rng = random.Random(0x5A17 + number * 1709)
    chapter = (number - 1) // 10 + 1
    brief, repair_text = briefs[number]
    # Alternating orientations make the depot and objective order vary visibly.
    if re.search(r'\([SRM]\)', repair_text) and not any(word in repair_text.lower() for word in ('lamp', 'beacon', 'latch')):
        x0, y0 = 1, 1
        x1, y1 = 6, 6
    elif chapter <= 2:
        x0, y0 = 1, 1
        x1, y1 = 6, 6
    elif chapter <= 6:
        x0, y0 = rng.choice([0, 1]), rng.choice([0, 1])
        x1, y1 = rng.choice([6, 7]), rng.choice([6, 7])
    else:
        x0, y0 = rng.choice([0, 0, 1]), rng.choice([0, 0, 1])
        x1, y1 = rng.choice([7, 7, 6]), rng.choice([7, 7, 6])
    path = ring(x0, y0, x1, y1)
    offset = rng.randrange(len(path))
    path = path[offset:] + path[:offset]
    if number % 2 == 0:
        path = [path[0]] + path[:0:-1]
    length = len(path)
    picks = [2, 5, 8] if number <= 5 else [round(length * fraction) for fraction in (0.19, 0.48, 0.73)]
    picks = sorted(set(picks))
    assert len(picks) == 3 and picks[0] >= 2 and picks[-1] < length - 2
    depot = path[0]
    homes = [path[i] for i in picks]
    spine = path + [depot]
    keep = {key(p) for p in path}

    # Every board has its own wall pattern; the complete outer loop stays open.
    candidates = [[x, y] for y in range(8) for x in range(8) if key([x, y]) not in keep]
    rng.shuffle(candidates)
    wall_count = number + 1 if number <= 5 else 8 + min(7, chapter // 2) + number % 4
    walls = {key(p) for p in candidates[:wall_count]}

    repair = None
    band_match = re.search(r'\(([SRM])\)', repair_text)
    if band_match:
        band = band_match.group(1)
        # Prefer a blocked tile joining two otherwise open roads inside the loop.
        choices = []
        for p in candidates:
            k = key(p)
            if k not in walls:
                continue
            accessible = [q for q in neighbors(p) if 0 <= q[0] < 8 and 0 <= q[1] < 8 and key(q) not in walls]
            if len(accessible) >= 2:
                score = len(accessible) + sum(key(q) in keep for q in accessible) * 2
                choices.append((score, p))
        if not choices:
            # A marker on an off-spine tile can always be opened safely.
            p = candidates[0]
            walls.add(key(p))
        else:
            top = max(score for score, _ in choices)
            p = rng.choice([p for score, p in choices if score == top])
        repair = {'tile': p, 'name': repair_text.rsplit('(', 1)[0].strip(),
                  'band': band, 'cost': price(number, band)}

    occupied_features = {key(depot), *(key(p) for p in homes)}
    def feature_near(fraction):
        target = round(length * fraction)
        choices = sorted(range(length), key=lambda i: (abs(i - target), i))
        tile = next(path[i] for i in choices if key(path[i]) not in occupied_features)
        occupied_features.add(key(tile))
        return tile

    fade = feature_near(.32) if chapter >= 2 else None
    dark = feature_near(.57) if (chapter >= 3 and (number % 3 != 0 or number == 81)) or (repair and 'lamp' in repair['name'].lower()) else None
    switch = feature_near(.25) if chapter >= 4 and (number % 2 == 0 or number == 31) else None
    gate = feature_near(.34) if switch else None
    ice = feature_near(.64) if chapter >= 6 and number % 2 == 1 else None
    echo = chapter >= 5 and number % 2 == 1
    second = chapter >= 7 and (number % 3 != 1 or number == 61)
    if repair:
        label = repair['name'].lower()
        if 'lamp' in label:
            repair.update(tile=dark, effect='lamp')
        elif 'beacon' in label:
            repair.update(tile=depot, effect='beacon')
        elif 'latch' in label and gate:
            repair.update(tile=gate, effect='latch')
        else:
            repair['effect'] = 'open'
        if repair['effect'] != 'open':
            walls.discard(key(repair['tile']))
        else:
            # Block one segment of the delivery loop. Its three-tile inner
            # detour keeps the level solvable; opening the segment saves 2 moves.
            options = []
            features = [fade, dark, switch, gate, ice, depot] + homes
            for i in range(picks[0] + 1, picks[2]):
                target = path[i]
                before, after = path[i - 1], path[(i + 1) % length]
                if target in features or before[0] != after[0] and before[1] != after[1]:
                    continue
                if before[1] == after[1]:
                    outside = -1 if target[1] == y0 else 1
                    offset = [0, outside if 0 <= target[1] + outside < 8 else -outside]
                else:
                    outside = -1 if target[0] == x0 else 1
                    offset = [outside if 0 <= target[0] + outside < 8 else -outside, 0]
                detour = [[p[0] + offset[0], p[1] + offset[1]] for p in (before, target, after)]
                if all(0 <= p[0] < 8 and 0 <= p[1] < 8 and key(p) not in keep for p in detour):
                    options.append((i, target, detour))
            assert options, f'no repair detour on level {number}'
            i, target, detour = rng.choice(options)
            repair.update(tile=target, stepsSaved=2)
            walls.add(key(target))
            for p in detour:
                walls.discard(key(p))
            spine = path[:i] + detour + path[i + 1:] + [depot]
    # A shadow patrol touches the known route on some boards. Choose a phase
    # that allows at least one full delivery route before repairs.
    def make_patrol(prefer_crossing):
        anchor = path[round(length * rng.uniform(.35, .65))]
        squares = []
        for dx in (0, -1):
            for dy in (0, -1):
                ax, ay = anchor[0] + dx, anchor[1] + dy
                if 0 <= ax <= 6 and 0 <= ay <= 6:
                    squares.append([[ax, ay], [ax + 1, ay], [ax + 1, ay + 1], [ax, ay + 1]])
        if prefer_crossing:
            rng.shuffle(squares)
        else:
            squares.sort(key=lambda sq: sum(key(p) in keep for p in sq))
        for square in squares:
            if repair and repair['effect'] == 'open' and repair['tile'] in square:
                continue
            if any(p in homes for p in square):
                continue
            for phase in range(4):
                activation = spine.index(homes[0])
                if all(spine[step] != square[(phase + step - activation) % 4]
                       and spine[step] != square[(phase + step - activation - 1) % 4]
                       for step in range(activation + 1, len(spine))):
                    return square, phase
        square = [[3, 3], [4, 3], [4, 4], [3, 4]]
        assert not any(p in homes for p in square)
        return square, 0

    patrol, phase = make_patrol(number > 2 and number % 4 != 0)
    patrol2, phase2 = make_patrol(True) if second else (None, None)
    for p in patrol + (patrol2 or []):
        walls.discard(key(p))
    if repair and repair['effect'] == 'open':
        assert key(repair['tile']) in walls, f'repair was erased by patrol on level {number}'
        protected = {key(p) for p in spine + patrol + (patrol2 or [])}
        gapkey = key(repair['tile'])
        def saved_steps():
            closed = shortest_full(depot, homes, walls)
            opened = shortest_full(depot, homes, walls - {gapkey})
            return closed - opened
        closable = [[x, y] for y in range(8) for x in range(8)
                    if key([x, y]) not in walls and key([x, y]) not in protected]
        closable.sort(key=lambda p: abs(p[0]-repair['tile'][0])+abs(p[1]-repair['tile'][1]))
        for p in closable:
            if saved_steps() > 0:
                break
            walls.add(key(p))
        assert saved_steps() > 0, f'repair does not save steps on level {number}: path={path}, homes={homes}, gap={repair["tile"]}, patrol={patrol}, walls={len(walls)}'
        repair['stepsSaved'] = saved_steps()

    # Measure the guaranteed clockwise route, including two-light streets.
    extra = int(dark is not None)
    target_spare = 6 if chapter <= 2 else 5 if chapter <= 4 else 4 if chapter <= 6 else 3 if chapter <= 8 else 2
    cap = len(spine) - 1 + extra - 6 + target_spare
    cap = max(cap, picks[0] + 1)
    if number <= 5:
        cap = max(cap, 23 if number <= 2 else 21)
    homes_data = [{'p': p, 'name': name, 'points': base + 30 * (chapter - 1)}
                  for p, name, base in zip(homes, ['Lantern Row', 'East Watch', 'The Mill'], [120, 180, 240])]
    level = {'n': number, 'chapter': chapter, 'brief': brief,
             'depot': depot, 'homes': homes_data, 'walls': sorted(walls),
             'repair': repair, 'fade': fade, 'dark': dark, 'switch': switch,
             'gate': gate, 'ice': ice, 'echo': echo, 'patrol': patrol,
             'phase': phase, 'patrol2': patrol2, 'phase2': phase2,
             'cap': cap, 'spine': spine, 'required': 1 if number <= 2 else 3 if number % 10 == 0 else 2,
             'bonus': 100 + 25 * (chapter - 1)}
    # Static checks protect the authored guarantee and map integrity.
    assert len(set(map(key, path))) == length
    assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(spine, spine[1:]))
    assert all(key(p) not in walls for p in spine)
    assert repair is None or (key(repair['tile']) in walls) == (repair['effect'] == 'open')
    static_tiles = [depot, *homes, *(p for p in (fade, dark, switch, gate, ice) if p)]
    assert len({key(p) for p in static_tiles}) == len(static_tiles), f'overlapping board features on level {number}'
    layout = json.dumps([depot, homes, sorted(walls), fade, dark, switch, gate, ice, patrol, patrol2], sort_keys=True)
    assert layout not in seen_layouts, f'duplicate layout on level {number}'
    seen_layouts.add(layout)
    levels.append(level)

(ROOT / 'CAMPAIGN_LEVELS.json').write_text(json.dumps(levels, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
template = (ROOT / 'campaign' / 'campaign.template.html').read_text(encoding='utf-8')
output = template.replace('/*__LEVEL_DATA__*/', 'const LEVELS=' + json.dumps(levels, ensure_ascii=False, separators=(',', ':')) + ';')
output = output.replace('/*__ISOMETRIC_SCENE__*/', (ROOT / 'campaign' / 'isometric-scene.js').read_text(encoding='utf-8'))
output = output.replace('/*__FEEDBACK_CODE__*/', (ROOT / 'campaign' / 'feedback.js').read_text(encoding='utf-8'))
assert '/*__LEVEL_DATA__*/' not in output
assert '/*__ISOMETRIC_SCENE__*/' not in output
assert '/*__FEEDBACK_CODE__*/' not in output
(ROOT / 'CAMPAIGN_100_LEVELS.html').write_text(output, encoding='utf-8')
print(f'Built {len(levels)} distinct campaign levels')
