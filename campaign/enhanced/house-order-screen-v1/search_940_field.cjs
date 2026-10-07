const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const api=require(path.join(root,'test_integrated_preview.cjs'));
const n=940;
const old=JSON.parse(fs.readFileSync(path.join(root,'quake-variant-screen-v1/static-901-ENWS.json'))).rows.find(r=>r.level===n).staticCandidateRoute;
const latest=JSON.parse(fs.readFileSync(path.join(__dirname,'candidate-six-rotate.json'))).rows.find(r=>r.level===n).staticCandidateRoute;
const reference=JSON.parse(fs.readFileSync(path.join(root,'quakes-v1/post_event_routes.json'))).find(r=>r.level===n).route.map(s=>s.p);
const level=api.LEVELS[n-1],prior=level.shadowInfluence2x2;
const key=p=>p.join(',');
const protectedTiles=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
  ...['fade','ice','dark','switch','gate'].flatMap(field=>level[field]?[level[field]]:[]),
  ...(level.repair?[level.repair.tile]:[]),...(level.quakeEvent?[level.quakeEvent.close,level.quakeEvent.open]:[]),
  ...(level.aftershock?[level.aftershock.tile]:[])].map(key));
const walls=new Set(level.walls);
function replay(route){
  api.choose(n);api.begin();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return {done:false,step:i};
  const s=api.getState();return {done:s.done&&!s.failed,step:null};
}
const results=[];
for(const triggerCount of [1,2,3])for(let y=0;y<level.grid-1;y++)for(let x=0;x<level.grid-1;x++){
  const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]];
  if(cells.some(p=>walls.has(key(p))||protectedTiles.has(key(p))))continue;
  level.shadowInfluence2x2={trigger:['','first_delivery','second_delivery','third_delivery'][triggerCount],triggerCount,origin:[x,y],cells};
  if(!replay(reference).done)continue;
  const a=replay(old),b=replay(latest);
  if(!a.done&&!b.done)results.push({origin:[x,y],triggerCount,oldBlockedAt:a.step,newBlockedAt:b.step,cells});
}
level.shadowInfluence2x2=prior;
fs.writeFileSync(path.join(__dirname,'field-940-dual-candidates.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify({viable:results.length,first:results.slice(0,10)}));
