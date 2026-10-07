const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname,n=525,level=api.LEVELS[n-1],original=level.hunterDen;
const archive=JSON.parse(fs.readFileSync(path.join(dir,'../../../design/map-solutions-1000.json'),'utf8')).levels;
const reference=archive[n-1].solutions[0].route.map(s=>s.p),routes=[];
for(const order of ['ENWS','WSEN','NESW','SWNE']){
  const source=JSON.parse(fs.readFileSync(path.join(dir,`reroute-501-${order}.json`),'utf8')).rows.find(x=>x.level===n);
  const report=JSON.parse(fs.readFileSync(path.join(dir,`reroute-replay-501-${order}.json`),'utf8'));
  if(report.completedRoutes.some(x=>x.level===n))routes.push(source.staticCandidateRoute);
}
const key=p=>p.join(',');
function replay(points){api.choose(n);api.begin();if(level.repairRequired)api.buyFreeRepair();
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return false;
  const s=api.getState();return s.done&&!s.failed;}
const valid=[];
for(let y=0;y<level.grid;y++)for(let x=0;x<level.grid;x++){
  const p=[x,y];
  if(level.walls.includes(key(p))||level.homes.some(h=>key(h.p)===key(p))||key(level.depot)===key(p)||reference.some(q=>key(q)===key(p)))continue;
  level.hunterDen=p;
  if(replay(reference)&&routes.every(route=>!replay(route)))valid.push({den:p});
}
level.hunterDen=original;
fs.writeFileSync(path.join(dir,'hunter_525_candidates.json'),JSON.stringify(valid,null,2));
console.log(`Hunter dens blocking ${routes.length} fast routes: ${valid.length}`,valid.slice(0,15));
