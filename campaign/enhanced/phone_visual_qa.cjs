// Headless phone-size smoke test of the self-contained browser preview.
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const width=Number(process.env.LLC_QA_WIDTH||390);
  const page=await browser.newPage({viewport:{width,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  const errors=[];
  page.on('pageerror',error=>errors.push(error.stack||String(error)));
  page.on('console',message=>{if(message.type()==='error')errors.push(message.text())});
  const url=pathToFileURL(path.resolve(__dirname,'../../design/campaign-2000-preview/index.html')).href;
  await page.goto(url,{waitUntil:'load'});
  await page.waitForTimeout(2500);
  const start=page.locator('[data-action="start"]');
  if(await start.count())await start.first().click();
  await page.locator('#menuLevelOne').click();
  const all=process.argv[2]==='all';
  const requested=all?Array.from({length:2000},(_,i)=>i+1):(process.argv[2]||'1').split(',').map(Number);
  const results=[];
  for(const n of requested){
    if(n!==1){
      await page.locator('#levels').click();
      await page.locator('#jumpLevel').fill(String(n));
      await page.locator('#jumpGo').click();
    }
    if(await start.isVisible())await start.first().click();
    const result=await page.evaluate(()=>({bodyWidth:document.body.scrollWidth,viewport:window.innerWidth,scrollY:window.scrollY,board:document.getElementById('board')?.getBoundingClientRect().toJSON(),cells:document.querySelectorAll('#board .cell').length,scrolls:(()=>{let e=document.getElementById('board'),a=[];while(e){if(e.scrollTop||e.scrollLeft)a.push({id:e.id,class:e.className,top:e.scrollTop,left:e.scrollLeft});e=e.parentElement}return a})(),visibleDialogs:[...document.querySelectorAll('dialog,[role=dialog]')].filter(x=>x.open||getComputedStyle(x).display!=='none').map(x=>x.id)}));
    results.push({n,...result});
    if(requested.length<=4)await page.screenshot({path:path.join(__dirname,`phone-qa-level-${n}-${width}.png`)});
  }
  const report={viewport:{width,height:844},tested:results.length,levels:results.map(r=>({n:r.n,cells:r.cells,bodyWidth:r.bodyWidth,playScroll:r.scrolls.find(s=>s.id==='playScreen')?.top||0})),failures:results.filter(r=>r.bodyWidth>width||!r.cells||r.scrolls.some(s=>s.id==='playScreen')),errors};
  fs.writeFileSync(process.env.LLC_QA_REPORT?path.resolve(process.env.LLC_QA_REPORT):path.join(__dirname,`phone-qa-report-${width}.json`),JSON.stringify(report,null,2));
  console.log(JSON.stringify(all?{tested:report.tested,failures:report.failures,errors}: {results,errors}));
  if(errors.length||report.failures.length)process.exitCode=1;
  await browser.close();
})().catch(error=>{console.error(error);process.exitCode=1});
