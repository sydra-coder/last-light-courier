const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const dir=__dirname;
const proofs=new Map(JSON.parse(fs.readFileSync(path.join(dir,'../quakes-v1/post_event_routes.json'),'utf8')).map(x=>[x.level,x.route.map(s=>s.p)]));
const targets=[819,865,866,891,940];
const orders=['ENWS','WSEN','NESW','SWNE'];
const screens=new Map();
for(const band of [801,901])for(const order of orders){
  const file=path.join(dir,`static-${band}-${order}.json`);
  for(const row of JSON.parse(fs.readFileSync(file,'utf8')).rows)screens.set(`${row.level}-${order}`,row.staticCandidateRoute);
}
function replay(n,route){
  api.choose(n);api.begin();const l=api.getLevel();
  if(l.repairRequired&&l.repair?.cost===0)api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))return false;
  const s=api.getState();return s.done&&!s.failed;
}
const chosen={};
for(const n of targets){
  const level=api.LEVELS[n-1],old=level.shadowInfluence2x2;
  const candidates=[];
  for(const timing of ['first','second'])candidates.push(...JSON.parse(fs.readFileSync(path.join(dir,`field-${n}-${timing}.json`),'utf8'))[0].top);
  const valid=[];
  for(const field of candidates){
    level.shadowInfluence2x2={trigger:field.triggerCount===1?'first_delivery':'second_delivery',triggerCount:field.triggerCount,origin:field.origin,cells:field.cells};
    const reference=replay(n,proofs.get(n));
    const completion=orders.filter(order=>replay(n,screens.get(`${n}-${order}`)));
    if(reference&&completion.length===0)valid.push({...field});
  }
  level.shadowInfluence2x2=old;
  valid.sort((a,b)=>a.triggerCount-b.triggerCount||b.hits-a.hits||a.directBlockedAt-b.directBlockedAt);
  if(valid.length)chosen[n]={trigger:valid[0].triggerCount===1?'first_delivery':'second_delivery',triggerCount:valid[0].triggerCount,origin:valid[0].origin,cells:valid[0].cells};
  console.log(n,`${valid.length}/${candidates.length} fields block all four screens`,chosen[n]||'NONE');
}
fs.writeFileSync(path.join(dir,'candidate_fields.json'),JSON.stringify(chosen,null,2));
