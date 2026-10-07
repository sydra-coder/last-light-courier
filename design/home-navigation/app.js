const saveKey = 'last-light-courier-campaign-v1';
let save = {wallet:0, cleared:{}, mastered:{}, hints:3, pendingHintRewards:0, viewMode:'isometric', soundOn:true, hapticsOn:true};
try { const stored = JSON.parse(localStorage.getItem(saveKey) || 'null'); if (stored && typeof stored.wallet === 'number') save = {...save, ...stored}; } catch (_) {}
const cleared = new Set(Object.keys(save.cleared || {}).filter(n => save.cleared[n]).map(Number));
const count = [...cleared].filter(n => n >= 1 && n <= 200).length;
const next = Array.from({length:200}, (_,i) => i+1).find(n => !cleared.has(n)) || 200;
const mastered = Object.keys(save.mastered || {}).filter(n => save.mastered[n]).length;
let tab = 'home', chapterStart = Math.floor((next-1)/10)*10+1;
const content = document.getElementById('content');
document.getElementById('wallet').textContent = Number(save.wallet || 0).toLocaleString();
const card = (title, body, action='') => `<section class="card"><h2>${title}</h2><p>${body}</p>${action}</section>`;
function render() {
  document.querySelectorAll('[data-tab]').forEach(button => {
    const active = button.dataset.tab === tab;
    button.classList.toggle('active', active);
    if (active) button.setAttribute('aria-current','page'); else button.removeAttribute('aria-current');
  });
  if (tab === 'home') {
    content.innerHTML = `<div class="hero" aria-label="Night village, courier, lantern and houses"><div class="stars"></div><div class="moon"></div><div class="hill"></div><div class="lane"></div><div class="house h1"></div><div class="house h2"></div><div class="house h3"></div><div class="shadow"></div><div class="courier"></div><div class="lantern"></div><div class="heroLabel">The village is waiting</div></div>
      <div class="progress"><div><div class="eyebrow">Your journey</div><strong>${count} / 200 routes cleared</strong></div><span class="pill">Level ${next}</span></div>
      <div class="meter" role="progressbar" aria-valuenow="${count}" aria-valuemax="200"><span style="--progress:${count/2}%"></span></div>
      <div class="note">${count === 200 ? 'All 200 routes cleared · replay any level' : count ? `Next stop: Level ${next}` : 'Begin with Level 1'} · 20 playable chapters</div>
      <button class="primary" id="play">▶ ${count === 200 ? 'Replay' : 'Play'} level ${next}</button>
      ${card('A new route awaits','Light every house, avoid the shadows, and return to the depot to bank your points.','<button class="ghost" data-go="map">Browse levels</button>')}`;
  } else if (tab === 'map') {
    const start = chapterStart;
    content.innerHTML = `<h1 class="title">Village map</h1><div class="muted">Chapter ${Math.ceil(start/10)} · Levels ${start}–${start+9}</div>
      <div class="path">${Array.from({length:10},(_,i) => {const n=start+i,x=15+(i%3)*29,y=12+Math.floor(i/3)*24;return `<button class="stop ${cleared.has(n)?'done':n===next?'next':''}" data-level="${n}" style="left:${x}%;top:${y}%" aria-label="Level ${n}${cleared.has(n)?', cleared':''}">${n}</button>`}).join('')}</div>
      <div class="row"><button class="ghost" id="prev">← Chapter</button><span class="tag">Tap a stop</span><button class="ghost" id="next">Chapter →</button></div>
      ${card('Later roads','Levels 201–1000 are archived maps under review; they are not yet playable.')}
      <p class="note">All levels 1–200 remain selectable, matching the restored game.</p>`;
  } else if (tab === 'shop') {
    content.innerHTML = `<h1 class="title">Village shop</h1><p class="muted">Preview of the proposed item economy</p>
      <div class="card"><div class="row"><strong>✦ ${Number(save.wallet||0).toLocaleString()} banked points</strong><span class="pill">Current game</span></div><p>These points are earned by returning to the depot. The existing game uses them for marked repairs on individual levels.</p><button class="ghost" id="openRepairs">See repairs in game</button></div>
      ${card('Lantern hints','Proposed replenishment: one hint for a displayed gem price. Your current hints: '+(save.hints??3)+' / 5.','<span class="tag">Concept · unavailable</span>')}
      ${card('Repair voucher','Proposed item for a marked repair. A required map would receive its reserved free repair.','<span class="tag">Concept · unavailable</span>')}
      ${card('Tunnel token','Proposed item for one eligible rubble tile, subject to map rules.','<span class="tag">Concept · unavailable</span>')}
      <p class="note">Gems, item inventory, prices, and purchases are not implemented here. No real money purchase is proposed.</p>`;
  } else if (tab === 'courier') {
    content.innerHTML = `<h1 class="title">Courier</h1><p class="muted">Your satchel and delivery record</p>
      ${card('Lantern hints',`You carry ${save.hints??3} / 5 hints. ${save.pendingHintRewards||0} milestone reward(s) wait to be collected in the game.`,'<button class="ghost" id="openHints">Open playable game</button>')}
      ${card('Journey log',`${count} unique levels cleared. ${mastered} recorded as mastered.`,'<button class="ghost" data-go="map">See village map</button>')}
      ${card('Keepsakes · proposed','Village postcards and courier equipment could appear here after their rules and art are approved.')}
      <p class="note">This screen reads current progress. It does not claim or spend items.</p>`;
  } else if (tab === 'trophies') {
    content.innerHTML = `<h1 class="title">Trophies</h1><p class="muted">A clear view of earned progress</p>
      ${card('Completed deliveries',`${count} of 200 playable levels cleared.`, `<div class="meter"><span style="--progress:${count/2}%"></span></div>`)}
      ${card('Mastered routes',`${mastered} mastery records saved.`, '<span class="tag">Current game record</span>')}
      ${card('Chapter milestones',`${Math.floor(count/10)} full sets of ten unique clears. Hint milestones are based on unique levels, not repeat play.`, '<span class="tag">Progress summary</span>')}
      ${card('Future achievements · proposed','Named trophies, badges, and rewards need separate rules. None are awarded by this mockup.')}`;
  } else if (tab === 'settings') {
    content.innerHTML = `<h1 class="title">Settings</h1>${card('Current preferences',`View: ${String(save.viewMode||'isometric').replaceAll('-',' ')} · Sound ${save.soundOn?'on':'off'} · Haptics ${save.hapticsOn?'on':'off'}.`,'<button class="ghost" id="openGame">Open game settings</button>')}${card('How to play','Open the playable game for the house, depot, shadow, light, and repair rules.','<button class="ghost" id="openGame2">Open game</button>')}`;
  }
}
document.addEventListener('click', event => {
  const button = event.target.closest('button'); if (!button) return;
  if (button.dataset.concept) { document.body.dataset.concept=button.dataset.concept; document.querySelectorAll('[data-concept]').forEach(x=>x.classList.toggle('on',x===button)); return; }
  if (button.dataset.tab || button.dataset.go || button.id==='settings') { tab=button.dataset.tab||button.dataset.go||'settings'; render(); content.parentElement.scrollTop=0; return; }
  if (button.id==='play' || button.dataset.level || ['openGame','openGame2','openRepairs','openHints'].includes(button.id)) { location.href=`../../index.html?level=${button.dataset.level||next}`; return; }
  if (button.id==='prev' || button.id==='next') { chapterStart=Math.max(1,Math.min(191,chapterStart+(button.id==='next'?10:-10))); render(); }
});
render();
