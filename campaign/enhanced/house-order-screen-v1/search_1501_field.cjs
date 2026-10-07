// Search one visible 2x2 influence field against all saved level-1501 tours.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname,n=1501,level=api.LEVELS[n-1];
const files=[];
for(let band=1001;band<=1901;band+=100){
  for(const variant of ['reverse','rotate','swap_first','swap_middle','swap_last']) files.push(`final-${band}-${variant}.json`);
  const prefix=band===1901?'candidate-events-1901-v2':`candidate-events-${band}`;
  for(const direction of ['ENWS','WSEN','NESW','SWNE'])files.push(`${prefix}-${direction}.json`);
}
for(let seed=1;seed<=12;seed++)files.push(`random-1001-2000-seed${seed}.json`);
const tours=files.flatMap(file=>{
  const row=JSON.parse(fs.readFileSync(path.join(dir,file))).rows.find(x=>x.level===n);
  return row?.staticCandidateRoute?[{file,route:row.staticCandidateRoute}]:[];
});
const reference=JSON.parse(fs.readFileSync(path.join(dir,'../road-events-v1/post_event_routes.json'))).find(x=>x.level===n).route.map(x=>x.p);
const signal=JSON.parse(fs.readFileSync(path.join(dir,'../candidates-v3/ROUTES_1001_2000_BASELINE.json'))).find(x=>x.level===n).solutions[0].route.map(x=>x.p);
function replay(route,useSignal=false){api.choose(n);api.begin();if(useSignal&&!api.signal())return false;for(let i=1;i<route.length;i++)if(!api.move(route[i]))return false;let s=api.getState();return s.done&&!s.failed;}
const original=level.shadowInfluence2x2,results=[];
for(let triggerCount of [1,2,3])for(let y=0;y<level.grid-1;y++)for(let x=0;x<level.grid-1;x++){
  const cells=[[x,y],[x+1,y],[x,y+1],[x+1,y+1]];
  if(cells.some(p=>level.walls.includes(p.join(','))||level.homes.some(h=>h.p.join(',')===p.join(','))||level.depot.join(',')===p.join(',')))continue;
  level.shadowInfluence2x2={trigger:'delivery',triggerCount,origin:[x,y],cells};
  if(!replay(reference)||(level.phaseChoice&&!replay(signal,true)))continue;
  const completed=tours.filter(t=>replay(t.route)).map(t=>t.file);
  results.push({triggerCount,origin:[x,y],completed:completed.length,files:completed});
}
level.shadowInfluence2x2=original;
results.sort((a,b)=>a.completed-b.completed||a.triggerCount-b.triggerCount);
fs.writeFileSync(path.join(dir,'search-1501-field-results.json'),JSON.stringify({tours:tours.length,results},null,2));
console.log(JSON.stringify({tours:tours.length,best:results.slice(0,10)}));
