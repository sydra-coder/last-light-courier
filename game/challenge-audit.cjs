const fs=require('node:fs');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'..','design','campaign-2000-preview','index.html'),'utf8');
const marker='const LEVELS=';const start=source.indexOf(marker)+marker.length;const end=source.indexOf('];',start)+1;
if(start<marker.length||end<=start)throw Error('Level data not found');
const levels=JSON.parse(source.slice(start,end));
const describe=l=>({n:l.n,grid:l.grid,required:l.required,homes:l.homes.length,cap:l.cap,spine:l.spine?.length,patrol:l.patrol,patrol2:l.patrol2,echo:l.echo,phase:l.phase,phase2:l.phase2,repair:l.repair?.cost,wallCount:l.walls?.length});
for(const n of [10,20,40,60,70,80,100,120,200,220,500,1000,2000])console.log(JSON.stringify(describe(levels[n-1])));
console.log('counts',JSON.stringify({levels:levels.length,echo:levels.filter(l=>l.echo).length,patrol2:levels.filter(l=>l.patrol2).length,milestones:levels.filter(l=>l.n%20===0).length,milestonesWithSecond:levels.filter(l=>l.n%20===0&&l.patrol2).length}));
