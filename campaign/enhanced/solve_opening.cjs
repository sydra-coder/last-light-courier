// Recalculate exact shortest no-repair routes after the first-50 rule overlay.
const fs=require('fs');
const path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const solve=require('../route-solver.js').solve;
const folder=path.join(__dirname,'opening-v1');
const levels=JSON.parse(fs.readFileSync(path.join(folder,'authored_levels.json'),'utf8'));
const results=[];
for(const level of levels){
  const result=solve(level,null,{repaired:false});
  if(result.status!=='solved')throw new Error(`Level ${level.n}: ${result.status}`);
  if(level.noShadow&&result.route.some(s=>s.active))throw new Error(`Level ${level.n}: active shadow in no-shadow band`);
  if(result.route.at(-1).light<0)throw new Error(`Level ${level.n}: negative final light`);
  results.push({level:level.n,steps:result.steps,finishLight:result.route.at(-1).light,
    explored:result.explored,route:result.route});
}
fs.writeFileSync(path.join(folder,'shortest_routes.json'),JSON.stringify(results));
console.log(`Solved ${results.length} opening maps; 1–7: ${results.slice(0,7).map(r=>r.steps).join(', ')}; 41–50 finish light: ${results.slice(40).map(r=>r.finishLight).join(', ')}`);
