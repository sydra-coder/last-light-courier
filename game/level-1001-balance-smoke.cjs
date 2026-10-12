const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const overlay=JSON.parse(fs.readFileSync(path.join(__dirname,'../campaign/enhanced/level-1001-balance-v1/overlay.json'),'utf8'));

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    for(const file of ['index.html','tester.html'])for(const proof of overlay.verifiedFirstHouses){
      const page=await browser.newPage(),errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto('file://'+path.join(__dirname,file).replaceAll('\\','/')+'?level=1001');
      await page.waitForFunction(()=>!!window.__campaign);
      const result=await page.evaluate(({route})=>{
        const c=window.__campaign,level=c.getCurrentLevel();let first=null,blockedAt=null;
        if(level.cap!==120)throw Error('Expected 120 starting light');
        for(let i=1;i<route.length;i++){
          if(!c.move(route[i].slice(0,2))){blockedAt=i;break}
          const state=c.getState();if(first===null&&state.mask)first=Math.log2(state.mask&-state.mask)+1;
        }
        const state=c.getState();return {first,blockedAt,done:state.done,failed:state.failed,turns:state.turns,light:state.light,flooded:state.floodStart!==null&&state.turns-state.floodStart>=level.floodRoad.closeAfter,repair:!!c.getSave().repairs[1001]};
      },{route:proof.route});
      if(result.first!==proof.firstHouse||result.blockedAt!==null||!result.done||result.failed||!result.flooded||result.repair||result.turns!==proof.steps||result.light!==proof.finishLight||errors.length)throw Error(file+' first house '+proof.firstHouse+': '+JSON.stringify({result,errors}));
      console.log(`PASS ${file} first house ${proof.firstHouse}: ${result.turns} moves, ${result.light} light`);
      await page.close();
    }
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
