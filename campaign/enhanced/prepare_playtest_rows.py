"""Make compact, source-grounded rows for the filtered playtest workbook."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'campaign' / 'enhanced' / 'playtest_rows.json'
known_network_shortcuts = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'unresolved-network-shortcuts.json').read_text(encoding='utf-8'))['rows']}
resolved_network_circuits = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'unresolved-network-shortcuts.json').read_text(encoding='utf-8')).get('resolved',[])}
express_routes = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'express_routes.json').read_text(encoding='utf-8'))}
transit_current_overrides_path = ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'current_route_overrides.json'
transit_current_overrides = {int(k):v for k,v in json.loads(transit_current_overrides_path.read_text(encoding='utf-8')).items()} if transit_current_overrides_path.exists() else {}
exact_transit = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'exact_transit_minima.json').read_text(encoding='utf-8'))['certified']}
exact_signal = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'phase-choices-v1' / 'exact_signal_minima.json').read_text(encoding='utf-8'))['certified']}
express_stops_path = ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'current_stop_overlays.json'
if not express_stops_path.exists():
    express_stops_path = ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'express_stop_overlays.json'
express_stops = json.loads(express_stops_path.read_text(encoding='utf-8'))
known_event_aware = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'event-aware-unresolved-shortcuts.json').read_text(encoding='utf-8'))['rows']}
late_exact = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'event-aware-exact-minima-late.json').read_text(encoding='utf-8'))['certified']}
levels = json.loads((ROOT / 'CAMPAIGN_1000_LEVELS.json').read_text(encoding='utf-8'))
authored = json.loads((ROOT / 'campaign' / 'enhanced' / 'road-events-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
levels += authored
opening = json.loads((ROOT / 'campaign' / 'enhanced' / 'opening-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
opening_shortest = json.loads((ROOT / 'campaign' / 'enhanced' / 'opening-v1' / 'shortest_routes.json').read_text(encoding='utf-8'))
opening_repaired = {item['level']: item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'opening-v1' / 'repaired_shortest_routes.json').read_text(encoding='utf-8'))}
early_exact = {item['level']: item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'early-winding-v1' / 'shortest_routes.json').read_text(encoding='utf-8'))}
assert len(early_exact) == 100
levels[:50] = opening
hidden = json.loads((ROOT / 'campaign' / 'enhanced' / 'hidden-routes-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in hidden:
    levels[l['n']-1] = l
influence = json.loads((ROOT / 'campaign' / 'enhanced' / 'shadow-influence-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in influence:
    levels[l['n']-1] = l
leech = json.loads((ROOT / 'campaign' / 'enhanced' / 'leech-houses-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in leech:
    levels[l['n']-1] = l
causeways = json.loads((ROOT / 'campaign' / 'enhanced' / 'causeways-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in causeways:
    levels[l['n']-1] = l
sentinels = json.loads((ROOT / 'campaign' / 'enhanced' / 'sentinels-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in sentinels:
    levels[l['n']-1] = l
hunters = json.loads((ROOT / 'campaign' / 'enhanced' / 'hunters-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in hunters:
    levels[l['n']-1] = l
doors = json.loads((ROOT / 'campaign' / 'enhanced' / 'shadow-doors-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in doors:
    levels[l['n']-1] = l
bridges = json.loads((ROOT / 'campaign' / 'enhanced' / 'light-bridges-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
bridge_proofs = json.loads((ROOT / 'campaign' / 'enhanced' / 'light-bridges-v1' / 'route_proofs.json').read_text(encoding='utf-8'))
bridge_detour_wall_path = ROOT / 'campaign' / 'enhanced' / 'light-bridges-v1' / 'detour_walls.json'
bridge_detour_wall_levels = set(json.loads(bridge_detour_wall_path.read_text(encoding='utf-8'))) if bridge_detour_wall_path.exists() else set()
for l in bridges:
    levels[l['n']-1] = l
quakes = json.loads((ROOT / 'campaign' / 'enhanced' / 'quakes-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
quake_proofs = json.loads((ROOT / 'campaign' / 'enhanced' / 'quakes-v1' / 'post_event_routes.json').read_text(encoding='utf-8'))
for l in quakes:
    levels[l['n']-1] = l
aftershocks = json.loads((ROOT / 'campaign' / 'enhanced' / 'aftershocks-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in aftershocks:
    levels[l['n']-1] = l
storms = json.loads((ROOT / 'campaign' / 'enhanced' / 'storms-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in storms:
    levels[l['n']-1] = l
floods = json.loads((ROOT / 'campaign' / 'enhanced' / 'floods-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in floods:
    levels[l['n']-1] = l
nightfall = json.loads((ROOT / 'campaign' / 'enhanced' / 'nightfall-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in nightfall:
    levels[l['n']-1] = l
day_night = json.loads((ROOT / 'campaign' / 'enhanced' / 'day-night-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in day_night:
    levels[l['n']-1] = l
spawners = json.loads((ROOT / 'campaign' / 'enhanced' / 'spawners-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in spawners:
    levels[l['n']-1] = l
merge_split = json.loads((ROOT / 'campaign' / 'enhanced' / 'merge-split-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in merge_split:
    levels[l['n']-1] = l
networks = json.loads((ROOT / 'campaign' / 'enhanced' / 'light-networks-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in networks:
    levels[l['n']-1] = l
overload = json.loads((ROOT / 'campaign' / 'enhanced' / 'light-overload-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in overload:
    levels[l['n']-1] = l
transfer = json.loads((ROOT / 'campaign' / 'enhanced' / 'light-transfer-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in transfer:
    levels[l['n']-1] = l
convergence = json.loads((ROOT / 'campaign' / 'enhanced' / 'convergence-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in convergence:
    levels[l['n']-1] = l
chains = json.loads((ROOT / 'campaign' / 'enhanced' / 'chain-events-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
for l in chains:
    levels[l['n']-1] = l
transit = json.loads((ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
transit_proofs = json.loads((ROOT / 'campaign' / 'enhanced' / 'transit-v1' / 'route_proofs.json').read_text(encoding='utf-8'))
for l in transit:
    levels[l['n']-1] = l
phases = json.loads((ROOT / 'campaign' / 'enhanced' / 'phase-choices-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
phase_proofs = json.loads((ROOT / 'campaign' / 'enhanced' / 'phase-choices-v1' / 'route_proofs.json').read_text(encoding='utf-8'))
signal_hint_routes = json.loads((ROOT / 'campaign' / 'enhanced' / 'reference-hints-v1' / 'normalized_signal_routes.json').read_text(encoding='utf-8'))
verified_phase_defaults = {item['level']: item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'phase-choices-v1' / 'verified_default_detours.json').read_text(encoding='utf-8'))}
for l in phases:
    levels[l['n']-1] = l
mastery = json.loads((ROOT / 'campaign' / 'enhanced' / 'mastery-v1' / 'authored_levels.json').read_text(encoding='utf-8'))
mastery_proofs = json.loads((ROOT / 'campaign' / 'enhanced' / 'mastery-v1' / 'route_proofs.json').read_text(encoding='utf-8'))
for l in mastery:
    levels[l['n']-1] = l
late_field_path = ROOT / 'campaign' / 'enhanced' / 'shadow-fields-late-v1' / 'fields.json'
if late_field_path.exists():
    for level_number, field in json.loads(late_field_path.read_text(encoding='utf-8')).items():
        levels[int(level_number)-1]['shadowInfluence2x2'] = field
house_order_event_path = ROOT / 'campaign' / 'enhanced' / 'house-order-screen-v1' / 'event_tiles.json'
house_order_event_levels = set()
if house_order_event_path.exists():
    house_order_events = json.loads(house_order_event_path.read_text(encoding='utf-8'))
    house_order_event_levels = {int(level_number) for level_number in house_order_events}
    for level_number, tile in house_order_events.items():
        level = levels[int(level_number)-1]
        if level.get('phaseChoice'):
            level['phaseChoice']['defaultClose'] = tile
        level['authoredEvent']['tile'] = tile
finale_wall_path = ROOT / 'campaign' / 'enhanced' / 'finale-corridor-v1' / 'walls.json'
if finale_wall_path.exists():
    for level_number, extra_walls in json.loads(finale_wall_path.read_text(encoding='utf-8')).items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
late_wall_path = ROOT / 'campaign' / 'enhanced' / 'late-shortcut-streets-v1' / 'walls.json'
late_wall_levels = set()
if late_wall_path.exists():
    late_walls = json.loads(late_wall_path.read_text(encoding='utf-8'))
    late_wall_levels = {int(level_number) for level_number in late_walls}
    for level_number, extra_walls in late_walls.items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
variant_wall_path = ROOT / 'campaign' / 'enhanced' / 'finale-shortcut-variants-v1' / 'walls.json'
variant_wall_levels = set()
if variant_wall_path.exists():
    variant_walls = json.loads(variant_wall_path.read_text(encoding='utf-8'))
    variant_wall_levels = {int(level_number) for level_number in variant_walls}
    for level_number, extra_walls in variant_walls.items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
storm_variant_path = ROOT / 'campaign' / 'enhanced' / 'storm-variant-streets-v1' / 'walls.json'
storm_variant_levels = set()
if storm_variant_path.exists():
    storm_variant_walls = json.loads(storm_variant_path.read_text(encoding='utf-8'))
    storm_variant_levels = {int(level_number) for level_number in storm_variant_walls}
    for level_number, extra_walls in storm_variant_walls.items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
multi_band_path = ROOT / 'campaign' / 'enhanced' / 'multi-band-variants-v1' / 'walls.json'
multi_band_levels = set()
if multi_band_path.exists():
    multi_band_walls = json.loads(multi_band_path.read_text(encoding='utf-8'))
    multi_band_levels = {int(level_number) for level_number in multi_band_walls}
    for level_number, extra_walls in multi_band_walls.items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
if bridge_detour_wall_path.exists():
    for level_number, extra_walls in json.loads(bridge_detour_wall_path.read_text(encoding='utf-8')).items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
middle_wall_path = ROOT / 'campaign' / 'enhanced' / 'middle-shortcut-screen-v1' / 'walls.json'
middle_wall_levels = set()
if middle_wall_path.exists():
    middle_walls = json.loads(middle_wall_path.read_text(encoding='utf-8'))
    middle_wall_levels = {int(level_number) for level_number in middle_walls}
    for level_number, extra_walls in middle_walls.items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
house_order_wall_path = ROOT / 'campaign' / 'enhanced' / 'house-order-screen-v1' / 'walls.json'
house_order_wall_levels = set()
if house_order_wall_path.exists():
    house_order_walls = json.loads(house_order_wall_path.read_text(encoding='utf-8'))
    house_order_wall_levels = {int(level_number) for level_number in house_order_walls}
    for level_number, extra_walls in house_order_walls.items():
        levels[int(level_number)-1]['walls'].extend(extra_walls)
hunter_overlay_path = ROOT / 'campaign' / 'enhanced' / 'middle-shortcut-screen-v1' / 'hunter_overlays.json'
if hunter_overlay_path.exists():
    for level_number, den in json.loads(hunter_overlay_path.read_text(encoding='utf-8')).items():
        levels[int(level_number)-1]['hunterDen'] = den
oneway_path = ROOT / 'campaign' / 'enhanced' / 'oneway-shortcuts-v1' / 'overlays.json'
if oneway_path.exists():
    for level_number, overlay in json.loads(oneway_path.read_text(encoding='utf-8')).items():
        levels[int(level_number)-1].update(overlay)
bridge_spur_path = ROOT / 'campaign' / 'enhanced' / 'bridge-spurs-v1' / 'overlays.json'
bridge_spurs = json.loads(bridge_spur_path.read_text(encoding='utf-8')) if bridge_spur_path.exists() else {}
bridge_route_path = ROOT / 'campaign' / 'enhanced' / 'bridge-spurs-v1' / 'routes.json'
bridge_spur_routes = json.loads(bridge_route_path.read_text(encoding='utf-8')) if bridge_route_path.exists() else {}
for level_number, spur in bridge_spurs.items():
    level = levels[int(level_number)-1]
    level['lightBridge'] = spur['bridge']
    level['homes'][spur['houseIndex']]['p'] = spur['house']
    level['walls'] = sorted((set(level['walls']) | set(spur['addedWalls'])) - set(spur['openedCells']))
    level['oneWayTile'] = spur['oneWayTile']
    level['oneWayFrom'] = spur['oneWayFrom']
    level['phase'] = spur['phase']
    level['phase2'] = spur['phase2']
    level['cap'] += spur['capBoost']
    level['bridgeHouseIndex'] = spur['houseIndex']
legacy = json.loads((ROOT / 'design' / 'map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
post = json.loads((ROOT / 'campaign' / 'enhanced' / 'road-events-v1' / 'post_event_routes.json').read_text(encoding='utf-8'))
power_samples = {item['level'] for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'power-sample-results.json').read_text(encoding='utf-8'))['samples']}
early_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'early-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
bridge_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'bridge-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
quake_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'quake-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
quake_revisions_v2 = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'quake-route-rebalance-v2' / 'revisions.json').read_text(encoding='utf-8'))}
quake_revisions_v3 = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'quake-route-rebalance-v3' / 'revisions.json').read_text(encoding='utf-8'))}
quake_revisions_v4 = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'aftershock-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
quake_revisions_v5 = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'aftershock-route-rebalance-v2' / 'revisions.json').read_text(encoding='utf-8'))}
storm_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'storm-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
night_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'night-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
spawner_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'spawner-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
relay_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'relay-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
chain_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'chain-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
transit_walk_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'transit-walk-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
signal_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'signal-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
current_phase_choices = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'phase-choices-v1' / 'current_revisions.json').read_text(encoding='utf-8'))}
finale_revisions = {item['level']:item for item in json.loads((ROOT / 'campaign' / 'enhanced' / 'finale-route-rebalance-v1' / 'revisions.json').read_text(encoding='utf-8'))}
assert len(levels) == 2000 and [l['n'] for l in levels] == list(range(1, 2001))
for level_number in json.loads((ROOT / 'campaign' / 'enhanced' / 'light-networks-v1' / 'circuit_objectives.json').read_text(encoding='utf-8')):
    levels[int(level_number)-1]['networkCircuitRequired'] = True
for level_number,stops in express_stops.items():
    levels[int(level_number)-1]['transitLink']['stops'] = stops
cap_overlays = ROOT / 'campaign' / 'enhanced' / 'lantern-balance-v1' / 'promoted_caps.json'
if cap_overlays.exists():
    for level_number,new_cap in json.loads(cap_overlays.read_text(encoding='utf-8')).items():
        levels[int(level_number)-1]['cap'] = new_cap

headers = ['Level', 'Grid', 'Houses', 'Shadow actors', 'Echo', 'Lantern',
           'Assigned power', 'Live map event', 'Other live hazards',
           'Repair', 'No-power route steps', 'Power / alternate steps',
           'No-power shortest?', 'Review state']
rows = []
for l in levels:
    n = l['n']
    hazards = []
    for field, label in [('fade', 'Fading crossing'), ('ice', 'Thin ice'),
                         ('dark', 'Dark street'), ('switch', 'Timed gate')]:
        if l.get(field):
            hazards.append(label)
    if l.get('sentinelCenter'):
        hazards.append('3×3 Sentinel ×1')
    if l.get('shadowInfluence2x2'):
        hazards.append('2×2 Shadow Influence ×1')
    if l.get('rechargeHouse'):
        hazards.append('Leech patrol ×1; drains recharge house')
    if l.get('aftershock'):
        hazards.append('Marked road closes 8 moves after first quake')
    if l.get('hunterDen'):
        hazards.append('Hunter ×1; pursues every 2 moves')
    if l.get('nightfall'):
        hazards.append('Fog radius 3; dusk road +1 light')
    if l.get('dayNightCycle'):
        hazards.append('Night 6 moves / day 4; moon road opens at night')
    if l.get('floodRoad'):
        hazards.append('Low road floods 4 moves after delivery')
    if l.get('shadowSpawner'):
        hazards.append('Shadow Spawner ×1; 2×2 growth')
    if l.get('mergeSplit'):
        hazards.append('2×2 merges into 3×3, then splits into 2')
    if l.get('lumenNetwork'):
        hazards.append('Source house unlocks relay; first crossing +2 light')
    if l.get('lightOverloadGate'):
        gate=l['lightOverloadGate']
        hazards.append(f"Voltage gate accepts {gate['minLight']}–{gate['maxLight']} light")
    if l.get('lightTransfer'):
        hazards.append('Relay sends 1 light to receiver beyond gate')
    if l.get('networkCircuitRequired'):
        hazards.append('Clear requires relay, voltage gate and receiver')
    if l.get('transitLink'):
        hazards.append(('Express return ride' if n in express_routes else 'Transit ride')+' costs 2 light')
    if l.get('phaseChoice') and n <= 1900:
        hazards.append('Depot signal '+('costs 1 light' if l['phaseChoice']['signalLightCost'] else 'free')+'; selects closure')
    if l.get('shadowDoor'):
        hazards.append('Shadow Door opens on patrol lock')
    if l.get('oneWayTile'):
        hazards.append('One-way road; enter from marked arrow side')
    if l.get('collapseTile'):
        hazards.append('Causeway collapses after exit')
    if n in (901, 951):
        power = 'Map Stabilizer ×1'
    elif n in (402, 902, 952):
        power = 'Road Repair ×1'
    elif 101 <= n <= 150:
        power = 'Anchor Trap ×1'
    elif 151 <= n <= 200:
        power = 'Decoy Light ×1'
    elif 201 <= n <= 300:
        power = 'Reveal Pulse ×1'
    elif 701 <= n <= 800:
        power = 'Light Bridge ×1'
    elif 1401 <= n <= 1500:
        power = 'Freeze Seal ×1' if n % 2 else 'Rewind ×1'
    elif n >= 1001:
        power = ['Lumen Flask ×1', 'Road Repair ×1', 'Map Stabilizer ×1'][(n-1001)%3]
    else:
        power = 'None'
    if n <= 1000:
        # Original 51–100 solution rows are shortest route searches. Revised
        # 101–1,000 rows contain legal reference routes with optimal=False.
        solutions = legacy[n-1]['solutions']
        baseline = [s['steps'] for s in solutions if not s['repairPurchased']]
        chosen = min(baseline) if baseline else None
        shortcut = min((s['steps'] for s in solutions if s['repairPurchased']), default=None)
        shortest = 'Yes' if n <= 100 else 'No — reference only'
    else:
        chosen = None if l.get('repairRequired') else post[n-1001]['steps']
        shortcut = post[n-1001]['steps'] if l.get('repairRequired') else None
        shortest = 'No — reference only'
    if l.get('quakeEvent'):
        quake_steps = quake_proofs[n-801]['postEventSteps']
        chosen = None if l.get('repairRequired') else quake_steps
        shortcut = quake_steps if l.get('repairRequired') else None
    if l.get('lightBridgeRequiresPower'):
        chosen = None
        shortcut = len(bridge_spur_routes[str(n)])-1 if str(n) in bridge_spur_routes else bridge_proofs[n-701]['routeSteps']
        shortest = 'Power required — bridge house unreachable' if str(n) in bridge_spur_routes else ('No route — free repair required' if l.get('repairRequired') else 'No-power route unverified')
    if l.get('transitLink'):
        shortcut = transit_proofs[n-1701]['transitSteps']
        if n in express_routes:
            shortcut = express_routes[n]['transitSteps']
    if l.get('phaseChoice') and n <= 1900:
        chosen = phase_proofs[n-1801]['defaultSteps']
        shortcut = phase_proofs[n-1801]['signalSteps']
    if l.get('masteryArchetype'):
        chosen = mastery_proofs[n-1901]['defaultSteps']
        shortcut = mastery_proofs[n-1901].get('signalSteps')
    if n in verified_phase_defaults:
        chosen = verified_phase_defaults[n]['steps']
    if n in (1807, 1828, 1873, 1980, 1994):
        # These shorter signal-branch completions were replayed under the
        # actual selected closure; old authoring proofs contain a winding route.
        shortcut = min(shortcut, len(signal_hint_routes[str(n)])-1)
    if n <= 50:
        chosen = opening_shortest[n-1]['steps']
        shortcut = opening_repaired[n]['steps'] if n in opening_repaired else None
    if 101 <= n <= 200:
        exact = early_exact[n]
        if l.get('repairRequired'):
            assert exact.get('freeRepairRequired') and l['repair']['cost'] == 0
            chosen = None
            shortcut = exact['steps']
            shortest = 'No route — free repair required'
        else:
            assert not exact.get('freeRepairRequired', False)
            chosen = exact['steps']
            shortest = 'Yes'
    if n > 200 and l.get('repairRequired') and l.get('bridgeHouseIndex') is None:
        # The free repair is mandatory, so a completion cannot be labeled
        # as a no-power/no-action route even when an authored replay exists.
        verified = [steps for steps in (chosen, shortcut) if isinstance(steps, int)]
        chosen = None
        shortcut = min(verified) if verified else None
        shortest = 'No route — free repair required'
    if n in known_event_aware:
        known = known_event_aware[n]
        if known['defaultSteps'] is not None:
            if l.get('repairRequired'):
                shortcut = min([known['defaultSteps'], *([shortcut] if isinstance(shortcut,int) else [])])
            else:
                chosen = min([known['defaultSteps'], *([chosen] if isinstance(chosen,int) else [])])
                shortest = 'No - faster route verified; exact pending'
        if known['signalSteps'] is not None:
            shortcut = min([known['signalSteps'], *([shortcut] if isinstance(shortcut,int) else [])])
    if n in express_routes:
        shortcut = express_routes[n]['transitSteps']
    if n in exact_transit:
        assert exact_transit[n]['exactSteps'] == shortcut
        if not exact_transit[n]['freeRepairRequired']:
            chosen = exact_transit[n]['exactSteps']
            shortest = 'Yes - exact no-power minimum'
    if n in exact_signal:
        shortcut = exact_signal[n]['exactSignalSteps']
    if n in late_exact:
        chosen = late_exact[n]['exactNoPowerSteps']
        shortest = 'Yes - exact no-power minimum'
    if l.get('noShadow') and not l.get('repair'):
        shortcut = None
    if n in early_revisions:
        revision = early_revisions[n]
        assert l['cap'] == revision['newCap']
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in bridge_revisions:
        revision = bridge_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('lightBridgeRequiresPower')
        chosen = None
        shortcut = revision['newRouteSteps']
        shortest = 'Power required - bridge house unreachable'
    if n in quake_revisions or n in quake_revisions_v2 or n in quake_revisions_v3 or n in quake_revisions_v4 or n in quake_revisions_v5:
        revision = quake_revisions.get(n) or quake_revisions_v2.get(n) or quake_revisions_v3.get(n) or quake_revisions_v4.get(n) or quake_revisions_v5[n]
        assert l['cap'] == revision['newCap'] and l.get('quakeEvent')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in storm_revisions:
        revision = storm_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('floodRoad')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in night_revisions:
        revision = night_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('dayNightCycle')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in spawner_revisions:
        revision = spawner_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('shadowSpawner')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in relay_revisions:
        revision = relay_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('lumenNetwork') and l.get('shadowSpawner')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in chain_revisions:
        revision = chain_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('chainEvent')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n in transit_walk_revisions:
        revision = transit_walk_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('transitLink')
        assert n in transit_current_overrides and l['transitLink']['stops'] == transit_current_overrides[n]['stops']
        chosen = revision['newRouteSteps']
        shortcut = transit_current_overrides[n]['transitSteps']
        shortest = 'No - verified walking and transit routes; exact pending'
    if n in signal_revisions:
        revision = signal_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('phaseChoice')
        chosen = revision['newRouteSteps']
        shortcut = revision['newSignalSteps']
        shortest = 'No - both road choices verified; exact pending'
    if n == 1804:
        # Full-rule default detour replayed at 60 moves; the signal route is
        # also 60 moves. Keep the exact-minimum claim pending.
        assert l.get('phaseChoice') and chosen >= 60
        chosen = 60
        shortest = 'No - both road choices verified; exact pending'
    if n in current_phase_choices:
        revision = current_phase_choices[n]
        assert l.get('phaseChoice') and chosen is not None and revision['defaultSteps'] > revision['signalSteps']
        chosen, shortcut = revision['defaultSteps'], revision['signalSteps']
        shortest = 'No - both road choices verified; exact pending'
    if n in finale_revisions:
        revision = finale_revisions[n]
        assert l['cap'] == revision['newCap'] and l.get('masteryArchetype') and not l.get('phaseChoice')
        chosen = revision['newRouteSteps']
        shortest = 'No - verified route; exact pending'
    if n == 1943:
        shortcut = 88
        shortest = 'No - 88-step default alternate verified; exact pending'
    repair = 'Free required' if l.get('repairRequired') else 'Optional' if l.get('repair') else 'None'
    event = 'Build Light Bridge; one-way house lane; 2x2 field after first delivery' if n == 778 else \
            'Mastery: '+l['masteryArchetype'] if l.get('masteryArchetype') else \
            'Depot signal selects first-delivery road closure' if l.get('phaseChoice') else \
            'Transit unlocks after delivery; road closes' if l.get('transitLink') else \
            'First delivery closes road; second swaps roads' if l.get('chainEvent') else \
            'Spawner grows; relay opens; road closes' if l.get('shadowSpawner') and l.get('lumenNetwork') else \
            'Wind shifts; nightfall; road closes' if l.get('stormWind') and l.get('nightfall') else \
            'Circuit objective: relay, voltage gate, receiver; road closes' if l.get('networkCircuitRequired') else \
            'Relay splits light; voltage gate; receiver; road closes' if l.get('lightTransfer') else \
            'Relay and voltage gate; road closes' if l.get('lightOverloadGate') else \
            'Light relay opens after delivery; road closes' if l.get('lumenNetwork') else \
            'Shadow nest grows, merges, splits; road closes' if l.get('mergeSplit') else \
            'Shadow nest grows after delivery; road closes' if l.get('shadowSpawner') else \
            'Day/night cycle; moon road; road closes' if l.get('dayNightCycle') else \
            'Nightfall fog and dusk road; road closes' if l.get('nightfall') else \
            'Wind moves blocker; low road floods; road closes' if l.get('floodRoad') else \
            'Storm moves blocker; road closes' if l.get('stormWind') else \
            'Road closes after first delivery' if n >= 1001 else \
            'Beacon reveals hidden house and road; 2×2 shadow field after first delivery' if n == 250 else \
            ('2×2 shadow field after second delivery' if l['shadowInfluence2x2'].get('triggerCount') == 2 else '2×2 shadow field after first delivery') if l.get('shadowInfluence2x2') else \
            'Beacon reveals hidden house and road' if l.get('hiddenRoad') else \
            'Build Light Bridge; one-way lane reaches house' if l.get('bridgeHouseIndex') is not None else \
            'One-way road' if l.get('oneWayTile') else \
            'Causeway collapses after use' if l.get('collapseTile') else \
            'Hunter pursues; Sentinel wakes after delivery' if l.get('hunterDen') else \
            'Sentinel wakes after first delivery' if l.get('sentinelCenter') else \
            'Shadow Door opens on patrol lock' if l.get('shadowDoor') else \
            'Build marked bridge with power for 1 light' if l.get('lightBridge') else \
            'Earthquake changes roads; aftershock closes road in 8 moves' if l.get('aftershock') else \
            'Earthquake closes and opens roads' if l.get('quakeEvent') else \
            'Leech drains recharge house' if l.get('rechargeHouse') else 'None'
    state = 'Opening revision; no-shadow shortest route verified' if l.get('noShadow') else \
            'Opening revision; tight-light shortest route verified' if 41 <= n <= 50 else \
            'Candidate; mastery route verified, shortest pending' if l.get('masteryArchetype') else \
            'Candidate; both chosen phases verified, shortest pending' if l.get('phaseChoice') else \
            'Candidate; walking and transit routes verified, shortest pending' if l.get('transitLink') else \
            'Candidate; two-event route verified, shortest pending' if l.get('chainEvent') else \
            'Candidate; combined route verified, shortest pending' if 1501 <= n <= 1600 else \
            'Playable preview; Decoy route verified, shortest pending' if 151 <= n <= 200 else \
            'Playable preview; powered route not verified' if n <= 200 else \
            'Candidate; Beacon route verified, shortest pending' if l.get('hiddenRoad') else \
            'Candidate; causeway route verified, shortest pending' if l.get('oneWayTile') or l.get('collapseTile') else \
            'Candidate; Hunter chase and Sentinel avoidance verified, shortest pending' if l.get('hunterDen') else \
            'Candidate; Sentinel avoidance verified, shortest pending' if l.get('sentinelCenter') else \
            'Candidate; Shadow Door timing verified, shortest pending' if l.get('shadowDoor') else \
            'Candidate; player-built bridge route verified, no-power route pending' if l.get('lightBridge') else \
            'Candidate; first quake and aftershock route verified, shortest pending' if l.get('aftershock') else \
            'Candidate; post-quake route verified, shortest pending' if l.get('quakeEvent') else \
            'Candidate; Leech timing verified, powered route pending' if l.get('rechargeHouse') else \
            'Candidate; split-light, voltage and closure route verified, shortest pending' if l.get('lightTransfer') else \
            'Candidate; voltage-range and closure route verified, shortest pending' if l.get('lightOverloadGate') else \
            'Candidate; light network and closure route verified, shortest pending' if l.get('lumenNetwork') else \
            'Candidate; merge/split and closure route verified, shortest pending' if l.get('mergeSplit') else \
            'Candidate; spawner and closure route verified, shortest pending' if l.get('shadowSpawner') else \
            'Candidate; day/night phase and closure route verified, shortest pending' if l.get('dayNightCycle') else \
            'Candidate; nightfall and closure route verified, shortest pending' if l.get('nightfall') else \
            'Candidate; flood countdown, storm and closure route verified, shortest pending' if l.get('floodRoad') else \
            'Candidate; storm and closure route verified, shortest pending' if l.get('stormWind') else \
            'Candidate; power-use route verified, shortest pending' if 1401 <= n <= 1500 else \
            'Candidate; post-event route verified, other systems pending' if n >= 1001 else \
            'Archived map; advanced systems pending'
    state = ('Bridge route replayed; no-power route unverified' if l.get('lightBridgeRequiresPower') else
             'Power sample and route replayed; visual review pending' if n in power_samples else
             'Both routes replayed; visual review pending' if l.get('phaseChoice') else
             'Opening minima replayed; visual review pending' if n in opening_repaired else
             'Opening route replayed; visual review pending' if n <= 50 else
             'Preview route replayed; visual review pending')
    if 101 <= n <= 200:
        state = 'Exact minimum replayed; optional power route pending visual review'
    if n in (819, 865, 866, 891, 899, 940, 943, 953, 960, 974, 982, 1902, 1904, 1939, 1959, 1963):
        state = 'Shadow field blocks known fast route; visual review pending'
    if n in (1905, 1910, 1916, 1926):
        state = 'Finale roads revised; known fast route blocked; visual review pending'
    if n in late_wall_levels:
        state = 'Shortcut streets revised; route replayed; visual review pending'
    if n in variant_wall_levels:
        state = 'Finale variant streets revised; visual review pending'
    if n in storm_variant_levels:
        state = 'Storm variant streets revised; visual review pending'
    if n in multi_band_levels:
        state = 'Multi-route streets revised; visual review pending'
    if n in middle_wall_levels:
        state = 'Middle shortcut revised; visual review pending'
    if n in house_order_wall_levels:
        state = 'Alternate house-order shortcut blocked; visual review pending'
    if n in house_order_event_levels:
        state = 'Road-close event revised; alternate routes replayed; visual review pending'
    if n in (927, 933, 940, 998):
        state = 'Alternate house-order field replayed; visual review pending'
    if n == 399:
        state = 'Known alternate house-order route blocked; visual review pending'
    if n in (400, 669):
        state = 'Known swapped-order route blocked; visual review pending'
    if n == 250:
        state = 'Beacon shortcut shadow field replayed; visual review pending'
    if str(n) in bridge_detour_wall_levels:
        state = 'Bridge bypass revised; no-power route unverified'
    if str(n) in bridge_spurs:
        state = 'Bridge house requires power; route replayed; visual review pending'
    if n in (768, 778) and str(n) in bridge_spurs:
        state = 'Bridge house required; known fast route blocked; visual review pending'
    if n == 1113:
        state = 'One-way route revised; visual review pending' if l.get('oneWayTile') else 'Known 102-step straight route; redesign pending'
    if n in known_event_aware:
        state = 'Known faster route; redesign pending'
    if n in express_routes:
        state = ('Exact transit minimum with free repair; balance and visual review pending' if exact_transit[n]['freeRepairRequired'] else
                 'Exact no-power transit minimum; balance and visual review pending')
    if n in exact_signal:
        state = ('Exact signaled minimum with free repair; balance and visual review pending' if exact_signal[n]['freeRepairRequired'] else
                 'Exact signaled minimum; balance and visual review pending')
    if n in late_exact:
        state = 'Exact no-power route; lantern balance and visual review pending'
    if n in late_exact and n in exact_signal:
        state = 'Exact default and signal routes; lantern balance and visual review pending'
    if n in known_network_shortcuts:
        state = 'Known relay, gate and receiver bypass; structural redesign pending'
    if n in resolved_network_circuits:
        state = 'Circuit bypass blocked; balance and visual review pending'
    if n in early_revisions:
        state = 'Shorter route replayed; 12-light balance; visual review pending'
    if n in bridge_revisions:
        state = 'Shorter bridge route replayed; 12-light balance; visual review pending'
    if n in quake_revisions or n in quake_revisions_v2 or n in quake_revisions_v3 or n in quake_revisions_v4 or n in quake_revisions_v5:
        state = ('Shorter aftershock route replayed; 12-light balance; visual review pending' if n in quake_revisions_v5 and n >= 951 else 'Shorter quake route replayed; 12-light balance; visual review pending')
    if n in storm_revisions:
        state = 'Shorter storm route replayed; 12-light balance; visual review pending'
    if n in night_revisions:
        state = 'Shorter day/night route replayed; 12-light balance; visual review pending'
    if n in spawner_revisions:
        state = 'Shorter spawner route replayed; 12-light balance; visual review pending'
    if n in relay_revisions:
        state = 'Shorter relay route replayed; 12-light balance; visual review pending'
    if n in chain_revisions:
        state = 'Shorter chain-event route replayed; 12-light balance; visual review pending'
    if n in transit_walk_revisions:
        state = 'Walking and faster transit routes replayed; visual review pending'
    if n in signal_revisions:
        state = 'Both road choices replayed; same fast route; choice design review pending'
    if n in current_phase_choices and n not in exact_signal:
        revision = current_phase_choices[n]
        state = f"Road choice: {revision['defaultSteps']}-step detour or {revision['signalSteps']}-step signal; visual review pending"
    if n in finale_revisions:
        state = 'Shorter finale route replayed; 12-light balance; visual review pending'
    if n == 1943:
        state = '88-step default shortcut known; signal branch conflicts with cap change'
    # Influence fields and spawner zones occupy cells but are not extra actors.
    # Leech behavior reuses an existing patrol rather than creating one.
    shadows = int(not l.get('noShadow')) + bool(l.get('patrol2')) + bool(l.get('sentinelCenter')) + bool(l.get('hunterDen'))
    rows.append([n, l.get('grid',8), len(l['homes']), shadows,
                 int(bool(l.get('echo'))), l['cap'], power, event,
                 ', '.join(hazards), repair, chosen, shortcut, shortest, state])
assert len(rows) == 2000
def workbook_text(value):
    if not isinstance(value,str):
        return value
    # Historic copy in this generator contains UTF-8 read through CP1252.
    # Normalize once, then use plain characters that Excel and the exporter
    # preserve consistently across Windows installations.
    if any(ord(ch)>127 for ch in value):
        try:
            value=value.encode('cp1252').decode('utf-8')
        except UnicodeError:
            pass
    value=value.translate(str.maketrans({'×':'x','–':'-','—':'-','“':'"','”':'"','’':"'"}))
    assert value.isascii(),ascii(value)
    return value
headers=[workbook_text(value) for value in headers]
rows=[[workbook_text(value) for value in row] for row in rows]
OUT.write_text(json.dumps({'headers': headers, 'rows': rows}, ensure_ascii=False), encoding='utf-8')
print(f'Prepared {len(rows)} level rows and {len(headers)} compact columns: {OUT}')

if __name__ == '__main__':
    pass
