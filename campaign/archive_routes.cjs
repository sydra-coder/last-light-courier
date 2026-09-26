const fs=require('fs'),crypto=require('crypto'),path=require('path');
const root=path.resolve(__dirname,'..'),out=path.resolve(process.argv[2]||path.join(root,'design'));
fs.mkdirSync(out,{recursive:true});
const solver=require(root+'/campaign/route-solver.js'),levels=JSON.parse(fs.readFileSync(root+'/CAMPAIGN_LEVELS.json','utf8'));
const entries=[];
for(const level of levels){
 const variants=[];
 for(const bought of level.repair?[false,true]:[false]){
  const result=solver.solve(level,null,{repaired:bought});if(result.status!=='solved')throw Error('Unsolved '+level.n+' repaired='+bought);
  variants.push({repairPurchased:bought,...result});
 }
 entries.push({level:level.n,mapFingerprint:crypto.createHash('sha256').update(JSON.stringify(level)).digest('hex'),map:level,solutions:variants});
 if(level.n%20===0)console.log('Archived through level '+level.n);
}
const archive={schemaVersion:1,created:'2026-09-26',rulesFingerprint:crypto.createHash('sha256').update(fs.readFileSync(root+'/campaign/route-solver.js')).digest('hex'),description:'Shortest valid completion routes under current rules. Coordinates are zero-based in JSON; route[0] is the starting state. Required houses, not necessarily every house, define completion. Recalculate after map/rule changes. Fixed purchased terrain, no mid-route purchase actions.',levels:entries};
fs.writeFileSync(out+'/Last-Light-Courier-'+levels.length+'-Map-Solutions.json',JSON.stringify(archive));fs.writeFileSync(root+'/design/map-solutions-'+levels.length+'.json',JSON.stringify(archive));console.log('Saved '+entries.length+' maps, '+entries.reduce((n,l)=>n+l.solutions.length,0)+' routes');
