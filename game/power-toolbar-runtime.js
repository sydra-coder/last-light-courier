// Injected inside the campaign closure by build.cjs. It uses the live game state.
const POWER_UI={
  anchor_trap:{icon:'⚓',scope:'Current road tile',help:'Stand on a patrol route, then tap to leave a trap under your feet. It catches a patrol after you move away.'},
  decoy_light:{icon:'✧',scope:'Current road tile',help:'Place false light where you stand. The nearest patrol follows its route toward that spot for four moves.'},
  reveal_pulse:{icon:'◉',scope:'Whole map',help:'Reveal the hidden house and sealed road on this map.'},
  lumen_flask:{icon:'✦',scope:'Courier',help:'Restore up to three lantern light immediately.'},
  road_repair:{icon:'⚒',scope:'Marked road',help:'Reopen the marked closed road, aftershock tile, quake tile, or collapsed causeway.'},
  light_bridge:{icon:'▰',scope:'Marked crossing',help:'After a delivery, spend one lantern light to build the marked crossing.'},
  map_stabilizer:{icon:'⬡',scope:'Whole map',help:'Protect a marked road from a closure or aftershock.'},
  freeze_seal:{icon:'❄',scope:'Whole map',help:'Pause patrol shadows for three moves.'},
  rewind:{icon:'↶',scope:'Courier',help:'Undo the last move, including its light, delivery, shadow step, and map event.'}
};
const oldCanTrapAt=canTrapAt,oldCanDecoyAt=canDecoyAt,oldPowerReady=powerReady,oldUseCandidatePower=useCandidatePower;
canTrapAt=function(p){
  if(eq(p,state.pos))return state.trapArmed&&!powerUsedFor('anchor_trap')&&state.active&&!state.done&&!state.failed&&open(p)&&[level.patrol,level.patrol2,level.patrol3].some(route=>route?.some(tile=>eq(tile,p)));
  return oldCanTrapAt(p);
};
canDecoyAt=function(p){
  if(eq(p,state.pos))return state.decoyArmed&&!powerUsedFor('decoy_light')&&state.active&&!state.done&&!state.failed&&open(p);
  return oldCanDecoyAt(p);
};
powerReady=function(power){
  if(!oldPowerReady(power))return false;
  if(power==='anchor_trap')return state.active&&[level.patrol,level.patrol2,level.patrol3].some(route=>route?.some(tile=>eq(tile,state.pos)));
  return true;
};
function routeBudgetCheck(){
  if(state.done)return {kind:'complete',text:'Delivery complete.'};
  if(state.failed)return {kind:'impossible',text:'This run has ended.'};
  const unlit=level.homes.filter((_,i)=>!(state.mask&(1<<i))),needed=Math.max(0,level.required-popcount(state.mask));
  const distance=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1]);
  let optimistic=distance(state.pos,level.depot);
  if(needed>0&&unlit.length<=12){
    const full=1<<unlit.length,dp=Array.from({length:full},()=>Array(unlit.length).fill(Infinity));
    for(let i=0;i<unlit.length;i++)dp[1<<i][i]=distance(state.pos,unlit[i].p);
    optimistic=Infinity;
    for(let mask=1;mask<full;mask++){
      const count=popcount(mask);
      for(let last=0;last<unlit.length;last++){
        const cost=dp[mask][last];if(!Number.isFinite(cost))continue;
        if(count>=needed)optimistic=Math.min(optimistic,cost+distance(unlit[last].p,level.depot));
        if(count>=needed)continue;
        for(let next=0;next<unlit.length;next++)if(!(mask&(1<<next)))dp[mask|(1<<next)][next]=Math.min(dp[mask|(1<<next)][next],cost+distance(unlit[last].p,unlit[next].p));
      }
    }
  }
  const flask=canSpendPowerCharge('lumen_flask')&&!powerUsedFor('lumen_flask')?3:0;
  const maxLight=state.light+unlit.length*2+flask;
  const extraRefill=!!(level.rechargeHouse||level.lumenNetwork||level.lightTransfer||level.transitLink);
  if(!extraRefill&&optimistic>maxLight)return {kind:'impossible',text:`At least ${optimistic} moves remain, but at most ${maxLight} lantern light can be available. Restart or change the route.`};
  const simple=level.n<=100&&!level.authoredEvent&&!level.quakeEvent&&!level.stormWind&&!level.aftershock&&!level.floodRoad&&!level.transitLink&&!level.lightBridge&&!level.hiddenRoad&&!state.trapTile&&!state.decoyTile&&!state.freezeTurns&&!state.roadRepaired&&!state.eventStabilized;
  if(simple){
    const route=ROUTE_SOLVER.solve(level,structuredClone(state),{repaired:repaired()});
    if(route.status==='solved')return {kind:'verified',text:`A route to the depot is verified in ${route.steps} moves with the remaining light.`};
    if(route.status==='no_solution'){
      const rescue=availablePowers().some(id=>!powerUsedFor(id)&&canSpendPowerCharge(id));
      if(!rescue)return {kind:'impossible',text:'No safe completion route fits the current light and patrol timing.'};
      return {kind:'unverified',text:'No route is verified without using another inventory power.'};
    }
  }
  return {kind:'unverified',text:`Best-case travel needs at least ${optimistic} moves. Current hazards and powers still need a full route check.`};
}
function explainPower(power){
  const item=POWER_CATALOG.find(entry=>entry.id===power),info=POWER_UI[power];
  if(!item||!info)return;
  const stock=save.powerStock?.[power]||0,ready=powerReady(power);
  const waitReason={
    anchor_trap:!state.active?'Patrols wake after the first delivery.':'Stand on a patrol route to place this trap.',
    decoy_light:'Patrols wake after the first delivery.',
    reveal_pulse:'Use on a map with a hidden house before its Beacon reveals it.',
    lumen_flask:'Spend at least one lantern light first.',
    road_repair:'Wait for a marked road to close, then reopen it.',
    light_bridge:'Build the marked crossing after a delivery, with enough light.',
    map_stabilizer:'Use before the marked road event closes it.',
    freeze_seal:'Patrols wake after the first delivery.',
    rewind:'Make a move first.'
  };
  const reason=powerUsedFor(power)?'Already used this run.':!canSpendPowerCharge(power)?'No charge available.':!ready?waitReason[power]:'Tap once to use it now.';
  const panel=$('candidatePower').querySelector('.powerInfo');
  panel.dataset.power=power;
  panel.innerHTML='<button type="button" class="powerInfoClose" aria-label="Close power details">×</button><strong>'+item.name+' · '+info.scope+'</strong><span>'+info.help+'</span><small>'+stock+' charge'+(stock===1?'':'s')+' · '+reason+'</small>';
  panel.hidden=false;
}
function closePowerInfo(){const panel=$('candidatePower').querySelector('.powerInfo');if(panel)panel.hidden=true}
function togglePowerInfo(power){const panel=$('candidatePower').querySelector('.powerInfo');if(panel&&!panel.hidden&&panel.dataset.power===power){closePowerInfo();return true}explainPower(power);return false}
renderCandidatePower=function(){
  const box=$('candidatePower'),options=availablePowers();
  if(!options.length){box.hidden=true;return}
  box.hidden=false;
  const open=box.querySelector('.powerInfo:not([hidden])'),openPower=open?.dataset.power;
  box.innerHTML='<div class="powerTray" role="group" aria-label="Powers and utilities">'+options.map(id=>{
    const item=POWER_CATALOG.find(entry=>entry.id===id),info=POWER_UI[id],stock=save.powerStock?.[id]||0,ready=powerReady(id);
    return '<button type="button" class="powerIcon '+(ready?'ready':'unavailable')+'" data-power="'+id+'" aria-label="'+item.name+', '+stock+' charges, '+(ready?'ready':'tap for requirements')+'" title="'+item.name+'" aria-disabled="'+(!ready)+'"><span aria-hidden="true">'+info.icon+'</span><i aria-hidden="true">'+stock+'</i></button>';
  }).join('')+'</div><div class="powerInfo" hidden data-power="'+(openPower||'')+'"></div>';
  if(openPower&&options.includes(openPower))explainPower(openPower);
};
useCandidatePower=function(){
  const power=state.selectedPower||level.reviewPower;
  if(!powerReady(power)){explainPower(power);return}
  const before=JSON.stringify(state.usedPowers),light=state.light;
  if(power==='anchor_trap'){
    state.trapArmed=true;state.decoyArmed=false;placeTrap([...state.pos]);
  }else if(power==='decoy_light'){
    state.decoyArmed=true;state.trapArmed=false;placeDecoy([...state.pos]);
  }else oldUseCandidatePower();
  if(before===JSON.stringify(state.usedPowers)&&light===state.light)return;
  const turn=state.turns,mask=state.mask,pos=state.pos.join(','),currentTitle=$('statusTitle').textContent,currentText=$('statusText').textContent;
  setTimeout(()=>{
    if(state.turns!==turn||state.mask!==mask||state.pos.join(',')!==pos||state.done||state.failed)return;
    const result=routeBudgetCheck();
    setStatus('Power used · route check',currentTitle,currentText+' '+result.text);
  },0);
};
(()=>{
  const box=$('candidatePower');let timer=null,pressed=null,long=false,startX=0,startY=0;
  box.addEventListener('pointerdown',e=>{const button=e.target.closest('button.powerIcon[data-power]');if(!button)return;pressed=button.dataset.power;long=false;startX=e.clientX;startY=e.clientY;clearTimeout(timer);timer=setTimeout(()=>{long=true;togglePowerInfo(pressed)},520)});
  box.addEventListener('pointermove',e=>{if(pressed&&Math.hypot(e.clientX-startX,e.clientY-startY)>12){clearTimeout(timer);pressed=null}});
  box.addEventListener('pointerup',e=>{if(!pressed)return;clearTimeout(timer);const id=pressed;pressed=null;if(!long){if(togglePowerInfo(id))return;closePowerInfo();state.selectedPower=id;useCandidatePower()}});
  box.addEventListener('pointercancel',()=>{clearTimeout(timer);pressed=null});
  box.addEventListener('contextmenu',e=>{const button=e.target.closest('button.powerIcon[data-power]');if(button){e.preventDefault();explainPower(button.dataset.power)}});
  box.addEventListener('click',e=>{if(e.target.closest('.powerInfoClose')){closePowerInfo();return}const button=e.target.closest('button.powerIcon[data-power]');if(button&&e.detail===0){if(togglePowerInfo(button.dataset.power))return;closePowerInfo();state.selectedPower=button.dataset.power;useCandidatePower()}});
  document.addEventListener('pointerdown',e=>{if(!e.target.closest('#candidatePower'))closePowerInfo()});
})();
