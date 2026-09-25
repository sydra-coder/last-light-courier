// One icon family for the menu, game controls, and result actions.
const UI_ICONS={
  continue:'<path d="M5 12h13m-5-5 5 5-5 5"/><path d="M4 5v14"/>',
  levelOne:'<path d="M6 21V3m0 1h12l-2.5 4L18 12H6"/><path d="M11 16h2m-1-1v5"/>',
  menu:'<path d="M3 11.5 12 4l9 7.5V21H3z"/><path d="M9 21v-7h6v7"/>',
  map:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  restart:'<path d="M4 11a8 8 0 1 1 2.3 6.6"/><path d="M4 4v7h7"/>',
  next:'<path d="M5 12h14m-6-6 6 6-6 6"/>',
  help:'<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 0 1 5 0c0 2-2.5 2-2.5 4"/><path d="M12 17h.01"/>',
  sound:'<path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16 9a4 4 0 0 1 0 6m2-9a8 8 0 0 1 0 12"/>',
  mute:'<path d="M4 9v6h4l5 4V5L8 9z"/><path d="m17 9 5 6m0-6-5 6"/>',
  vibration:'<rect x="8" y="3" width="8" height="18" rx="2"/><path d="M5 7 3 9v6l2 2m14-10 2 2v6l-2 2"/>',
  vibrationOff:'<rect x="8" y="3" width="8" height="18" rx="2"/><path d="M3 3 21 21"/>'
};
function iconSvg(name){return '<svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+UI_ICONS[name]+'</svg>'}
function setButtonIcon(button,name,label){button.classList.add('iconOnly');button.innerHTML=iconSvg(name);button.setAttribute('aria-label',label);button.title=label}
function setIcon(id,name,label){setButtonIcon($(id),name,label)}
function refreshSettingsIcons(){setIcon('menuSound',save.soundOn===false?'mute':'sound','Sound '+(save.soundOn===false?'off':'on'));setIcon('menuHaptics',save.hapticsOn===false?'vibrationOff':'vibration','Vibration '+(save.hapticsOn===false?'off':'on'))}
function setupNavigationIcons(){for(const [id,name,label] of [
  ['menuContinue','continue','Continue journey'],['menuLevelOne','levelOne','Play Level 1'],['menuChoose','map','Choose level'],['menuHow','help','How to play'],
  ['menu','menu','Main menu'],['retry','restart','Restart level'],['help','help','How to play'],['levels','map','Choose level']
])setIcon(id,name,label);refreshSettingsIcons()}
function enhanceOverlayIcons(){const actions={restart:['restart','Restart level'],next:['next','Next level'],menu:['menu','Main menu'],map:['map','Choose level'],start:['continue','Start level']};for(const button of document.querySelectorAll('#board .overlayActions button')){const action=actions[button.dataset.action];if(action)setButtonIcon(button,...action)}}
