// Verify mandatory progress never requires a paid repair or earned tool stock.
const test=require('./test_integrated_preview.cjs');
const levels=test.LEVELS;
if(levels.length!==2000)throw Error(`Expected 2000 levels, got ${levels.length}`);
let requiredRepairs=0,requiredBridges=0,reviewSamples=0;
for(const level of levels){
  if(level.repairRequired){
    requiredRepairs++;
    if(!level.repair||level.repair.cost!==0)throw Error(`Level ${level.n}: required repair is paid`);
  }
  if(level.lightBridgeRequiresPower){
    requiredBridges++;
    test.choose(level.n);
    if(level.reviewPower!=='light_bridge'||test.powerChargeSource('light_bridge')!=='level')
      throw Error(`Level ${level.n}: level-provided bridge charge unavailable at reset`);
  }
  if(level.reviewPower)reviewSamples++;
}
console.log(`PASS: ${levels.length} levels; ${requiredRepairs} required repairs are free, ${requiredBridges} bridge routes have level charges, ${reviewSamples} assigned review samples`);
