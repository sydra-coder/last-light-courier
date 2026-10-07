const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname,n=525,level=api.LEVELS[n-1],original=level.sentinelCenter;
const archive=JSON.parse(fs.readFileSync(path.join(dir,'../../../design/map-solutions-1000.json'),'utf8')).levels;
const reference=archive[n-1].solutions[0].route.map(s=>s.p);
const routes=[];
for(const order of ['ENWS','WSEN','NESW','SWNE']){
  const source=JSON.parse(fs.readFileSync(path.join(dir,`reroute-501-${order}.json`),'utf8')).rows.find(x=>x.level===n);
  const report=JSON.parse(fs.readFileSync(path.join(dir,`reroute-replay-501-${order}.json`),'utf8'));
  if(report.completedRoutes.some(x=>x.level===n))routes.push(source.staticCandidateRoute);
}
const key=p=>p.join(',');
const first=archive[n-1].solutions[0].route.findIndex(s=>s.mask>0);
const afterRef=new Set(reference.slice(first+1).map(key));
function replay(points){api.choose(n);api.begin();if(level.repairRequired)api.buyFreeRepair();
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return false;
  const s=api.getState();return s.done&&!s.failed;}
const valid=[];
for(let y=1;y<level.grid-1;y++)for(let x=1;x<level.grid-1;x++){
  const zone=[];for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++)zone.push([x+dx,y+dy]);
  if(zone.some(p=>level.walls.includes(key(p))||afterRef.has(key(p))||level.homes.some(h=>key(h.p)===key(p))||key(level.depot)===key(p)))continue;
  level.sentinelCenter=[x,y];
  if(replay(reference)&&routes.every(route=>!replay(route)))valid.push({center:[x,y]});
}
level.sentinelCenter=original;
fs.writeFileSync(path.join(dir,'sentinel_525_candidates.json'),JSON.stringify(valid,null,2));
console.log(`Sentinel positions blocking ${routes.length} fast routes: ${valid.length}`,valid.slice(0,15));
