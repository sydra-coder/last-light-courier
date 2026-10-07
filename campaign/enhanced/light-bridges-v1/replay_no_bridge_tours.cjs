const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const input=process.env.LLC_NO_BRIDGE_TOURS||path.join(__dirname,'no_bridge_tours.json');
const output=process.env.LLC_NO_BRIDGE_REPLAY||path.join(__dirname,'no_bridge_rule_replay.json');
const tours=JSON.parse(fs.readFileSync(input,'utf8'));
const rows=[];
for(const tour of tours){
  api.choose(tour.level);api.begin();
  const l=api.getLevel();
  if(l.repairRequired&&l.repair?.cost===0)api.buyFreeRepair();
  let failure=null;
  for(let i=1;i<tour.route.length;i++)if(!api.move(tour.route[i])){
    const s=api.getState();failure={step:i,reason:s.reason||'move rejected',light:s.light};break;
  }
  const end=api.getState();
  rows.push({level:tour.level,order:tour.order||null,steps:tour.steps,completed:!failure&&end.done&&!end.failed,finishLight:!failure&&end.done?end.light:null,failure});
}
fs.writeFileSync(output,JSON.stringify({scope:'Screened candidate tours; a failed tour does not prove power required',rows},null,2));
const complete=rows.filter(r=>r.completed);
console.log(`No-bridge static tour: ${complete.length}/${rows.length} completed`);
console.log(complete.slice(0,20));
