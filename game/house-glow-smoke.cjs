const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>!!window.__campaign&&!!window.__integratedShell);
    const before=await page.evaluate(()=>{
      __campaign.choose(1);
      const home=__campaign.levels[0].homes[0].p,cell=document.querySelector(`#board .cell[data-x="${home[0]}"][data-y="${home[1]}"]`);
      return {classes:cell.className,shadow:getComputedStyle(cell).boxShadow};
    });
    if(!before.classes.includes('houseUnlit')||!before.shadow.includes('255, 154, 60'))throw Error('Unlit house lacks orange glow: '+JSON.stringify(before));
    await page.screenshot({path:path.join(__dirname,'house-orange-review.png')});
    const adjacent=await page.evaluate(()=>{
      const level=__campaign.levels[0];__campaign.move(level.spine[1]);
      const home=level.homes[0].p,cell=document.querySelector(`#board .cell[data-x="${home[0]}"][data-y="${home[1]}"]`);
      return {classes:cell.className,shadow:getComputedStyle(cell).boxShadow};
    });
    if(!adjacent.classes.includes('houseUnlit')||!adjacent.shadow.includes('255, 154, 60'))throw Error('Adjacent unlit house lost orange glow: '+JSON.stringify(adjacent));
    const after=await page.evaluate(()=>{
      const level=__campaign.levels[0];
      for(const tile of level.spine.slice(2)){
        if(!__campaign.move(tile))throw Error('Reference move blocked');
        if(__campaign.getState().mask&1)break;
      }
      const home=level.homes[0].p,cell=document.querySelector(`#board .cell[data-x="${home[0]}"][data-y="${home[1]}"]`);
      return {mask:__campaign.getState().mask,classes:cell.className,shadow:getComputedStyle(cell).boxShadow};
    });
    if(!(after.mask&1)||!after.classes.includes('houseLit')||after.classes.includes('houseUnlit')||!after.shadow.includes('112, 239, 173'))throw Error('Reached house did not turn green: '+JSON.stringify(after));
    await page.screenshot({path:path.join(__dirname,'house-green-review.png')});
    if(errors.length)throw Error(errors.join(' | '));
    console.log('PASS orange unlit house changes to green when reached');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
