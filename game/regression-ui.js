(() => {
  const app=window.__campaign,fixture=window.LLCRegression;
  if(!app||!fixture)return;
  const play=document.getElementById('playScreen');
  window.__integratedShell?.enterBoard();
  const bar=document.createElement('section');
  bar.id='regressionBar';
  bar.innerHTML=`<div class="regressionHeading"><strong>${fixture.title||'Regression Arena'}</strong><span>One 12×12 map · isolated tester save</span></div><div class="regressionActions"><label>Hazards <select id="regressionScenario" aria-label="Hazard setup">${Object.entries(fixture.options).map(([id,label])=>`<option value="${id}" ${id===fixture.scenario?'selected':''}>${label}</option>`).join('')}</select></label><button type="button" id="regressionReplay">↻ Replay fresh</button></div><details><summary>What can I test?</summary><p>All nine implemented powers start with ten charges each. Switch hazard setups to test roads, weather, shadows, and circuits on this same map. Deliver ${fixture.level.required} houses and return to the blue depot to finish. Replay fresh resets the route, powers, repair purchase, and banked points. Campaign levels and player saves are separate.</p></details>`;
  play.prepend(bar);
  const controls=play.querySelector('.boardZoom');
  const hint=document.getElementById('useHint');
  const hintCount=document.getElementById('hintCount')?.textContent||'5 / 5';
  hint.innerHTML=`<span aria-hidden="true">💡</span><span id="hintCount">${hintCount}</span>`;
  hint.setAttribute('aria-label','Use a route hint');
  hint.title='Use a route hint';
  controls.prepend(hint);
  controls.append(document.getElementById('collectHint'));
  const status=document.getElementById('boardMessage');
  const statusToggle=document.createElement('button');
  statusToggle.type='button';statusToggle.id='regressionMessageToggle';
  statusToggle.setAttribute('aria-label','Show latest map message');
  statusToggle.setAttribute('aria-expanded','false');
  statusToggle.textContent='ⓘ';
  controls.append(statusToggle,status);
  status.classList.remove('expanded');
  status.hidden=true;
  statusToggle.addEventListener('click',()=>{
    status.hidden=!status.hidden;
    status.classList.toggle('expanded',!status.hidden);
    statusToggle.setAttribute('aria-expanded',String(!status.hidden));
  });
  status.addEventListener('click',()=>{status.hidden=true;status.classList.remove('expanded');statusToggle.setAttribute('aria-expanded','false')});
  const labelMessage=()=>{statusToggle.title=[status.querySelector('strong')?.textContent,status.querySelector('span')?.textContent].filter(Boolean).join(' · ')};
  new MutationObserver(labelMessage).observe(status,{childList:true,subtree:true,characterData:true});
  labelMessage();
  const powerLabels={anchor_trap:'Trap',decoy_light:'Decoy',reveal_pulse:'Reveal',lumen_flask:'Flask',road_repair:'Repair',light_bridge:'Bridge',map_stabilizer:'Guard',freeze_seal:'Freeze',rewind:'Undo'};
  const powerTray=document.getElementById('candidatePower');
  const labelPowers=()=>powerTray.querySelectorAll('.powerIcon').forEach(button=>{button.dataset.label=powerLabels[button.dataset.power]||button.dataset.power});
  new MutationObserver(labelPowers).observe(powerTray,{childList:true,subtree:true});
  labelPowers();
  document.getElementById('regressionScenario').addEventListener('change',e=>{
    const url=new URL(location.href);url.searchParams.set('scenario',e.target.value);location.href=url.href;
  });
  document.getElementById('regressionReplay').addEventListener('click',()=>{
    localStorage.removeItem(fixture.saveKey||'last-light-courier-regression-v1');location.reload();
  });
  document.title='Last Light Courier · '+(fixture.title||'Regression Arena');
})();
