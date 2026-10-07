// Reposition existing road-close cues, preserving map-event variety and reference completion.
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const api=require(path.join(root,'test_integrated_preview.cjs'));
const band=Number(process.env.LLC_SCREEN_BAND||1001);
const randomMode=process.env.LLC_SCREEN_RANDOM==='1';
const variants=['reverse','rotate','swap_first','swap_middle','swap_last'];
const seeds=(process.env.LLC_SCREEN_SEEDS||'1,2,3,4').split(',').map(Number);
const audits=randomMode?seeds.map(seed=>({name:`random_seed${seed}`,
  rows:JSON.parse(fs.readFileSync(path.join(__dirname,`random-1001-2000-seed${seed}.json`))).rows,
  done:new Set(JSON.parse(fs.readFileSync(path.join(__dirname,`random-1001-2000-seed${seed}-replay.json`))).completedRoutes.map(x=>x.level))})):
  variants.map(v=>({name:v,rows:JSON.parse(fs.readFileSync(path.join(__dirname,`final-${band}-${v}.json`))).rows,
  done:new Set(JSON.parse(fs.readFileSync(path.join(__dirname,`final-${band}-${v}-replay.json`))).completedRoutes.map(x=>x.level))}));
if(!randomMode&&band===1001)audits.push({name:'best_SWNE',rows:JSON.parse(fs.readFileSync(path.join(__dirname,'candidate-events-1001-SWNE.json'))).rows,
  done:new Set(JSON.parse(fs.readFileSync(path.join(__dirname,'candidate-events-1001-SWNE-replay.json'))).completedRoutes.map(x=>x.level))});
if(!randomMode&&band===1901)for(const variant of ['swap_first','swap_middle'])audits.push({name:`reroute_${variant}`,
  rows:JSON.parse(fs.readFileSync(path.join(__dirname,`final-1901-${variant}.json`))).rows,
  done:new Set(JSON.parse(fs.readFileSync(path.join(__dirname,`candidate-events-1901-${variant}-replay.json`))).completedRoutes.map(x=>x.level))});
if(randomMode)audits.push({name:'previous_reverse_1873',
  rows:JSON.parse(fs.readFileSync(path.join(__dirname,'final-1801-reverse.json'))).rows,
  done:new Set([1873])});
if(process.env.LLC_EXTRA_COMPLETED_REPORT){
  const extra=JSON.parse(fs.readFileSync(path.resolve(process.env.LLC_EXTRA_COMPLETED_REPORT))).shorterRoutes;
  const grouped=new Map();
  for(const row of extra){if(!grouped.has(row.source))grouped.set(row.source,new Set());grouped.get(row.source).add(row.level);}
  for(const [source,done] of grouped)audits.push({name:`prior_${source}`,
    rows:JSON.parse(fs.readFileSync(path.join(__dirname,source))).rows,done});
}
const proofs=new Map(JSON.parse(fs.readFileSync(path.join(root,'road-events-v1/post_event_routes.json'))).map(x=>[x.level,x]));
const signalProofs=new Map(JSON.parse(fs.readFileSync(path.join(root,'candidates-v3/ROUTES_1001_2000_BASELINE.json'))).map(x=>[x.level,x.solutions[0].route.map(s=>s.p)]));
const targetFilter=process.env.LLC_SCREEN_TARGETS?new Set(process.env.LLC_SCREEN_TARGETS.split(',').map(Number)):null;
const targets=[...new Set(audits.flatMap(a=>[...a.done]))].filter(n=>!targetFilter||targetFilter.has(n)).sort((a,b)=>a-b);
const key=p=>p.join(',');
function replay(n,route,signal=false){api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  if(signal&&!api.signal())return {done:false,step:0};
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return {done:false,step:i};
  const s=api.getState();return {done:s.done&&!s.failed,step:null};}
const out=[];
for(const n of targets){
  const level=api.LEVELS[n-1],event=level.authoredEvent,original=event.tile,oldDefault=level.phaseChoice?.defaultClose;
  if(event.kind!=='road_close'||event.trigger!=='first_delivery')throw Error(`Unexpected event ${n}`);
  const reference=proofs.get(n).route.map(s=>s.p);
  const shortcuts=audits.filter(a=>a.done.has(n)).map(a=>({variant:a.name,route:a.rows.find(r=>r.level===n).staticCandidateRoute}));
  const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
    ...(level.repair?[level.repair.tile]:[]),
    ...(level.stormWind?[level.stormWind.from,level.stormWind.to]:[]),
    ...(level.floodRoad?[level.floodRoad.tile]:[]),
    ...(level.nightfall?[level.nightfall.tile]:[]),
    ...(level.dayNightCycle?[level.dayNightCycle.moonRoad]:[]),
    ...(level.shadowSpawner?[level.shadowSpawner.origin,...level.shadowSpawner.stages]:[]),
    ...(level.lumenNetwork?[level.lumenNetwork.relayTile]:[]),
    ...(level.lightOverloadGate?[level.lightOverloadGate.tile]:[]),
    ...(level.lightTransfer?[level.lightTransfer.source,level.lightTransfer.receiver]:[]),
    ...(level.chainEvent?[level.chainEvent.close,...level.chainEvent.open]:[]),
    ...(level.transitLink?level.transitLink.stops:[]),
    ...(level.phaseChoice?[level.phaseChoice.alternateClose]:[]),
    ...(level.aftershock?[level.aftershock.tile]:[]),
    ...(level.hiddenRoad?[level.hiddenRoad]:[]),
    ...(level.collapseTile?[level.collapseTile]:[]),
    ...(level.rechargeHouse?[level.rechargeHouse.tile]:[])].map(key));
  const walls=new Set(level.walls),candidates=[];
  const tiles=[...new Map(shortcuts.flatMap(s=>s.route.map(p=>[key(p),p]))).values()];
  for(const tile of tiles){
    if(walls.has(key(tile))||protectedTiles.has(key(tile))||key(tile)===key(original))continue;
    event.tile=tile;
    if(level.phaseChoice)level.phaseChoice.defaultClose=tile;
    if(!replay(n,reference).done)continue;
    if(level.phaseChoice&&!replay(n,signalProofs.get(n),true).done)continue;
    const checks=shortcuts.map(s=>({...replay(n,s.route),variant:s.variant}));
    if(checks.every(x=>!x.done))candidates.push({tile,checks});
  }
  event.tile=original;
  if(level.phaseChoice)level.phaseChoice.defaultClose=oldDefault;
  candidates.sort((a,b)=>Math.min(...a.checks.map(x=>x.step))-Math.min(...b.checks.map(x=>x.step)));
  out.push({level:n,original,shortcuts:shortcuts.map(s=>s.variant),viable:candidates.length,best:candidates[0]||null,top:candidates.slice(0,8)});
}
const output=process.env.LLC_EVENT_TILE_SEARCH_OUTPUT||path.join(__dirname,randomMode?'event-tile-search-random-1001-2000.json':`event-tile-search-${band}.json`);
fs.writeFileSync(output,JSON.stringify(out,null,2));
console.log(out.map(x=>({level:x.level,viable:x.viable,best:x.best})));
