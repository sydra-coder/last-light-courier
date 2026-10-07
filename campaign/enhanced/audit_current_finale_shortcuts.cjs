const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const sources={NESW:[1911],SWNE:[1903,1919,1928,1934,1943,1944,1952],WSEN:[1906]};
const rows=[];
for(const [order,numbers] of Object.entries(sources)){
  const found=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,`event-aware-1901-2000-current-${order}.json`))).rows.map(x=>[x.level,x]));
  for(const n of numbers){
    const candidate=found.get(n);
    for(const choice of ['default','power',...(n===1943?['signal']:[])]){
      api.choose(n);api.begin();
      const power=api.getLevel().reviewPower;
      if(choice==='signal'&&!api.signal())throw Error(`Signal unavailable ${n}`);
      let used=false,blockedAt=null;
      if(choice==='power'&&power==='map_stabilizer')used=api.usePower(power);
      for(let i=1;i<candidate.staticCandidateRoute.length;i++){
        if(!api.move(candidate.staticCandidateRoute[i])){blockedAt=i;break}
        if(choice==='power'&&!used&&((power==='lumen_flask'&&i===1)||(power==='road_repair'&&api.getState().mask)))
          used=api.usePower(power);
      }
      const state=api.getState();
      rows.push({level:n,choice,power,powerUsed:used,blockedAt,completed:state.done&&!state.failed,
        steps:state.turns,light:state.light,referenceSteps:candidate.verifiedRouteSteps,order:candidate.order,source:order});
    }
  }
}
fs.writeFileSync(path.join(__dirname,'current-finale-shortcuts-audit.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows));
