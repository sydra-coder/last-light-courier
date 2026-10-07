// Canonical state key for hints tied to a replayed reference route.
const HINT_STATE_KEYS=[
  'pos','light','mask','turns','phase','phase2','active','fade','ice','gate','trail',
  'eventTriggered','eventStabilized','roadRepaired','quakeTriggered','quakeStabilized','quakeRepaired',
  'chainTriggered','phaseSignal','floodStart','aftershockStart','aftershockStabilized','aftershockRepaired',
  'nightStart','spawnerTurn','networkReady','networkCharged','networkChargeTurn','transferStored',
  'transferCollected','transferCollectedTurn','freezeTurns','powerUsed','usedPowers','trapArmed',
  'trapTile','trapPatrol','trappedPatrol','decoyArmed','decoyTile','decoyPatrol','decoyTargetPhase',
  'decoyTurns','rechargeLit','rechargeDrained','leechTriggered','beaconRevealed','collapseUsed',
  'collapseRepaired','bridgeBuilt','hunterPos','hunterAge'
];
function hintStateHash(state){
  const serialized=JSON.stringify(HINT_STATE_KEYS.map(key=>state[key]));
  let first=2166136261,second=2246822519;
  for(let i=0;i<serialized.length;i++){
    const value=serialized.charCodeAt(i);
    first=Math.imul(first^value,16777619);
    second=Math.imul(second^value,1597334677);
  }
  return (first>>>0).toString(36)+'.'+(second>>>0).toString(36);
}
if(typeof module!=='undefined')module.exports={hintStateHash,HINT_STATE_KEYS};
