// Confirm a saved shorter signaled completion through normal browser clicks.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
const preview=path.resolve(process.env.LLC_PREVIEW_PATH||path.join(root,'design/campaign-2000-preview/index.html'));
const records=JSON.parse(fs.readFileSync(process.env.LLC_SIGNAL_SHORTCUT_REPORT||
  path.join(__dirname,'house-order-screen-v1/signal-tour-screen-before-shortcut.json'))).shorterRoutes;
const n=Number(process.env.LLC_SIGNAL_SHORTCUT_LEVEL||1803);
const record=records.filter(x=>x.level===n).sort((a,b)=>a.steps-b.steps)[0];
if(!record)throw Error(`No saved shorter signal route for ${n}`);
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(pathToFileURL(preview).href,{waitUntil:'load'});
  const intro=page.locator('[data-action="start"]');if(await intro.isVisible())await intro.click();
  await page.locator('#menuLevelOne').click();await page.locator('#levels').click();
  await page.locator('#jumpLevel').fill(String(n));await page.locator('#jumpGo').click();
  if(await intro.isVisible())await intro.click();
  await page.locator('#sendPhaseSignal').click();
  let blockedAt=null;
  for(let i=1;i<record.route.length;i++){
    const [x,y]=record.route[i];
    const state=await page.evaluate(([x,y])=>{
      const cell=document.querySelector(`#board .cell[data-x="${x}"][data-y="${y}"]`);
      if(!cell)throw Error(`missing ${x},${y}`);cell.click();
      return {turns:document.getElementById('turns').textContent};
    },[x,y]);
    if(!state.turns.includes(String(i))){blockedAt=i;break}
  }
  const final=await page.evaluate(()=>({turns:document.getElementById('turns').textContent,
    houses:document.getElementById('housesLit').textContent,
    text:document.body.innerText.slice(-600)}));
  await page.screenshot({path:path.join(__dirname,`signal-shortcut-${n}.png`)});
  const result={level:n,steps:record.steps,signalReferenceSteps:record.signalReferenceSteps,
    blockedAt,final,errors};
  console.log(JSON.stringify(result));
  if(errors.length||Boolean(blockedAt)!==(process.env.LLC_EXPECT_BLOCK!=='0'))process.exitCode=1;
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
