"""Replay every reference route against production movement, not the generator."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))
hook='''window.__mapValidation={setup(levels){render=()=>{};renderLevels=()=>{};renderRepair=()=>{};renderLegend=()=>{};setStatus=()=>{};ISO.move=()=>{};FEEDBACK.emit=()=>{};LEVELS.splice(0,LEVELS.length,...levels);},run({n,bought,route}){save.repairs[n]=bought;choose(n);state.help=false;let blocked=null;for(const s of route.slice(1)){if(!move(s.p)){blocked=s.p;break;}if(state.light!==s.light||state.mask!==s.mask||state.phase!==s.phase||state.phase2!==s.phase2)return {mismatch:state.turns};}return {blocked,done:state.done,failed:state.failed,mask:state.mask,light:state.light,steps:state.turns};}};'''
testfile=ROOT/'work/1000-validation.html';testfile.parent.mkdir(exist_ok=True)
testfile.write_text((ROOT/'CAMPAIGN_100_LEVELS.html').read_text(encoding='utf-8').replace('window.__campaign={',hook+'window.__campaign={'),encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Users\rahul\AppData\Local\Google\Chrome\Application\chrome.exe',headless=True)
    page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(testfile.as_uri())
    page.evaluate('levels=>__mapValidation.setup(levels)',[e['map'] for e in archive['levels']])
    checked=0
    for e in archive['levels']:
        for v in e['solutions']:
            result=page.evaluate('args=>__mapValidation.run(args)',dict(n=e['level'],bought=v['repairPurchased'],route=v['route']))
            assert result.get('blocked') is None and result.get('done') and not result.get('failed'),(e['level'],result)
            checked+=1
        if e['level']%100==0:print('Live game replay through',e['level'],flush=True)
    assert not errors,errors
    print('PASS:',checked,'routes, all 1000 maps, production movement and state agreement')
    browser.close()
