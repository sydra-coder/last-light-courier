(() => {
  const app=window.__campaign,fixture=window.LLCRegression;
  if(!app||!fixture)return;
  const play=document.getElementById('playScreen');
  window.__integratedShell?.enterBoard();
  const bar=document.createElement('section');
  bar.id='regressionBar';
  bar.innerHTML=`<div class="regressionHeading"><strong>Regression Arena</strong><span>One 12×12 map · isolated tester save</span></div><div class="regressionActions"><label>Hazards <select id="regressionScenario" aria-label="Hazard setup">${Object.entries(fixture.options).map(([id,label])=>`<option value="${id}" ${id===fixture.scenario?'selected':''}>${label}</option>`).join('')}</select></label><button type="button" id="regressionReplay">↻ Replay fresh</button></div><details><summary>What can I test?</summary><p>All nine implemented powers start with ten charges each. Switch hazard setups to test roads, weather, shadows, and circuits on this same map. Deliver three houses and return to the blue depot to finish. Replay fresh resets the route, powers, repair purchase, and banked points. Campaign levels and player saves are separate.</p></details>`;
  play.prepend(bar);
  document.getElementById('regressionScenario').addEventListener('change',e=>{
    const url=new URL(location.href);url.searchParams.set('scenario',e.target.value);location.href=url.href;
  });
  document.getElementById('regressionReplay').addEventListener('click',()=>{
    localStorage.removeItem('last-light-courier-regression-v1');location.reload();
  });
  document.title='Last Light Courier · Regression Arena';
})();
