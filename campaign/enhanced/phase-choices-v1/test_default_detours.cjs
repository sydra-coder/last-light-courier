const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const root=path.resolve(__dirname,'..');
const signals=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_signal_routes.json')));
const plans=[
  {n:1804,at:50,detour:[[8,14],[7,14],[6,14]]},
  {n:1900,at:82,detour:[[20,9],[20,10],[20,11]]},
];
const rows=[];
for(const {n,at,detour} of plans){
  const route=signals[n].map(s=>s.slice(0,2));
  const amended=[...route.slice(0,at),...detour,...route.slice(at+1)];
  api.choose(n);api.begin();if(api.getLevel().repairRequired&&!api.buyFreeRepair())throw Error(`Repair unavailable ${n}`);
  let blocked=null;
  for(let i=1;i<amended.length;i++)if(!api.move(amended[i])){blocked={step:i,tile:amended[i],state:api.getState()};break}
  const end=api.getState();
  rows.push({level:n,completed:!blocked&&end.done&&!end.failed,blocked,steps:end.turns,finishLight:end.light,route:amended});
}
fs.writeFileSync(path.join(__dirname,'default_detour_trials.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows.map(({level,completed,blocked,steps,finishLight})=>({level,completed,blocked:blocked&&{step:blocked.step,tile:blocked.tile},steps,finishLight}))));
