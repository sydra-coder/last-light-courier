// Let the courier choose any earned tool; the assigned review tool remains selectable.
function powerUsedFor(power){return !!state.usedPowers?.[power]}
function availablePowers(){
  const ids=[];
  if(level.reviewPower)ids.push(level.reviewPower);
  for(const item of POWER_CATALOG)if(save.powerUnlocked?.[item.id]&&!ids.includes(item.id))ids.push(item.id);
  return ids;
}
function repairableRoad(){
  if(level.authoredEvent&&state.eventTriggered&&!state.eventStabilized&&!state.roadRepaired)return 'authored';
  if(level.aftershock&&!state.aftershockStabilized&&!state.aftershockRepaired&&state.aftershockStart!==null&&state.turns-state.aftershockStart>=level.aftershock.closeAfter)return 'aftershock';
  if(level.quakeEvent&&state.quakeTriggered&&!state.quakeStabilized&&!state.quakeRepaired)return 'quake';
  if(level.collapseTile&&state.collapseClosed&&!state.collapseRepaired)return 'causeway';
  return null;
}
function powerReady(power){
  if(!power||powerUsedFor(power)||!canSpendPowerCharge(power)||state.done||state.failed)return false;
  if(power==='lumen_flask')return state.light<cap();
  if(power==='road_repair')return !!repairableRoad();
  if(power==='map_stabilizer')return (!!level.authoredEvent&&!state.eventTriggered)||(!!level.aftershock&&!state.aftershockStabilized)||(!!level.quakeEvent&&!level.aftershock&&!state.quakeStabilized);
  if(power==='reveal_pulse')return !!level.hiddenRoad&&!state.beaconRevealed;
  if(power==='light_bridge')return !!level.lightBridge&&state.active&&!state.bridgeBuilt&&state.light>level.bridgeCost;
  if(power==='freeze_seal')return state.active&&state.freezeTurns===0;
  if(power==='rewind')return !!state.lastMoveState;
  if(power==='decoy_light')return state.active&&!state.decoyArmed;
  if(power==='anchor_trap')return !state.trapArmed;
  return false;
}
function renderCandidatePower(){
  const box=$('candidatePower'),options=availablePowers();
  if(!options.length){box.hidden=true;return}
  box.hidden=false;
  if(!options.includes(state.selectedPower))state.selectedPower=level.reviewPower||options[0];
  const power=state.selectedPower;
  const help={
    lumen_flask:'Restore up to three lantern light.',
    road_repair:'Restore the marked closed road, aftershock tile, quake tile, or collapsed causeway.',
    map_stabilizer:level.aftershock?'Keep or reopen the aftershock road.':level.quakeEvent?'Keep the marked quake road open; newly opened streets still appear.':'Protect the marked road before the first delivery.',
    anchor_trap:'Arm a trap, then choose a highlighted patrol tile within two steps.',
    decoy_light:'Place a false light within two tiles to redirect one patrol for four moves.',
    reveal_pulse:'Reveal the hidden house and sealed road before reaching the Beacon.',
    light_bridge:'After a delivery, spend one light to build the marked crossing.',
    freeze_seal:'Hold both patrol shadows for the next three moves.',
    rewind:'Undo the last move and its light, delivery, shadow, and map changes.'
  };
  const choices=options.map(id=>{
    const item=POWER_CATALOG.find(entry=>entry.id===id);
    return '<option value="'+id+'" '+(id===power?'selected':'')+'>'+item.name+' · '+chargeLabel(id)+'</option>';
  }).join('');
  box.innerHTML='<strong>Tools</strong><select id="selectedPower" aria-label="Choose a tool">'+choices+'</select><span>'+help[power]+'</span><button type="button" id="useCandidatePower" '+(powerReady(power)?'':'disabled')+'>'+(powerUsedFor(power)?'USED':state.trapArmed||state.decoyArmed?'Select a tile':'Use tool')+'</button>';
}
function useCandidatePower(){
  const power=state.selectedPower||level.reviewPower;
  if(!powerReady(power))return;
  if(power==='anchor_trap'){
    state.trapArmed=true;state.decoyArmed=false;
    setStatus('Choose a trap tile','Tap a highlighted patrol tile','The selected shadow stops when it enters your trap.');
    render();return;
  }
  if(power==='decoy_light'){
    state.decoyArmed=true;state.trapArmed=false;
    setStatus('Choose a decoy tile','Tap a highlighted road within two steps','The nearest patrol turns toward your false light.');
    render();return;
  }
  if(power==='rewind'){
    const before=state.lastMoveState,already={...state.usedPowers};
    if(!consumePowerCharge(power))return;
    state={...before,usedPowers:{...before.usedPowers,...already,rewind:true},selectedPower:power,powerUsed:true,lastMoveState:null};
    if(level.lightBridgeRequiresPower&&!state.bridgeBuilt)delete state.usedPowers.light_bridge;
    hintPath=null;ISO.cancel();
    setStatus('Move rewound','Previous position restored','Light, shadows, delivery, and map event returned to their prior state.');
    render();return;
  }
  if(power==='lumen_flask')state.light=Math.min(cap(),state.light+3);
  else if(power==='road_repair'){
    const target=repairableRoad();
    if(target==='authored')state.roadRepaired=true;
    else if(target==='aftershock')state.aftershockRepaired=true;
    else if(target==='quake')state.quakeRepaired=true;
    else if(target==='causeway')state.collapseRepaired=true;
  }
  else if(power==='map_stabilizer'){
    if(level.aftershock)state.aftershockStabilized=true;
    else if(level.quakeEvent)state.quakeStabilized=true;
    else state.eventStabilized=true;
  }
  else if(power==='reveal_pulse')state.beaconRevealed=true;
  else if(power==='light_bridge'){state.light-=level.bridgeCost;state.bridgeBuilt=true}
  else if(power==='freeze_seal')state.freezeTurns=3;
  else return;
  if(!consumePowerCharge(power))return;
  state.usedPowers[power]=true;state.powerUsed=true;
  setStatus('Tool used',POWER_CATALOG.find(item=>item.id===power).name,
    power==='light_bridge'?'Marked crossing built for one lantern light.':power==='road_repair'?'The marked damaged road is open again.':'One charge spent. Other available tools remain usable this run.');
  render();
}
function canTrapAt(p){
  if(!state.trapArmed||powerUsedFor('anchor_trap')||!open(p)||eq(p,state.pos)||Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])>2)return false;
  return [level.patrol,level.patrol2].some(patrol=>patrol?.some(tile=>eq(tile,p)))&&!(state.active&&(eq(p,level.patrol[state.phase])||eq(p,level.patrol2?.[state.phase2])));
}
function canDecoyAt(p){
  return state.decoyArmed&&!powerUsedFor('decoy_light')&&state.active&&!state.done&&!state.failed&&open(p)&&!eq(p,state.pos)&&Math.abs(p[0]-state.pos[0])+Math.abs(p[1]-state.pos[1])<=2;
}
$('candidatePower').addEventListener('change',event=>{
  if(event.target.id!=='selectedPower')return;
  const power=event.target.value;
  if(!availablePowers().includes(power))return;
  state.selectedPower=power;state.trapArmed=false;state.decoyArmed=false;
  render();
});
