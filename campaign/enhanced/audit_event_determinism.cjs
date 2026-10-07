// Replay each authored event route twice after reset and compare event checkpoints.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const dir=__dirname;
const quake=JSON.parse(fs.readFileSync(path.join(dir,'quakes-v1/post_event_routes.json'),'utf8'));
const later=JSON.parse(fs.readFileSync(path.join(dir,'road-events-v1/post_event_routes.json'),'utf8'));
const currentDefaults=JSON.parse(fs.readFileSync(process.env.LLC_HINTS_PATH||path.join(dir,'reference-hints-v1/normalized_routes.json'),'utf8'));
const currentSignals=JSON.parse(fs.readFileSync(process.env.LLC_SIGNAL_HINTS_PATH||path.join(dir,'reference-hints-v1/normalized_signal_routes.json'),'utf8'));
for(const item of quake)item.route=currentDefaults[item.level-201].map(step=>({p:step.slice(0,2)}));
for(const item of later)item.route=currentDefaults[item.level-201].map(step=>({p:step.slice(0,2)}));
const signal=JSON.parse(fs.readFileSync(path.join(dir,'candidates-v3/ROUTES_1001_2000_BASELINE.json'),'utf8'))
  .filter(item=>api.LEVELS[item.level-1].phaseChoice)
  .map(item=>({level:item.level,route:currentSignals[item.level].map(step=>({p:step.slice(0,2)}))}));
const spurRoutes=JSON.parse(fs.readFileSync(path.join(dir,'bridge-spurs-v1/routes.json'),'utf8'));
const bridges=Object.entries(spurRoutes).map(([number])=>({level:Number(number),
  route:currentDefaults[Number(number)-201].map(step=>({p:step.slice(0,2)})),bridge:true}));
