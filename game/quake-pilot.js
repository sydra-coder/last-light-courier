(() => {
  const plans=new Map((window.LLC_QUAKE_PILOT_PLANS?.plans||[]).map(plan=>[plan.level,plan]));
  const same=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
  const count=m=>{let n=0;while(m){n+=m&1;m>>>=1}return n};
  let forced=new URLSearchParams(location.search).get('quakeVariant')||sessionStorage.getItem('llc-quake-variant')||'';
  const options={eventAware:true,search:'astar',maxExplored:100000};
  let lastRoute=null;

  function routeLightNeeded(level,start,route){
    for(let initial=1;initial<=level.cap;initial++){
      let light=initial,valid=true;
      for(let i=1;i<route.length;i++){
        const step=route[i],fresh=step.mask!==route[i-1].mask;
        light-=same(step.p,level.dark)?2:1;
        if(fresh)light=Math.min(level.cap,light+2);
        if(light<=0){valid=false;break}
      }
      if(valid)return initial;
    }
    return start.light;
  }

  function select(level,state,solver,save){
    const plan=plans.get(level.n);if(!plan)return null;
    lastRoute=null;
    const availableLight=state.light;
    const original=level.__quakeBase||level.quakeEvent;
    const preferred=plan.variants.filter(item=>item.id===forced);
    const pool=preferred.length?preferred:[...plan.variants];
    if(!preferred.length)for(let i=pool.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]]}
    const checked=[];
    const solve=(id,quakeEvent,light=state.light)=>{
      const started=performance.now(),current={...state,light};
      const result=solver.solve({...level,quakeEvent},current,{...options,repaired:!!save.repairs?.[level.n]});
      checked.push({id,status:result.status,ms:Math.round(performance.now()-started),explored:result.explored});
      return result;
    };
    const accept=(id,quakeEvent,result,topUp=0)=>{lastRoute=result.route.map(step=>[...step.p]);return {quakeEvent:structuredClone(quakeEvent),log:{variant:id,random:!preferred.length,checked,availableLight,neededLight:routeLightNeeded(level,state,result.route),completionMoves:result.steps,finishingLight:result.route.at(-1).light,topUp}}};
    const started=performance.now();
    for(const item of pool){
      if(performance.now()-started>550)break;
      const result=solve(item.id,item.quakeEvent);
      if(result.status==='solved')return accept(item.id,item.quakeEvent,result);
    }
    const safe={...original,close:[-1,-1],closeExtra:[],open:original.open};
    if(performance.now()-started>900)return {quakeEvent:safe,log:{variant:'unverified-no-closure',random:false,checked,availableLight,neededLight:null,completionMoves:null,finishingLight:null,topUp:0}};
    const baseline=solve('original',original);
    if(baseline.status==='solved')return accept('original',original,baseline);
    const noClosure=solve('no-closure',safe);
    if(noClosure.status==='solved')return accept('no-closure',safe,noClosure);
    const full=solve('light-rescue',safe,level.cap);
    if(full.status==='solved'){
      const needed=routeLightNeeded(level,{...state,light:level.cap},full.route),topUp=Math.max(0,Math.min(level.cap,needed+3)-state.light);
      state.light+=topUp;
      return accept('light-rescue',safe,full,topUp);
    }
    return {quakeEvent:safe,log:{variant:'unverified-no-closure',random:false,checked,availableLight,neededLight:null,completionMoves:null,finishingLight:null,topUp:0}};
  }

  window.LLCQuakePilot=Object.freeze({has:n=>plans.has(n),variants:n=>plans.get(n)?.variants.map(v=>v.id)||[],getForced:()=>forced,setForced:id=>{forced=id||'';if(forced)sessionStorage.setItem('llc-quake-variant',forced);else sessionStorage.removeItem('llc-quake-variant')},lastVerifiedRoute:()=>lastRoute?.map(p=>[...p])||null,select});
})();
