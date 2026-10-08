(() => {
  const key=document.body.classList.contains('testerBuild')?'llc-regression-data-v1':'llc-player-data-v1';
  const fresh=()=>({version:1,rulesRevision:3,profile:{guestId:crypto.randomUUID?.()||'guest-'+Date.now().toString(36),displayName:'Guest Courier',createdAt:new Date().toISOString(),linkedAccount:false},bestByLevel:{},recentRuns:[]});
  let data;
  try{const saved=JSON.parse(localStorage.getItem(key)||'null');data=saved?.version===1&&saved.profile&&saved.bestByLevel&&Array.isArray(saved.recentRuns)?saved:fresh()}catch(_){data=fresh()}
  if(data.rulesRevision!==3){data.bestByLevel={};data.rulesRevision=3}
  const persist=()=>{try{localStorage.setItem(key,JSON.stringify(data))}catch(_){}};
  persist();
  const seen=new Set();
  const record=run=>{if(!Number.isInteger(run.levelId)||!Number.isInteger(run.steps)||run.steps<1)return null;const marker=[run.levelId,run.steps,run.mask,run.wallet].join(':');if(seen.has(marker))return null;seen.add(marker);const entry={levelId:run.levelId,steps:run.steps,allHomes:!!run.allHomes,repairActive:!!run.repairActive,powerUsed:!!run.powerUsed,mask:run.mask,earned:run.earned,completedAt:new Date().toISOString(),rulesRevision:3};data.recentRuns.unshift(entry);data.recentRuns.length=Math.min(data.recentRuns.length,100);if(entry.allHomes&&(!data.bestByLevel[run.levelId]||entry.steps<data.bestByLevel[run.levelId].steps))data.bestByLevel[run.levelId]={steps:entry.steps,completedAt:entry.completedAt};persist();return entry};
  const globalBest=async levelId=>{const base=window.LLC_RESULTS_API;if(!base)return {status:'offline'};try{const response=await fetch(String(base).replace(/\/$/,'')+'/levels/'+levelId+'/best',{cache:'no-store'});if(!response.ok)throw Error('Results unavailable');const body=await response.json();if(body.levelId!==levelId||body.rulesRevision!==3||!Number.isInteger(body.bestSteps)||body.bestSteps<1)throw Error('Invalid result');return {status:'ready',steps:body.bestSteps,playerName:String(body.playerName||'Courier')}}catch(_){return {status:'offline'}}};
  window.LLCPlayerData={profile:()=>({...data.profile}),bestFor:levelId=>data.bestByLevel[levelId]||null,record,globalBest,snapshot:()=>structuredClone(data)};
})();
