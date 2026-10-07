// Exact no-tool, no-repair minima for the revised trap and decoy introduction.
const fs=require('fs');
const path=require('path');
const solve=require('../route-solver.js').solve;
const root=path.resolve(__dirname,'../..');
const maps=JSON.parse(fs.readFileSync(path.join(root,'CAMPAIGN_1000_LEVELS.json'),'utf8'));
const out=path.join(__dirname,'early-winding-v1','shortest_routes.json');
fs.mkdirSync(path.dirname(out),{recursive:true});
let records=fs.existsSync(out)?JSON.parse(fs.readFileSync(out,'utf8')):[];
for(let n=101+records.length;n<=200;n++){
  const level=maps[n-1];
  if(level.n!==n)throw Error(`Level order mismatch ${n}`);
  const start=Date.now();
  const freeRepairRequired=!!level.repairRequired;
  if(freeRepairRequired&&(!level.repair||level.repair.cost!==0))
    throw Error(`Level ${n}: mandatory repair is not free`);
  const result=solve(level,null,{repaired:freeRepairRequired});
  if(result.status!=='solved')throw Error(`Level ${n}: ${result.status}`);
  records.push({level:n,freeRepairRequired,steps:result.steps,finishLight:result.route.at(-1).light,
    explored:result.explored,route:result.route});
  fs.writeFileSync(out,JSON.stringify(records));
  if(n%10===0||n===101)console.log(`Solved ${n}; steps=${result.steps}; explored=${result.explored}; elapsed=${((Date.now()-start)/1000).toFixed(1)}s`);
}
console.log(`Exact no-tool shortest routes saved for ${records.length} levels`);
