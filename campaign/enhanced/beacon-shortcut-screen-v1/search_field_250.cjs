const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const n=250,level=api.LEVELS[n-1],old=level.shadowInfluence2x2;
const reference=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../design/map-solutions-1000.json'),'utf8')).levels[n-1].solutions[0].route.map(s=>s.p);
const orders=['ENWS','WSEN','NESW','SWNE'];
const routes=[];
for(const order of orders){
  const suffix=order==='ENWS'?'':`-${order}`;
  const result=JSON.parse(fs.readFileSync(path.join(__dirname,`replay${suffix}.json`),'utf8'));
  if(result.completedRoutes.some(r=>r.level===n)){
    const audit=JSON.parse(fs.readFileSync(path.join(__dirname,`audit${suffix}.json`),'utf8'));
    routes.push(audit.rows.find(r=>r.level===n).staticCandidateRoute);
  }
}
const key=p=>p.join(',');
const protectedCells=new Set([level.depot,...level.homes.map(h=>h.p),...level.patrol,...(level.patrol2||[]),
  ...['fade','ice','dark','switch','gate','hiddenRoad'].flatMap(k=>level[k]?[level[k]]:[]),level.repair.tile].map(key));
const walls=new Set(level.walls);
function replay(route){
  api.choose(n);api.begin();api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return false;
  const state=api.getState();return state.done&&!state.failed;
}
const options=[];
for(const triggerCount of [1,2,3,4,5,6,7,8]){
  const first=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../design/map-solutions-1000.json'),'utf8')).levels[n-1].solutions[0].route.findIndex(s=>s.mask.toString(2).replace(/0/g,'').length>=triggerCount);
  if(first<0)continue;
  const later=new Set(reference.slice(first+1).map(key));
  for(let y=0;y<level.grid-1;y++)for(let x=0;x<level.grid-1;x++){
    const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]];
    if(cells.some(p=>walls.has(key(p))||protectedCells.has(key(p))||later.has(key(p))))continue;
    level.shadowInfluence2x2={trigger:'delivery',triggerCount,origin:[x,y],cells};
    if(replay(reference)&&routes.every(route=>!replay(route)))options.push({triggerCount,origin:[x,y],cells});
  }
}
level.shadowInfluence2x2=old;
fs.writeFileSync(path.join(__dirname,'field_options_250.json'),JSON.stringify(options,null,2));
console.log(JSON.stringify({knownRoutes:routes.length,viable:options.length,first:options[0]||null}));
