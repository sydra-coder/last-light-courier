// Exercise every assigned late-campaign review charge on its recorded route.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'),'utf8'));
const tuned=JSON.parse(fs.readFileSync(process.env.LLC_BALANCE_CAPS_PATH||path.join(__dirname,'lantern-balance-v1/promoted_caps.json'),'utf8'));
const normalized=JSON.parse(fs.readFileSync(process.env.LLC_HINTS_PATH||path.join(__dirname,'reference-hints-v1/normalized_routes.json'),'utf8'));
for(const [number,cap] of Object.entries(tuned)){
  const n=Number(number);
  if(api.LEVELS[n-1].cap===cap)
    proofs[n-1001]={level:n,route:normalized[n-201].map(step=>({p:[step[0],step[1]],mask:step[2]}))};
}
const failures=[];
const counts={};
const freezeTimings={};
for(const proof of proofs){
  const {level:n,route}=proof;
  api.choose(n);api.begin();
  const level=api.getLevel(),power=level.reviewPower;
  counts[power]=(counts[power]||0)+1;
  if(level.repairRequired&&level.repair?.cost===0&&!api.buyFreeRepair())throw Error(`Level ${n}: free repair unavailable`);
  let used=false,problem=null;
  const activate=()=>{
    const before=api.getState();
    if(!api.usePower(power))return 'power unavailable';
    const after=api.getState();
    const effect={lumen_flask:after.light>before.light,road_repair:after.roadRepaired,
      map_stabilizer:after.eventStabilized,freeze_seal:after.freezeTurns===3,
      rewind:after.turns===before.turns-1}[power];
    if(!effect)return 'power had no effect';
    used=true;
    return null;
  };
  if(power==='map_stabilizer')problem=activate();
  for(let i=1;i<route.length&&!problem;i++){
    if(!api.move(route[i].p)){problem=`route blocked at ${i}: ${api.getState().reason||'move rejected'}`;break}
    const firstDelivery=api.getState().mask>0;
    if(!used&&(power==='lumen_flask'&&i===1||power==='rewind'&&i===1||power==='road_repair'&&firstDelivery||power==='freeze_seal'&&firstDelivery)){
      problem=activate();
      if(!problem&&power==='rewind'&&!api.move(route[i].p))problem=`rewound move could not repeat at ${i}`;
    }
  }
  const end=api.getState();
  if(!problem&&(!used||!end.done||end.failed))problem=used?'route did not finish':'power not used';
  if(problem&&power==='freeze_seal'){
    for(let at=1;at<=route.length-4&&problem;at++){
      if(!route[at].mask)continue;
      api.choose(n);api.begin();
      if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
      let retryProblem=null;
      for(let i=1;i<route.length;i++){
        if(!api.move(route[i].p)){retryProblem=`move ${i} blocked`;break}
        if(i===at){
          if(!api.usePower(power)||api.getState().freezeTurns!==3){retryProblem=`freeze failed at ${i}`;break}
        }
      }
      const retryEnd=api.getState();
      if(!retryProblem&&retryEnd.done&&!retryEnd.failed&&retryEnd.freezeTurns===0){
        problem=null;
        freezeTimings[n]=at;
      }
    }
  }
  if(problem)failures.push({level:n,power,problem});
}
const report={levels:proofs.length,counts,passed:proofs.length-failures.length,failed:failures.length,freezeTimings,failures,
  scope:'Each assigned power is used on one completed recorded route; Freeze Seal timing may be later than the first delivery. No claim of optimality or all possible power timings.'};
const reportDir=process.env.LLC_POWER_AUDIT_OUTPUT_DIR?path.resolve(process.env.LLC_POWER_AUDIT_OUTPUT_DIR):__dirname;
fs.mkdirSync(reportDir,{recursive:true});
fs.writeFileSync(path.join(reportDir,'late-assigned-power-route-audit.json'),JSON.stringify(report,null,2));
console.log(`Assigned late powers: ${report.passed}/${report.levels} recorded routes completed; ${report.failed} failures`);
if(failures.length){console.log(JSON.stringify(failures.slice(0,12),null,2));process.exitCode=1}
