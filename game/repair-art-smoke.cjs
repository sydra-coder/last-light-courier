const path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>!!window.__integratedShell&&!!window.__campaign);
    await page.evaluate(()=>__campaign.choose(6));
    const before=await page.evaluate(()=>({wallet:__campaign.getSave().wallet,gems:__campaign.getSave().gems,turns:__campaign.getState().turns,r:__campaign.getCurrentLevel().repair}));
    const tile=`#board .cell[data-x="${before.r.tile[0]}"][data-y="${before.r.tile[1]}"]`;
    await page.locator(tile).click();
    const distant=await page.evaluate(()=>({cost:document.querySelector('#repairPopover strong')?.textContent,move:!!document.querySelector('[data-repair-move]'),wallet:__campaign.getSave().wallet,gems:__campaign.getSave().gems}));
    if(distant.cost!==Math.ceil(before.r.cost/100)+' gems'||distant.move||distant.wallet!==before.wallet||distant.gems!==before.gems)throw Error('Distant repair cost changed balance: '+JSON.stringify(distant));
    await page.locator('[data-repair-tile-cancel]').click();
    const pathToRepair=await page.evaluate(()=>{
      const l=__campaign.getCurrentLevel(),start=__campaign.getState().pos,target=l.repair.tile,walls=new Set(l.walls),key=p=>p.join(','),queue=[[start,[]]],seen=new Set([key(start)]);while(queue.length){const [p,path]=queue.shift();if(Math.abs(p[0]-target[0])+Math.abs(p[1]-target[1])===1)return path;for(const q of [[p[0]+1,p[1]],[p[0]-1,p[1]],[p[0],p[1]+1],[p[0],p[1]-1]]){const k=key(q);if(q[0]<0||q[1]<0||q[0]>=l.grid||q[1]>=l.grid||walls.has(k)||seen.has(k))continue;seen.add(k);queue.push([q,[...path,q]])}}throw Error('Repair unreachable')
    });
    await page.evaluate(path=>{for(const p of path)__campaign.move(p)},pathToRepair);
    const adjacent=await page.evaluate(()=>({can:__campaign.canRepairMove(__campaign.getCurrentLevel().repair.tile),wallet:__campaign.getSave().wallet,gems:__campaign.getSave().gems,turns:__campaign.getState().turns}));
    if(!adjacent.can)throw Error('Adjacent repair tile not safe');
    await page.locator(tile).click();
    if(!(await page.locator('[data-repair-move]').count()))throw Error('Repair and move confirmation missing');
    await page.screenshot({path:path.join(__dirname,'repair-tile-review.png')});
    await page.locator('[data-repair-tile-cancel]').click();
    if((await page.evaluate(()=>__campaign.getSave().gems))!==adjacent.gems)throw Error('Cancel spent gems');
    await page.locator(tile).click();await page.locator('[data-repair-move]').click();
    const after=await page.evaluate(()=>({wallet:__campaign.getSave().wallet,gems:__campaign.getSave().gems,turns:__campaign.getState().turns,pos:__campaign.getState().pos,repaired:!!__campaign.getSave().repairs?.[6]}));
    if(after.wallet!==adjacent.wallet||after.gems!==adjacent.gems-Math.ceil(before.r.cost/100)||after.turns!==adjacent.turns+1||after.pos.join(',')!==before.r.tile.join(',')||!after.repaired)throw Error('Repair and move transaction failed: '+JSON.stringify(after));
    if(errors.length)throw Error('Browser errors: '+errors.join(' | '));
    console.log('PASS repair art, cost-only distant tap, cancel, atomic repair and move');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
