"""Create a self-contained, human-readable handoff for the 100 browser levels."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = json.loads((ROOT / 'CAMPAIGN_LEVELS.json').read_text(encoding='utf-8'))
CHAPTERS = ['First Deliveries', 'Broken Crossings', 'Waterline', 'Switchyard',
            'Echo District', 'Winter Canal', 'Shadow Market', 'Old City',
            'Blackout', 'Last Light']


def point(p):
    return f'({p[0]},{p[1]})' if p is not None else '—'


def point_list(points):
    return ' → '.join(point(p) for p in points)


def directions(path):
    lookup = {(1, 0): 'R', (-1, 0): 'L', (0, 1): 'D', (0, -1): 'U'}
    moves = [lookup[(b[0]-a[0], b[1]-a[1])] for a, b in zip(path, path[1:])]
    groups = []
    for move in moves:
        if groups and groups[-1][0] == move:
            groups[-1][1] += 1
        else:
            groups.append([move, 1])
    return ' '.join(f'{letter}{count}' for letter, count in groups)


def map_rows(level):
    board = [['.' for _ in range(8)] for _ in range(8)]
    for raw in level['walls']:
        x, y = map(int, raw.split(','))
        board[y][x] = '#'
    for field, glyph in [('fade', 'f'), ('ice', 'i'), ('dark', 'd'),
                         ('switch', 's'), ('gate', 'g')]:
        p = level[field]
        if p is not None:
            board[p[1]][p[0]] = glyph
    repair = level['repair']
    if repair and repair['effect'] == 'open':
        x, y = repair['tile']
        board[y][x] = 'R'
    x, y = level['depot']
    board[y][x] = 'D'
    for glyph, home in zip('ABC', level['homes']):
        x, y = home['p']
        board[y][x] = glyph
    return [''.join(row) for row in board]


def full_route_result(level):
    light = level['cap']
    visited = set()
    homes = {tuple(h['p']): h for h in level['homes']}
    walls = set(level['walls'])
    for index, p in enumerate(level['spine'][1:], 1):
        assert f'{p[0]},{p[1]}' not in walls
        light -= 2 if p == level['dark'] else 1
        home = homes.get(tuple(p))
        if home and tuple(p) not in visited:
            visited.add(tuple(p))
            light = min(level['cap'], light + 2)
        elif index < len(level['spine']) - 1:
            assert light > 0, f'lantern expired on level {level["n"]}'
        assert light >= 0, f'negative lantern on level {level["n"]}'
    assert len(visited) == 3 and level['spine'][-1] == level['depot']
    return light, sum(h['points'] for h in level['homes']) + level['bonus']


lines = [
    '# Last Light Courier — complete 100-level handoff',
    '',
    'This is the exact board-data handoff for the standalone browser campaign. Use it with '
    '[CAMPAIGN_LEVELS.json](CAMPAIGN_LEVELS.json) and [CAMPAIGN_100_LEVELS.html](CAMPAIGN_100_LEVELS.html). '
    'The JSON is the machine-readable authority; this document makes every level inspectable without running the game.',
    '',
    '## Current status and scope',
    '',
    '- 100 distinct 8×8 playable boards, ten chapters, one-tile tap controls, 41 repair opportunities.',
    '- Every listed full-delivery route was checked in the browser engine with no purchase; it reaches all three homes and returns to the depot. The road-repair projects were checked to save two moves on a shortest all-house route in the static map.',
    '- This is a first-pass generated campaign, not 100 hand-tuned production levels. The level briefs express design intent; some named scenery is currently represented by the same blocked-tile rule. The routes prove playability, but difficulty, pacing, visual identity, partial-return choices, and touch clarity still need player review.',
    '- An Android build does not exist. The browser campaign saves its wallet, level clears, tutorials, best scores, and level-specific repairs in local storage.',
    '',
    '## Rules implemented in the browser',
    '',
    '1. Tap one orthogonally adjacent green tile. Ordinary entry costs 1 light; an unrepaired dark tile costs 2. The courier and each active patrol advance one turn per tap.',
    '2. A first visit to a house adds its points to the at-risk total and refills 2 light, capped at the level start capacity. Its tile becomes **DONE**. The first delivery wakes the shadow patrols.',
    '3. A red neighboring tile would be occupied by a shadow after the tap and is disabled. The next shadow tile is not separately marked. A completed house acts as a safe island for collision checking.',
    '4. Echo Shadow, when present, retraces the courier trail. Its displayed position is from two moves earlier; the move the echo would occupy next is blocked.',
    '5. A fading crossing starts at 5 on first entry; thin ice starts at 4. Each subsequent move reduces its timer. At 0 the tile closes for that run. A switch sets its gate timer to 4; a bought latch holds that gate open.',
    '6. Returning to the depot after at least one delivery banks that run and ends it. Level 1 clears with 1 house; ordinary levels clear with at least 2; every tenth level requires 3. Banking all 3 also awards the chapter mastery bonus.',
    '7. If light reaches zero on a non-house, non-depot move, the lantern-out card shows the at-risk points lost. Banked wallet points are never lost. Repairs are purchased before moving, use banked wallet points, and persist on that specific level.',
    '8. All 100 levels are selectable in the design preview, even before clearing earlier levels. Production progression gating is still a design decision.',
    '',
    '### Coordinates and map legend',
    '',
    'Coordinates are **zero based**: (0,0) is top left; x increases right and y increases downward. Map rows are y=0–7, with x=0–7 from left to right.',
    '',
    '`D` depot; `A/B/C` houses in point-value order; `#` blocked tile; `R` blocked repair tile; `f` fading crossing; `i` thin ice; `d` two-light dark tile; `s` switch; `g` timed gate; `.` ordinary road. A lamp, latch, or beacon repair changes the named feature rather than replacing a blocked tile. Shadow patrols are specified below each map because their positions change every turn.',
    '',
    'A route such as `R3 D2 L1` means three right taps, two down taps, then one left tap from the depot. It is one verified **full three-house return**, not the only solution. It uses no repair.',
    '',
    '### Points and repair bands',
    '',
    'In chapter c (1–10), houses A/B/C award 120/180/240 + 30×(c−1) each. The all-house bonus is 100 + 25×(c−1). Small repairs cost 150 + 75×(c−1); route repairs 300 + 100×(c−1); major repairs 500 + 125×(c−1). Every entry below lists its actual price.',
    '',
    '## Chapter index',
    '',
    '| Chapter | Levels | Theme | Start light | Repairs |',
    '|---:|---:|---|---:|---:|',
]
for chapter in range(1, 11):
    group = LEVELS[(chapter - 1) * 10:chapter * 10]
    caps = [level['cap'] for level in group]
    repairs = sum(level['repair'] is not None for level in group)
    lines.append(f'| {chapter} | {group[0]["n"]}–{group[-1]["n"]} | {CHAPTERS[chapter-1]} | {min(caps)}–{max(caps)} | {repairs} |')

lines += ['', '## Level-by-level boards', '']
for level in LEVELS:
    n = level['n']
    chapter = level['chapter']
    light_left, full_score = full_route_result(level)
    houses = '; '.join(f'{label} {home["name"]} {point(home["p"])} = {home["points"]} pts'
                       for label, home in zip('ABC', level['homes']))
    parts = []
    for field, label in [('fade', 'fading crossing'), ('dark', 'two-light dark tile'),
                         ('switch', 'switch'), ('gate', 'timed gate'), ('ice', 'thin ice')]:
        if level[field] is not None:
            parts.append(f'{label} {point(level[field])}')
    if level['echo']:
        parts.append('Echo Shadow active after first delivery')
    if level['patrol2']:
        parts.append('second patrol active after first delivery')
    repair = level['repair']
    if repair:
        effects = {'open': f'opens the R tile; verified {repair.get("stepsSaved", 0)}-move static all-house shortcut',
                   'lamp': 'dark tile costs 1 light after repair',
                   'latch': 'timed gate stays open after repair',
                   'beacon': 'start capacity rises by 3 on this level'}
        repair_line = (f'**Repair:** {repair["name"]} at {point(repair["tile"])}; '
                       f'{repair["band"]} band, **{repair["cost"]} points**; {effects[repair["effect"]]}.')
    else:
        repair_line = '**Repair:** none on this board.'
    lines += [
        f'### {n:03d} — {CHAPTERS[chapter-1]}',
        '',
        f'**Design brief:** {level["brief"]}',
        '',
        f'**Goal:** bank {level["required"]} of 3 houses to clear; bank all 3 for mastery. '
        f'**Start:** depot {point(level["depot"])}, lantern {level["cap"]}.',
        '',
        f'**Houses:** {houses}.',
        '',
        '```text',
        '    01234567',
    ]
    for y, row in enumerate(map_rows(level)):
        lines.append(f'{y}   {row}')
    lines += [
        '```',
        '',
        f'**Hazards:** first patrol {point_list(level["patrol"])}; initial index {level["phase"]}. '
        + (f'Second patrol {point_list(level["patrol2"])}; initial index {level["phase2"]}. ' if level['patrol2'] else '')
        + ('; '.join(parts) + '.' if parts else 'No timed tile on this board.'),
        '',
        repair_line,
        '',
        f'**Verified no-purchase full route:** `{directions(level["spine"])}`. '
        f'{len(level["spine"])-1} moves, {light_left} light left, '
        f'{full_score} points banked including the {level["bonus"]}-point mastery bonus.',
        '',
    ]

lines += [
    '## Notes for the design review chat',
    '',
    '- Treat the coordinates, prices, and timing above as the **current playable baseline**. Preserve the clear, immediate tap interaction and visible DONE status when reviewing art or tutorials.',
    '- Level 1 currently shows all three houses immediately, although its brief says to reveal the later houses after the first return. Treat that reveal as an unimplemented tutorial detail.',
    '- The generator varies rectangular route geometry and blocked cells. Many levels still share an outer-loop structure; review whether chapters feel distinct enough in play. The full-route proof does not prove that an exact two-house return is feasible or interesting on every ordinary level.',
    '- Flood, rubble, crates, tunnel, tower, and bridge repair names currently share a blocked-tile implementation. Their final art and any distinct rules still need design decisions. Buying a road repair does demonstrably shorten the static all-house route by two moves.',
    '- The tested full routes prove mechanical solvability, not a finished difficulty curve. Validate intended route choices, reward pacing, repair usefulness against the moving shadows, first-time comprehension, and real-phone tap targets with people before calling these production-ready.',
    '- Do not copy the old route-drawing/Go-button rules into this campaign. The selected interaction is direct tap-to-move with every currently safe adjacent option highlighted.',
    '',
]

output = ROOT / 'CAMPAIGN_100_LEVEL_HANDOFF.md'
output.write_text('\n'.join(lines), encoding='utf-8')
assert sum(line.startswith('### ') and line[4:7].isdigit() for line in lines) == 100
print(f'Wrote {output.name}: {len(LEVELS)} levels, {len(lines)} lines')
