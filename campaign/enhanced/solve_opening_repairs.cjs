// Exact repaired shortest routes for the revised opening maps.
const fs=require('fs');
const path=require('path');
const solver=require('../route-solver.js');
const opening=JSON.parse(fs.readFileSync(path.join(__dirname,'opening-v1/authored_levels.json'),'utf8'));
const plain=JSON.parse(fs.readFileSync(path.join(__dirname,'opening-v1/shortest_routes.json'),'utf8'));
const results=[];
for(const level of opening){
  if(!level.repair)continue;
  const solved=solver.solve(level,null,{repaired:true});
  if(solved.status!=='solved'||!solved.route||solved.steps>plain[level.n-1].steps)throw Error(`Level ${level.n} repaired minimum invalid`);
  results.push({level:level.n,steps:solved.steps,finishLight:solved.route.at(-1).light,explored:solved.explored,route:solved.route});
}
const output=path.join(__dirname,'opening-v1/repaired_shortest_routes.json');
fs.writeFileSync(output,JSON.stringify(results));
console.log(`PASS: exact repaired shortest routes for ${results.length} opening levels; ${results.filter((r)=>r.steps<plain[r.level-1].steps).length} save steps`);
