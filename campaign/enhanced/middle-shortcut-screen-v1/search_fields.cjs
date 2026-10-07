// Search reusable 2x2 delivery-triggered shadow fields for persistent shortcuts.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname;
const archive=JSON.parse(fs.readFileSync(path.join(dir,'../../../design/map-solutions-1000.json'),'utf8')).levels;
const targets=process.env.LLC_MIDDLE_FIELD_TARGETS?process.env.LLC_MIDDLE_FIELD_TARGETS.split(',').map(Number):[406,525,557,630,664];
const orders=['ENWS','WSEN','NESW','SWNE'];
const key=p=>p.join(',');
function replay(n,points){
  api.choose(n);api.begin();const l=api.getLevel();
  if(l.repairRequired&&l.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<points.length;i++)if(!api.move(points[i]))return false;
  const s=api.getState();return s.done&&!s.failed;
}
const results=[];
for(const n of targets){
  const l=api.LEVELS[n-1],old=l.shadowInfluence2x2;
  const reference=archive[n-1].solutions[0].route.map(s=>s.p);
  const direct=[];
  for(const order of orders){
    const row=JSON.parse(fs.readFileSync(path.join(dir,`reroute-${Math.floor((n-1)/100)*100+1}-${order}.json`),'utf8')).rows.find(x=>x.level===n);
    const result=JSON.parse(fs.readFileSync(path.join(dir,`reroute-replay-${Math.floor((n-1)/100)*100+1}-${order}.json`),'utf8'));
    if(result.completedRoutes.some(x=>x.level===n))direct.push(row.staticCandidateRoute);
  }
  const protectedCells=new Set([l.depot,...l.homes.map(h=>h.p),...l.patrol,...(l.patrol2||[]),
    ...['fade','ice','dark','switch','gate','oneWayTile','collapseTile','sentinelCenter','shadowDoor','shadowLock','lightBridge','hiddenRoad'].flatMap(f=>l[f]?[l[f]]:[]),
    ...(l.repair?[l.repair.tile]:[])].map(key));
  const walls=new Set(l.walls),valid=[];
  const triggerCounts=process.env.LLC_MIDDLE_FIELD_LATE==='1'?[5,6,7,8,9,10]:[1,2,3,4];
  for(const triggerCount of triggerCounts){
    const first=archive[n-1].solutions[0].route.findIndex(s=>s.mask.toString(2).replace(/0/g,'').length>=triggerCount);
    if(first<0)continue;
    const afterRef=new Set(reference.slice(first+1).map(key));
    for(let y=0;y<l.grid-1;y++)for(let x=0;x<l.grid-1;x++){
      const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]];
      if(cells.some(p=>walls.has(key(p))||protectedCells.has(key(p))||afterRef.has(key(p))))continue;
      l.shadowInfluence2x2={trigger:['','first_delivery','second_delivery','third_delivery','fourth_delivery'][triggerCount]||'delivery',triggerCount,origin:[x,y],cells};
      if(!replay(n,reference))continue;
      if(direct.every(route=>!replay(n,route)))valid.push({triggerCount,origin:[x,y],cells});
    }
  }
  l.shadowInfluence2x2=old;
  valid.sort((a,b)=>a.triggerCount-b.triggerCount||a.origin[1]-b.origin[1]||a.origin[0]-b.origin[0]);
  const field=valid[0];
  results.push({level:n,knownRoutes:direct.length,viable:valid.length,best:field||null});
  console.log(n,'routes',direct.length,'fields',valid.length,field?.origin||'NONE');
}
fs.writeFileSync(path.join(dir,'field_search.json'),JSON.stringify(results,null,2));
const output=process.env.LLC_MIDDLE_FIELD_LATE==='1'?'candidate_late_fields.json':'candidate_fields.json';
fs.writeFileSync(path.join(dir,output),JSON.stringify(Object.fromEntries(results.filter(x=>x.best).map(x=>[x.level,{trigger:['','first_delivery','second_delivery','third_delivery','fourth_delivery'][x.best.triggerCount]||'delivery',...x.best}])),null,2));
