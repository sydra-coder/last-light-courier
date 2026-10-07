// Replay one real campaign route after exercising each assigned tool.
const fs=require('fs');
const path=require('path');
const t=require('./test_integrated_preview.cjs');
const root=path.resolve(__dirname,'../..');
const early=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
const late=JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'),'utf8'));
const bridgeSpurs=JSON.parse(fs.readFileSync(path.join(__dirname,'bridge-spurs-v1/routes.json'),'utf8'));
const arsenal=JSON.parse(fs.readFileSync(path.join(__dirname,'arsenal-v1/power_proofs.json'),'utf8'));
const decoy=JSON.parse(fs.readFileSync(path.join(__dirname,'decoys-v1/power_proofs.json'),'utf8'))[0];
const route=n=>bridgeSpurs[n]?bridgeSpurs[n].map(p=>({p})):n<=1000?early[n-1].solutions[0].route:late[n-1001].route;
const trials=[
  {n:1001,power:'lumen_flask',after:1},
  {n:1002,power:'road_repair',after:'first_delivery'},
  {n:1003,power:'map_stabilizer',after:0},
  {n:701,power:'light_bridge',after:'first_delivery'},
  {n:201,power:'reveal_pulse',after:0},
  {n:decoy.level,power:'decoy_light',after:decoy.useAfterStep,tile:decoy.decoyTile},
  {n:arsenal[0].level,power:'freeze_seal',after:arsenal[0].useAfterStep},
  {n:arsenal[1].level,power:'rewind',after:arsenal[1].useAfterStep}
];
const results=[];
for(const trial of trials){
  t.choose(trial.n);t.begin();
  if(t.getLevel().repair?.cost===0&&t.getLevel().repairRequired&&!t.buyFreeRepair())throw Error(`Level ${trial.n} repair failed`);
  let used=false;
  const activate=step=>{
    const before=t.getState();
    if(!t.usePower(trial.power))throw Error(`Level ${trial.n} ${trial.power} unavailable at ${step}`);
    if(trial.power==='decoy_light'){
      if(!t.canDecoyAt(trial.tile))throw Error(`Level ${trial.n} decoy target unavailable`);
      t.placeDecoy(trial.tile);
    }
    const after=t.getState();
    const expected={lumen_flask:after.light>before.light,road_repair:after.roadRepaired,map_stabilizer:after.eventStabilized,light_bridge:after.bridgeBuilt&&after.light===before.light-1,reveal_pulse:after.beaconRevealed,decoy_light:after.decoyTurns===4,freeze_seal:after.freezeTurns===3,rewind:after.turns===before.turns-1};
    if(!expected[trial.power])throw Error(`Level ${trial.n} ${trial.power} had no expected effect`);
    used=true;
    if(trial.power==='rewind'){
      const previous=route(trial.n)[step];
      if(!t.move(previous.p))throw Error(`Level ${trial.n} could not repeat rewound move`);
    }
  };
  if(trial.after===0)activate(0);
  const steps=route(trial.n);
  for(let i=1;i<steps.length;i++){
    if(!t.move(steps[i].p))throw Error(`Level ${trial.n} route blocked at ${i}: ${JSON.stringify(t.getState().reason)}`);
    if(!used&&(trial.after===i||trial.after==='first_delivery'&&t.getState().mask))activate(i);
  }
  const end=t.getState();
  if(!used||!end.done||end.failed)throw Error(`Level ${trial.n} ${trial.power} did not finish`);
  results.push({level:trial.n,power:trial.power,steps:end.turns});
}
let anchorSample=null;
const anchorCounts={eligible:0,placed:0,captured:0,completed:0};
for(let n=101;n<=150&&!anchorSample;n++){
  const steps=route(n),level=t.LEVELS[n-1];
  for(let i=1;i<steps.length-1&&!anchorSample;i++){
    if(!steps[i].mask)continue;
    const remaining=new Set(steps.slice(i+1).map(step=>step.p.join(',')));
    const targets=[...level.patrol,...(level.patrol2||[])].filter(tile=>!remaining.has(tile.join(',')));
    for(const tile of targets){
      t.choose(n);t.begin();
      let prefixOk=true;
      for(let j=1;j<=i;j++)if(!t.move(steps[j].p)){prefixOk=false;break}
      if(!prefixOk||!t.usePower('anchor_trap')||!t.canTrapAt(tile))continue;
      anchorCounts.eligible++;
      t.placeTrap(tile);
      if(!t.getState().trapTile)continue;
      anchorCounts.placed++;
      let trapped=false,held=false,finished=true;
      for(let j=i+1;j<steps.length;j++){
        const before=t.getState();
        if(!t.move(steps[j].p)){finished=false;break}
        const after=t.getState();
        if(after.trappedPatrol)trapped=true;
        if(before.trappedPatrol){
          const field=before.trappedPatrol===1?'phase':'phase2';
          if(after[field]!==before[field])throw Error(`Level ${n} trapped shadow moved`);
          held=true;
        }
      }
      const end=t.getState();
      if(trapped)anchorCounts.captured++;
      if(finished&&end.done&&!end.failed)anchorCounts.completed++;
      if(finished&&trapped&&held&&end.done&&!end.failed)anchorSample={level:n,power:'anchor_trap',tile,placedAfterStep:i,steps:end.turns};
      if(anchorSample)break;
    }
  }
}
if(!anchorSample)throw Error('No completed sample with a captured and immobilized shadow: '+JSON.stringify(anchorCounts));
results.push(anchorSample);
fs.writeFileSync(path.join(__dirname,'power-sample-results.json'),JSON.stringify({passed:results.length,samples:results},null,2));
console.log('PASS: '+results.map(r=>`${r.power} ${r.level}`).join(', '));
