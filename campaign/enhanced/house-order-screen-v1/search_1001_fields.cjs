// Search one 2x2 post-delivery field per affected map against every known fast tour.
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const api=require(path.join(root,'test_integrated_preview.cjs'));
const variants=['reverse','rotate','swap_first','swap_middle','swap_last'];
const audits=variants.map(v=>({
  name:v,
  rows:JSON.parse(fs.readFileSync(path.join(__dirname,`final-1001-${v}.json`))).rows,
  done:new Set(JSON.parse(fs.readFileSync(path.join(__dirname,`final-1001-${v}-replay.json`))).completedRoutes.map(x=>x.level)),
}));
const proofs=new Map(JSON.parse(fs.readFileSync(path.join(root,'road-events-v1/post_event_routes.json'))).map(x=>[x.level,x]));
const targets=[...new Set(audits.flatMap(a=>[...a.done]))].sort((a,b)=>a-b);
const key=p=>p.join(',');
function replay(n,route){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return {done:false,step:i};
  const s=api.getState();return {done:s.done&&!s.failed,step:null};
}
const results=[];
for(const n of targets){
  const level=api.LEVELS[n-1],prior=level.shadowInfluence2x2;
  const reference=proofs.get(n).route.map(s=>s.p);
  const shortcuts=audits.filter(a=>a.done.has(n)).map(a=>({variant:a.name,route:a.rows.find(r=>r.level===n).staticCandidateRoute}));
  const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
    ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
    ...(level.repair?[level.repair.tile]:[]),
    ...(level.authoredEvent?[level.authoredEvent.tile]:[]),
    ...(level.stormWind?[level.stormWind.from,level.stormWind.to]:[]),
    ...(level.floodRoad?[level.floodRoad.tile]:[])].map(key));
  const walls=new Set(level.walls),candidates=[];
  for(const triggerCount of [1,2,3])for(let y=0;y<level.grid-1;y++)for(let x=0;x<level.grid-1;x++){
    const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]];
    if(cells.some(p=>walls.has(key(p))||protectedTiles.has(key(p))))continue;
    level.shadowInfluence2x2={trigger:['','first_delivery','second_delivery','third_delivery'][triggerCount],triggerCount,origin:[x,y],cells};
    if(!replay(n,reference).done)continue;
    const checked=shortcuts.map(s=>({...replay(n,s.route),variant:s.variant}));
    if(checked.every(x=>!x.done))candidates.push({origin:[x,y],cells,triggerCount,blocked:checked});
  }
  level.shadowInfluence2x2=prior;
  candidates.sort((a,b)=>Math.min(...a.blocked.map(x=>x.step))-Math.min(...b.blocked.map(x=>x.step)));
  results.push({level:n,shortcuts:shortcuts.map(x=>x.variant),viable:candidates.length,best:candidates[0]||null,top:candidates.slice(0,8)});
}
fs.writeFileSync(path.join(__dirname,'field-search-1001.json'),JSON.stringify(results,null,2));
console.log(results.map(x=>({level:x.level,shortcuts:x.shortcuts,viable:x.viable,best:x.best&&{origin:x.best.origin,triggerCount:x.best.triggerCount,blocked:x.best.blocked}})));
