// Replay authored routes through the generated preview's movement functions.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const root=path.resolve(__dirname,'../..');
const previewPath=process.env.LLC_PREVIEW_PATH?path.resolve(process.env.LLC_PREVIEW_PATH):path.join(root,'design/campaign-2000-preview/index.html');
const html=fs.readFileSync(previewPath,'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
if(!script)throw Error('Preview script missing');
const prefix=script.slice(0,script.indexOf("$('board').addEventListener('click'"));
if(!prefix||prefix.length<1000000)throw Error('Preview test slice missing');
const economy=fs.readFileSync(path.join(__dirname,'power-economy.js'),'utf8');
const loadout=fs.readFileSync(path.join(__dirname,'power-loadout.js'),'utf8');
const phaseHandler=script.split(/\r?\n/).find(line=>line.startsWith("$('phaseChoiceControl').addEventListener('click'"));
if(!phaseHandler)throw Error('Generated phase-choice handler missing');
const placementCode=['placeTrap','placeDecoy'].map(name=>script.split(/\r?\n/).find(line=>line.startsWith(`function ${name}(p){`)));
if(placementCode.some(line=>!line))throw Error('Generated trap or decoy placement missing');
const element=()=>({hidden:true,innerHTML:'',textContent:'',handlers:{},getContext:()=>({}),focus(){},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(type,handler){this.handlers[type]=handler},getBoundingClientRect(){return {left:0,top:0,width:0,height:0}},parentElement:{classList:{add(){},remove(){}}}});
const elements=new Map();
const ctx={
  document:{getElementById:id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id)},querySelectorAll:()=>[],querySelector:()=>element(),createElement:()=>element(),body:element(),addEventListener(){}},
  window:{},navigator:{vibrate(){}},localStorage:{getItem:()=>null,setItem(){}},
  location:{search:''},URLSearchParams,Map,Set,Math,Date,JSON,Number,String,Array,Object,
  setTimeout:()=>0,clearTimeout:()=>{},structuredClone,
  console
};
vm.runInNewContext(prefix+'\n'+economy+'\n'+loadout+'\n'+placementCode.join('\n')+'\n'+phaseHandler+"\nfunction showScreen(){};render=()=>{};renderLevels=()=>{};renderRepair=()=>{};renderLegend=()=>{};setStatus=()=>{};spendAnimation=()=>{};ISO.cancel=()=>{};ISO.move=()=>{};ISO.render=()=>{};ISO.repair=()=>{};FEEDBACK.emit=()=>{};this.__test={LEVELS,choose,move,legal,shadowBlocked,isOpen:open,getState:()=>structuredClone(state),getLevel:()=>level,minimum:()=>shortestSafeRoute((1<<level.homes.length)-1),hint:()=>{requestHint();return {title:$('hintTitle').textContent,message:$('hintMessage').textContent,approveHidden:$('hintApprove').hidden,hints:save.hints,pending:pendingHint?structuredClone(pendingHint):null}},rejectHint:()=>{closeHint();return save.hints},begin:()=>{state.help=false},grantPower:(power,count)=>{save.powerUnlocked[power]=true;save.powerStock[power]=(save.powerStock[power]||0)+count},signal:()=>{$('phaseChoiceControl').handlers.click({target:{id:'sendPhaseSignal'}});return state.phaseSignal},buyFreeRepair:()=>level.repair?.cost===0?attemptRepair(null):false,buyPaidRepair:()=>{if(!level.repair||level.repair.cost<=0)return false;save.wallet=level.repair.cost;return attemptRepair(null)&&save.wallet===0},useBridge:()=>{state.selectedPower='light_bridge';if(!powerReady('light_bridge'))return false;useCandidatePower();return state.bridgeBuilt},powerReady,powerChargeSource, usePower:power=>{state.selectedPower=power;if(!powerReady(power))return false;useCandidatePower();return true},canTrapAt,placeTrap,canDecoyAt,placeDecoy};})();",ctx,{timeout:30000});
if(require.main!==module)module.exports=ctx.__test;
if(require.main===module){
const archive=process.argv.includes('--archive');
const signalMode=process.argv.includes('--signal');
const transitMode=process.argv.includes('--transit');
const repairMode=process.argv.includes('--paid-repair');
const openingRepairMode=process.argv.includes('--opening-repair');
let routes=archive?JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels.map(item=>({level:item.level,route:item.solutions[0].route})):JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'),'utf8'));
if(!archive&&!signalMode&&!transitMode&&!repairMode&&!openingRepairMode){
  const tuned=JSON.parse(fs.readFileSync(process.env.LLC_BALANCE_CAPS_PATH||path.join(__dirname,'lantern-balance-v1/promoted_caps.json'),'utf8'));
  const normalized=JSON.parse(fs.readFileSync(process.env.LLC_HINTS_PATH||path.join(__dirname,'reference-hints-v1/normalized_routes.json'),'utf8'));
  for(const [number,cap] of Object.entries(tuned)){
    const n=Number(number);
    if(ctx.__test.LEVELS[n-1].cap===cap)
      routes[n-1001]={level:n,route:normalized[n-201].map(step=>({p:[step[0],step[1]],mask:step[2]}))};
  }
}
if(openingRepairMode)routes=JSON.parse(fs.readFileSync(path.join(__dirname,'opening-v1/repaired_shortest_routes.json'),'utf8'));
if(repairMode){
  const records=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
  routes=records.slice(50,200).flatMap(item=>item.solutions.filter(solution=>solution.repairPurchased).map(solution=>({level:item.level,route:solution.route})));
}
if(signalMode){
  const baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'candidates-v3/ROUTES_1001_2000_BASELINE.json'),'utf8'));
  routes=baseline.filter(item=>ctx.__test.LEVELS[item.level-1].phaseChoice).map(item=>({level:item.level,route:item.solutions[0].route}));
  const tuned=JSON.parse(fs.readFileSync(process.env.LLC_BALANCE_CAPS_PATH||path.join(__dirname,'lantern-balance-v1/promoted_caps.json'),'utf8'));
  const normalized=JSON.parse(fs.readFileSync(process.env.LLC_SIGNAL_HINTS_PATH||path.join(__dirname,'reference-hints-v1/normalized_signal_routes.json'),'utf8'));
  for(const item of routes){
    const n=item.level;
    if(tuned[n]===ctx.__test.LEVELS[n-1].cap&&normalized[n])
      item.route=normalized[n].map(step=>({p:[step[0],step[1]],mask:step[2]}));
  }
}
if(transitMode){
  const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'transit-v1/route_proofs.json'),'utf8'));
  const express=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'transit-v1/express_routes.json'),'utf8')).map(x=>[x.level,x]));
  const overridePath=process.env.LLC_TRANSIT_ROUTE_OVERRIDES||path.join(__dirname,'transit-v1/current_route_overrides.json');
  const transitOverrides=fs.existsSync(overridePath)?JSON.parse(fs.readFileSync(overridePath,'utf8')):{};
  routes=proofs.map(proof=>{
    if(transitOverrides[proof.level]){
      const revised=transitOverrides[proof.level];
      return {level:proof.level,route:revised.route.map(p=>({p})),
        expectedSteps:revised.transitSteps,expectedLight:revised.transitFinishLight};
    }
    if(express.has(proof.level)){
      const fast=express.get(proof.level);
      return {level:proof.level,route:fast.route.map(p=>({p})),expectedSteps:fast.transitSteps,expectedLight:fast.transitFinishLight};
    }
    const walking=routes[proof.level-1001].route;
    return {level:proof.level,route:[...walking.slice(0,proof.boardAtStep+1),...walking.slice(proof.exitAtOldStep)],expectedSteps:proof.transitSteps,expectedLight:proof.transitFinishLight};
  });
}
if(archive){
  const quakes=JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'),'utf8'));
  for(const proof of quakes)routes[proof.level-1]={level:proof.level,route:proof.route};
  const spurPath=process.env.LLC_BRIDGE_SPUR_ROUTES_PATH||path.join(__dirname,'bridge-spurs-v1/routes.json');
  if(fs.existsSync(spurPath)){
    const spurs=JSON.parse(fs.readFileSync(spurPath,'utf8'));
    for(const [number,points] of Object.entries(spurs))routes[Number(number)-1]={level:Number(number),route:points.map(p=>({p}))};
  }
}
const failures=[];
let passed=0;
let freeRepairs=0;
let bridgesBuilt=0;
for(const proof of routes){
  const replay=()=>{
    let problem=null;
    for(const [index,step] of proof.route.entries()){
      if(!index)continue;
      const current=ctx.__test.getLevel();
      const snapshot=ctx.__test.getState();
      if(current.lightBridge&&snapshot.active&&!snapshot.bridgeBuilt&&!ctx.__test.useBridge()){
        problem={level:proof.level,step:index,tile:step.p,reason:'required bridge unavailable',light:snapshot.light,failed:snapshot.failed};
        break;
      }
      if(!ctx.__test.move(step.p)){
        const state=ctx.__test.getState();
        problem={level:proof.level,step:index,tile:step.p,reason:state.reason||'move blocked',light:state.light};
        break;
      }
    }
    const finish=ctx.__test.getState();
    if(!problem&&(!finish.done||finish.failed))problem={level:proof.level,step:finish.turns,reason:finish.reason||'did not finish',light:finish.light};
    if(!problem&&proof.expectedSteps!==undefined&&(finish.turns!==proof.expectedSteps||finish.light!==proof.expectedLight))problem={level:proof.level,step:finish.turns,reason:`transit proof mismatch: expected ${proof.expectedSteps} steps and ${proof.expectedLight} light`,light:finish.light};
    return problem;
  };
  ctx.__test.choose(proof.level);
  ctx.__test.begin();
  let problem=(repairMode||openingRepairMode)&&!ctx.__test.buyPaidRepair()?{level:proof.level,reason:'paid repair rejected'}:signalMode&&!ctx.__test.signal()?{level:proof.level,reason:'signal action rejected'}:replay();
  if(problem&&ctx.__test.getLevel().repair?.cost===0){
    ctx.__test.choose(proof.level);
    ctx.__test.begin();
    if(ctx.__test.buyFreeRepair()){
      freeRepairs++;
      problem=signalMode&&!ctx.__test.signal()?{level:proof.level,reason:'signal action rejected after repair'}:replay();
    }
  }
  if(problem)failures.push(problem);
  else{
    passed++;
    if(ctx.__test.getLevel().lightBridge&&ctx.__test.getState().bridgeBuilt)bridgesBuilt++;
  }
}
const report={band:archive?'1-1000':signalMode?'signal branches':transitMode?'transit rides':repairMode?'paid repair routes':openingRepairMode?'opening repaired minima':'1001-2000',levels:routes.length,passed,freeRepairs,bridgesBuilt,failed:failures.length,failures};
const reportDir=process.env.LLC_REPLAY_REPORT_DIR?path.resolve(process.env.LLC_REPLAY_REPORT_DIR):__dirname;
fs.mkdirSync(reportDir,{recursive:true});
fs.writeFileSync(path.join(reportDir,archive?'integrated-preview-replay-1-1000.json':signalMode?'integrated-preview-signal-branches.json':transitMode?'integrated-preview-transit-rides.json':repairMode?'integrated-preview-paid-repairs.json':openingRepairMode?'integrated-preview-opening-repairs.json':'integrated-preview-replay.json'),JSON.stringify(report,null,2));
console.log(`Generated preview replay: ${passed}/${routes.length} recorded routes passed; ${freeRepairs} free repairs; ${bridgesBuilt} bridges built`);
if(failures.length){console.log(JSON.stringify(failures.slice(0,12),null,2));process.exitCode=1;}
}



