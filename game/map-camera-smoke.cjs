const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    await page.evaluate(()=>{__campaign.choose(1401);__integratedShell.enterBoard()});
    await page.waitForTimeout(150);
    const result=await page.evaluate(async()=>{
      const viewport=document.querySelector('.mapViewport'),frame=viewport.querySelector('.boardframe');
      if(!frame.classList.contains('zoomed'))return {error:'large map did not open zoomed'};
      viewport.scrollLeft=0;viewport.scrollTop=0;
      const pre={x:viewport.scrollLeft,y:viewport.scrollTop};
      document.querySelector('#focusCourier').click();
      const start={x:viewport.scrollLeft,y:viewport.scrollTop};
      await new Promise(resolve=>setTimeout(resolve,90));
      const middle={x:viewport.scrollLeft,y:viewport.scrollTop};
      await new Promise(resolve=>setTimeout(resolve,550));
      const end={x:viewport.scrollLeft,y:viewport.scrollTop};
      return {pre,start,middle,end};
    });
    if(result.error||result.start.x===result.end.x&&result.start.y===result.end.y)throw Error('Camera did not travel: '+JSON.stringify(result));
    if(result.middle.x===result.start.x&&result.middle.y===result.start.y||result.middle.x===result.end.x&&result.middle.y===result.end.y)throw Error('Camera skipped smooth transition: '+JSON.stringify(result));
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS large-map camera pans smoothly to courier');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