const cases=[...quake,...later,...signal.map(item=>({...item,signal:true})),...bridges];
const checked={quakeEvent:0,authoredEvent:0,aftershock:0,floodRoad:0,nightfall:0,dayNightCycle:0,shadowSpawner:0,chainEvent:0,signal:0};
const checkedRoadState={quakeClosed:0,quakeOpened:0,authoredClosed:0,chainClosed:0,chainOpened:0,floodClosed:0,aftershockClosed:0};
function count(mask){let c=0;while(mask){c+=mask&1;mask>>>=1}return c}
function verifyCheckpoint(level,item,delivery,state,countThisRun){
  const present=value=>value!==null&&value!==undefined;
  const expected=delivery===1?[
    ['quakeEvent',!!level.quakeEvent,!!state.quakeTriggered],
    ['authoredEvent',!!level.authoredEvent,!!state.eventTriggered],
    ['aftershock',!!level.aftershock,present(state.aftershockStart)],
    ['floodRoad',!!level.floodRoad,present(state.floodStart)],
    ['nightfall',!!level.nightfall,!!state.eventTriggered],
    ['dayNightCycle',!!level.dayNightCycle,present(state.nightStart)],
    ['shadowSpawner',!!level.shadowSpawner,present(state.spawnerTurn)],
    ['signal',!!item.signal,!!state.phaseSignal],
  ]:[['chainEvent',!!level.chainEvent,!!state.chainTriggered]];
  for(const [name,applies,active] of expected)if(applies){
    if(!active)throw Error(`Level ${item.level}: ${name} missing after delivery ${delivery}`);
    if(countThisRun)checked[name]++;
  }
  const expectRoad=(tile,open,name)=>{
    if(api.isOpen(tile)!==open)throw Error(`Level ${item.level}: ${name} road state wrong after delivery ${delivery}`);
    if(countThisRun)checkedRoadState[name]++;
  };
  if(delivery===1){
    if(level.quakeEvent){expectRoad(level.quakeEvent.close,false,'quakeClosed');for(const tile of level.quakeEvent.open)expectRoad(tile,true,'quakeOpened');}
    if(level.authoredEvent){const tile=item.signal&&level.phaseChoice?level.phaseChoice.alternateClose:level.authoredEvent.tile;expectRoad(tile,false,'authoredClosed');
      if(level.phaseChoice)expectRoad(item.signal?level.authoredEvent.tile:level.phaseChoice.alternateClose,true,'phaseOtherOpen');}
  }
  if(delivery===2&&level.chainEvent){expectRoad(level.chainEvent.close,false,'chainClosed');for(const tile of level.chainEvent.open)expectRoad(tile,true,'chainOpened');}
}
function run(item,countThisRun=false){
  api.choose(item.level);api.begin();
  const level=api.getLevel();
  // A free repair can persist in the review save after the first run.
  if(level.repairRequired)api.buyFreeRepair();
  if(item.signal&&!api.signal())throw Error(`Level ${item.level}: signal unavailable`);
  const checkpoints=[];let deliveries=0,floodChecked=false,aftershockChecked=false;
  for(let i=1;i<item.route.length;i++){
    const p=item.route[i].p;
    if(item.bridge&&api.getState().active&&!api.getState().bridgeBuilt&&!api.useBridge())
      throw Error(`Level ${item.level}: bridge power unavailable`);
    if(!api.move(p))throw Error(`Level ${item.level}${item.signal?' signal':''}: move ${i} rejected`);
    const state=api.getState(),newCount=count(state.mask);
    if(level.floodRoad&&!floodChecked&&state.floodStart!==null&&state.turns-state.floodStart>=level.floodRoad.closeAfter){
      if(api.isOpen(level.floodRoad.tile))throw Error(`Level ${item.level}: flood road still open after deadline`);
      floodChecked=true;if(countThisRun)checkedRoadState.floodClosed++;
    }
    if(level.aftershock&&!aftershockChecked&&state.aftershockStart!==null&&state.turns-state.aftershockStart>=level.aftershock.closeAfter){
      if(api.isOpen(level.aftershock.tile))throw Error(`Level ${item.level}: aftershock road still open after deadline`);
      aftershockChecked=true;if(countThisRun)checkedRoadState.aftershockClosed++;
    }
    if(newCount>deliveries){
      deliveries=newCount;
      if(deliveries<=2){verifyCheckpoint(level,item,deliveries,state,countThisRun);checkpoints.push({delivery:deliveries,step:i,state});}
    }
  }
  const done=api.getState();
  if(!done.done||done.failed||checkpoints.length<2)throw Error(`Level ${item.level}: route incomplete or no second delivery`);
  if(level.floodRoad&&!floodChecked)throw Error(`Level ${item.level}: flood deadline never tested`);
  if(level.aftershock&&!aftershockChecked)throw Error(`Level ${item.level}: aftershock deadline never tested`);
  return {checkpoints,finish:{turns:done.turns,light:done.light,mask:done.mask,done:done.done}};
}
const mismatches=[];
for(const item of cases){
  const first=run(item,true),second=run(item);
  if(JSON.stringify(first)!==JSON.stringify(second))mismatches.push({level:item.level,signal:!!item.signal,first,second});
}
const report={cases:cases.length,defaultCases:quake.length+later.length,signalCases:signal.length,bridgeCases:bridges.length,mismatches:mismatches.length,
  checkedFeatureActivations:checked,
  checkedRoadState,
  scope:'Recorded actions trigger expected first/second-delivery mechanics, then reproduce checkpoint state and completion from reset. This does not test all reachable states or global route viability.',
  mismatchSamples:mismatches.slice(0,3)};
const outputDir=process.env.LLC_EVENT_AUDIT_OUTPUT_DIR?path.resolve(process.env.LLC_EVENT_AUDIT_OUTPUT_DIR):dir;
fs.mkdirSync(outputDir,{recursive:true});
fs.writeFileSync(path.join(outputDir,'event-determinism-report.json'),JSON.stringify(report,null,2));
if(mismatches.length)throw Error(`${mismatches.length} deterministic checkpoint mismatches`);
console.log(`PASS: ${cases.length} event routes repeated; first/second delivery and finish state identical`);
