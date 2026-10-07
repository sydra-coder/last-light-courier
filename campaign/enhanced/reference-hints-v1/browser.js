// Hints follow a route replayed through the generated game's actual rules.
function requestVerifiedHint(){
  if(hintBusy||state.help||state.done||state.failed)return;
  $('hintDialog').hidden=false;
  $('hintApprove').hidden=true;
  $('hintReject').textContent='Close';
  $('hintReject').focus();
  if(hintPath&&hintPath.route.length>1){
    $('hintTitle').textContent='Your hint is already shown';
    $('hintMessage').textContent='Follow the gold arrows. No further hint was spent.';
    return;
  }
  if(save.hints<=0){
    $('hintTitle').textContent='No hints left';
    $('hintMessage').textContent=save.pendingHintRewards?'Collect your waiting reward to get another hint.':'Earn one hint for every ten new levels completed.';
    return;
  }
  if(popcount(state.mask)===level.homes.length){
    $('hintTitle').textContent='All houses are lit';
    $('hintMessage').textContent='Return to the blue depot. No hint was used.';
    return;
  }
  const checkpoints=state.phaseSignal?VERIFIED_SIGNAL_HINT_ROUTES[level.n]:VERIFIED_HINT_ROUTES[level.n-201];
  if(!checkpoints){
    $('hintTitle').textContent='Hint under review';
    $('hintMessage').textContent='No replayed hint is available for this map yet. No hint was spent.';
    return;
  }
  if(level.lightBridgeRequiresPower&&state.active&&!state.bridgeBuilt){
    $('hintTitle').textContent='Build the bridge first';
    $('hintMessage').textContent='Use the level-provided Light Bridge charge, then request the next route hint. No hint was spent.';
    return;
  }
  if(!!repaired()!==!!level.repairRequired){
    $('hintTitle').textContent=level.repairRequired?'Use the free repair first':'Route changed by repair';
    $('hintMessage').textContent=level.repairRequired?'Activate the marked free repair, then request the hint again. No hint was spent.':'This repaired route has no verified hint from the current state. No hint was spent.';
    return;
  }
  const here=checkpoints[state.turns];
  const key=hintStateHash(state);
  if(!here||(here[3]!==key&&here[4]!==key)){
    $('hintTitle').textContent='No verified hint from here';
    $('hintMessage').textContent='This run has diverged from the replayed route. Continue your own route or restart to use its hints. No hint was spent.';
    return;
  }
  let end=state.turns+1;
  while(end<checkpoints.length&&checkpoints[end][2]===state.mask)end++;
  const towardDepot=end>=checkpoints.length;
  if(towardDepot)end=checkpoints.length-1;
  if(end<=state.turns){
    $('hintTitle').textContent='No route ahead';
    $('hintMessage').textContent='No further recorded moves are available. No hint was spent.';
    return;
  }
  const segment=checkpoints.slice(state.turns,end+1).map(step=>({p:[step[0],step[1]]}));
  pendingHint={status:'solved',steps:segment.length-1,route:segment};
  $('hintTitle').textContent='Use a hint?';
  $('hintMessage').textContent='Show a verified '+(towardDepot?'route to the depot':'route to the next house')+' in '+pendingHint.steps+' moves? This route is safe from the current recorded state; it is not claimed shortest. Approving uses 1 hint. You have '+save.hints+' of 5.';
  $('hintReject').textContent='Reject';
  $('hintApprove').hidden=false;
}
