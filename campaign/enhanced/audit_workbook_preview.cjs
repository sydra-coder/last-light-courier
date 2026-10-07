// Compare compact planning rows against the levels loaded by the playable preview.
const fs=require('fs');
const path=require('path');
const preview=require('./test_integrated_preview.cjs').LEVELS;
const table=JSON.parse(fs.readFileSync(path.join(__dirname,'playtest_rows.json'),'utf8'));
const lateWallPath=path.join(__dirname,'late-shortcut-streets-v1/walls.json');
const lateWallLevels=new Set(fs.existsSync(lateWallPath)?Object.keys(JSON.parse(fs.readFileSync(lateWallPath,'utf8'))).map(Number):[]);
const variantWallPath=path.join(__dirname,'finale-shortcut-variants-v1/walls.json');
const variantWallLevels=new Set(fs.existsSync(variantWallPath)?Object.keys(JSON.parse(fs.readFileSync(variantWallPath,'utf8'))).map(Number):[]);
const stormVariantPath=path.join(__dirname,'storm-variant-streets-v1/walls.json');
const stormVariantLevels=new Set(fs.existsSync(stormVariantPath)?Object.keys(JSON.parse(fs.readFileSync(stormVariantPath,'utf8'))).map(Number):[]);
const multiBandPath=path.join(__dirname,'multi-band-variants-v1/walls.json');
const multiBandLevels=new Set(fs.existsSync(multiBandPath)?Object.keys(JSON.parse(fs.readFileSync(multiBandPath,'utf8'))).map(Number):[]);
const bridgeDetourWalls=new Set(Object.keys(JSON.parse(fs.readFileSync(path.join(__dirname,'light-bridges-v1/detour_walls.json'),'utf8'))).map(Number));
const middleWallLevels=new Set(Object.keys(JSON.parse(fs.readFileSync(path.join(__dirname,'middle-shortcut-screen-v1/walls.json'),'utf8'))).map(Number));
const unresolvedNetwork=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'unresolved-network-shortcuts.json'),'utf8')).rows.map(x=>[x.level,x]));
const resolvedNetwork=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'unresolved-network-shortcuts.json'),'utf8')).resolved.map(x=>[x.level,x]));
const expressTransit=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'transit-v1/express_routes.json'),'utf8')).map(x=>[x.level,x]));
const exactTransit=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'transit-v1/exact_transit_minima.json'),'utf8')).certified.map(x=>[x.level,x]));
const exactSignal=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'phase-choices-v1/exact_signal_minima.json'),'utf8')).certified.map(x=>[x.level,x]));
const eventAware=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'event-aware-unresolved-shortcuts.json'),'utf8')).rows.map(x=>[x.level,x]));
const lateExact=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'event-aware-exact-minima-late.json'),'utf8')).certified.map(x=>[x.level,x]));
if(preview.length!==2000||table.rows.length!==2000)throw Error('Campaign row count mismatch');
if(table.headers[3]!=='Shadow actors')throw Error('Shadow count is not labeled as actors');
for(let i=0;i<2000;i++){
  const level=preview[i],row=table.rows[i],n=i+1;
  const actors=Number(!level.noShadow)+Number(!!level.patrol2)+Number(!!level.sentinelCenter)+Number(!!level.hunterDen);
  const expected=[n,level.grid||8,level.homes.length,actors,Number(!!level.echo),level.cap];
  for(let j=0;j<expected.length;j++)if(row[j]!==expected[j])
    throw Error(`Level ${n}: column ${j+1} says ${row[j]}, preview has ${expected[j]}`);
  const hazard=row[8]||'';
  for(const [field,label] of [['shadowInfluence2x2','Shadow Influence'],['shadowSpawner','Shadow Spawner'],
    ['rechargeHouse','Leech patrol'],['sentinelCenter','Sentinel'],['hunterDen','Hunter'],
    ['lumenNetwork','Source house unlocks relay'],['nightfall','Fog radius 3'],['oneWayTile','One-way road']]){
    if(!!level[field]!==hazard.includes(label))throw Error(`Level ${n}: ${field} mismatch`);
  }
  const repair=level.repairRequired?'Free required':level.repair?'Optional':'None';
  if(row[9]!==repair)throw Error(`Level ${n}: repair row mismatch`);
  if(level.repairRequired){
    if(row[10]!==null||!Number.isInteger(row[11])||
       !['No route - free repair required','Power required - bridge house unreachable'].includes(row[12]))
      throw Error(`Level ${n}: mandatory repair misfiled as a no-power route`);
  }
  if(bridgeDetourWalls.has(n)){
    if(!level.lightBridge||row[10]!==null||!row[13].toLowerCase().includes('bridge'))
      throw Error(`Level ${n}: bridge bypass revision missing from review row`);
  }
  if(middleWallLevels.has(n)&&!row[13].includes('visual review pending')&&!row[13].includes('redesign pending'))
    throw Error(`Level ${n}: middle shortcut review flag missing`);
  if([819,865,866,891,899,940,943,953,960,974,982,1902,1904,1939,1959,1963].includes(n)&&!variantWallLevels.has(n)&&!row[13].includes('visual review pending')&&!row[13].includes('redesign pending'))
    throw Error(`Level ${n}: shadow field shortcut review missing`);
  if([1905,1910,1916,1926].includes(n)&&!row[13].includes('visual review pending')&&!row[13].includes('redesign pending'))
    throw Error(`Level ${n}: finale shortcut not flagged`);
  if((lateWallLevels.has(n)||variantWallLevels.has(n)||stormVariantLevels.has(n)||multiBandLevels.has(n))
     &&n!==1113&&!row[13].includes('visual review pending')&&!row[13].includes('redesign pending'))
    throw Error(`Level ${n}: revised street review flag missing`);
  if(n===1113&&row[13]!==(level.oneWayTile?'One-way route revised; visual review pending':'Known 102-step straight route; redesign pending'))
    throw Error('Level 1113: shortcut review state mismatch');
  if(unresolvedNetwork.has(n)){
    const known=unresolvedNetwork.get(n);
    if(row[10]!==known.steps||row[12]!=='No - faster route verified; exact pending'||
       row[13]!=='Known relay, gate and receiver bypass; structural redesign pending')
      throw Error(`Level ${n}: known network bypass is not shown accurately`);
  }
  if(resolvedNetwork.has(n)){
    if(!level.networkCircuitRequired||row[7]!=='Circuit objective: relay, voltage gate, receiver; road closes'||
       !row[8].includes('Clear requires relay, voltage gate and receiver')||
       row[13]!=='Circuit bypass blocked; balance and visual review pending')
      throw Error(`Level ${n}: resolved network circuit missing from workbook`);
  }
  if(eventAware.has(n)){
    const known=eventAware.get(n);
    if(!row[13].includes('redesign pending')&&!lateExact.has(n)&&!expressTransit.has(n)&&!exactSignal.has(n))throw Error(`Level ${n}: known shortcut review flag missing`);
    if(known.defaultSteps!==null){
      const column=level.repairRequired?11:10;
      if(!Number.isInteger(row[column])||row[column]>known.defaultSteps)
        throw Error(`Level ${n}: verified faster default route missing`);
    }
    if(known.signalSteps!==null&&(!Number.isInteger(row[11])||row[11]>known.signalSteps))
      throw Error(`Level ${n}: verified faster signal route missing`);
  }
  if(expressTransit.has(n)){
    const express=expressTransit.get(n);
    const exact=exactTransit.get(n);
    if(!exact||row[11]!==express.transitSteps||!row[8].includes('Express return ride')||
       (exact.freeRepairRequired?(row[10]!==null||row[13]!=='Exact transit minimum with free repair; balance and visual review pending'):
         (row[10]!==exact.exactSteps||row[12]!=='Yes - exact no-power minimum'||row[13]!=='Exact no-power transit minimum; balance and visual review pending')))
      throw Error(`Level ${n}: express transit proof or review flag missing`);
  }
  if(exactSignal.has(n)){
    const proof=exactSignal.get(n);
    const state=proof.freeRepairRequired?'Exact signaled minimum with free repair; balance and visual review pending':
      'Exact signaled minimum; balance and visual review pending';
    const expected=lateExact.has(n)?'Exact default and signal routes; lantern balance and visual review pending':state;
    if(row[11]!==proof.exactSignalSteps||row[13]!==expected)
      throw Error(`Level ${n}: exact signaled alternate not shown accurately`);
  }
  if(lateExact.has(n)){
    if(row[10]!==lateExact.get(n).exactNoPowerSteps||row[12]!=='Yes - exact no-power minimum'||
       row[13]!==(exactSignal.has(n)?'Exact default and signal routes; lantern balance and visual review pending':'Exact no-power route; lantern balance and visual review pending'))
      throw Error(`Level ${n}: certified exact route or review flag missing`);
  }
}
console.log('PASS: all 2,000 planning rows match preview size, houses, actors, Echo, lantern, selected hazards and repair policy');
