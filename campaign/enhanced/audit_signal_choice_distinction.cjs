// Describe how much the currently recorded default and depot-signal paths differ.
// This is a route comparison, not proof of optimality or player-facing value.
const fs=require('fs'),path=require('path');
const root=__dirname;
const defaults=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_routes.json')));
const signals=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_signal_routes.json')));
const balance=JSON.parse(fs.readFileSync(path.join(root,'lantern-balance-audit.json')));
const pairByLevel=new Map(balance.phasePairs.map(x=>[x.level,x]));
const key=p=>`${p[0]},${p[1]}`;
const rows=[];
for(const [label,signal] of Object.entries(signals)){
  const level=Number(label),base=defaults[level-201],pair=pairByLevel.get(level);
  if(!pair||!base)throw Error(`Missing current pair for ${level}`);
  const baseTiles=new Set(base.map(key)),signalTiles=new Set(signal.map(key));
  const baseOnly=[...baseTiles].filter(x=>!signalTiles.has(x)).length;
  const signalOnly=[...signalTiles].filter(x=>!baseTiles.has(x)).length;
  let sharedPrefix=0;
  while(sharedPrefix<Math.min(base.length,signal.length)&&key(base[sharedPrefix])===key(signal[sharedPrefix]))sharedPrefix++;
  rows.push({level,defaultSteps:pair.defaultSteps,signalSteps:pair.signalSteps,
    stepGap:pair.stepGap,lightGap:pair.lightGap,sharedPrefixMoves:Math.max(0,sharedPrefix-1),
    distinctDefaultTiles:baseOnly,distinctSignalTiles:signalOnly,
    sameTileSet:baseOnly===0&&signalOnly===0});
}
const report={scope:'Current recorded route geometry and outcome comparison for all 125 signal choices; not an optimal-route or subjective-choice certification.',
  pairs:rows.length,equalStepCount:rows.filter(x=>x.stepGap===0).length,
  equalStepAndLight:rows.filter(x=>x.stepGap===0&&x.lightGap===0).length,
  sameTileSet:rows.filter(x=>x.sameTileSet).length,
  shallowDivergence:rows.filter(x=>x.distinctDefaultTiles<=2&&x.distinctSignalTiles<=2).length,
  rows};
fs.writeFileSync(path.join(root,'signal-choice-distinction-audit.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({pairs:report.pairs,equalStepCount:report.equalStepCount,
  equalStepAndLight:report.equalStepAndLight,sameTileSet:report.sameTileSet,
  shallowDivergence:report.shallowDivergence,
  leastDistinct:rows.slice().sort((a,b)=>a.distinctDefaultTiles+a.distinctSignalTiles-b.distinctDefaultTiles-b.distinctSignalTiles).slice(0,12)}));
