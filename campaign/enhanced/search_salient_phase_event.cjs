// Find a visible first-delivery road closure that changes a real house route.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=path.join(__dirname,'house-order-screen-v1'),n=Number(process.env.LLC_SALIENCE_LEVEL||1901),level=api.LEVELS[n-1];
if(n<1801||n>2000||!level.phaseChoice)throw Error('Expected phase-choice level 1801–2000');
const band=Math.floor((n-1001)/100)*100+1001;
const proof=JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'))).find(x=>x.level===n);
const reference=proof.route.map(s=>s.p),referenceSteps=reference.length-1;
const first=proof.route.find(s=>s.mask).p;
const signalRoute=JSON.parse(fs.readFileSync(path.join(__dirname,'candidates-v3/ROUTES_1001_2000_BASELINE.json'))).find(x=>x.level===n).solutions[0].route.map(s=>s.p);
const homes=level.homes.map(h=>h.p),targets=[...homes.filter(p=>p.join(',')!==first.join(',')),level.depot];
const key=p=>p.join(',');
const prefix=band===1901?'candidate-events-1901-v2':`candidate-events-${band}`;
const sourceFiles=[...['reverse','rotate','swap_first','swap_middle','swap_last'].map(x=>`final-${band}-${x}.json`),
  ...['ENWS','WSEN','NESW','SWNE'].map(x=>`${prefix}-${x}.json`),
  ...Array.from({length:16},(_,i)=>`random-1001-2000-seed${i+1}.json`)];
for(const file of sourceFiles)if(!fs.existsSync(path.join(dir,file)))throw Error(`Missing screen ${file}`);
const blocked=new Set(level.walls);
const tours=sourceFiles.map(file=>({file,route:JSON.parse(fs.readFileSync(path.join(dir,file))).rows.find(r=>r.level===n)?.staticCandidateRoute})).filter(x=>x.route);
const signalShortcuts=fs.existsSync(path.join(dir,'signal-tour-screen.json'))?
  JSON.parse(fs.readFileSync(path.join(dir,'signal-tour-screen.json'))).shorterRoutes.filter(x=>x.level===n):[];
const event=level.authoredEvent,alternateMode=process.env.LLC_PHASE_SIDE==='alternate';
const original=alternateMode?level.phaseChoice.alternateClose:event.tile;
function setTile(tile){if(alternateMode)level.phaseChoice.alternateClose=tile;else{event.tile=tile;level.phaseChoice.defaultClose=tile}}
function replay(route,signal=false){api.choose(n);api.begin();if(level.repairRequired&&level.repair?.cost===0&&!api.buyFreeRepair())return false;if(signal&&!api.signal())return false;for(let i=1;i<route.length;i++)if(!api.move(route[i]))return false;const s=api.getState();return s.done&&!s.failed}
setTile([-1,-1]);
const critical=tours.filter(t=>t.route.length-1<referenceSteps&&replay(t.route));
setTile(original);
function distances(start,extra){const seen=new Map([[key(start),0]]),queue=[start];for(let i=0;i<queue.length;i++){
  const [x,y]=queue[i],d=seen.get(key(queue[i]));for(const p of [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]){
    const k=key(p);if(p[0]<0||p[1]<0||p[0]>=level.grid||p[1]>=level.grid||blocked.has(k)||(extra&&k===key(extra))||seen.has(k))continue;
    seen.set(k,d+1);queue.push(p);
  }}return seen}
const open=distances(first,null);
const protectedTiles=new Set([level.depot,...homes,...level.patrol,...(level.patrol2||[]),
  ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
  ...(level.repair?[level.repair.tile]:[]),
  ...(level.stormWind?[level.stormWind.from,level.stormWind.to]:[]),
  ...(level.floodRoad?[level.floodRoad.tile]:[]),
  ...(level.nightfall?[level.nightfall.tile]:[]),
  ...(level.shadowSpawner?[level.shadowSpawner.origin,...level.shadowSpawner.stages]:[]),
  ...(level.lumenNetwork?[level.lumenNetwork.relayTile]:[]),
  ...(level.lightOverloadGate?[level.lightOverloadGate.tile]:[]),
  ...(level.lightTransfer?[level.lightTransfer.source,level.lightTransfer.receiver]:[]),
  ...(level.chainEvent?[level.chainEvent.close,...level.chainEvent.open]:[]),
  ...(level.transitLink?level.transitLink.stops:[]),
  ...(level.phaseChoice?[alternateMode?level.phaseChoice.defaultClose:level.phaseChoice.alternateClose]:[]),
  ...(level.aftershock?[level.aftershock.tile]:[]),
  ...(level.hiddenRoad?[level.hiddenRoad]:[]),
  ...(level.collapseTile?[level.collapseTile]:[]),
  ...(level.rechargeHouse?[level.rechargeHouse.tile]:[])].map(key));
for(const p of [
  ...(level.shadowInfluence2x2?[level.shadowInfluence2x2.origin,...level.shadowInfluence2x2.cells]:[]),
  ...(level.hunterDen?[level.hunterDen]:[]),
  ...(level.sentinelCenter?[level.sentinelCenter]:[]),
  ...(level.oneWayTile?[level.oneWayTile]:[]),
  ...(level.shadowDoor?[level.shadowDoor]:[]),
  ...(level.lightBridge?[level.lightBridge]:[])
])protectedTiles.add(key(p));
const results=[];
for(let y=0;y<level.grid;y++)for(let x=0;x<level.grid;x++){
  const tile=[x,y],k=key(tile);
  if(blocked.has(k)||protectedTiles.has(k)||k===key(original))continue;
  const closed=distances(first,tile);
  const affected=targets.filter(t=>open.has(key(t))&&closed.get(key(t))!==open.get(key(t)));
  if(!affected.length)continue;
  setTile(tile);
  if(!replay(reference)||!replay(signalRoute,true)||critical.some(t=>replay(t.route))||
     signalShortcuts.some(t=>replay(t.route,true)))continue;
  api.choose(n);api.begin();
  if(level.repairRequired&&level.repair?.cost===0&&!api.buyFreeRepair())throw Error(`Free repair failed ${n}`);
  for(let i=1;i<proof.route.length;i++){if(!api.move(proof.route[i].p))throw Error(`Reference failed ${n} at ${i}`);if(api.getState().mask)break}
  const state=api.getState(),[sx,sy]=state.pos,prior=proof.route.findIndex(s=>s.mask)-1;
  const legal=[[sx+1,sy],[sx-1,sy],[sx,sy+1],[sx,sy-1]].filter(api.legal);
  const forward=legal.filter(p=>key(p)!==key(proof.route[prior].p)).length;
  results.push({tile,affectedTargets:affected.length,distanceToFirst:open.get(k),firstDeliveryForward:forward,blockedKnownShortcuts:critical.length});
}
setTile(original);
results.sort((a,b)=>b.affectedTargets-a.affectedTargets||b.firstDeliveryForward-a.firstDeliveryForward||a.distanceToFirst-b.distanceToFirst);
const report={level:n,original,first,referenceSteps,knownTours:tours.length,
  criticalTours:critical.map(t=>t.file),criticalSignalTours:signalShortcuts.length,results};
fs.writeFileSync(path.join(__dirname,`salient-phase-${alternateMode?'alternate':'default'}-search-${n}.json`),JSON.stringify(report,null,2));
console.log(JSON.stringify({level:n,original,knownTours:tours.length,criticalTours:critical.length,viable:results.length,top:results.slice(0,12)}));
