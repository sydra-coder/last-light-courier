// Offline procedural sound and short, event-specific phone vibration cues.
const FEEDBACK=(()=>{
  let audio=null;
  const history=[];
  const vibrations={step:[10],shadowNear:[28,32,35],house:[24,24,45],repair:[35,28,65],denied:[55,35,55],complete:[30,40,30,40,75],failure:[75,45,100],crossing:[18,25,18]};
  function unlock(){
    if(save.soundOn===false)return null;
    try{audio??=new (window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();return audio}catch(_){return null}
  }
  function tone(frequency,duration,delay=0,type='sine',volume=.045,endFrequency=frequency){
    const context=unlock();if(!context)return;
    const start=context.currentTime+delay,osc=context.createOscillator(),gain=context.createGain();
    osc.type=type;osc.frequency.setValueAtTime(frequency,start);osc.frequency.exponentialRampToValueAtTime(Math.max(30,endFrequency),start+duration);
    gain.gain.setValueAtTime(.0001,start);gain.gain.exponentialRampToValueAtTime(Math.max(.0002,volume),start+.012);
    gain.gain.exponentialRampToValueAtTime(.0001,start+duration);osc.connect(gain);gain.connect(context.destination);
    osc.start(start);osc.stop(start+duration+.015);
  }
  function sound(kind){
    if(save.soundOn===false)return;
    if(kind==='step')tone(390,.085,0,'triangle',.018,270);
    else if(kind==='shadowNear'){tone(190,.28,0,'sawtooth',.034,95);tone(255,.21,.07,'sine',.018,150)}
    else if(kind==='house'){[523,659,784].forEach((f,i)=>tone(f,.28,i*.09,'sine',.045))}
    else if(kind==='repair'){[392,494,659,880].forEach((f,i)=>tone(f,.19,i*.07,'triangle',.04))}
    else if(kind==='denied')tone(230,.17,0,'square',.018,125);
    else if(kind==='complete'){[523,659,784,1046].forEach((f,i)=>tone(f,.35,i*.11,'sine',.05))}
    else if(kind==='failure'){tone(270,.35,0,'sawtooth',.03,95);tone(130,.3,.2,'sine',.025,70)}
    else if(kind==='crossing')tone(460,.12,0,'triangle',.027,210);
  }
  function haptic(kind){
    if(save.hapticsOn===false||!vibrations[kind])return;
    try{if(window.CourierAndroid?.haptic){window.CourierAndroid.haptic(kind);return}if(matchMedia('(pointer:coarse)').matches&&typeof navigator.vibrate==='function')navigator.vibrate(vibrations[kind])}catch(_){}
  }
  function emit(kind){history.push(kind);if(history.length>40)history.shift();sound(kind);haptic(kind)}
  function labels(){const s=$('menuSound'),h=$('menuHaptics');if(s)s.textContent='Sound: '+(save.soundOn===false?'Off':'On');if(h)h.textContent='Vibration: '+(save.hapticsOn===false?'Off':'On')}
  function toggleSound(){save.soundOn=save.soundOn===false;persist();labels();if(save.soundOn)tone(660,.1,0,'sine',.03)}
  function toggleHaptics(){save.hapticsOn=save.hapticsOn===false;persist();labels();if(save.hapticsOn)haptic('house')}
  return {emit,preview:sound,unlock,labels,toggleSound,toggleHaptics,history:()=>[...history]};
})();
