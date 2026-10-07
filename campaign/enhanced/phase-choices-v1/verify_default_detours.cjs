const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const here=__dirname;
const trial=JSON.parse(fs.readFileSync(path.join(here,'default_detour_trials.json'))).find(x=>x.level===1804);
const search=JSON.parse(fs.readFileSync(path.join(here,'default_1900_search.json'))).found;
const rows=[];
for(const item of [trial,search]){
  api.choose(item.level);api.begin();
  if(api.getLevel().repairRequired)api.buyFreeRepair();
  for(let i=1;i<item.route.length;i++)if(!api.move(item.route[i]))throw Error(`${item.level} blocked at ${i}`);
  const state=api.getState();
  if(!state.done||state.failed||state.turns!==item.steps||state.light!==item.finishLight)
    throw Error(`${item.level} full-rule replay mismatch`);
  rows.push({level:item.level,steps:state.turns,finishLight:state.light,freeRepairRequired:!!api.getLevel().repairRequired,route:item.route});
}
fs.writeFileSync(path.join(here,'verified_default_detours.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows.map(({level,steps,finishLight,freeRepairRequired})=>({level,steps,finishLight,freeRepairRequired}))));
