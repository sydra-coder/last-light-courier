// Search first/second-delivery 2x2 fields against level 778 house-order shortcuts.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const n=778,level=api.LEVELS[n-1],old=level.shadowInfluence2x2;
const reference=JSON.parse(fs.readFileSync(path.join(__dirname,'../bridge-spurs-v1/routes.json'),'utf8'))[n];
const sources=['final-bridge-reverse.json','fieldfresh-reverse-SWNE.json'];
const direct=[];
for(const name of sources){
  const row=JSON.parse(fs.readFileSync(path.join(__dirname,name),'utf8')).rows.find(x=>x.level===n);
  const replay=JSON.parse(fs.readFileSync(path.join(__dirname,name.replace('.json','-replay.json')),'utf8'));
  if(replay.completedRoutes.some(x=>x.level===n))direct.push(row.staticCandidateRoute);
}
const key=p=>p.join(',');
const protectedCells=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
  ...['fade','ice','dark','switch','gate','lightBridge','oneWayTile','oneWayFrom'].flatMap(f=>level[f]?[level[f]]:[]),
  ...(level.repair?[level.repair.tile]:[])].map(key));
const walls=new Set(level.walls);
function replay(route){
  api.choose(n);api.begin();if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++){
    const state=api.getState();if(state.active&&!state.bridgeBuilt&&!api.useBridge())return false;
    if(!api.move(route[i]))return false;
  }
  const state=api.getState();return state.done&&!state.failed;
}
const options=[];
for(const triggerCount of [1,2,3,4]){
  api.choose(n);api.begin();if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  let first=-1;
  for(let i=1;i<reference.length;i++){
    if(api.getState().active&&!api.getState().bridgeBuilt)api.useBridge();
    if(!api.move(reference[i]))throw Error(`Reference failed at ${i}`);
    if(first<0&&api.getState().mask.toString(2).replace(/0/g,'').length>=triggerCount)first=i;
  }
  if(first<0)continue;
  const later=new Set(reference.slice(first+1).map(key));
  for(let y=0;y<level.grid-1;y++)for(let x=0;x<level.grid-1;x++){
    const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]];
    if(cells.some(p=>walls.has(key(p))||protectedCells.has(key(p))||later.has(key(p))))continue;
    level.shadowInfluence2x2={trigger:'delivery',triggerCount,origin:[x,y],cells};
    if(replay(reference)&&direct.every(route=>!replay(route)))options.push({triggerCount,origin:[x,y],cells});
  }
}
level.shadowInfluence2x2=old;
fs.writeFileSync(path.join(__dirname,'field_778_options.json'),JSON.stringify(options,null,2));
console.log(JSON.stringify({knownFastRoutes:direct.length,viableFields:options.length,first:options[0]||null}));
