(() => {
  const legacyNav = document.getElementById('bottomNav');
  if (!legacyNav || !window.__campaign) return;
  const nav = document.createElement('nav');
  nav.id = 'integratedNav';
  nav.setAttribute('aria-label', 'Main game navigation');
  nav.innerHTML = [
    ['map','◇','Map'],['shop','♜','Shop'],['play','▶','Play'],['courier','♟','Courier'],['trophies','♛','Trophies']
  ].map(([id,icon,label]) => `<button type="button" data-destination="${id}" aria-label="${label}"><span>${icon}</span>${label}</button>`).join('');
  document.body.append(nav);
  const overlay = document.createElement('div');
  overlay.id = 'integratedOverlay';
  overlay.hidden = true;
  document.body.append(overlay);
  const shopScreen=document.createElement('section');
  shopScreen.id='shopScreen';
  shopScreen.className='shopPage gemShopPanel';
  shopScreen.setAttribute('aria-label','Night Market');
  const side=document.querySelector('.side');
  side.append(shopScreen);
  const courierScreen=document.createElement('section');courierScreen.id='courierScreen';courierScreen.className='tabPage courierPanel courierPage';courierScreen.setAttribute('aria-label','Choose Courier');side.append(courierScreen);
  const trophiesScreen=document.createElement('section');trophiesScreen.id='trophiesScreen';trophiesScreen.className='tabPage trophiesPage';trophiesScreen.setAttribute('aria-label','Trophy Cabinet');side.append(trophiesScreen);
  const playScreen = document.getElementById('playScreen');
  const home = document.createElement('section');
  home.id = 'storybookHome';
  home.setAttribute('aria-label','Last Light Courier home');
  home.innerHTML = `<div class="storybookTop"><div class="storybookWordmark">LAST LIGHT<br>COURIER</div><button type="button" data-home-settings aria-label="Settings">⚙</button></div><p class="storybookTagline">Small deliveries.<br>A brighter tomorrow.</p><div class="storybookArt" role="img" aria-label="Moonlit storybook village, bridge, and courier with a lantern"></div><div class="storybookProgress"><strong id="homeProgress">0 / 2000 routes cleared</strong><span class="storybookMeter"><i id="homeProgressFill"></i></span><small id="homeNext">Next: Level 1</small></div><button type="button" id="storybookPlay">PLAY <span aria-hidden="true">›</span></button><p class="storybookMotto">Go further. Light the way.</p>`;
  playScreen.prepend(home);
  const enterBoard = () => { playScreen.classList.remove('homeMode'); setActive('play'); };
  const showHome = () => { const s=window.__campaign.getSave(); const cleared=Object.keys(s.cleared||{}).filter(n=>s.cleared[n]&&+n<=2000).length; const next=window.__campaign.levels.find(l=>!s.cleared?.[l.n])?.n||2000; home.querySelector('#homeProgress').textContent=`${cleared} / 2000 routes cleared`; home.querySelector('#homeNext').textContent=`Next: Level ${next}`; home.querySelector('#homeProgressFill').style.width=`${cleared/20}%`; playScreen.classList.add('homeMode'); setActive('play'); };
  home.addEventListener('click',e=>{if(e.target.closest('[data-home-settings]'))document.getElementById('gameSettings').click();if(e.target.closest('#storybookPlay')){startAmbient();const s=window.__campaign.getState();if(s.done||s.failed){const save=window.__campaign.getSave();window.__campaign.choose(window.__campaign.levels.find(l=>!save.cleared?.[l.n])?.n||2000)}else enterBoard();}});
  const baseNames = ['Asha Emberlane','Tavi Mossbrook','Nila Lockwater','Rohan Bellwright','Eira Frostmere','Pip Patchwell','Fenn Rooftop','Bram Gearford','Lina Willowfen','Kavi Seabright','Sable Ashdown','Mara Daybreak','Orin Foxglove','Skye Bluecrest','Iris Lamplight','Zuri Marketwind','Noor Moonmere','Sol Sunward'];
  const ids = ['ember-scout','moss-ranger','canal-pilot','bell-messenger','winter-warden','patchwork-runner','rooftop-finch','clockwork-porter','willow-guide','harbor-skipper','ash-cartographer','dawn-baker','foxglove-courier','bluebird-runner','lantern-keeper','market-sprinter','mooncap-wanderer','sunset-relayer'];
  const shadowIds = ['night-wisp','dussehra-ember','halloween-hush','diwali-afterglow','winter-frost','new-year-stardrift','canal-mist','old-city-cinder','bell-hollow','ribbon-wraith','moth-veil','crescent-lurker','shard-mask','ink-puddle','thorn-crown','eclipse-orb','veil-hand','serpent-coil','hourglass-shade'];
  const shadowNames = ['Night Wisp','Dussehra Ember','Halloween Hush','Diwali Afterglow','Winter Frost','New Year Stardrift','Canal Mist','Old City Cinder','Bell Hollow','Ribbon Wraith','Moth Veil','Crescent Lurker','Shard Mask','Ink Puddle','Thorn Crown','Eclipse Orb','Veil Hand','Serpent Coil','Hourglass Shade'];
  const savedAppearance = (() => { try { return JSON.parse(localStorage.getItem('llc-appearance-v1') || '{}'); } catch { return {}; } })();
  let selectedCourier = Math.min(17,Math.max(0,Number(savedAppearance.courier)||0));
  let selectedLook = Math.min(5,Math.max(0,Number(savedAppearance.look)||0));
  const regionShadow = window.LLC_REGION_SHADOWS;
  let selectedShadow = regionShadow[Math.min(19,Math.floor(((Number(document.getElementById('levelTitle').textContent.match(/\d+/)?.[0])||1)-1)/100))];
  const looks = ['Roadworn','Marigold Trail','Hollowmoon','Gilded Lantern','Hearthbound','Starwake'];
  const lookAssets = ['','dussehra','halloween','diwali','christmas','new-year'];
  const image = i => `../design/character-variants/${String(i+1).padStart(2,'0')}-${ids[i]}.png`;
  const shadowImage = i => `../design/shadow-variants/${String(i+1).padStart(2,'0')}-${shadowIds[i]}.png`;
  const cache = new Map();
  const storyBackdrop = new Image();
  storyBackdrop.onload = () => window.__campaign.redraw();
  storyBackdrop.src = '../design/home-navigation/five-screen-concept.png';
  const getImage = src => { if (!cache.has(src)) { const img = new Image(); img.onload = () => window.__campaign.redraw(); img.src = src; cache.set(src,img); } return cache.get(src); };
  const courierAsset = () => !selectedLook ? image(selectedCourier) : selectedCourier === 0 ? `../design/character-variants/holiday-wardrobe/01-ember-scout-${lookAssets[selectedLook]}.png` : `../design/character-variants/holiday-wardrobe/${String(selectedCourier+1).padStart(2,'0')}-${ids[selectedCourier]}-five-looks.png`;
  const saveAppearance = () => { localStorage.setItem('llc-appearance-v1',JSON.stringify({courier:selectedCourier,look:selectedLook})); getImage(courierAsset()); window.__campaign.redraw(); };
  const onLevelChosen = n => { selectedShadow=regionShadow[Math.min(19,Math.floor((n-1)/100))];playScreen.classList.toggle('largeBoard',(window.__campaign.levels[n-1]?.grid||8)>=12);getImage(shadowImage(selectedShadow));updateAmbient();startAmbient(); };
  window.__appearance = {
    drawBackdrop(ctx,w,h) { if(!storyBackdrop.complete||!storyBackdrop.naturalWidth)return false; ctx.drawImage(storyBackdrop,727,228,337,315,0,0,w,h); ctx.fillStyle='#0a1a2b98'; ctx.fillRect(0,0,w,h); return true; },
    drawCourier(ctx,x,y,moving,t) { const img=getImage(courierAsset()); if (!img.complete || !img.naturalWidth) return false; ctx.save(); const bob=moving?Math.sin(t*.028)*2:0; ctx.shadowColor='#f8c777'; ctx.shadowBlur=8; if (selectedLook && selectedCourier !== 0) { const w=img.naturalWidth/5; ctx.drawImage(img,w*(selectedLook-1),0,w,img.naturalHeight,x-29,y-57+bob,58,66); } else ctx.drawImage(img,x-29,y-57+bob,58,66); ctx.restore(); return true; },
    drawShadow(ctx,x,y,echo,moving,t) { const img=getImage(shadowImage(selectedShadow)); if (!img.complete || !img.naturalWidth) return false; ctx.save(); ctx.globalAlpha=echo?.58:1; ctx.shadowColor='#ba8dec'; ctx.shadowBlur=12; const sway=moving?Math.sin(t*.02)*2:0; ctx.drawImage(img,x-25+sway,y-51,50,56); ctx.restore(); return true; }
  };
  const outfit = () => {
    if (!selectedLook) return `<img src="${image(selectedCourier)}" alt="${baseNames[selectedCourier]} in Roadworn clothes">`;
    if (selectedCourier === 0) return `<img src="../design/character-variants/holiday-wardrobe/01-ember-scout-${lookAssets[selectedLook]}.png" alt="${baseNames[selectedCourier]} in ${looks[selectedLook]}">`;
    return `<canvas class="outfitCanvas" width="125" height="155" role="img" aria-label="${baseNames[selectedCourier]} in ${looks[selectedLook]}" data-sheet="../design/character-variants/holiday-wardrobe/${String(selectedCourier+1).padStart(2,'0')}-${ids[selectedCourier]}-five-looks.png" data-look="${selectedLook}"></canvas>`;
  };
  const drawOutfitCanvas = () => { const canvas=courierScreen.querySelector('.outfitCanvas');if(!canvas)return;const img=new Image();img.onload=()=>{if(!canvas.isConnected)return;const ctx=canvas.getContext('2d'),sw=img.naturalWidth/5,scale=Math.min(canvas.width/sw,canvas.height/img.naturalHeight),dw=sw*scale,dh=img.naturalHeight*scale;ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(img,(Number(canvas.dataset.look)-1)*sw,0,sw,img.naturalHeight,(canvas.width-dw)/2,(canvas.height-dh)/2,dw,dh)};img.src=canvas.dataset.sheet;};
  const getSave = () => window.__campaign.getSave();
  const gems = window.LLCGemShop;
  const gemAmount = amount => `${gems.icon}<span>${Number(amount||0).toLocaleString()}</span>`;
  const pointIcon = '<svg class="pointIcon" viewBox="0 0 32 36" aria-hidden="true"><path d="M13 3h6m-3 0v5M9 12l3-4h8l3 4M9 12h14v17H9z" fill="#7a4b2c" stroke="#ffe5a7" stroke-width="2" stroke-linejoin="round"/><path d="M12 15h8v10h-8z" fill="#ffd275"/><path d="M13 20l3-5 3 5-3 5z" fill="#fff4b9"/><path d="M7 29h18v3H7z" fill="#c88a46" stroke="#ffe5a7" stroke-width="1.5"/></svg>';
  const pointAmount = amount => `${pointIcon}<span>${Number(amount||0).toLocaleString()}</span>`;
  const resourceStrip=document.createElement('div');resourceStrip.id='resourceStrip';resourceStrip.setAttribute('aria-label','Gem and lantern point balances');side.prepend(resourceStrip);
  const updateResources=()=>{const s=getSave();resourceStrip.innerHTML=`<strong class="gemAmount" aria-label="${s.gems} gems">${gemAmount(s.gems)}</strong><strong class="pointAmount" aria-label="${s.wallet} earned points">${pointAmount(s.wallet)}</strong>`};
  updateResources();
  new MutationObserver(updateResources).observe(document.getElementById('mobileWallet'),{subtree:true,childList:true,characterData:true});
  let exchangeQty=1;
  const settingsPanel=document.getElementById('settingsPanel');
  const extras=document.createElement('div');
  extras.id='integratedSettings';
  document.getElementById('settingsViews').after(extras);
  let ambient=null;
  const updateAmbient=()=>{if(!ambient)return;const s=getSave(),n=Number(document.getElementById('levelTitle').textContent.match(/\d+/)?.[0])||1,state=window.__campaign.getState();ambient.update({region:Math.min(19,Math.floor((n-1)/100)),light:Number(state.light||0),cap:Number(document.getElementById('cap').textContent.match(/\d+/)?.[0])||20,musicOn:s.musicOn!==false,volume:Number.isFinite(s.musicVolume)?s.musicVolume:.35})};
  const startAmbient=()=>{try{if(!ambient)ambient=new window.LLCAmbient();updateAmbient();ambient.start().catch(()=>{})}catch(_){}};
  const renderSettings=()=>{const s=getSave();extras.innerHTML=`<section><h3>Audio</h3><label class="settingToggle"><span>Background music <small>Soft phrases that change by region</small></span><input type="checkbox" data-setting="musicOn" ${s.musicOn===false?'':'checked'}></label><label class="settingRange">Music level <input type="range" min="0" max="100" value="${Math.round((Number.isFinite(s.musicVolume)?s.musicVolume:.35)*100)}" data-setting="musicVolume"><output>${Math.round((Number.isFinite(s.musicVolume)?s.musicVolume:.35)*100)}%</output></label><label class="settingToggle"><span>Sound effects <small>Moves, deliveries and results</small></span><input type="checkbox" data-setting="soundOn" ${s.soundOn===false?'':'checked'}></label><label class="settingRange">Effects level <input type="range" min="0" max="100" value="${Math.round((Number.isFinite(s.effectVolume)?s.effectVolume:1)*100)}" data-setting="effectVolume"><output>${Math.round((Number.isFinite(s.effectVolume)?s.effectVolume:1)*100)}%</output></label><label class="settingToggle"><span>Haptics <small>On supported phones</small></span><input type="checkbox" data-setting="hapticsOn" ${s.hapticsOn===false?'':'checked'}></label></section><section><h3>Comfort</h3><label class="settingToggle"><span>Reduce motion</span><input type="checkbox" data-setting="reduceMotion" ${s.reduceMotion?'checked':''}></label><label class="settingToggle"><span>Stronger move cues</span><input type="checkbox" data-setting="highContrast" ${s.highContrast?'checked':''}></label><button type="button" id="settingsHelp">Show level guide</button></section>`;};
  const applyComfort=()=>{const s=getSave();document.body.classList.toggle('reduceMotion',!!s.reduceMotion);document.body.classList.toggle('highContrast',!!s.highContrast)};
  extras.addEventListener('input',e=>{const input=e.target.closest('[data-setting]');if(!input)return;const key=input.dataset.setting,value=input.type==='range'?Number(input.value)/100:input.checked;window.__campaign.setPreference(key,value);input.closest('.settingRange')?.querySelector('output')?.replaceChildren(`${input.value}%`);applyComfort();if(key==='musicOn'||key==='musicVolume'){startAmbient();updateAmbient()}});
  extras.addEventListener('click',e=>{if(!e.target.closest('#settingsHelp'))return;settingsPanel.hidden=true;enterBoard();document.getElementById('help').click()});
  new MutationObserver(()=>{if(!settingsPanel.hidden)renderSettings()}).observe(settingsPanel,{attributes:true,attributeFilter:['hidden']});
  renderSettings();applyComfort();
  const mapScreen = document.getElementById('levelsScreen');
  const levelButtons = document.getElementById('levelButtons');
  const journey = document.createElement('div');
  journey.id = 'journeyMap';
  document.getElementById('chapters').after(journey);
  const stopPositions = [[22,12],[43,20],[76,28],[78,38],[49,46],[22,54],[25,63],[68,71],[76,80],[45,89]];
  let selectedStop = null;
  const renderJourney = () => {
    const chapterLevels = [...levelButtons.querySelectorAll('[data-level]')].map(b=>Number(b.dataset.level));
    if(chapterLevels.length!==10)return;
    const chapter = Math.ceil(chapterLevels[0]/10);
    const save=getSave();
    const current=window.__campaign.levels.find(l=>!save.cleared?.[l.n])?.n||2000;
    if(!chapterLevels.includes(selectedStop))selectedStop=chapterLevels.includes(current)?current:chapterLevels[0];
    const stops=chapterLevels.map((n,i)=>{const [x,y]=stopPositions[i],done=!!save.cleared?.[n],active=n===current,mastered=!!save.mastered?.[n];return `<button type="button" class="journeyStop ${done?'done':''} ${active?'current':''} ${n===selectedStop?'chosen':''}" data-stop="${n}" style="left:${x}%;top:${y}%" aria-label="Level ${n}, ${done?'completed':active?'next delivery':'unplayed'}"><span class="stopIcon">${done?'⌂':active?'✦':'◆'}</span><span class="stopNumber">${n}</span>${mastered?'<span class="stopStar" aria-label="Mastered">★</span>':''}</button>`}).join('');
    const level=window.__campaign.levels[selectedStop-1];
    journey.innerHTML=`<div class="journeyHead"><strong>Lantern Road</strong><span>Chapter ${chapter} · ${chapterLevels[0]}–${chapterLevels[9]}</span></div><div class="journeyScene"><div class="journeyStars" aria-hidden="true"></div><div class="journeyRiver" aria-hidden="true"></div><svg class="journeyRoute" viewBox="0 0 360 620" preserveAspectRatio="none" aria-hidden="true"><path d="M80 545 C50 510 85 476 155 495 S290 475 280 430 S170 396 90 330 S85 278 92 228 S260 217 275 160 S220 115 160 70"/></svg><span class="journeyLandmark house" aria-hidden="true">⌂</span><span class="journeyLandmark bridge" aria-hidden="true">⌒</span>${stops}</div><div class="journeyDetail"><small>${save.cleared?.[selectedStop]?'DELIVERED':selectedStop===current?'NEXT DELIVERY':'OPEN ROAD'}</small><strong>Level ${selectedStop} · ${level.brief}</strong><p>${level.grid||8} × ${level.grid||8} map · ${level.required} of ${level.homes.length} houses · ${level.cap} light</p><button type="button" data-play-stop="${selectedStop}">Play level ${selectedStop} →</button></div>`;
    journey.querySelector('.journeyScene').before(journey.querySelector('.journeyDetail'));
  };
  new MutationObserver(renderJourney).observe(levelButtons,{childList:true});
  renderJourney();
  journey.addEventListener('click', e=>{const stop=e.target.closest('[data-stop]');if(stop){selectedStop=Number(stop.dataset.stop);renderJourney();return}const play=e.target.closest('[data-play-stop]');if(play){levelButtons.querySelector(`[data-level="${play.dataset.playStop}"]`)?.click();setActive('play');}});
  const setActive = id => {nav.querySelectorAll('button').forEach(b => b.classList.toggle('active', b.dataset.destination === id));updateResources()};
  const powerShop=document.getElementById('powerShop'),powerShopHome=powerShop.parentElement;
  const restorePowerShop=()=>{if(powerShop.parentElement!==powerShopHome)powerShopHome.append(powerShop)};
  const close = () => { restorePowerShop();overlay.hidden = true; overlay.innerHTML = '';document.body.classList.remove('modalOpen'); };
  const panel = (title, body) => { restorePowerShop();overlay.hidden = false;document.body.classList.add('modalOpen');overlay.innerHTML = `<section class="integratedPanel" role="dialog" aria-modal="true" aria-label="${title}"><div class="head"><h2>${title}</h2><button class="close" type="button" aria-label="Close">×</button></div>${body}</section>`; };
  const legendButton=document.createElement('button');
  legendButton.type='button';legendButton.id='boardLegendButton';legendButton.setAttribute('aria-label','Map symbols');legendButton.textContent='?';
  document.getElementById('zoomMap').after(legendButton);
  document.querySelector('.boardZoom').prepend(document.getElementById('retry'));
  legendButton.addEventListener('click',()=>{const rows=[...document.querySelectorAll('#mapLegend .mapLegendRow')].map(row=>{const canvas=row.querySelector('canvas');return `<div class="symbolRow"><img src="${canvas.toDataURL()}" alt=""><div><strong>${row.querySelector('b')?.textContent||''}</strong><small>${row.querySelector('small')?.textContent||''}</small></div></div>`}).join('');panel('Help and map symbols',`<button type="button" class="guideButton" data-open-guide>How to play this level</button><p>Symbols used on this route. Tap a highlighted neighboring tile to move.</p><div class="symbolList">${rows}</div>`);overlay.querySelector('.integratedPanel').classList.add('legendPanel')});
  const repairCallout=document.createElement('section');
  repairCallout.id='repairCallout';
  const repairPopover=document.createElement('div');repairPopover.id='repairPopover';repairPopover.hidden=true;
  document.querySelector('.boardframe').append(repairPopover);
  const closeRepairTile=()=>{repairPopover.hidden=true;repairPopover.replaceChildren()};
  const showRepairTile=cell=>{const level=window.__campaign.getCurrentLevel(),r=level?.repair,s=getSave();if(!r||s.repairs?.[level.n])return;const p=[Number(cell.dataset.x),Number(cell.dataset.y)],cost=gems.repairPrice(r.cost),stock=s.powerStock?.road_repair||0,moveRequired=r.effect==='open',beside=Math.abs(p[0]-window.__campaign.getState().pos[0])+Math.abs(p[1]-window.__campaign.getState().pos[1])===1,canKit=stock>0&&(!moveRequired||window.__campaign.canRepairMove(p,'inventory')),canGems=s.gems>=cost&&(!moveRequired||window.__campaign.canRepairMove(p,'gems'));const frame=document.querySelector('.boardframe'),box=cell.getBoundingClientRect(),outer=frame.getBoundingClientRect();repairPopover.style.left=Math.max(4,Math.min(outer.width-202,box.left-outer.left+box.width/2-100))+'px';repairPopover.style.top=Math.max(4,box.top-outer.top-118)+'px';repairPopover.innerHTML=`<strong>${r.name}</strong><small>${moveRequired?'Clear this tile, then step onto it.':r.effect==='lamp'?'Restore this streetlamp.':r.effect==='beacon'?'Restore this beacon.':'Repair this marked tile.'}</small><div class="repairChoices"><button type="button" data-repair-apply="inventory" ${canKit?'':'disabled'} aria-label="Use one Road Repair charge">⚒ ×${stock}</button><button type="button" data-repair-apply="gems" ${canGems?'':'disabled'} aria-label="Spend ${cost} gems">${gemAmount(cost)}</button></div>${moveRequired&&!beside?'<small>Move beside the tile first</small>':''}<button type="button" data-repair-tile-cancel aria-label="Close repair choices">×</button>`;repairPopover.dataset.x=p[0];repairPopover.dataset.y=p[1];repairPopover.hidden=false};
  repairPopover.addEventListener('click',e=>{e.stopPropagation();if(e.target.closest('[data-repair-tile-cancel]')){closeRepairTile();return}const button=e.target.closest('[data-repair-apply]');if(!button)return;const payment=button.dataset.repairApply,p=[Number(repairPopover.dataset.x),Number(repairPopover.dataset.y)],r=window.__campaign.getCurrentLevel()?.repair,cell=document.querySelector(`#board .cell[data-x="${p[0]}"][data-y="${p[1]}"]`);closeRepairTile();if(r?.effect==='open')window.__campaign.repairAndMove(p,payment);else window.__campaign.buyRepairConfirmed(cell,payment);renderRepairCallout()});
  document.getElementById('zoomMap').closest('.boardZoom').before(repairCallout);
  const boardMessage=document.createElement('section');
  boardMessage.id='boardMessage';boardMessage.setAttribute('role','status');boardMessage.setAttribute('aria-live','polite');
  boardMessage.innerHTML='<strong></strong><span></span>';
  document.getElementById('zoomMap').closest('.boardZoom').before(boardMessage);
  const showBoardMessage=(title,body)=>{boardMessage.querySelector('strong').textContent=title||'Route update';boardMessage.querySelector('span').textContent=body||'';boardMessage.classList.remove('expanded')};
  const copyStatus=()=>showBoardMessage(document.getElementById('statusTitle').textContent,document.getElementById('statusText').textContent);
  new MutationObserver(copyStatus).observe(document.querySelector('.side .status'),{subtree:true,childList:true,characterData:true});
  boardMessage.addEventListener('click',()=>boardMessage.classList.toggle('expanded'));
  copyStatus();
  const inspectTile=cell=>{const tag=[...cell.querySelectorAll('.timer,.done')].map(el=>el.textContent.trim()).filter(Boolean).join(' · ');showBoardMessage(cell.getAttribute('aria-label')?.split(': ').at(-1)||'Map tile',tag||'Tap a green neighboring tile to move.');boardMessage.classList.add('expanded')};
  const renderRepairCallout=()=>{const level=window.__campaign.getCurrentLevel(),r=level?.repair,s=getSave();if(!r||r.effect==='open'||s.repairs?.[level.n]){repairCallout.hidden=true;return}repairCallout.hidden=false;repairCallout.innerHTML=`<div class="repairMark" aria-hidden="true">⚒</div><div class="repairInfo"><strong>${r.name}</strong></div><button type="button" data-repair-open>Show tile</button>`};
  new MutationObserver(renderRepairCallout).observe(document.getElementById('repairBody'),{childList:true,subtree:true});
  repairCallout.addEventListener('click',e=>{if(e.target.closest('[data-repair-open]'))confirmRepair()});
  const confirmRepair=()=>{const r=window.__campaign.getCurrentLevel()?.repair;if(!r)return;const cell=document.querySelector(`#board .cell[data-x="${r.tile[0]}"][data-y="${r.tile[1]}"]`);if(cell)showRepairTile(cell)};
  renderRepairCallout();
  const handledResults=new WeakSet();
  new MutationObserver(()=>{const result=document.querySelector('#board .boardOverlay .routeResults');if(!result||handledResults.has(result))return;const state=window.__campaign.getState(),level=window.__campaign.getCurrentLevel();if(!state.done)return;handledResults.add(result);const allHomes=state.mask===(1<<level.homes.length)-1,save=getSave();window.LLCPlayerData.record({levelId:level.n,steps:state.turns,mask:state.mask,wallet:save.wallet,earned:state.earned,allHomes,repairActive:!!save.repairs?.[level.n],powerUsed:!!state.powerUsed});if(allHomes){const personal=window.LLCPlayerData.bestFor(level.n);if(personal)result.children[1].querySelector('strong').textContent=personal.steps}const best=result.querySelector('[data-global-best]'),note=result.parentElement.querySelectorAll('.routeNote')[1];if(!allHomes){if(note)note.textContent='All-player best is for lighting every house and returning to the depot.';return}window.LLCPlayerData.globalBest(level.n).then(record=>{if(!result.isConnected)return;if(record.status==='ready'){best.textContent=record.steps.toLocaleString();if(note)note.textContent='Best full-delivery route by '+record.playerName+'.'}else if(note)note.textContent='All-player best is unavailable until shared results are connected.'})}).observe(document.getElementById('board'),{childList:true});
  const openTrophies = () => {
    const profile=window.LLCPlayerData.profile(),s = getSave(), clear = Object.keys(s.cleared || {}).filter(n => s.cleared[n] && +n <= 2000).length;
    const mastery = Object.keys(s.mastered || {}).filter(n => s.mastered[n] && +n <= 2000).length;
    trophiesScreen.innerHTML=`<h2>Trophy Cabinet</h2><p>${profile.displayName} · results saved on this device. A linked player account is planned for shared records.</p><div class="stats"><div class="stat"><label>Levels cleared</label><strong>${clear} / 2000</strong></div><div class="stat"><label>Mastered</label><strong>${mastery}</strong></div></div><div class="badge"><strong>First Delivery</strong><p>${clear >= 1 ? 'Earned' : 'Clear your first level'}</p></div><div class="badge"><strong>Ten Roads</strong><p>${clear >= 10 ? 'Earned' : `${10 - clear} unique clears to go`}</p></div><div class="badge"><strong>Chapter Lantern</strong><p>${Math.floor(clear / 10)} sets of ten clears recorded. A chapter-specific trophy rule needs review.</p></div><p class="note">Trophy rewards and shared leaderboards are not active in this offline build.</p>`;
    document.body.dataset.screen='trophies';setActive('trophies');side.scrollTop=0;
  };
  const openShop = () => {
    close();
    const s = getSave();
    const maxExchange=Math.floor(s.wallet/gems.exchangePoints);
    exchangeQty=maxExchange?Math.max(1,Math.min(exchangeQty,maxExchange)):0;
    const exchangeMarkup=`<div class="shopExchange" aria-label="Exchange earned points for gems"><div class="exchangeAmounts"><strong class="pointAmount" data-exchange-points>${pointAmount(exchangeQty*gems.exchangePoints)}</strong><span aria-hidden="true">➜</span><strong class="gemAmount" data-exchange-total>${gemAmount(exchangeQty*gems.exchangeGems)}</strong></div><div class="exchangeControls"><button type="button" data-exchange-minus aria-label="Exchange one fewer batch" ${exchangeQty<=1?'disabled':''}>−</button><output data-exchange-qty aria-label="Exchange batches">${exchangeQty}</output><button type="button" data-exchange-plus aria-label="Exchange one more batch" ${exchangeQty>=maxExchange?'disabled':''}>+</button><button type="button" class="exchangeCommit" data-exchange-submit ${!exchangeQty?'disabled':''}>Exchange</button></div></div>`;
    shopScreen.innerHTML=`<h2>Night Market</h2><div class="shopWallet"><strong class="gemAmount" aria-label="${s.gems} gems">${gemAmount(s.gems)}</strong><span class="shopPoints" aria-label="${s.wallet} earned points">${pointAmount(s.wallet)}</span></div>${exchangeMarkup}<h3>✦ Powers</h3><div id="marketPowerSlot"></div><h3>${gems.icon} Gems</h3><div class="gemPacks">${gems.packs.map((pack,i)=>`<button type="button" class="gemPack gemPack${i}" data-gem-pack="${pack.id}" aria-label="Preview ${pack.amount} gems for ${pack.usd}"><span class="packArt" aria-hidden="true">${gems.icon.repeat(i+1)}</span><strong>${pack.amount.toLocaleString()}</strong><b>${pack.usd}</b></button>`).join('')}</div><p class="shopNote">Preview prices · Checkout unavailable</p>`;
    shopScreen.querySelector('#marketPowerSlot').append(powerShop);
    powerShop.querySelector('details').open=true;
    document.body.dataset.screen='shop';setActive('shop');
  };
  window.addEventListener('llc:gem-balance-change',()=>{if(document.body.dataset.screen==='shop')openShop()});
  const updateExchange=()=>{
    const max=Math.floor(getSave().wallet/gems.exchangePoints);
    exchangeQty=max?Math.max(1,Math.min(exchangeQty,max)):0;
    shopScreen.querySelector('[data-exchange-points]').innerHTML=pointAmount(exchangeQty*gems.exchangePoints);
    shopScreen.querySelector('[data-exchange-total]').innerHTML=gemAmount(exchangeQty*gems.exchangeGems);
    shopScreen.querySelector('[data-exchange-qty]').textContent=exchangeQty;
    shopScreen.querySelector('[data-exchange-minus]').disabled=exchangeQty<=1;
    shopScreen.querySelector('[data-exchange-plus]').disabled=exchangeQty>=max;
    shopScreen.querySelector('[data-exchange-submit]').disabled=!exchangeQty;
  };
  shopScreen.addEventListener('click',e=>{
    if(e.target.closest('[data-exchange-minus]')){exchangeQty--;updateExchange();return}
    if(e.target.closest('[data-exchange-plus]')){exchangeQty++;updateExchange();return}
    if(e.target.closest('[data-exchange-submit]')){if(!window.__campaign.exchangePointsForGems(exchangeQty))return;exchangeQty=1;openShop();return}
    if(e.target.closest('[data-gem-pack]')){const note=shopScreen.querySelector('.shopNote');note.textContent='Checkout unavailable in this browser build';note.scrollIntoView({block:'nearest',behavior:'smooth'})}
  });
  const openCourier = () => {
    courierScreen.innerHTML=`<h2>Choose Courier</h2><div class="appearanceStage"><div class="appearanceHero">${outfit()}</div><div class="appearanceSelected"><strong>${baseNames[selectedCourier]}</strong><span>${looks[selectedLook]}</span></div></div><h3>Courier <small>${selectedCourier+1} / 18</small></h3><div class="appearanceGrid courierGrid">${baseNames.map((name,i) => `<button type="button" data-courier="${i}" class="${i===selectedCourier?'selected':''}" aria-label="Choose ${name}" title="${name}"><img src="${image(i)}" alt=""><span>${name.split(' ')[0]}</span></button>`).join('')}</div><h3>Wardrobe <small>${looks[selectedLook]}</small></h3><div class="appearanceGrid lookGrid">${looks.map((name,i) => `<button type="button" data-look="${i}" class="${i===selectedLook?'selected':''}" aria-label="Choose ${name}" title="${name}"><span class="lookSwatch look${i}">✦</span><span>${name}</span></button>`).join('')}</div><p class="appearanceNote">Courier and outfit selections save on this device. Shadows follow the map region.</p>`;
    document.body.dataset.screen='courier';setActive('courier');side.scrollTop=0;drawOutfitCanvas();
  };
  courierScreen.addEventListener('click',e=>{const b=e.target.closest('[data-courier]');if(b){selectedCourier=Number(b.dataset.courier);saveAppearance();openCourier();return}const look=e.target.closest('[data-look]');if(look){selectedLook=Number(look.dataset.look);saveAppearance();openCourier()}});
  const navigate = id => {
    setActive(id); close();
    if (id === 'map') { legacyNav.querySelector('[data-screen="levels"]').click(); renderJourney(); }
    else if (id === 'shop') openShop();
    else if (id === 'play') { legacyNav.querySelector('[data-screen="play"]').click(); showHome(); }
    else if (id === 'courier') openCourier();
    else if (id === 'trophies') openTrophies();
  };
  nav.addEventListener('click', e => {
    const button = e.target.closest('[data-destination]');
    if (!button) return;
    navigate(button.dataset.destination);
  });
  overlay.addEventListener('click', e => {
    if (e.target === overlay || e.target.closest('.close')) { close(); return; }
    if(e.target.closest('[data-open-guide]')){close();enterBoard();document.getElementById('help').click();return}
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !overlay.hidden) close(); });
  try{if(!localStorage.getItem('llc-storybook-view-v1')){window.__campaign.setView('overhead');localStorage.setItem('llc-storybook-view-v1','1')}}catch(_){}
  showHome();
  playScreen.classList.toggle('largeBoard',(window.__campaign.getCurrentLevel()?.grid||8)>=12);
  getImage(courierAsset()); getImage(shadowImage(selectedShadow));
  window.__integratedShell = { openTrophies, openCourier, openShop, navigate, close, enterBoard, showHome, onLevelChosen, confirmRepair, showRepairTile, inspectTile, currentShadow:()=>selectedShadow };
})();
