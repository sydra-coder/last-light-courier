"""Build a separate 2,000-map baseline browser review; never overwrite index.html."""
from pathlib import Path
import argparse,json,re

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'campaign'/'enhanced'/'candidates-v3'/'CAMPAIGN_2000_CANDIDATES.json'
TARGET=ROOT/'design'/'campaign-2000-preview'/'index.html'
regions=['Ember Road','Dimming Crossroads','Veiled Hamlet','Lantern District','Broken Causeways','Hunting Dark','The Shadowworks','River of Glass','Quake Frontier','Faultline City','Storm March','The Long Night','Breachlands','The Lumen Engine',"Keeper's Arsenal",'Convergence','The Moving Kingdom','Last Provinces','Black Horizon','The Last Light']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mastery-dir',type=Path,default=ROOT/'campaign/enhanced/mastery-v1')
    parser.add_argument('--hints-path',type=Path,default=ROOT/'campaign/enhanced/reference-hints-v1/normalized_routes.json')
    parser.add_argument('--signal-hints-path',type=Path,default=ROOT/'campaign/enhanced/reference-hints-v1/normalized_signal_routes.json')
    parser.add_argument('--exact-late-minima',type=Path,default=ROOT/'campaign/enhanced/event-aware-exact-minima-late.json')
    parser.add_argument('--exact-transit-minima',type=Path,default=ROOT/'campaign/enhanced/transit-v1/exact_transit_minima.json')
    parser.add_argument('--exact-signal-minima',type=Path,default=ROOT/'campaign/enhanced/phase-choices-v1/exact_signal_minima.json')
    parser.add_argument('--extra-shadow-fields',type=Path,default=ROOT/'campaign/enhanced/shadow-fields-late-v1/fields.json')
    parser.add_argument('--extra-walls',type=Path,default=ROOT/'campaign/enhanced/finale-corridor-v1/walls.json')
    parser.add_argument('--late-walls',type=Path,default=ROOT/'campaign/enhanced/late-shortcut-streets-v1/walls.json')
    parser.add_argument('--variant-walls',type=Path,default=ROOT/'campaign/enhanced/finale-shortcut-variants-v1/walls.json')
    parser.add_argument('--storm-variant-walls',type=Path,default=ROOT/'campaign/enhanced/storm-variant-streets-v1/walls.json')
    parser.add_argument('--multi-band-walls',type=Path,default=ROOT/'campaign/enhanced/multi-band-variants-v1/walls.json')
    parser.add_argument('--oneway-overlays',type=Path,default=ROOT/'campaign/enhanced/oneway-shortcuts-v1/overlays.json')
    parser.add_argument('--bridge-detour-walls',type=Path,default=ROOT/'campaign/enhanced/light-bridges-v1/detour_walls.json')
    parser.add_argument('--middle-shortcut-walls',type=Path,default=ROOT/'campaign/enhanced/middle-shortcut-screen-v1/walls.json')
    parser.add_argument('--house-order-walls',type=Path,default=ROOT/'campaign/enhanced/house-order-screen-v1/walls.json')
    parser.add_argument('--house-order-event-tiles',type=Path,default=ROOT/'campaign/enhanced/house-order-screen-v1/event_tiles.json')
    parser.add_argument('--phase-alternate-tiles',type=Path,default=ROOT/'campaign/enhanced/phase-choices-v1/alternate_event_tiles.json')
    parser.add_argument('--chain-open-tiles',type=Path,default=ROOT/'campaign/enhanced/chain-events-v1/open_tiles.json')
    parser.add_argument('--chain-close-tiles',type=Path,default=ROOT/'campaign/enhanced/chain-events-v1/close_tiles.json')
    parser.add_argument('--bridge-spur-overlays',type=Path,default=ROOT/'campaign/enhanced/bridge-spurs-v1/overlays.json')
    parser.add_argument('--hunter-overlays',type=Path,default=ROOT/'campaign/enhanced/middle-shortcut-screen-v1/hunter_overlays.json')
    parser.add_argument('--network-objectives',type=Path,default=ROOT/'campaign/enhanced/light-networks-v1/circuit_objectives.json')
    parser.add_argument('--express-stops',type=Path,default=ROOT/'campaign/enhanced/transit-v1/current_stop_overlays.json')
    parser.add_argument('--lantern-caps',type=Path,default=ROOT/'campaign/enhanced/lantern-balance-v1/promoted_caps.json')
    parser.add_argument('--output',type=Path,default=TARGET)
    args=parser.parse_args()
    levels=json.loads(SOURCE.read_text(encoding='utf-8'))
    assert len(levels)==2000 and [l['n'] for l in levels]==list(range(1,2001))
    authored=json.loads((ROOT/'campaign'/'enhanced'/'road-events-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(authored)==1000 and [l['n'] for l in authored]==list(range(1001,2001))
    sample_powers=['lumen_flask','road_repair','map_stabilizer']
    levels[1000:]=authored
    opening=json.loads((ROOT/'campaign'/'enhanced'/'opening-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(opening)==50 and [l['n'] for l in opening]==list(range(1,51))
    levels[:50]=opening
    hidden=json.loads((ROOT/'campaign'/'enhanced'/'hidden-routes-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(hidden)==100 and [l['n'] for l in hidden]==list(range(201,301))
    for l in hidden:levels[l['n']-1]=l
    influence=json.loads((ROOT/'campaign'/'enhanced'/'shadow-influence-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(influence)==25
    for l in influence:levels[l['n']-1]=l
    leech=json.loads((ROOT/'campaign'/'enhanced'/'leech-houses-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(leech)>=60 and all(301<=l['n']<=400 for l in leech)
    for l in leech:levels[l['n']-1]=l
    causeways=json.loads((ROOT/'campaign'/'enhanced'/'causeways-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(causeways)==100 and [l['n'] for l in causeways]==list(range(401,501))
    for l in causeways:levels[l['n']-1]=l
    levels[401]['reviewPower']='road_repair'
    sentinels=json.loads((ROOT/'campaign'/'enhanced'/'sentinels-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(sentinels)==100 and [l['n'] for l in sentinels]==list(range(501,601))
    for l in sentinels:levels[l['n']-1]=l
    hunters=json.loads((ROOT/'campaign'/'enhanced'/'hunters-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(hunters)>=40 and all(501<=l['n']<=600 for l in hunters)
    for l in hunters:levels[l['n']-1]=l
    doors=json.loads((ROOT/'campaign'/'enhanced'/'shadow-doors-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(doors)==100 and [l['n'] for l in doors]==list(range(601,701))
    for l in doors:levels[l['n']-1]=l
    bridges=json.loads((ROOT/'campaign'/'enhanced'/'light-bridges-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(bridges)==100 and [l['n'] for l in bridges]==list(range(701,801))
    for l in bridges:levels[l['n']-1]=l
    quakes=json.loads((ROOT/'campaign'/'enhanced'/'quakes-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(quakes)==200 and [l['n'] for l in quakes]==list(range(801,1001))
    for l in quakes:levels[l['n']-1]=l
    levels[900]['reviewPower']='map_stabilizer'
    levels[901]['reviewPower']='road_repair'
    aftershocks=json.loads((ROOT/'campaign'/'enhanced'/'aftershocks-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(aftershocks)==50 and [l['n'] for l in aftershocks]==list(range(951,1001))
    for l in aftershocks:levels[l['n']-1]=l
    levels[950]['reviewPower']='map_stabilizer'
    levels[951]['reviewPower']='road_repair'
    storms=json.loads((ROOT/'campaign'/'enhanced'/'storms-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(storms)==100 and [l['n'] for l in storms]==list(range(1001,1101))
    for l in storms:levels[l['n']-1]=l
    floods=json.loads((ROOT/'campaign'/'enhanced'/'floods-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(floods)==100 and [l['n'] for l in floods]==list(range(1001,1101))
    for l in floods:levels[l['n']-1]=l
    nightfall=json.loads((ROOT/'campaign'/'enhanced'/'nightfall-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(nightfall)==100 and [l['n'] for l in nightfall]==list(range(1101,1201))
    for l in nightfall:levels[l['n']-1]=l
    day_night=json.loads((ROOT/'campaign'/'enhanced'/'day-night-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(day_night)==100 and [l['n'] for l in day_night]==list(range(1101,1201))
    for l in day_night:levels[l['n']-1]=l
    spawners=json.loads((ROOT/'campaign'/'enhanced'/'spawners-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(spawners)==100 and [l['n'] for l in spawners]==list(range(1201,1301))
    for l in spawners:levels[l['n']-1]=l
    merge_split=json.loads((ROOT/'campaign'/'enhanced'/'merge-split-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(merge_split)>=20 and all(1201<=l['n']<=1300 for l in merge_split)
    for l in merge_split:levels[l['n']-1]=l
    networks=json.loads((ROOT/'campaign'/'enhanced'/'light-networks-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(networks)==100 and [l['n'] for l in networks]==list(range(1301,1401))
    for l in networks:levels[l['n']-1]=l
    overload=json.loads((ROOT/'campaign'/'enhanced'/'light-overload-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(overload)==100 and [l['n'] for l in overload]==list(range(1301,1401))
    for l in overload:levels[l['n']-1]=l
    transfer=json.loads((ROOT/'campaign'/'enhanced'/'light-transfer-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(transfer)==100 and [l['n'] for l in transfer]==list(range(1301,1401))
    for l in transfer:levels[l['n']-1]=l
    convergence=json.loads((ROOT/'campaign'/'enhanced'/'convergence-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(convergence)==100 and [l['n'] for l in convergence]==list(range(1501,1601))
    for l in convergence:levels[l['n']-1]=l
    chains=json.loads((ROOT/'campaign'/'enhanced'/'chain-events-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(chains)==100 and [l['n'] for l in chains]==list(range(1601,1701))
    for l in chains:levels[l['n']-1]=l
    transit=json.loads((ROOT/'campaign'/'enhanced'/'transit-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(transit)==100 and [l['n'] for l in transit]==list(range(1701,1801))
    for l in transit:levels[l['n']-1]=l
    phases=json.loads((ROOT/'campaign'/'enhanced'/'phase-choices-v1'/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(phases)==100 and [l['n'] for l in phases]==list(range(1801,1901))
    for l in phases:levels[l['n']-1]=l
    mastery=json.loads((args.mastery_dir/'authored_levels.json').read_text(encoding='utf-8'))
    assert len(mastery)==100 and [l['n'] for l in mastery]==list(range(1901,2001))
    for l in mastery:levels[l['n']-1]=l
    if args.extra_shadow_fields.exists():
        late_fields=json.loads(args.extra_shadow_fields.read_text(encoding='utf-8'))
        for level_number,field in late_fields.items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and 'shadowInfluence2x2' not in level
            level['shadowInfluence2x2']=field
            ordinal='second' if field.get('triggerCount')==2 else 'first'
            level['brief']=(level.get('brief','').rstrip()+' A 2×2 shadow field blocks four road tiles after the '+ordinal+' delivery.').strip()
    if args.house_order_event_tiles.exists():
        for level_number,tile in json.loads(args.house_order_event_tiles.read_text(encoding='utf-8')).items():
            level=levels[int(level_number)-1]
            event=level['authoredEvent']
            assert event['kind']=='road_close' and event['trigger']=='first_delivery'
            assert len(tile)==2 and all(isinstance(v,int) and 0<=v<level['grid'] for v in tile)
            assert f'{tile[0]},{tile[1]}' not in level['walls']
            if level.get('phaseChoice'):
                assert level['phaseChoice']['defaultClose']==event['tile']
                assert level['phaseChoice']['alternateClose']!=tile
                level['phaseChoice']['defaultClose']=tile
            event['tile']=tile
    if args.phase_alternate_tiles.exists():
        for level_number,tile in json.loads(args.phase_alternate_tiles.read_text(encoding='utf-8')).items():
            level=levels[int(level_number)-1]
            assert 1801<=int(level_number)<=2000 and level.get('phaseChoice')
            assert len(tile)==2 and all(isinstance(v,int) and 0<=v<level['grid'] for v in tile)
            assert f'{tile[0]},{tile[1]}' not in level['walls']
            assert tile!=level['phaseChoice']['defaultClose']
            level['phaseChoice']['alternateClose']=tile
    if args.chain_open_tiles.exists():
        for level_number,tile in json.loads(args.chain_open_tiles.read_text(encoding='utf-8')).items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and level.get('chainEvent')
            assert len(tile)==2 and all(isinstance(v,int) and 0<=v<level['grid'] for v in tile)
            assert f'{tile[0]},{tile[1]}' not in level['walls']
            assert tile!=level['chainEvent']['close']
            level['chainEvent']['open']=[tile]
    if args.chain_close_tiles.exists():
        for level_number,tile in json.loads(args.chain_close_tiles.read_text(encoding='utf-8')).items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and level.get('chainEvent')
            assert len(tile)==2 and all(isinstance(v,int) and 0<=v<level['grid'] for v in tile)
            assert f'{tile[0]},{tile[1]}' not in level['walls']
            assert tile not in level['chainEvent']['open']
            level['chainEvent']['close']=tile
    for wall_path in (args.extra_walls,args.late_walls,args.variant_walls,args.storm_variant_walls,args.multi_band_walls,args.bridge_detour_walls,args.middle_shortcut_walls,args.house_order_walls):
        if wall_path.exists():
            extra_walls=json.loads(wall_path.read_text(encoding='utf-8'))
            for level_number,walls in extra_walls.items():
                level=levels[int(level_number)-1]
                assert level['n']==int(level_number)
                assert not set(walls).intersection(level['walls'])
                level['walls']=[*level['walls'],*walls]
    if args.hunter_overlays.exists():
        hunters=json.loads(args.hunter_overlays.read_text(encoding='utf-8'))
        for level_number,den in hunters.items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and level.get('hunterDen')
            level['hunterDen']=den
    if args.oneway_overlays.exists():
        overlays=json.loads(args.oneway_overlays.read_text(encoding='utf-8'))
        for level_number,overlay in overlays.items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and 'oneWayTile' not in level
            level.update(overlay)
            level['brief']=(level.get('brief','').rstrip()+' Enter the marked one-way road from its arrow side.').strip()
    if args.bridge_spur_overlays.exists():
        spurs=json.loads(args.bridge_spur_overlays.read_text(encoding='utf-8'))
        assert len(spurs)==100 and set(map(int,spurs))==set(range(701,801))
        for level_number,spur in spurs.items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and level.get('lightBridge')
            level['lightBridge']=spur['bridge']
            level['homes'][spur['houseIndex']]['p']=spur['house']
            level['walls']=sorted((set(level['walls'])|set(spur['addedWalls']))-set(spur['openedCells']))
            level['oneWayTile']=spur['oneWayTile'];level['oneWayFrom']=spur['oneWayFrom']
            level['phase']=spur['phase'];level['phase2']=spur['phase2']
            level['cap']+=spur['capBoost']
            level['bridgeHouseIndex']=spur['houseIndex']
            level['brief']+=' The marked bridge reaches a house lane. Leave through its one-way road.'
    # Assign review tools after all authored overlays; overlays replace full records.
    for l in levels[1000:]:l['reviewPower']=sample_powers[(l['n']-1001)%len(sample_powers)]
    for l in levels[100:200]:l['reviewPower']='anchor_trap'
    for l in levels[150:200]:l['reviewPower']='decoy_light'
    for l in levels[200:300]:l['reviewPower']='reveal_pulse'
    for l in levels[700:800]:l['reviewPower']='light_bridge'
    for l in levels[1400:1500]:l['reviewPower']='freeze_seal' if l['n']%2 else 'rewind'
    for l in levels[200:]:
        # Review-only free actions avoid feeding proposed gem metadata into the old points economy.
        if l.get('repair'):l['repair']['cost']=0
    if args.network_objectives.exists():
        for level_number in json.loads(args.network_objectives.read_text(encoding='utf-8')):
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and level.get('lumenNetwork') and level.get('lightOverloadGate') and level.get('lightTransfer')
            level['networkCircuitRequired']=True
            level['brief']+=' Complete the circuit: charge the relay, cross the voltage gate, and reclaim the receiver light before returning to the depot.'
    if args.express_stops.exists():
        for level_number,stops in json.loads(args.express_stops.read_text(encoding='utf-8')).items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and level.get('transitLink') and len(stops)==2
            assert all(0<=v<level['grid'] for stop in stops for v in stop)
            assert all(f'{stop[0]},{stop[1]}' not in level['walls'] for stop in stops)
            level['transitLink']['stops']=stops
            level['brief']+=' The express stops now connect the far delivery lane to the depot approach.'
    if args.lantern_caps.exists():
        for level_number,new_cap in json.loads(args.lantern_caps.read_text(encoding='utf-8')).items():
            level=levels[int(level_number)-1]
            assert level['n']==int(level_number) and 0<new_cap<level['cap']
            level['cap']=new_cap
    template=(ROOT/'campaign'/'campaign.template.html').read_text(encoding='utf-8')
    html=template.replace('/*__LEVEL_DATA__*/','const LEVELS='+json.dumps(levels,ensure_ascii=False,separators=(',',':'))+';')
    for marker,source in [('/*__ISOMETRIC_SCENE__*/','isometric-scene.js'),('/*__FEEDBACK_CODE__*/','feedback.js'),('/*__UI_ICONS__*/','ui-icons.js'),('/*__ROUTE_SOLVER__*/','route-solver.js')]:
        html=html.replace(marker,(ROOT/'campaign'/source).read_text(encoding='utf-8'))
    chapter_names=[f'{regions[i//10]} · {i%10+1}' for i in range(200)]
    html,count=re.subn(r'^const CHAPTERS=.*;$','const CHAPTERS='+json.dumps(chapter_names,ensure_ascii=False,separators=(',',':'))+';',html,flags=re.M)
    assert count==1
    html=html.replace('const CHAPTERS='+json.dumps(chapter_names,ensure_ascii=False,separators=(',',':'))+';',
        'const CHAPTERS='+json.dumps(chapter_names,ensure_ascii=False,separators=(',',':'))+';\nconst DISTRICTS='+json.dumps(regions,ensure_ascii=False,separators=(',',':'))+';')
    html=html.replace('last-light-courier-campaign-v1','last-light-courier-2000-candidate-v1')
    html=html.replace('<button type="button" id="menuHow">How to play</button>',
        '<button type="button" id="menuHow">How to play</button><button type="button" id="menuFresh">Start fresh test (clear preview save)</button>')
    html=html.replace("$('menuHow').addEventListener('click',()=>{closeMenu();choose(1);state.help=true;render()});",
        "$('menuHow').addEventListener('click',()=>{closeMenu();choose(1);state.help=true;render()});\n"
        "$('menuFresh').addEventListener('click',()=>{if(!window.confirm('Clear this 2,000-level preview save, including progress, points and repairs? The older game save is unaffected.'))return;try{localStorage.removeItem(saveKey)}catch(_){}location.reload()});")
    html=html.replace('</style>','.menuActions #menuFresh{grid-column:1/-1;border-color:#b88e8e;color:#ffe8e8;background:#513b49}</style>')
    html=html.replace('200-level campaign','2,000-map candidate campaign').replace('200-level map','2,000-map review').replace('200-level','2,000-level')
    html=html.replace('All 200 levels','All 2,000 levels').replace('all 200 levels','all 2,000 levels').replace(' / 200',' / 2000')
    html,eyebrow_count=re.subn(r'<div class="eyebrow">[^<]*</div>',
        '<div class="eyebrow">Playable campaign preview | 2,000 levels</div>',html,count=1)
    assert eyebrow_count==1
    html=html.replace('/*__LEVEL_DATA__*/','')
    early_minima=json.loads((ROOT/'campaign/enhanced/early-winding-v1/shortest_routes.json').read_text(encoding='utf-8'))
    assert len(early_minima)==100 and [item['level'] for item in early_minima]==list(range(101,201))
    minimum_data=[{'steps':item['steps'],'freeRepairRequired':bool(item.get('freeRepairRequired'))} for item in early_minima]
    late_exact={str(item['level']):{'steps':item['exactNoPowerSteps'],'freeRepairRequired':False} for item in json.loads(args.exact_late_minima.read_text(encoding='utf-8'))['certified']}
    for item in json.loads(args.exact_transit_minima.read_text(encoding='utf-8'))['certified']:
        key=str(item['level'])
        assert key not in late_exact
        late_exact[key]={'steps':item['exactSteps'],'freeRepairRequired':item['freeRepairRequired']}
    signal_exact={str(item['level']):{'steps':item['exactSignalSteps'],'freeRepairRequired':item['freeRepairRequired']} for item in json.loads(args.exact_signal_minima.read_text(encoding='utf-8'))['certified']}
    html=html.replace('function minimumForLevel(n,bought=false){',
        'const EARLY_MINIMA='+json.dumps(minimum_data,separators=(',',':'))+';\n'
        'const EXACT_LATE_MINIMA='+json.dumps(late_exact,separators=(',',':'))+';\n'
        'const EXACT_SIGNAL_MINIMA='+json.dumps(signal_exact,separators=(',',':'))+';\n'
        'function minimumForLevel(n,bought=false,signaled=false){if(n>200){const proof=signaled?EXACT_SIGNAL_MINIMA[n]:EXACT_LATE_MINIMA[n];return proof&&bought===proof.freeRepairRequired?proof.steps:null}if(n>=101){const proof=EARLY_MINIMA[n-101];return bought===proof.freeRepairRequired?proof.steps:null;}')
    html=html.replace('function shortestSafeRoute(targetMask){',
        'function shortestSafeRoute(targetMask){if(state?.powerUsed||state?.trapTile)return null;'
        'if(level.n>200){const proof=state.phaseSignal?EXACT_SIGNAL_MINIMA[level.n]:EXACT_LATE_MINIMA[level.n];return proof&&!!repaired()===proof.freeRepairRequired&&targetMask===(1<<level.homes.length)-1?proof.steps:null}'
        'if(level.n>=101){const proof=EARLY_MINIMA[level.n-101];return targetMask===(1<<level.homes.length)-1&&!!repaired()===proof.freeRepairRequired?proof.steps:null;}')
    html=html.replace('The first house wakes the shadow; red tiles show moves that would touch it.','Shadows first appear at Level 8. Learn the light and delivery loop here.')
    html=html.replace("2:['Watch the shadow','One delivery still clears this level. After a house lights up, the violet shadow moves on every tap. Its current tile and next tile are unsafe, even if a house is there. Take your time and use the green tiles.']",
        "2:['Choose a house','One delivery still clears this level. Try either nearby house, then return to the depot. Each move costs light, so compare the two routes.']")
    html=html.replace("3:['Optional repair','Light two houses and return to clear this level. A marked obstacle can be repaired with banked points. Tap REPAIR to buy it instantly, or follow the open route without spending.']",
        "3:['Use the detour','Light two houses and return to clear this level. The blocked street changes your route. Follow open roads and keep enough light for the depot.']")
    html=html.replace('Watch the shadow after the first delivery, then choose any green neighbor to keep moving.','Choose any green neighbor to keep moving and compare the house order.')
    html=html.replace("  11:['Fading crossing'", "  8:['First shadow','After the first delivery, a patrol wakes. Its current and next tiles are unsafe. Green neighboring tiles remain safe moves.'],\n  11:['Fading crossing'")
    # The authored closure is deterministic and becomes a real wall immediately
    # after the first delivery. Base movement, reachable-neighbor highlighting,
    # and the board all consume activeWalls(), so the rule stays in one place.
    html=html.replace("if(repaired()&&level.repair?.effect==='open')walls.delete(k(level.repair.tile));return walls;}",
        "if(repaired()&&level.repair?.effect==='open')walls.delete(k(level.repair.tile));if(level.lumenNetwork&&!state?.networkReady)walls.add(k(level.lumenNetwork.relayTile));if(level.stormWind)walls.add(k(state?.eventTriggered?level.stormWind.to:level.stormWind.from));if(level.floodRoad&&state?.floodStart!==null&&state?.floodStart!==undefined&&state.turns-state.floodStart>=level.floodRoad.closeAfter)walls.add(k(level.floodRoad.tile));if(level.aftershock&&!state?.aftershockStabilized&&state?.aftershockStart!==null&&state?.aftershockStart!==undefined&&state.turns-state.aftershockStart>=level.aftershock.closeAfter)walls.add(k(level.aftershock.tile));if(level.dayNightCycle&&!nightPhase())walls.add(k(level.dayNightCycle.moonRoad));if(state?.quakeTriggered&&level.quakeEvent){for(const tile of level.quakeEvent.open)walls.delete(k(tile));walls.add(k(level.quakeEvent.close))}if(state?.chainTriggered&&level.chainEvent){for(const tile of level.chainEvent.open)walls.delete(k(tile));walls.add(k(level.chainEvent.close))}if(state?.eventTriggered&&!state.eventStabilized&&!state.roadRepaired&&level.authoredEvent?.kind==='road_close')walls.add(k(state.phaseSignal&&level.phaseChoice?level.phaseChoice.alternateClose:level.authoredEvent.tile));if(level.hiddenRoad&&!state?.beaconRevealed)walls.add(k(level.hiddenRoad));if(level.collapseTile&&state?.collapseClosed)walls.add(k(level.collapseTile));return walls;}")
    assert html.count("walls.add(k(level.quakeEvent.close))")==1
    html=html.replace("walls.add(k(level.quakeEvent.close))","if(!state?.quakeStabilized&&!state?.quakeRepaired)walls.add(k(level.quakeEvent.close))")
    html=html.replace("if(level.aftershock&&!state?.aftershockStabilized&&state?.aftershockStart",
        "if(level.aftershock&&!state?.aftershockStabilized&&!state?.aftershockRepaired&&state?.aftershockStart")
    html=html.replace("if(level.collapseTile&&state?.collapseClosed)walls.add(k(level.collapseTile))",
        "if(level.collapseTile&&state?.collapseClosed&&!state?.collapseRepaired)walls.add(k(level.collapseTile))")
    html=html.replace('help:!!TUTORIALS[level.n]&&!save.seenTutorials[level.n]};',
        'eventTriggered:false,eventStabilized:false,roadRepaired:false,quakeTriggered:false,quakeStabilized:false,chainTriggered:false,phaseSignal:false,floodStart:null,aftershockStart:null,aftershockStabilized:false,nightStart:null,spawnerTurn:null,networkReady:false,networkCharged:false,networkChargeTurn:null,transferStored:false,transferCollected:false,transferCollectedTurn:null,freezeTurns:0,lastMoveState:null,powerUsed:false,usedPowers:{},selectedPower:level.reviewPower||null,trapArmed:false,trapTile:null,trapPatrol:0,trappedPatrol:0,decoyArmed:false,decoyTile:null,decoyPatrol:0,decoyTargetPhase:0,decoyTurns:0,rechargeLit:false,rechargeDrained:false,leechTriggered:false,beaconRevealed:false,collapseUsed:false,bridgeBuilt:false,hunterPos:level.hunterDen?[...level.hunterDen]:null,hunterAge:0,help:!!TUTORIALS[level.n]&&!save.seenTutorials[level.n]};')
    html=html.replace('quakeStabilized:false,','quakeStabilized:false,quakeRepaired:false,')
    html=html.replace('aftershockStabilized:false,','aftershockStabilized:false,aftershockRepaired:false,')
    html=html.replace('collapseUsed:false,','collapseUsed:false,collapseRepaired:false,')
    html=html.replace("function nextShadow(phase,patrol){return patrol?.[(phase+1)%patrol.length]}",
        "function nextShadow(phase,patrol){return patrol?.[(phase+1)%patrol.length]}function transitJump(p,s=state){if(!level.transitLink||!s.active)return false;const [a,b]=level.transitLink.stops;return eq(s.pos,a)&&eq(p,b)||eq(s.pos,b)&&eq(p,a)}function nextShadowPhase(index,s=state){const patrol=index===1?level.patrol:level.patrol2,phase=index===1?s.phase:s.phase2;if(!patrol)return phase;if(s.decoyTurns>0&&s.decoyPatrol===index){const target=s.decoyTargetPhase;if(phase===target)return phase;const cw=(target-phase+patrol.length)%patrol.length,ccw=(phase-target+patrol.length)%patrol.length;return (phase+(cw<=ccw?1:-1)+patrol.length)%patrol.length}return (phase+1)%patrol.length}")
    html=html.replace("function homeIndex(p){return level.homes.findIndex(h=>eq(h.p,p))}",
        "function homeIndex(p){return level.homes.findIndex((h,i)=>eq(h.p,p)&&(i!==level.hiddenHouseIndex||state.beaconRevealed))}")
    hunter_code="""function hunterNext(target,s=state){if(!level.hunterDen)return null;const current=s.hunterPos||level.hunterDen,walls=activeWalls(),size=level.grid||8,dirs=[[0,-1],[1,0],[0,1],[-1,0]],queue=[target],dist=new Map([[k(target),0]]);for(let i=0;i<queue.length;i++){const p=queue[i],d=dist.get(k(p));for(const [dx,dy] of dirs){const q=[p[0]+dx,p[1]+dy],id=k(q);if(q[0]<0||q[1]<0||q[0]>=size||q[1]>=size||walls.has(id)||dist.has(id))continue;dist.set(id,d+1);queue.push(q)}}let best=current,bestDistance=Infinity;for(const [dx,dy] of dirs){const q=[current[0]+dx,current[1]+dy],id=k(q);if(q[0]<0||q[1]<0||q[0]>=size||q[1]>=size||walls.has(id))continue;const distance=dist.get(id)??Infinity;if(distance<bestDistance){best=q;bestDistance=distance}}return best}
"""
    html=html.replace("function featureAt(p){",hunter_code+"function featureAt(p){")
    html=html.replace("function featureAt(p){",
        "function nightPhase(s=state){if(!level.dayNightCycle)return !!s.eventTriggered;if(s.nightStart===null)return false;const cycle=level.dayNightCycle.nightMoves+level.dayNightCycle.dayMoves;return (s.turns-s.nightStart)%cycle<level.dayNightCycle.nightMoves}function featureAt(p){")
    html=html.replace("function featureAt(p){if(eq(p,level.fade))",
        "function featureAt(p){if(eq(p,level.transitLink?.stops[0])||eq(p,level.transitLink?.stops[1]))return 'transitstop';if(eq(p,level.lumenNetwork?.relayTile))return 'lumenrelay';if(eq(p,level.nightfall?.tile))return 'duskroad';if(eq(p,level.lightBridge))return 'lightbridge';if(eq(p,level.shadowDoor))return 'shadowdoor';if(eq(p,level.shadowLock))return 'shadowlock';if(eq(p,level.oneWayTile))return 'oneway';if(eq(p,level.collapseTile))return 'collapse';if(eq(p,level.rechargeHouse))return 'recharge';if(eq(p,level.fade))")
    html=html.replace("if(eq(p,level.rechargeHouse))return 'recharge';",
        "if(eq(p,level.hunterDen))return 'hunterden';if(eq(p,level.rechargeHouse))return 'recharge';")
    html=html.replace("if(eq(p,level.lumenNetwork?.relayTile))return 'lumenrelay';",
        "if(eq(p,level.lightTransfer?.receiver))return 'lightreceiver';if(eq(p,level.lumenNetwork?.relayTile))return 'lumenrelay';")
    html=html.replace("if(eq(p,level.lumenNetwork?.relayTile))return 'lumenrelay';",
        "if(eq(p,level.lightOverloadGate?.tile))return 'overloadgate';if(eq(p,level.lumenNetwork?.relayTile))return 'lumenrelay';")
    html=html.replace("if(eq(p,level.lightTransfer?.receiver))return 'lightreceiver';",
        "if(eq(p,level.dayNightCycle?.moonRoad))return 'moonroad';if(eq(p,level.floodRoad?.tile))return 'floodroad';if(eq(p,level.lightTransfer?.receiver))return 'lightreceiver';")
    html=html.replace("if(eq(p,level.dayNightCycle?.moonRoad))return 'moonroad';",
        "if(eq(p,level.aftershock?.tile))return 'aftershockroad';if(eq(p,level.dayNightCycle?.moonRoad))return 'moonroad';")
    html=html.replace("Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])!==1",
        "!(Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])===1||transitJump(p))")
    html=html.replace("const wasNear=shadowNear(),cost=", "const usingTransit=transitJump(p),wasNear=shadowNear(),cost=")
    html=html.replace("function open(p){const walls=activeWalls();",
        "function shadowDoorOpen(s=state){if(!level.shadowDoor||!s.active)return false;const patrol=level.lockPatrol===1?level.patrol:level.patrol2,phase=level.lockPatrol===1?s.phase:s.phase2;return !!patrol&&eq(patrol[phase],level.shadowLock)}function spawnCellCount(s=state,predict=false){if(!level.shadowSpawner||s.spawnerTurn===null)return 0;const age=s.turns-s.spawnerTurn+(predict?1:0);return age>=6?4:age>=3?2:1}function open(p){const walls=activeWalls();")
    html=html.replace("function open(p){const walls=activeWalls();",
        "function spawnCells(s=state,predict=false){if(!level.shadowSpawner||s.spawnerTurn===null)return [];const age=s.turns-s.spawnerTurn+(predict?1:0);if(level.mergeSplit&&age>=level.mergeSplit.splitAfter)return level.mergeSplit.splitCells;if(level.mergeSplit&&age>=level.mergeSplit.mergeAfter)return level.mergeSplit.mergedCells;return level.shadowSpawner.stages.slice(0,spawnCellCount(s,predict))}function open(p){const walls=activeWalls();")
    html=html.replace("if(eq(p,level.fade)&&state.fade===0)return false;",
        "if(eq(p,level.lightBridge)&&!state.bridgeBuilt)return false;if(eq(p,level.shadowDoor)&&!shadowDoorOpen())return false;if(eq(p,level.fade)&&state.fade===0)return false;")
    html=html.replace("cost=eq(p,level.dark)&&!(repaired()&&level.repair?.effect==='lamp')?2:1;",
        "cost=(usingTransit?level.transitLink.rideLight:(eq(p,level.dark)&&!(repaired()&&level.repair?.effect==='lamp')?2:1))+(level.nightfall&&state.eventTriggered&&eq(p,level.nightfall.tile)?level.nightfall.extraLight:0);")
    html=html.replace("||!open(p))return false;return !shadowBlocked(p)}",
        "||!open(p)||(level.oneWayTile&&eq(p,level.oneWayTile)&&!eq(state.pos,level.oneWayFrom)))return false;return !shadowBlocked(p)}")
    html=html.replace("return !shadowBlocked(p)}",
        "if(level.lightOverloadGate&&eq(p,level.lightOverloadGate.tile)){const after=state.light-1;if(after<level.lightOverloadGate.minLight||after>level.lightOverloadGate.maxLight)return false}return !shadowBlocked(p)}")
    html=html.replace("if(level.lightOverloadGate&&eq(p,level.lightOverloadGate.tile)){const after=state.light-1;",
        "if(level.floodRoad&&state.floodStart!==null&&eq(p,level.floodRoad.tile)&&state.turns-state.floodStart+1>=level.floodRoad.closeAfter)return false;if(level.lightOverloadGate&&eq(p,level.lightOverloadGate.tile)){const after=state.light-1;")
    html=html.replace("return !shadowBlocked(p)}",
        "if(level.networkCircuitRequired&&eq(p,level.depot)&&state.mask===(1<<level.homes.length)-1&&!(state.networkCharged&&state.overloadCrossed&&state.transferCollected))return false;return !shadowBlocked(p)}")
    html=html.replace("if(level.floodRoad&&state.floodStart!==null&&eq(p,level.floodRoad.tile)",
        "if(level.aftershock&&!state.aftershockStabilized&&!state.aftershockRepaired&&state.aftershockStart!==null&&eq(p,level.aftershock.tile)&&state.turns-state.aftershockStart+1>=level.aftershock.closeAfter)return false;if(level.floodRoad&&state.floodStart!==null&&eq(p,level.floodRoad.tile)")
    html=html.replace("const safe=adjacent&&legal(p);const danger=adjacent&&open(p)&&!safe",
        "const safe=(adjacent||transitJump(p))&&legal(p);const danger=(adjacent||transitJump(p))&&open(p)&&!safe")
    html=html.replace("if([[x+1,y],[x-1,y],[x,y+1],[x,y-1]].some(legal))return false;",
        "const candidates=[[x+1,y],[x-1,y],[x,y+1],[x,y-1]];if(level.transitLink&&state.active){const [a,b]=level.transitLink.stops;if(eq(state.pos,a))candidates.push(b);else if(eq(state.pos,b))candidates.push(a)}if(candidates.some(legal))return false;")
    html=html.replace("for(const [patrol,phase] of [[level.patrol,s.phase],[level.patrol2,s.phase2]])if(patrol&&(eq(p,patrol[phase])||eq(p,nextShadow(phase,patrol))))return true;",
        "for(const [patrol,phase,index] of [[level.patrol,s.phase,1],[level.patrol2,s.phase2,2]])if(patrol&&(eq(p,patrol[phase])||(s.trappedPatrol!==index&&s.freezeTurns<=0&&eq(p,patrol[nextShadowPhase(index,s)]))))return true;")
    html=html.replace("function move(p){if(!$('hintDialog').hidden||!legal(p))return false;",
        "function move(p){if(!$('hintDialog').hidden||!legal(p))return false;const rewindSnapshot=JSON.parse(JSON.stringify({...state,lastMoveState:null}));")
    html=html.replace("if(!$('hintDialog').hidden||!legal(p))return false;const rewindSnapshot",
        "if(!$('hintDialog').hidden||!legal(p)){if(level.lightOverloadGate&&Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])===1&&eq(p,level.lightOverloadGate.tile)){const after=state.light-1;if(after<level.lightOverloadGate.minLight||after>level.lightOverloadGate.maxLight){setStatus('Voltage gate refused entry','Light after entry must be '+level.lightOverloadGate.minLight+'–'+level.lightOverloadGate.maxLight,'Spend light elsewhere or adjust your route, then return to the marked gate.');render()}}return false}const rewindSnapshot")
    html=html.replace("if(!$('hintDialog').hidden||!legal(p)){if(level.lightOverloadGate",
        "if(!$('hintDialog').hidden||!legal(p)){if(level.networkCircuitRequired&&eq(p,level.depot)&&state.mask===(1<<level.homes.length)-1){const missing=[!state.networkCharged?'relay':null,!state.overloadCrossed?'voltage gate':null,!state.transferCollected?'receiver':null].filter(Boolean);if(missing.length){setStatus('Circuit incomplete','Visit '+missing.join(', '),'Charge the relay, cross the voltage gate at its shown light range, then reclaim the receiver light before returning.');render()}}if(level.lightOverloadGate")
    html=html.replace("state.light-=cost;state.turns++;FEEDBACK.emit('step');",
        "state.light-=cost;state.turns++;state.lastMoveState=rewindSnapshot;FEEDBACK.emit('step');")
    html=html.replace("if(level.echo&&s.trail.length){if(eq(p,s.trail[s.trail.length-1])",
        "if(level.sentinelCenter&&Math.max(Math.abs(p[0]-level.sentinelCenter[0]),Math.abs(p[1]-level.sentinelCenter[1]))<=1)return true;if(level.shadowSpawner&&spawnCells(s,true).some(tile=>eq(tile,p)))return true;if(level.echo&&s.trail.length){if(eq(p,s.trail[s.trail.length-1])")
    html=html.replace("if(level.echo&&s.trail.length){if(eq(p,s.trail[s.trail.length-1])",
        "if(level.hunterDen&&s.active){const hunter=s.hunterPos||level.hunterDen;if(eq(p,hunter)||((s.hunterAge+1)%2===0&&eq(p,hunterNext(p,s))))return true}if(level.echo&&s.trail.length){if(eq(p,s.trail[s.trail.length-1])")
    html=html.replace("if(level.sentinelCenter&&Math.max(Math.abs(p[0]-level.sentinelCenter[0])",
        "if(level.shadowInfluence2x2&&s.active&&level.shadowInfluence2x2.cells.some(tile=>eq(tile,p)))return true;if(level.sentinelCenter&&Math.max(Math.abs(p[0]-level.sentinelCenter[0])")
    html=html.replace("1+!!level.patrol2+!!level.echo","(!level.noShadow?1:0)+!!level.patrol2+!!level.echo+!!level.sentinelCenter+!!level.shadowSpawner+!!level.hunterDen")
    html=html.replace("eq(p,level.patrol2?.[state.phase2]));const isEcho=",
        "eq(p,level.patrol2?.[state.phase2])||eq(p,level.sentinelCenter));const isEcho=")
    html=html.replace("||eq(p,level.sentinelCenter));const isEcho=",
        "||eq(p,level.sentinelCenter)||(level.hunterDen&&eq(p,state.hunterPos)));const isEcho=")
    html=html.replace("if(state.active){state.phase=(state.phase+1)%4;if(level.patrol2)state.phase2=(state.phase2+1)%4;}",
        "if(state.active&&state.freezeTurns<=0){if(state.trappedPatrol!==1)state.phase=nextShadowPhase(1);if(level.patrol2&&state.trappedPatrol!==2)state.phase2=nextShadowPhase(2)}if(state.decoyTurns>0)state.decoyTurns--;if(state.freezeTurns>0)state.freezeTurns--;")
    html=html.replace("render();ISO.move(prev,p,oldShadow,",
        "render();if(usingTransit){ISO.cancel();ISO.render()}else ISO.move(prev,p,oldShadow,")
    html=html.replace("if(eq(p,level.switch))state.gate=4;",
        "if(eq(p,level.switch))state.gate=4;if(state.trapTile&&state.active&&!state.trappedPatrol){const patrol=state.trapPatrol===1?level.patrol:level.patrol2,phase=state.trapPatrol===1?state.phase:state.phase2;if(patrol&&eq(state.trapTile,patrol[phase]))state.trappedPatrol=state.trapPatrol;}")
    html=html.replace("state.pos=[...p];if(level.echo)",
        "state.pos=[...p];if(level.lumenNetwork&&state.networkReady&&!state.networkCharged&&eq(p,level.lumenNetwork.relayTile)){state.networkCharged=true;state.networkChargeTurn=state.turns;state.light=Math.min(cap(),state.light+level.lumenNetwork.charge)}if(level.collapseTile){if(eq(prev,level.collapseTile)&&!eq(p,level.collapseTile))state.collapseClosed=true;if(eq(p,level.collapseTile))state.collapseUsed=true;}if(level.echo)")
    html=html.replace("state.pos=[...p];if(level.lumenNetwork",
        "state.pos=[...p];if(level.lightOverloadGate&&eq(p,level.lightOverloadGate.tile))state.overloadCrossed=true;if(level.hunterDen&&state.active){state.hunterAge++;if(state.hunterAge%2===0)state.hunterPos=hunterNext(p,state)}if(level.lumenNetwork")
    html=html.replace("state.light=Math.min(cap(),state.light+level.lumenNetwork.charge)}if(level.collapseTile)",
        "state.transferStored=!!level.lightTransfer;state.light=Math.min(cap(),state.light+level.lumenNetwork.charge-(level.lightTransfer?.storedLight||0))}if(level.lightTransfer&&state.transferStored&&!state.transferCollected&&eq(p,level.lightTransfer.receiver)){state.light=Math.min(cap(),state.light+level.lightTransfer.storedLight);state.transferCollected=true;state.transferCollectedTurn=state.turns}if(level.collapseTile)")
    html=html.replace("state.active=true;FEEDBACK.emit('house');setStatus('Delivery complete',level.homes[hi].name+' is lit','+'+level.homes[hi].points+' points at risk. Two light restored. Return to the depot to bank.');",
        "state.active=true;if(hi===level.beaconHouseIndex)state.beaconRevealed=true;if(level.quakeEvent&&!state.quakeTriggered)state.quakeTriggered=true;if(level.chainEvent&&!state.chainTriggered&&popcount(state.mask)>=2)state.chainTriggered=true;if(level.shadowSpawner&&state.spawnerTurn===null)state.spawnerTurn=state.turns;if(level.lumenNetwork&&hi===level.lumenNetwork.sourceHouseIndex)state.networkReady=true;if(level.authoredEvent&&!state.eventTriggered)state.eventTriggered=true;FEEDBACK.emit('house');setStatus('Delivery complete',level.homes[hi].name+' is lit','+'+level.homes[hi].points+' points at risk. Two light restored. '+(hi===level.beaconHouseIndex?'The Beacon revealed a hidden house and opened its road.':state.chainTriggered&&popcount(state.mask)===2?'The second delivery closed an earlier street and opened a new side road.':state.quakeTriggered?'An earthquake closed a road and opened another.':level.shadowSpawner?'The shadow nest woke. Its 2×2 area grows after three and six more moves.':level.lumenNetwork?'The source house powered a sealed relay road. Crossing it restores two light once.':level.phaseChoice?state.phaseSignal?'Your signal kept the normal corridor open. The alternate road closed.':'You saved one light. The normal road closed; take its detour.':state.eventTriggered?(state.eventStabilized?'Your stabilizer kept the marked road open.':'The marked road has closed. Take the side street.'):'Return to the depot to bank.'));")
    html=html.replace("state.active=true;if(hi===level.beaconHouseIndex)",
        "state.active=!level.noShadow;if(hi===level.beaconHouseIndex)")
    html=html.replace("if(level.shadowSpawner&&state.spawnerTurn===null)state.spawnerTurn=state.turns;",
        "if(level.floodRoad&&state.floodStart===null)state.floodStart=state.turns;if(level.shadowSpawner&&state.spawnerTurn===null)state.spawnerTurn=state.turns;")
    html=html.replace("if(level.floodRoad&&state.floodStart===null)state.floodStart=state.turns;",
        "if(level.floodRoad&&state.floodStart===null)state.floodStart=state.turns;if(level.dayNightCycle&&state.nightStart===null)state.nightStart=state.turns;")
    html=html.replace("if(level.floodRoad&&state.floodStart===null)state.floodStart=state.turns;",
        "if(level.aftershock&&state.aftershockStart===null)state.aftershockStart=state.turns;if(level.floodRoad&&state.floodStart===null)state.floodStart=state.turns;")
    html=html.replace("level.phaseChoice?state.phaseSignal?'Your signal kept the normal corridor open. The alternate road closed.':'You saved one light. The normal road closed; take its detour.'",
        "level.phaseChoice?(state.eventStabilized?'Your stabilizer kept the selected road open.':state.phaseSignal?'Your signal kept the normal corridor open. The alternate road closed.':'The normal road closed; take its detour.')")
    html=html.replace("'The source house powered a sealed relay road. Crossing it restores two light once.'",
        "level.lightTransfer?'The source house powered the relay. It gives you one light and sends one to the marked receiver.':'The source house powered a sealed relay road. Crossing it restores two light once.'")
    html=html.replace("level.shadowSpawner?'The shadow nest woke.",
        "level.floodRoad?'The low road floods in four moves. Cross it now.':level.shadowSpawner?'The shadow nest woke.")
    html=html.replace("level.floodRoad?'The low road floods in four moves. Cross it now.'",
        "level.dayNightCycle?'Night begins now: six moves of fog and a costly dusk road, then four moves of day. The moon road opens only at night.':level.floodRoad?'The low road floods in four moves. Cross it now.'")
    html=html.replace("'An earthquake closed a road and opened another.'",
        "level.aftershock?'First quake changed roads. Aftershock in eight moves.':'An earthquake closed a road and opened another.'")
    html=html.replace("else if(eq(p,level.depot)&&state.mask){const count=popcount(state.mask);",
        "else if(level.rechargeHouse&&eq(p,level.rechargeHouse)&&!state.rechargeLit){state.rechargeLit=true;state.light=Math.min(cap(),state.light+(level.rechargeAmount||4));setStatus('Recharge house lit','Four light restored',state.rechargeDrained?'You relit the house after the Leech drained it.':'A Leech patrol can extinguish this house when it comes near.');}else if(eq(p,level.depot)&&state.mask){const count=popcount(state.mask);")
    html=html.replace("  endIfNoMoves();\n  if(state.active",
        "  if(level.rechargeHouse&&state.rechargeLit&&!state.leechTriggered&&state.active&&!state.done&&!state.failed){const patrol=level.leechPatrol===1?level.patrol:level.patrol2,phase=level.leechPatrol===1?state.phase:state.phase2,shadow=patrol?.[phase];if(shadow&&Math.abs(shadow[0]-level.rechargeHouse[0])+Math.abs(shadow[1]-level.rechargeHouse[1])<=1){state.rechargeLit=false;state.rechargeDrained=true;state.leechTriggered=true;setStatus('Leech drained the house','Recharge light went out','The house remains on the map. Reach it again to relight it and gain four light.');}}\n  endIfNoMoves();\n  if(state.active")
    html=html.replace("  if(level.rechargeHouse&&state.rechargeLit&&!state.leechTriggered",
        "  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))setStatus('Causeway collapsed','The road behind you is gone','Continue forward or find another route home.');\n  if(level.rechargeHouse&&state.rechargeLit&&!state.leechTriggered")
    html=html.replace("  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))",
        "  if(level.lumenNetwork&&state.networkChargeTurn===state.turns)setStatus('Light relay charged','Two lantern light restored','The relay road stays open, but its charge is spent.');\n  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))")
    html=html.replace("setStatus('Light relay charged','Two lantern light restored','The relay road stays open, but its charge is spent.');",
        "setStatus('Light relay charged',level.lightTransfer?'One light restored; one sent ahead':'Two lantern light restored',level.lightTransfer?'The marked receiver holds the other light beyond the voltage gate.':'The relay road stays open, but its charge is spent.');")
    html=html.replace("  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))",
        "  if(level.lightTransfer&&state.transferCollectedTurn===state.turns)setStatus('Stored light reclaimed','One lantern light restored','The relay receiver is now empty.');\n  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))")
    html=html.replace("  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))",
        "  if(level.floodRoad&&state.floodStart!==null&&state.turns-state.floodStart===level.floodRoad.closeAfter)setStatus('Low road flooded','Marked road is closed','Use the higher streets to finish the delivery.');\n  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))")
    html=html.replace("  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))",
        "  if(level.aftershock&&!state.aftershockStabilized&&state.aftershockStart!==null&&state.turns-state.aftershockStart===level.aftershock.closeAfter)setStatus('Aftershock','Marked road collapsed','The crossing is closed. Continue on the remaining streets.');\n  if(level.collapseTile&&state.collapseClosed&&eq(prev,level.collapseTile))")
    html=html.replace("  endIfNoMoves();\n  if(state.active",
        "  if(usingTransit&&!state.done&&!state.failed)setStatus('Transit ride','Two lantern light spent','You crossed the region in one turn. The shadows advanced once.');\n  endIfNoMoves();\n  if(state.active")
    html=html.replace("if(level.patrol2)features.push('second shadow');$('mechanics').textContent=features.length?",
        "if(level.patrol2)features.push('second shadow');if(level.sentinelCenter)features.push('stationary 3×3 Sentinel');if(level.shadowSpawner)features.push(state.spawnerTurn===null?'shadow nest wakes after first delivery':'shadow nest '+spawnCellCount()+'/4 cells active');if(level.lumenNetwork)features.push(state.networkCharged?'relay charge spent':state.networkReady?'relay open; +2 light once':'source house unlocks light relay');if(level.lightBridge)features.push(state.bridgeBuilt?'light bridge built':'light bridge costs one extra light');if(level.shadowDoor)features.push(shadowDoorOpen()?'Shadow Door OPEN':'Shadow Door waits for patrol on lock');if(level.oneWayTile)features.push('one-way road');if(level.collapseTile)features.push(state.collapseClosed?'causeway CLOSED':'causeway collapses after use');if(level.hiddenRoad)features.push(state.beaconRevealed?'Beacon revealed hidden house and road':'Beacon house reveals hidden house and road');if(level.rechargeHouse)features.push(state.rechargeDrained?'Leech drained recharge house':'Leech can drain recharge house');if(level.quakeEvent)features.push(state.quakeTriggered?'earthquake changed roads':'first house triggers earthquake');if(level.stormWind)features.push(state.eventTriggered?'wind moved roadblock':'wind moves roadblock after first delivery');if(level.nightfall)features.push(state.eventTriggered?'fog hides distant streets; dusk road costs two light':'first delivery brings fog and a dusk road');if(level.authoredEvent)features.push(state.eventTriggered?(state.eventStabilized||state.roadRepaired?'marked road OPEN':'marked road CLOSED'):'marked road closes after first delivery');$('mechanics').textContent=features.length?")
    html=html.replace("if(level.sentinelCenter)features.push('stationary 3×3 Sentinel');",
        "if(level.shadowInfluence2x2)features.push(state.active?'2×2 shadow field ACTIVE':'2×2 shadow field wakes after first delivery');if(level.sentinelCenter)features.push('stationary 3×3 Sentinel');")
    html=html.replace("if(level.lightBridge)features.push(",
        "if(level.lightOverloadGate)features.push('voltage gate accepts '+level.lightOverloadGate.minLight+'–'+level.lightOverloadGate.maxLight+' light after entry');if(level.lightBridge)features.push(")
    html=html.replace("if(level.quakeEvent)features.push(",
        "if(level.aftershock)features.push(state.aftershockStabilized?'aftershock road STABILIZED':state.aftershockStart===null?'first delivery starts eight-move aftershock':state.turns-state.aftershockStart>=level.aftershock.closeAfter?'aftershock road CLOSED':'aftershock in '+(level.aftershock.closeAfter-(state.turns-state.aftershockStart))+' moves');if(level.quakeEvent)features.push(")
    html=html.replace("if(level.sentinelCenter)features.push(",
        "if(level.hunterDen)features.push(state.active?'Hunter pursues every second move':'Hunter wakes after first delivery');if(level.sentinelCenter)features.push(")
    html=html.replace("if(level.lumenNetwork)features.push(",
        "if(level.lightTransfer)features.push(state.transferCollected?'remote light reclaimed':state.transferStored?'one light stored at marked receiver':'relay will split two light between courier and receiver');if(level.lumenNetwork)features.push(")
    html=html.replace("if(level.lightTransfer)features.push(",
        "if(level.networkCircuitRequired)features.push('circuit objective: relay '+(state.networkCharged?'done':'needed')+' · voltage gate '+(state.overloadCrossed?'done':'needed')+' · receiver '+(state.transferCollected?'done':'needed'));if(level.lightTransfer)features.push(")
    html=html.replace("if(level.stormWind)features.push(",
        "if(level.floodRoad)features.push(state.floodStart===null?'first delivery starts four-move flood countdown':state.turns-state.floodStart>=level.floodRoad.closeAfter?'low road FLOODED':'low road floods in '+(level.floodRoad.closeAfter-(state.turns-state.floodStart))+' moves');if(level.stormWind)features.push(")
    html=html.replace("if(level.nightfall)features.push(state.eventTriggered?'fog hides distant streets; dusk road costs two light':'first delivery brings fog and a dusk road');",
        "if(level.nightfall)features.push(level.dayNightCycle?(state.nightStart===null?'first delivery starts day/night cycle':(nightPhase()?'NIGHT':'DAY')+' · '+(nightPhase()?level.dayNightCycle.nightMoves-(state.turns-state.nightStart)%10:10-(state.turns-state.nightStart)%10)+' moves until change · moon road '+(nightPhase()?'OPEN':'CLOSED')):state.eventTriggered?'fog hides distant streets; dusk road costs two light':'first delivery brings fog and a dusk road');")
    html=html.replace("'Watch the shadow after the first delivery.';",
        "level.noShadow?'Deliver light and plan your return to the depot.':'Watch the shadow after the first delivery.';")
    html=html.replace("'relay open; +2 light once'",
        "level.lightTransfer?'relay gives 1 here and stores 1 remotely':'relay open; +2 light once'")
    html=html.replace("if(level.shadowSpawner)features.push(state.spawnerTurn===null?'shadow nest wakes after first delivery':'shadow nest '+spawnCellCount()+'/4 cells active');",
        "if(level.shadowSpawner)features.push(state.spawnerTurn===null?'shadow nest wakes after first delivery':level.mergeSplit&&state.turns-state.spawnerTurn>=level.mergeSplit.splitAfter?'merged shadow split into 2 cells':level.mergeSplit&&state.turns-state.spawnerTurn>=level.mergeSplit.mergeAfter?'shadows merged into a 3×3 threat':'shadow nest '+spawnCellCount()+'/4 cells active');")
    html=html.replace("const closed=(feature==='fade'",
        "const closed=(feature==='lightbridge'&&!state.bridgeBuilt)||(feature==='shadowdoor'&&!shadowDoorOpen())||(feature==='fade'")
    html=html.replace("const closed=(feature==='lightbridge'&&!state.bridgeBuilt)",
        "const closed=(feature==='overloadgate'&&(state.light-1<level.lightOverloadGate.minLight||state.light-1>level.lightOverloadGate.maxLight))||(feature==='lightbridge'&&!state.bridgeBuilt)")
    html=html.replace("safe?'safe':'',danger?'danger':'',isCourier&&base?'occupied':'']",
        "safe?'safe':'',danger?'danger':'',level.authoredEvent&&eq(p,level.authoredEvent.tile)?'eventRoad':'',level.quakeEvent&&eq(p,level.quakeEvent.close)?'quakeClose':'',level.quakeEvent&&level.quakeEvent.open.some(tile=>eq(p,tile))?'quakeOpen':'',state.trapArmed&&canTrapAt(p)?'trapTarget':'',state.trapTile&&eq(p,state.trapTile)?'trapPlaced':'',state.active&&level.sentinelCenter&&Math.max(Math.abs(x-level.sentinelCenter[0]),Math.abs(y-level.sentinelCenter[1]))<=1?'sentinelZone':'',level.shadowSpawner&&level.shadowSpawner.stages.some(tile=>eq(tile,p))?'spawnerZone':'',level.nightfall&&state.eventTriggered&&Math.max(Math.abs(x-state.pos[0]),Math.abs(y-state.pos[1]))>level.nightfall.fogRadius?'fogged':'',isCourier&&base?'occupied':'']")
    html=html.replace("level.shadowSpawner&&level.shadowSpawner.stages.some(tile=>eq(tile,p))?'spawnerZone':'',",
        "level.shadowSpawner&&(level.shadowSpawner.stages.some(tile=>eq(tile,p))||level.mergeSplit?.mergedCells.some(tile=>eq(tile,p)))?'spawnerZone':'',")
    html=html.replace("level.shadowSpawner&&(level.shadowSpawner.stages.some(tile=>eq(tile,p))||level.mergeSplit?.mergedCells.some(tile=>eq(tile,p)))?'spawnerZone':'',",
        "level.shadowSpawner&&(level.shadowSpawner.stages.some(tile=>eq(tile,p))||level.mergeSplit?.mergedCells.some(tile=>eq(tile,p)))?'spawnerZone':'',level.shadowInfluence2x2&&level.shadowInfluence2x2.cells.some(tile=>eq(tile,p))?'influenceZone':'',state.active&&level.shadowInfluence2x2&&level.shadowInfluence2x2.cells.some(tile=>eq(tile,p))?'influenceActive':'',")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.shadowInfluence2x2&&eq(p,level.shadowInfluence2x2.origin))badge+='<span class=\"timer\">'+(state.active?'2×2 BLOCKED':'2×2 WAKES')+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace('</style>','.cell.influenceZone:not(.wall){box-shadow:inset 0 0 0 2px #9a8db4;background:#4a4058}.cell.influenceZone.influenceActive:not(.wall){background:#7c3d67;box-shadow:inset 0 0 0 2px #e996b9}</style>')
    html=html.replace("level.quakeEvent&&eq(p,level.quakeEvent.close)?'quakeClose':'',",
        "level.quakeEvent&&eq(p,level.quakeEvent.close)?'quakeClose':'',level.chainEvent&&eq(p,level.chainEvent.close)?'chainClose':'',level.chainEvent&&level.chainEvent.open.some(tile=>eq(p,tile))?'chainOpen':'',")
    html=html.replace("level.authoredEvent&&eq(p,level.authoredEvent.tile)?'eventRoad':'',",
        "level.authoredEvent&&eq(p,level.authoredEvent.tile)?'eventRoad':'',level.phaseChoice&&eq(p,level.phaseChoice.alternateClose)?'phaseAlternate':'',")
    html=html.replace("if(isRepair&&!repaired())badge+='<span class=\"timer repairBadge\">REPAIR</span>';",
        "if(isRepair&&!repaired())badge+='<span class=\"timer repairBadge\">REPAIR</span>';if(level.authoredEvent&&eq(p,level.authoredEvent.tile)&&!level.phaseChoice)badge+='<span class=\"timer\">'+(state.eventTriggered&&!state.eventStabilized&&!state.roadRepaired?'CLOSED':'CLOSES')+'</span>';if(level.hiddenRoad&&eq(p,level.hiddenRoad))badge+='<span class=\"timer\">'+(state.beaconRevealed?'OPEN':'SEALED')+'</span>';if(level.lightBridge&&eq(p,level.lightBridge))badge+='<span class=\"timer\">'+(state.bridgeBuilt?'BRIDGE LIT':state.active?'SPEND 1 LIGHT':'DORMANT')+'</span>';if(level.shadowDoor&&eq(p,level.shadowDoor))badge+='<span class=\"timer\">'+(shadowDoorOpen()?'OPEN':'SHADOW DOOR')+'</span>';if(level.shadowLock&&eq(p,level.shadowLock))badge+='<span class=\"timer\">LOCK</span>';if(level.oneWayTile&&eq(p,level.oneWayTile)){const dx=p[0]-level.oneWayFrom[0],dy=p[1]-level.oneWayFrom[1];badge+='<span class=\"timer\">ONE WAY '+(dx===1?'→':dx===-1?'←':dy===1?'↓':'↑')+'</span>'}if(level.collapseTile&&eq(p,level.collapseTile))badge+='<span class=\"timer\">'+(state.collapseClosed?'CLOSED':'FRAGILE')+'</span>';")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(state.trapTile&&eq(p,state.trapTile))badge+='<span class=\"timer\">'+(state.trappedPatrol?'TRAPPED':'TRAP')+'</span>';if(hi===level.beaconHouseIndex)badge+='<span class=\"timer\">BEACON</span>';if(level.rechargeHouse&&eq(p,level.rechargeHouse))badge+='<span class=\"timer\">'+(state.rechargeLit?'RECHARGED':state.rechargeDrained?'DRAINED':'RECHARGE')+'</span>';if(level.leechPatrol&&state.active&&eq(p,(level.leechPatrol===1?level.patrol[state.phase]:level.patrol2[state.phase2])))badge+='<span class=\"done\">LEECH</span>';if(level.sentinelCenter&&eq(p,level.sentinelCenter))badge+='<span class=\"done\">SENTINEL</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.quakeEvent&&eq(p,level.quakeEvent.close))badge+='<span class=\"timer\">'+(state.quakeTriggered?'QUAKE CLOSED':'QUAKE CLOSES')+'</span>';if(level.quakeEvent&&level.quakeEvent.open.some(tile=>eq(p,tile)))badge+='<span class=\"timer\">'+(state.quakeTriggered?'QUAKE OPEN':'QUAKE OPENS')+'</span>';if(level.stormWind&&eq(p,level.stormWind.from))badge+='<span class=\"timer\">'+(state.eventTriggered?'WIND CLEARED':'WIND BLOCK')+'</span>';if(level.stormWind&&eq(p,level.stormWind.to))badge+='<span class=\"timer\">'+(state.eventTriggered?'WIND BLOCK':'WIND MOVES HERE')+'</span>';if(level.nightfall&&eq(p,level.nightfall.tile))badge+='<span class=\"timer\">'+(state.eventTriggered?'DUSK · 2 LIGHT':'DUSK AFTER DELIVERY')+'</span>';if(level.lumenNetwork&&eq(p,level.lumenNetwork.relayTile))badge+='<span class=\"timer\">'+(state.networkCharged?'RELAY SPENT':state.networkReady?'RELAY +2':'RELAY SEALED')+'</span>';if(level.lumenNetwork&&hi===level.lumenNetwork.sourceHouseIndex)badge+='<span class=\"timer\">SOURCE</span>';if(level.shadowSpawner){const si=level.shadowSpawner.stages.findIndex(tile=>eq(tile,p));if(si>=0)badge+='<span class=\"timer\">'+(si<spawnCellCount()?'SHADOW '+(si+1)+'/4':'NEST '+(si+1)+'/4')+'</span>';}const style=ISO.cellStyle(p);")
    html=html.replace("if(level.shadowSpawner){const si=level.shadowSpawner.stages.findIndex(tile=>eq(tile,p));if(si>=0)badge+='<span class=\"timer\">'+(si<spawnCellCount()?'SHADOW '+(si+1)+'/4':'NEST '+(si+1)+'/4')+'</span>';}",
        "if(level.shadowSpawner){const si=level.shadowSpawner.stages.findIndex(tile=>eq(tile,p)),inMerge=level.mergeSplit?.mergedCells.some(tile=>eq(tile,p)),active=spawnCells().some(tile=>eq(tile,p));if(si>=0||inMerge)badge+='<span class=\"timer\">'+(active?(level.mergeSplit&&state.spawnerTurn!==null&&state.turns-state.spawnerTurn>=level.mergeSplit.splitAfter?'SPLIT':level.mergeSplit&&state.spawnerTurn!==null&&state.turns-state.spawnerTurn>=level.mergeSplit.mergeAfter?'MERGED':'SHADOW'):'NEST')+'</span>';}")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.chainEvent&&eq(p,level.chainEvent.close))badge+='<span class=\"timer\">'+(state.chainTriggered?'CLOSED 2':'CLOSES 2')+'</span>';if(level.chainEvent&&level.chainEvent.open.some(tile=>eq(p,tile)))badge+='<span class=\"timer\">'+(state.chainTriggered?'OPEN 2':'OPENS 2')+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("if(level.authoredEvent)features.push(",
        "if(level.chainEvent)features.push(state.chainTriggered?'second delivery changed roads':'second delivery changes roads');if(level.authoredEvent)features.push(")
    html=html.replace("if(level.chainEvent)features.push(",
        "if(level.transitLink)features.push(state.active?'transit ride: 2 light, 1 turn':'transit unlocks after first delivery');if(level.chainEvent)features.push(")
    html=html.replace("light bridge costs one extra light","Light Bridge power builds the crossing for one light")
    html=html.replace("state.active?'SPEND 1 LIGHT':'DORMANT'","state.active?'USE BRIDGE POWER':'DORMANT'")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.phaseChoice&&eq(p,level.phaseChoice.defaultClose))badge+='<span class=\"timer\">'+(state.eventTriggered?(state.phaseSignal||state.eventStabilized||state.roadRepaired?'NORMAL OPEN':'NORMAL CLOSED'):'NORMAL CLOSES')+'</span>';if(level.phaseChoice&&eq(p,level.phaseChoice.alternateClose))badge+='<span class=\"timer\">'+(state.eventTriggered?(state.phaseSignal&&!state.eventStabilized&&!state.roadRepaired?'SIGNAL CLOSED':'SIGNAL OPEN'):'SIGNAL CLOSES')+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.lightOverloadGate&&eq(p,level.lightOverloadGate.tile))badge+='<span class=\"timer\">LIGHT '+level.lightOverloadGate.minLight+'–'+level.lightOverloadGate.maxLight+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.hunterDen&&eq(p,level.hunterDen))badge+='<span class=\"timer\">HUNTER DEN</span>';if(level.hunterDen&&state.active&&eq(p,state.hunterPos))badge+='<span class=\"done\">HUNTER</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.lightTransfer&&eq(p,level.lightTransfer.receiver))badge+='<span class=\"timer\">'+(state.transferCollected?'TRANSFER EMPTY':state.transferStored?'TAKE +1 LIGHT':'HOLDS 1 LIGHT')+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.floodRoad&&eq(p,level.floodRoad.tile))badge+='<span class=\"timer\">'+(state.floodStart===null?'FLOODS AFTER HOUSE':state.turns-state.floodStart>=level.floodRoad.closeAfter?'FLOODED':'FLOODS IN '+(level.floodRoad.closeAfter-(state.turns-state.floodStart)))+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.aftershock&&eq(p,level.aftershock.tile))badge+='<span class=\"timer\">'+(state.aftershockStabilized?'STABILIZED':state.aftershockStart===null?'AFTERSHOCK AFTER HOUSE':state.turns-state.aftershockStart>=level.aftershock.closeAfter?'AFTERSHOCK CLOSED':'AFTERSHOCK IN '+(level.aftershock.closeAfter-(state.turns-state.aftershockStart)))+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.dayNightCycle&&eq(p,level.dayNightCycle.moonRoad))badge+='<span class=\"timer\">'+(nightPhase()?'MOON OPEN':'MOON CLOSED')+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("if(level.authoredEvent)features.push(",
        "if(level.phaseChoice)features.push(state.eventTriggered?(state.phaseSignal?'signal branch active':'normal branch active'):state.phaseSignal?'alternate closure committed':level.phaseChoice.signalLightCost?'depot signal costs 1 light':'depot signal is free');if(level.authoredEvent)features.push(")
    html=html.replace("(!safe&&!(isRepair&&!repaired())?'disabled':'')",
        "(!safe&&!(isRepair&&!repaired())&&!canTrapAt(p)?'disabled':'')")
    html=html.replace("const p=[+cell.dataset.x,+cell.dataset.y];if(level.repair",
        "const p=[+cell.dataset.x,+cell.dataset.y];if(state.trapArmed&&canTrapAt(p)){placeTrap(p);return}if(level.repair")
    html=html.replace("state.trapArmed&&canTrapAt(p)?'trapTarget':'',",
        "state.trapArmed&&canTrapAt(p)?'trapTarget':'',state.decoyArmed&&canDecoyAt(p)?'decoyTarget':'',")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(state.decoyTile&&eq(p,state.decoyTile)&&state.decoyTurns>0)badge+='<span class=\"timer\">DECOY '+state.decoyTurns+'</span>';const style=ISO.cellStyle(p);")
    html=html.replace("const style=ISO.cellStyle(p);",
        "if(level.transitLink&&eq(p,level.transitLink.stops[0]))badge+='<span class=\"timer\">TRANSIT A</span>';if(level.transitLink&&eq(p,level.transitLink.stops[1]))badge+='<span class=\"timer\">TRANSIT B</span>';const style=ISO.cellStyle(p);")
    html=html.replace("&&!canTrapAt(p)?'disabled'", "&&!canTrapAt(p)&&!canDecoyAt(p)?'disabled'")
    html=html.replace("if(state.trapArmed&&canTrapAt(p)){placeTrap(p);return}if(level.repair",
        "if(state.trapArmed&&canTrapAt(p)){placeTrap(p);return}if(state.decoyArmed&&canDecoyAt(p)){placeDecoy(p);return}if(level.repair")
    html=html.replace("enhanceOverlayIcons();ISO.render();renderLevels();renderRepair();renderLegend();drawHint();",
        "enhanceOverlayIcons();ISO.render();renderLevels();renderRepair();renderLegend();renderCandidatePower();renderTransitControl();renderPhaseChoiceControl();drawHint();")
    hint_routes=json.loads(args.hints_path.read_text(encoding='utf-8'))
    signal_hint_routes=json.loads(args.signal_hints_path.read_text(encoding='utf-8'))
    assert len(hint_routes)==1800 and sum(route is not None for route in hint_routes)==1800
    hint_signature=(ROOT/'campaign/enhanced/reference-hints-v1/signature.js').read_text(encoding='utf-8')
    hint_browser=(ROOT/'campaign/enhanced/reference-hints-v1/browser.js').read_text(encoding='utf-8')
    hint_hook=(hint_signature+'\nconst VERIFIED_HINT_ROUTES='+json.dumps(hint_routes,separators=(',',':'))+';\nconst VERIFIED_SIGNAL_HINT_ROUTES='+json.dumps(signal_hint_routes,separators=(',',':'))+';\n'+hint_browser+
        "\nfunction requestHint(){if(level.n>200){requestVerifiedHint();return;}if(state.powerUsed){$('hintDialog').hidden=false;$('hintApprove').hidden=true;$('hintReject').textContent='Close';$('hintTitle').textContent='Hint unavailable after a power';$('hintMessage').textContent='This altered state has no verified hint route. No hint was spent.';return;}")
    html=html.replace('function requestHint(){',hint_hook)
    render_levels="""function renderLevels(){const completed=Object.keys(save.cleared).length,district=Math.floor((chapterShown-1)/10);$('chapterName').textContent=CHAPTERS[chapterShown-1]+' · '+completed+' / 2000 cleared';if(!$('districtSelect').options.length)$('districtSelect').innerHTML=DISTRICTS.map((name,i)=>'<option value="'+i+'">'+(i+1)+'. '+name+'</option>').join('');$('districtSelect').value=String(district);if($('chapters').dataset.chapter!==String(chapterShown)){$('chapters').innerHTML=CHAPTERS.slice(district*10,district*10+10).map((name,i)=>'<button type="button" data-chapter="'+(district*10+i+1)+'" class="'+(chapterShown===district*10+i+1?'active':'')+'">'+(i+1)+'</button>').join('');$('chapters').dataset.chapter=String(chapterShown)}$('levelButtons').innerHTML=LEVELS.slice((chapterShown-1)*10,chapterShown*10).map(l=>'<button type="button" data-level="'+l.n+'" class="'+(l.n===level.n?'active':'')+'">'+l.n+'</button>').join('');renderPicker()}"""
    render_picker="""function renderPicker(){const district=Math.floor((chapterShown-1)/10);$('pickerChapterName').textContent='Chapter '+chapterShown+' · '+CHAPTERS[chapterShown-1];if(!$('pickerDistrictSelect').options.length)$('pickerDistrictSelect').innerHTML=DISTRICTS.map((name,i)=>'<option value="'+i+'">'+(i+1)+'. '+name+'</option>').join('');$('pickerDistrictSelect').value=String(district);if($('pickerChapters').dataset.chapter!==String(chapterShown)){$('pickerChapters').innerHTML=CHAPTERS.slice(district*10,district*10+10).map((name,i)=>'<button type="button" data-picker-chapter="'+(district*10+i+1)+'" class="'+(chapterShown===district*10+i+1?'active':'')+'">'+(i+1)+'</button>').join('');$('pickerChapters').dataset.chapter=String(chapterShown)}$('pickerLevels').innerHTML=LEVELS.slice((chapterShown-1)*10,chapterShown*10).map(l=>'<button type="button" data-picker-level="'+l.n+'" class="'+(l.n===level.n?'active':'')+'">'+l.n+'<small>'+(save.cleared[l.n]?'Cleared':'Play')+'</small></button>').join('');const current=level.n>=((chapterShown-1)*10+1)&&level.n<=chapterShown*10?level.n:(chapterShown-1)*10+1;renderRouteBook(current)}"""
    route_book="""function renderRouteBook(n){const l=LEVELS[n-1],box=$('routeBook');if(!l||!box)return;const hazards=[];if(l.patrol?.length)hazards.push('Patrol shadow'+(l.patrol2?.length?' ×2':''));if(l.echo)hazards.push('Echo shadow');for(const [key,name] of [['shadowInfluence2x2','2×2 shadow field'],['leechPatrol','Shadow drains house light'],['hunterDen','Hunter'],['sentinelCenter','Sentinel field'],['shadowDoor','Shadow door'],['lightBridge','Light Bridge'],['quakeEvent','Quake'],['aftershock','Aftershock'],['stormWind','Storm'],['floodRoad','Flood'],['nightfall','Nightfall'],['dayNightCycle','Day/night cycle'],['shadowSpawner','Spawner'],['lumenNetwork','Lumen network'],['lightOverloadGate','Overload gate'],['lightTransfer','Light transfer'],['chainEvent','Chain event'],['transitLink','Transit'],['phaseChoice','Route choice'],['authoredEvent','Road event'],['hiddenRoad','Hidden road'],['rechargeHouse','Recharge house'],['collapseTile','Collapsing road'],['dark','Dark road'],['ice','Ice'],['switch','Switch'],['gate','Gate'],['repair','Repair']])if(l[key])hazards.push(name);const power=l.reviewPower?l.reviewPower.replaceAll('_',' ').replace(/\\b\\w/g,c=>c.toUpperCase()):'None';$('routeBookTitle').textContent='Level '+n+' · '+(l.grid||8)+'×'+(l.grid||8)+' · '+l.homes.length+' houses · '+l.cap+' light';$('routeBookBrief').textContent=l.brief||'Deliver to the houses and return to the depot.';$('routeBookFeatures').textContent=hazards.length?hazards.join(' · '):'No special hazard';$('routeBookPower').textContent='Test power: '+power;$('routeBookPlay').dataset.routeLevel=String(n)}"""
    event_labels={'quakeEvent':('Quake','Quake after first delivery'),
                  'aftershock':('Aftershock','Aftershock countdown after first delivery'),
                  'stormWind':('Storm','Wind shifts after first delivery'),
                  'floodRoad':('Flood','Flood countdown after first delivery'),
                  'nightfall':('Nightfall','Fog after first delivery'),
                  'shadowSpawner':('Spawner','Spawner wakes after first delivery'),
                  'chainEvent':('Chain event','Road change after second delivery'),
                  'authoredEvent':('Road event','Road closes after first delivery'),
                  'hiddenRoad':('Hidden road','Beacon reveals hidden road'),
                  'collapseTile':('Collapsing road','Road collapses after crossing')}
    for key,(old,new) in event_labels.items():
        route_book=route_book.replace(f"['{key}','{old}']",f"['{key}','{new}']")
    route_book=route_book.replace("['hiddenRoad','Beacon reveals hidden road']","['oneWayTile','One-way road'],['hiddenRoad','Beacon reveals hidden road']")
    route_book=route_book.replace("if(l[key])hazards.push(name);",
        "if(l[key])hazards.push(key==='shadowInfluence2x2'&&l[key].triggerCount===2?'2×2 shadow field after second delivery':name);")
    html,c1=re.subn(r'^function renderLevels\(\)\{.*$',lambda m:render_levels,html,flags=re.M)
    html,c2=re.subn(r'^function renderPicker\(\)\{.*$',lambda m:render_picker,html,flags=re.M)
    assert c1==c2==1,(c1,c2)
    html=html.replace(render_picker,route_book+'\n'+render_picker)
    html=html.replace('<div id="chapters" class="chapterButtons"></div>', '<label class="districtLabel" for="districtSelect">District</label><select id="districtSelect" class="districtSelect" aria-label="Choose district"></select><div id="chapters" class="chapterButtons"></div>')
    html=html.replace('<div id="pickerChapters" class="pickerChapters"></div>', '<label class="districtLabel" for="pickerDistrictSelect">District</label><select id="pickerDistrictSelect" class="districtSelect" aria-label="Choose district"></select><div id="pickerChapters" class="pickerChapters"></div>')
    html=html.replace('<div class="pickerLabel">Chapters</div>','<div class="pickerLabel">Jump to any level</div><div class="jump"><input id="jumpLevel" type="number" min="1" max="2000" placeholder="Level 1–2000" aria-label="Level number"><button id="jumpGo" type="button">Play level</button></div><div class="pickerLabel">Chapters</div>')
    html=html.replace('<div class="pickerLabel">Chapters</div>','<section id="routeBook" class="routeBook" aria-live="polite"><div class="pickerLabel">Route book</div><strong id="routeBookTitle"></strong><p id="routeBookBrief"></p><p id="routeBookFeatures"></p><p id="routeBookPower"></p><button id="routeBookPlay" type="button">Play previewed level</button></section><div class="pickerLabel">Chapters</div>',1)
    html=html.replace('.pickerNote{','.routeBook{margin-top:14px;padding:12px;border:1px solid #a18c78;border-radius:12px;background:#252c43}.routeBook .pickerLabel{margin:0 0 7px}.routeBook strong{color:#ffe4ad}.routeBook p{margin:5px 0;color:#d5d8e5;font-size:12px}.routeBook button{margin-top:7px;min-height:37px;padding:6px 11px;border:1px solid #d4b480;border-radius:8px;background:#655440;color:#fff2d8;font-weight:900}.pickerNote{',1)
    html=html.replace('<div class="gameControls">','<div id="candidatePower" class="candidatePower" hidden></div><div id="phaseChoiceControl" class="candidatePower" hidden></div><div id="transitControl" class="candidatePower" hidden></div><div class="reviewPad" aria-label="Hold an arrow to move"><button data-step="0,-1" aria-label="Move up">↑</button><button data-step="-1,0" aria-label="Move left">←</button><button data-step="1,0" aria-label="Move right">→</button><button data-step="0,1" aria-label="Move down">↓</button></div><div class="gameControls">')
    html=html.replace('<div id="repairBody"></div></section>','<div id="repairBody"></div><div id="powerShop"></div></section>')
    controls="""$('jumpGo').addEventListener('click',()=>{const n=Number($('jumpLevel').value);if(Number.isInteger(n)&&n>=1&&n<=LEVELS.length){hidePicker();choose(n)}});$('jumpLevel').addEventListener('input',()=>{const n=Number($('jumpLevel').value);if(Number.isInteger(n)&&n>=1&&n<=LEVELS.length)renderRouteBook(n)});$('jumpLevel').addEventListener('keydown',e=>{if(e.key==='Enter')$('jumpGo').click()});$('pickerLevels').addEventListener('pointerover',e=>{const b=e.target.closest('[data-picker-level]');if(b)renderRouteBook(+b.dataset.pickerLevel)});$('pickerLevels').addEventListener('focusin',e=>{const b=e.target.closest('[data-picker-level]');if(b)renderRouteBook(+b.dataset.pickerLevel)});$('routeBookPlay').addEventListener('click',()=>{const n=Number($('routeBookPlay').dataset.routeLevel);if(Number.isInteger(n)&&n>=1&&n<=LEVELS.length){hidePicker();choose(n)}});for(const id of ['districtSelect','pickerDistrictSelect'])$(id).addEventListener('change',e=>{const district=Number(e.target.value);if(Number.isInteger(district)&&district>=0&&district<DISTRICTS.length){chapterShown=district*10+1;renderLevels()}});let holdTimer=null;function step(dx,dy){if(state.done||state.failed||state.help)return;move([state.pos[0]+dx,state.pos[1]+dy])}for(const b of document.querySelectorAll('[data-step]')){const [dx,dy]=b.dataset.step.split(',').map(Number);b.addEventListener('pointerdown',e=>{e.preventDefault();b.setPointerCapture(e.pointerId);step(dx,dy);clearInterval(holdTimer);holdTimer=setInterval(()=>step(dx,dy),180)});for(const event of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(event,()=>{clearInterval(holdTimer);holdTimer=null})}document.addEventListener('keydown',e=>{if(['INPUT','TEXTAREA'].includes(document.activeElement?.tagName))return;const d={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]}[e.key];if(d){e.preventDefault();step(...d)}});"""
    power_code="""function canTrapAt(p){if(!state.trapArmed||state.powerUsed||!open(p)||eq(p,state.pos)||Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])>2)return false;return [level.patrol,level.patrol2].some(patrol=>patrol?.some(tile=>eq(tile,p)))&&!(state.active&&(eq(p,level.patrol[state.phase])||eq(p,level.patrol2?.[state.phase2])))}
function placeTrap(p){if(!canTrapAt(p))return;state.trapTile=[...p];state.trapPatrol=level.patrol.some(tile=>eq(tile,p))?1:2;state.trapArmed=false;state.powerUsed=true;setStatus('Trap laid','Shadow trap armed','When the selected patrol enters this tile, it stays there for the rest of this run.');render()}
function renderCandidatePower(){const box=$('candidatePower');if(!level.reviewPower){box.hidden=true;return}box.hidden=false;const names={lumen_flask:'Lumen Flask',road_repair:'Road Repair',map_stabilizer:'Map Stabilizer',anchor_trap:'Anchor Trap',freeze_seal:'Freeze Seal',rewind:'Rewind'};const help={lumen_flask:'Restore up to 3 lantern light (one charge).',road_repair:'Reopen the marked road after it closes (one charge).',map_stabilizer:'Use before the first delivery to keep the marked road open (one charge).',anchor_trap:'Arm it, then tap a highlighted patrol tile within two steps. The shadow stops there when it enters.',freeze_seal:'Hold both patrol shadows in place for the next three moves. Echo still follows your trail.',rewind:'Undo your last move, including its light cost, delivery, shadow step, and map event.'};const available=!state.powerUsed&&!state.done&&!state.failed&&(level.reviewPower==='road_repair'?state.eventTriggered&&!state.eventStabilized:level.reviewPower==='map_stabilizer'?!state.eventTriggered:level.reviewPower==='lumen_flask'?state.light<cap():level.reviewPower==='rewind'?!!state.lastMoveState:level.reviewPower==='freeze_seal'?state.active&&state.freezeTurns===0:!state.trapArmed);box.innerHTML='<strong>Test loadout: '+names[level.reviewPower]+'</strong><span>'+help[level.reviewPower]+'</span><button type="button" id="useCandidatePower" '+(available?'':'disabled')+'>'+(state.powerUsed?'USED':state.trapArmed?'Select a tile':'Use power')+'</button>'}
function useCandidatePower(){if(!level.reviewPower||state.powerUsed||state.done||state.failed)return;const power=level.reviewPower;if(power==='lumen_flask'){if(state.light>=cap())return;state.light=Math.min(cap(),state.light+3)}else if(power==='road_repair'){if(!state.eventTriggered||state.eventStabilized)return;state.roadRepaired=true}else if(power==='map_stabilizer'){if(state.eventTriggered)return;state.eventStabilized=true}else if(power==='freeze_seal'){if(!state.active||state.freezeTurns)return;state.freezeTurns=3}else if(power==='rewind'){if(!state.lastMoveState)return;state={...state.lastMoveState,powerUsed:true,lastMoveState:null};hintPath=null;setStatus('Move rewound','Previous position restored','Light, shadows, delivery, and map event returned to their prior state.');render();return}else if(power==='anchor_trap'){state.trapArmed=true;setStatus('Choose a trap tile','Tap a highlighted patrol tile','Choose one within two steps. The shadow stops there when it enters.');render();return}else return;state.powerUsed=true;setStatus('Power used',power.replaceAll('_',' '),'One charge spent for this run.');render()}
$('candidatePower').addEventListener('click',e=>{if(e.target.id==='useCandidatePower')useCandidatePower()});"""
    decoy_code="""function canDecoyAt(p){return state.decoyArmed&&!state.powerUsed&&state.active&&!state.done&&!state.failed&&open(p)&&!eq(p,state.pos)&&Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])<=2}
function placeDecoy(p){if(!canDecoyAt(p))return;const choices=[[1,level.patrol,state.phase],[2,level.patrol2,state.phase2]].filter(v=>v[1]);const pick=choices.sort((a,b)=>(Math.abs(a[1][a[2]][0]-p[0])+Math.abs(a[1][a[2]][1]-p[1]))-(Math.abs(b[1][b[2]][0]-p[0])+Math.abs(b[1][b[2]][1]-p[1])))[0];state.decoyPatrol=pick[0];state.decoyTargetPhase=pick[1].map(tile=>Math.abs(tile[0]-p[0])+Math.abs(tile[1]-p[1])).indexOf(Math.min(...pick[1].map(tile=>Math.abs(tile[0]-p[0])+Math.abs(tile[1]-p[1]))));state.decoyTile=[...p];state.decoyTurns=4;state.decoyArmed=false;state.powerUsed=true;setStatus('Decoy placed','Shadow '+pick[0]+' is attracted','For four moves, it follows its patrol loop toward the waypoint nearest your false light.');render()}
"""
    power_code=decoy_code+power_code
    power_code=power_code.replace("rewind:'Rewind'}","rewind:'Rewind',reveal_pulse:'Reveal Pulse'}")
    power_code=power_code.replace("rewind:'Undo your last move, including its light cost, delivery, shadow step, and map event.'}","rewind:'Undo your last move, including its light cost, delivery, shadow step, and map event.',reveal_pulse:'Reveal the hidden house and sealed road now, before reaching the Beacon.'}")
    power_code=power_code.replace("level.reviewPower==='rewind'?!!state.lastMoveState:","level.reviewPower==='reveal_pulse'?!state.beaconRevealed:level.reviewPower==='rewind'?!!state.lastMoveState:")
    power_code=power_code.replace("else if(power==='freeze_seal'){", "else if(power==='reveal_pulse'){if(!level.hiddenRoad||state.beaconRevealed)return;state.beaconRevealed=true}else if(power==='freeze_seal'){")
    power_code=power_code.replace("setStatus('Power used',power.replaceAll('_',' '),", "setStatus('Power used',power==='reveal_pulse'?'Hidden house and road revealed':power.replaceAll('_',' '),")
    assert "reveal_pulse:'Reveal Pulse'" in power_code and "state.beaconRevealed=true}else if(power==='freeze_seal')" in power_code
    power_code=power_code.replace("reveal_pulse:'Reveal Pulse'}","reveal_pulse:'Reveal Pulse',decoy_light:'Decoy Light'}")
    power_code=power_code.replace("reveal_pulse:'Reveal the hidden house and sealed road now, before reaching the Beacon.'}","reveal_pulse:'Reveal the hidden house and sealed road now, before reaching the Beacon.',decoy_light:'Place a false light within two tiles. The nearest patrol follows its loop toward it for four moves.'}")
    power_code=power_code.replace("level.reviewPower==='reveal_pulse'?!state.beaconRevealed:","level.reviewPower==='decoy_light'?state.active&&!state.decoyArmed:level.reviewPower==='reveal_pulse'?!state.beaconRevealed:")
    power_code=power_code.replace("state.trapArmed?'Select a tile':'Use power'","state.trapArmed||state.decoyArmed?'Select a tile':'Use power'")
    power_code=power_code.replace("else if(power==='anchor_trap'){","else if(power==='decoy_light'){if(!state.active)return;state.decoyArmed=true;setStatus('Choose a decoy tile','Tap a highlighted road within two steps','The nearest patrol will move toward the false light along its loop.');render();return}else if(power==='anchor_trap'){")
    assert "decoy_light:'Decoy Light'" in power_code and "state.decoyArmed=true" in power_code
    power_code=power_code.replace("hintPath=null;setStatus('Move rewound'","hintPath=null;ISO.cancel();setStatus('Move rewound'")
    power_code=power_code.replace("decoy_light:'Decoy Light'}","decoy_light:'Decoy Light',light_bridge:'Light Bridge'}")
    power_code=power_code.replace("decoy_light:'Place a false light within two tiles. The nearest patrol follows its loop toward it for four moves.'}","decoy_light:'Place a false light within two tiles. The nearest patrol follows its loop toward it for four moves.',light_bridge:'After one delivery, spend one light and this charge to create the marked crossing.'}")
    power_code=power_code.replace("level.reviewPower==='decoy_light'?state.active&&!state.decoyArmed:","level.reviewPower==='light_bridge'?state.active&&!state.bridgeBuilt&&state.light>level.bridgeCost:level.reviewPower==='decoy_light'?state.active&&!state.decoyArmed:")
    power_code=power_code.replace("else if(power==='freeze_seal'){","else if(power==='light_bridge'){if(!level.lightBridge||!state.active||state.bridgeBuilt||state.light<=level.bridgeCost)return;state.light-=level.bridgeCost;state.bridgeBuilt=true}else if(power==='freeze_seal'){")
    power_code=power_code.replace("power==='reveal_pulse'?'Hidden house and road revealed':power.replaceAll('_',' ')","power==='reveal_pulse'?'Hidden house and road revealed':power==='light_bridge'?'Marked crossing built for one light':power.replaceAll('_',' ')")
    assert "light_bridge:'Light Bridge'" in power_code and "state.light-=level.bridgeCost;state.bridgeBuilt=true" in power_code
    transit_code="""function renderTransitControl(){const box=$('transitControl');if(!level.transitLink||!state.active||state.done||state.failed){box.hidden=true;return}const [a,b]=level.transitLink.stops,other=eq(state.pos,a)?b:eq(state.pos,b)?a:null;if(!other){box.hidden=true;return}box.hidden=false;const canRide=legal(other)&&state.light>level.transitLink.rideLight;box.innerHTML='<strong>Transit stop</strong><span>Ride to the other stop in one turn for '+level.transitLink.rideLight+' light.</span><button type="button" id="rideTransit" '+(canRide?'':'disabled')+'>Ride transit</button>'}
$('transitControl').addEventListener('click',e=>{if(e.target.id!=='rideTransit'||!level.transitLink)return;const [a,b]=level.transitLink.stops,other=eq(state.pos,a)?b:eq(state.pos,b)?a:null;if(other&&legal(other)&&state.light>level.transitLink.rideLight)move(other)});
"""
    phase_code="""function renderPhaseChoiceControl(){const box=$('phaseChoiceControl');if(!level.phaseChoice||state.done||state.failed||state.eventTriggered){box.hidden=true;return}box.hidden=false;const price=level.phaseChoice.signalLightCost,canSignal=!state.phaseSignal&&!state.help&&eq(state.pos,level.depot)&&state.mask===0&&state.light>price;box.innerHTML='<strong>Choose the first road change</strong><span>'+(state.phaseSignal?'Signal committed: the purple alternate road will close after the first delivery.':'The orange normal road closes unless you signal at the depot. '+(price?'The signal costs one light.':'The signal is free.')+' The purple alternate road closes instead.')+'</span><button type="button" id="sendPhaseSignal" '+(canSignal?'':'disabled')+'>'+(state.phaseSignal?'Signal sent':price?'Spend 1 light: signal alternate':'Signal alternate road')+'</button>'}
$('phaseChoiceControl').addEventListener('click',e=>{if(e.target.id!=='sendPhaseSignal'||!level.phaseChoice||state.phaseSignal||state.help||state.eventTriggered||state.done||state.failed||!eq(state.pos,level.depot)||state.mask!==0||state.light<=level.phaseChoice.signalLightCost)return;state.light-=level.phaseChoice.signalLightCost;state.phaseSignal=true;setStatus('Signal sent','Alternate road change selected','The normal corridor stays open after delivery; the purple alternate road will close.');render()});
"""
    power_code=phase_code+transit_code+power_code
    economy_code=(ROOT/'campaign'/'enhanced'/'power-economy.js').read_text(encoding='utf-8')
    loadout_code=(ROOT/'campaign'/'enhanced'/'power-loadout.js').read_text(encoding='utf-8')
    html=html.replace('setupNavigationIcons();',controls+power_code+economy_code+loadout_code+'setupNavigationIcons();')
    html=html.replace("renderRepair();renderLegend();renderCandidatePower();",
        "renderRepair();renderPowerShop();renderLegend();renderCandidatePower();")
    html=html.replace("if(count===level.homes.length)save.mastered[level.n]=true;persist();",
        "if(count===level.homes.length)save.mastered[level.n]=true;syncPowerUnlocks();persist();")
    html=html.replace("if(level.patrol2)features.push('second shadow');",
        "if(level.patrol2)features.push('second shadow');if(state.freezeTurns>0)features.push('patrols frozen for '+state.freezeTurns+' moves');")
    html=html.replace('</style>','.jump{display:flex;gap:8px;margin:8px 0 14px}.jump input{flex:1;min-width:0;padding:11px;border-radius:8px;border:1px solid #8b9aaf;background:#18263b;color:white}.jump button,.reviewPad button{border:1px solid #aabbd0;background:#344d64;color:white;border-radius:8px;font-weight:900}.jump button{padding:9px 13px}.reviewPad{display:flex;justify-content:center;gap:6px;margin:10px 0}.reviewPad button{width:51px;height:48px;touch-action:none}.pickerChapters,.chapterButtons{max-height:125px;overflow:auto}.cell.eventRoad:not(.wall){box-shadow:inset 0 0 0 3px #f2a066}.cell.eventRoad.wall{box-shadow:inset 0 0 0 3px #e76e72}.cell.trapTarget{box-shadow:inset 0 0 0 3px #73e6ca}.cell.trapPlaced{box-shadow:inset 0 0 0 3px #67d8eb}.cell.recharge{background:#315b59;box-shadow:inset 0 0 0 2px #80dbc0}.candidatePower{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px;margin:7px 0;border:1px solid #8b9aaf;border-radius:10px;background:#20374a;font-size:12px}.candidatePower[hidden]{display:none}.candidatePower strong{color:#ffe0a0}.candidatePower span{flex:1;min-width:190px}.candidatePower button{border:1px solid #ffe0a0;border-radius:8px;background:#6d5946;color:white;padding:9px 12px;font-weight:900}.candidatePower button:disabled{opacity:.45}.pickerNote:after{content:" Review candidate maps: extra mechanics and global minimums are still under validation."}</style>')
    html=html.replace('Playable campaign preview · 2,000 levels','Baseline candidate preview · 2,000 maps')
    html=html.replace('</style>','.cell.oneway{background:#4b6176;box-shadow:inset 0 0 0 2px #85bfdd}.cell.collapse{background:#735947;box-shadow:inset 0 0 0 2px #edba77}</style>')
    html=html.replace('</style>','.cell.sentinelZone:not(.wall){background:#624a70;box-shadow:inset 0 0 0 2px #ca9ae1}.cell.sentinelZone.danger{background:#904459}</style>')
    html=html.replace('</style>','.cell.hunterden:not(.wall){background:#62435d;box-shadow:inset 0 0 0 2px #eaa0c3}</style>')
    html=html.replace('</style>','.cell.lightreceiver:not(.wall){background:#285a63;box-shadow:inset 0 0 0 2px #8fe4ed}</style>')
    html=html.replace('</style>','.cell.floodroad:not(.wall){background:#28506d;box-shadow:inset 0 0 0 2px #83d3fa}.cell.floodroad.wall{background:#294f67;box-shadow:inset 0 0 0 3px #7ac6e9}</style>')
    html=html.replace('</style>','.cell.aftershockroad:not(.wall){background:#745844;box-shadow:inset 0 0 0 2px #e7b37c}.cell.aftershockroad.wall{background:#674351;box-shadow:inset 0 0 0 3px #e49090}</style>')
    html=html.replace('</style>','.cell.shadowdoor{background:#544968;box-shadow:inset 0 0 0 2px #ba9cdd}.cell.shadowdoor.closed{filter:saturate(.5)}.cell.shadowlock{background:#486471;box-shadow:inset 0 0 0 2px #9bd5db}</style>')
    html=html.replace('</style>','.cell.lightbridge{background:#3e6878;box-shadow:inset 0 0 0 2px #8fe9e4}.cell.lightbridge.closed{opacity:.65}</style>')
    html=html.replace('</style>','.cell.overloadgate:not(.wall){background:#60507b;box-shadow:inset 0 0 0 3px #e8b4f5}.cell.overloadgate.closed{opacity:.55}</style>')
    html=html.replace('</style>','.cell.quakeClose:not(.wall){box-shadow:inset 0 0 0 3px #e78978}.cell.quakeClose.wall{background:#6b4152}.cell.quakeOpen:not(.wall){box-shadow:inset 0 0 0 3px #a7dea6}.cell.quakeOpen.wall{background:#42556b}</style>')
    html=html.replace('</style>','.cell.chainClose:not(.wall){box-shadow:inset 0 0 0 3px #df7c93}.cell.chainClose.wall{background:#764050}.cell.chainOpen:not(.wall){box-shadow:inset 0 0 0 3px #95d5b2}.cell.chainOpen.wall{background:#425f57}</style>')
    html=html.replace('</style>','.cell.transitstop{background:#345e77;box-shadow:inset 0 0 0 2px #8bd8f2}.cell.transitstop.safe{box-shadow:inset 0 0 0 3px #9bf9df}</style>')
    html=html.replace('</style>','.cell.phaseAlternate:not(.wall){box-shadow:inset 0 0 0 3px #c5a1ec}.cell.phaseAlternate.wall{background:#62466e}</style>')
    html=html.replace('</style>','.cell.duskroad{background:#655777;box-shadow:inset 0 0 0 2px #d7a9e4}.cell.fogged:not(.safe):not(.occupied){filter:brightness(.26) saturate(.4)}.cell.fogged:not(.safe):not(.occupied) .timer,.cell.fogged:not(.safe):not(.occupied) .done{visibility:hidden}</style>')
    html=html.replace('</style>','.cell.moonroad:not(.wall){background:#56517a;box-shadow:inset 0 0 0 2px #c6b9ff}.cell.moonroad.wall{background:#383e59;box-shadow:inset 0 0 0 2px #8077aa}</style>')
    html=html.replace('</style>','.cell.spawnerZone:not(.wall){box-shadow:inset 0 0 0 2px #bd77bb;background:#554363}.cell.spawnerZone.danger{background:#8d405a}</style>')
    html=html.replace('</style>','.cell.decoyTarget{box-shadow:inset 0 0 0 3px #f7d479}.cell.decoyTarget:not(.wall){background:#806d46}</style>')
    html=html.replace('</style>','.cell.lumenrelay:not(.wall){background:#446858;box-shadow:inset 0 0 0 2px #abf3ad}.cell.lumenrelay.wall{box-shadow:inset 0 0 0 2px #82bd8f}</style>')
    html=html.replace('Spend those points on lasting map repairs.','Browse all 2,000 maps and test their powers, shadows, and changing streets.')
    old_choose="function choose(n){showScreen('play');level=LEVELS[n-1];chapterShown=level.chapter;reset()}"
    new_choose="function choose(n){showScreen('play');level=LEVELS[n-1];chapterShown=level.chapter;const zoom=!!window.matchMedia?.('(max-width:610px)').matches&&level.grid>=16;$('scene').parentElement.classList[zoom?'add':'remove']('zoomed');$('zoomMap').textContent=zoom?'− Fit map':'＋ Zoom map';$('zoomMap').setAttribute?.('aria-pressed',String(zoom));reset();$('playScreen').scrollTop=0}"
    assert html.count(old_choose)==1
    html=html.replace(old_choose,new_choose)
    html=html.replace("const available=!state.powerUsed&&!state.done&&!state.failed&&(",
        "const available=canSpendPowerCharge(level.reviewPower)&&!state.powerUsed&&!state.done&&!state.failed&&(")
    html=html.replace("<strong>Test loadout: '+names[level.reviewPower]+'</strong>",
        "<strong>Power: '+names[level.reviewPower]+' · '+chargeLabel(level.reviewPower)+'</strong>")
    html=html.replace("if(!level.reviewPower||state.powerUsed||state.done||state.failed)return;const power=level.reviewPower;",
        "if(!level.reviewPower||state.powerUsed||state.done||state.failed||!canSpendPowerCharge(level.reviewPower))return;const power=level.reviewPower;")
    html=html.replace("state.trapArmed=false;state.powerUsed=true;",
        "state.trapArmed=false;consumePowerCharge('anchor_trap');state.powerUsed=true;")
    html=html.replace("state.decoyArmed=false;state.powerUsed=true;",
        "state.decoyArmed=false;consumePowerCharge('decoy_light');state.powerUsed=true;")
    html=html.replace("consumePowerCharge('anchor_trap');state.powerUsed=true;",
        "consumePowerCharge('anchor_trap');state.usedPowers.anchor_trap=true;state.powerUsed=true;")
    html=html.replace("consumePowerCharge('decoy_light');state.powerUsed=true;",
        "consumePowerCharge('decoy_light');state.usedPowers.decoy_light=true;state.powerUsed=true;")
    html=html.replace("state={...state.lastMoveState,powerUsed:true,lastMoveState:null};",
        "consumePowerCharge(power);state={...state.lastMoveState,powerUsed:true,lastMoveState:null};")
    html=html.replace("else return;state.powerUsed=true;setStatus('Power used'",
        "else return;consumePowerCharge(power);state.powerUsed=true;setStatus('Power used'")
    html=html.replace('</style>','.shopRow{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:7px 0;border-top:1px solid #71809655}.shopRow span{display:grid;gap:2px}.shopRow small{color:#bec9d9}.shopRow button{min-width:93px;min-height:35px;border:1px solid #e1c790;border-radius:7px;background:#63533f;color:white;font-weight:800}.shopRow button:disabled{opacity:.5}#powerShop{margin-top:16px}#powerShop summary{color:#ffdc9a;font-weight:900;cursor:pointer}</style>')
    html=html.replace('</style>','.candidatePower select{min-width:160px;max-width:100%;padding:8px;border:1px solid #a6bcd2;border-radius:7px;background:#243b50;color:#fff1df;font-weight:800}</style>')
    html=html.replace('</style>','.districtLabel{display:block;margin:11px 0 5px;color:#ffe0a0;font-size:11px;font-weight:900;text-transform:uppercase;letter-spacing:.08em}.districtSelect{width:100%;min-height:42px;padding:8px 10px;border:1px solid #899ab1;border-radius:8px;background:#21354d;color:#fff1df;font-weight:800}.chapterButtons,.pickerChapters{max-height:none}</style>')
    html=html.replace("level.nightfall&&state.eventTriggered&&eq(p,level.nightfall.tile)",
        "level.nightfall&&state.eventTriggered&&(!level.dayNightCycle||nightPhase())&&eq(p,level.nightfall.tile)")
    html=html.replace("level.nightfall&&state.eventTriggered&&Math.max(",
        "level.nightfall&&state.eventTriggered&&(!level.dayNightCycle||nightPhase())&&Math.max(")
    html=html.replace("state.quakeTriggered?'An earthquake closed a road and opened another.'",
        "state.quakeTriggered?(state.quakeStabilized?'The quake opened a road; your stabilizer kept the marked street open.':'An earthquake closed a road and opened another.')")
    html=html.replace("state.quakeTriggered?'earthquake changed roads':'first house triggers earthquake'",
        "state.quakeTriggered?(state.quakeStabilized?'quake opened a road; closure stabilized':'earthquake changed roads'):'first house triggers earthquake'")
    html=html.replace("state.quakeTriggered?'QUAKE CLOSED':'QUAKE CLOSES'",
        "state.quakeStabilized?'STABILIZED':state.quakeTriggered?'QUAKE CLOSED':'QUAKE CLOSES'")
    html=html.replace("state.quakeStabilized?'STABILIZED':state.quakeTriggered?'QUAKE CLOSED'",
        "state.quakeRepaired?'REPAIRED':state.quakeStabilized?'STABILIZED':state.quakeTriggered?'QUAKE CLOSED'")
    html=html.replace("state.collapseClosed?'causeway CLOSED':'causeway collapses after use'",
        "state.collapseRepaired?'causeway REPAIRED':state.collapseClosed?'causeway CLOSED':'causeway collapses after use'")
    html=html.replace("state.collapseClosed?'CLOSED':'FRAGILE'",
        "state.collapseRepaired?'REPAIRED':state.collapseClosed?'CLOSED':'FRAGILE'")
    html=html.replace("state.aftershockStabilized?'aftershock road STABILIZED':",
        "state.aftershockRepaired?'aftershock road REPAIRED':state.aftershockStabilized?'aftershock road STABILIZED':")
    html=html.replace("state.aftershockStabilized?'STABILIZED':state.aftershockStart",
        "state.aftershockRepaired?'REPAIRED':state.aftershockStabilized?'STABILIZED':state.aftershockStart")
    # The board uses a canvas; DOM cell backgrounds are intentionally hidden.
    # Draw the four early shadow cells on the canvas itself in both map modes.
    marker="const floor=wall?'#495b68':lit?"
    assert html.count(marker)==1
    html=html.replace(marker,
        "const influence=level.shadowInfluence2x2?.cells.some(tile=>eq(tile,p));const floor=influence?(state.active?'#874461':'#665872'):wall?'#495b68':lit?")
    marker="const edge=safe?'#b2f9d5':danger?'#ff9b9e':lit?"
    assert html.count(marker)==1
    html=html.replace(marker,
        "const edge=safe?'#b2f9d5':danger?'#ff9b9e':influence?(state.active?'#ffd0e6':'#baa9dc'):lit?")
    # A later influence field can wake after two deliveries; existing fields
    # retain their first-delivery behavior when triggerCount is absent.
    html=html.replace("if(level.shadowInfluence2x2&&s.active&&",
        "if(level.shadowInfluence2x2&&popcount(s.mask)>=(level.shadowInfluence2x2.triggerCount||1)&&")
    html=html.replace("state.active&&level.shadowInfluence2x2&&",
        "level.shadowInfluence2x2&&popcount(state.mask)>=(level.shadowInfluence2x2.triggerCount||1)&&")
    html=html.replace("state.active?'2×2 BLOCKED':'2×2 WAKES'",
        "popcount(state.mask)>=(level.shadowInfluence2x2.triggerCount||1)?'2×2 BLOCKED':'2×2 WAKES'")
    html=html.replace("state.active?'2×2 shadow field ACTIVE':'2×2 shadow field wakes after first delivery'",
        "popcount(state.mask)>=(level.shadowInfluence2x2.triggerCount||1)?'2×2 shadow field ACTIVE':'2×2 shadow field wakes after '+(level.shadowInfluence2x2.triggerCount===2?'second':'first')+' delivery'")
    assert html.count("+' shadows';")==1
    html=html.replace("+' shadows';",
        "+' shadows'+(level.networkCircuitRequired?' · Circuit '+(Number(!!state.networkCharged)+Number(!!state.overloadCrossed)+Number(!!state.transferCollected))+'/3':'');")
    html=html.replace("const floor=influence?(state.active?",
        "const floor=influence?(popcount(state.mask)>=(level.shadowInfluence2x2.triggerCount||1)?")
    html=html.replace("influence?(state.active?'#ffd0e6'",
        "influence?(popcount(state.mask)>=(level.shadowInfluence2x2.triggerCount||1)?'#ffd0e6'")
    marker="+!!level.shadowSpawner+!!level.hunterDen)+' shadows'"
    assert html.count(marker)==1
    html=html.replace(marker,"+!!level.shadowSpawner+!!level.hunterDen+!!level.shadowInfluence2x2)+' shadows'")
    assert not any(x in html for x in ['/*__LEVEL_DATA__*/','/*__ISOMETRIC_SCENE__*/','/*__ROUTE_SOLVER__*/'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(html,encoding='utf-8')
    print(f'Built {args.output}; {len(levels)} candidate maps; {args.output.stat().st_size} bytes',flush=True)

if __name__=='__main__':main()
