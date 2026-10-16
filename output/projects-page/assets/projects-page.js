/* Observe native Loop Grid output; never replace its query, filter or project links. */
(()=>{
  if(window.__syncsProjectsPageV1){window.__syncsProjectsPageV1.scan();return;}
  const states=new WeakMap();
  window.__syncsProjectsPageV1={scan};
  const mobile=()=>matchMedia('(max-width:600px)').matches;
  const reduced=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
  function mount(root){
    if(states.has(root))return;
    const state={track:null,items:[],active:null,frame:0,scrollFrame:0};
    states.set(root,state);
    function announce(){
      const controls=root.querySelector('.sx-live-controls');
      if(!controls)return;
      controls.hidden=state.items.length===0;
      const status=controls.querySelector('[role=status]');
      const text=state.items.length?`${state.items.indexOf(state.active)+1} / ${state.items.length}`:'0 / 0';
      if(status&&status.textContent!==text)status.textContent=text;
      controls.querySelectorAll('button').forEach(button=>button.disabled=state.items.length<2);
    }
    function select(item,scroll=false){
      if(!item||!state.items.includes(item))return;
      state.active=item;
      state.items.forEach(card=>{
        const selected=card===item;
        if(card.classList.contains('sx-is-active')!==selected)card.classList.toggle('sx-is-active',selected);
      });
      announce();
      if(scroll&&state.track){
        const rect=item.getBoundingClientRect(),trackRect=state.track.getBoundingClientRect();
        state.track.scrollBy({left:rect.left-trackRect.left-(state.track.clientWidth-rect.width)/2,behavior:reduced()?'instant':'smooth'});
      }
    }
    function sync(){
      const track=root.querySelector('.sx-live-grid .elementor-loop-container');
      state.track=track;
      state.items=track?Array.from(track.children).filter(el=>el.matches('.e-loop-item')&&!el.hidden&&getComputedStyle(el).display!=='none'):[];
      if(track){
        const visibleSlots=Math.max(1,Math.min(4,state.items.length));
        track.style.setProperty('--sx-count',String(visibleSlots));
        track.style.setProperty('--sx-denom',String(visibleSlots+1.9));
        track.setAttribute('tabindex','0');
        track.setAttribute('role','region');
        track.setAttribute('aria-label','Projects. Use left and right arrow keys to browse.');
      }
      if(!state.items.includes(state.active))state.active=state.items[mobile()?0:Math.min(2,state.items.length-1)]||null;
      if(state.active)select(state.active);else announce();
    }
    function schedule(){cancelAnimationFrame(state.frame);state.frame=requestAnimationFrame(sync)}
    function step(delta){
      if(!state.items.length)return;
      select(state.items[(state.items.indexOf(state.active)+delta+state.items.length)%state.items.length],true);
    }
    root.addEventListener('click',event=>{
      const button=event.target.closest('.sx-live-prev,.sx-live-next');
      if(button&&button.closest('.sx-live-projects')===root)step(button.matches('.sx-live-next')?1:-1);
    });
    root.addEventListener('pointerover',event=>{
      if(mobile()||!matchMedia('(hover:hover)').matches)return;
      const item=event.target.closest('.e-loop-item');
      if(state.items.includes(item))select(item);
    });
    root.addEventListener('focusin',event=>{
      const item=event.target.closest('.e-loop-item');
      if(state.items.includes(item))select(item);
    });
    root.addEventListener('keydown',event=>{
      if(event.target!==state.track||!['ArrowRight','ArrowLeft'].includes(event.key))return;
      event.preventDefault();
      const rtl=getComputedStyle(state.track).direction==='rtl';
      step((event.key==='ArrowRight'?1:-1)*(rtl?-1:1));
    });
    root.addEventListener('scroll',event=>{
      if(!mobile()||event.target!==state.track)return;
      cancelAnimationFrame(state.scrollFrame);
      state.scrollFrame=requestAnimationFrame(()=>{
        if(!state.items.length)return;
        const rect=state.track.getBoundingClientRect(),center=rect.left+rect.width/2;
        const distance=item=>{const r=item.getBoundingClientRect();return Math.abs(r.left+r.width/2-center)};
        select(state.items.reduce((best,item)=>distance(item)<distance(best)?item:best));
      });
    },true);
    // Native taxonomy-filter AJAX may replace the track or its children. No filter event names are assumed.
    new MutationObserver(records=>{
      if(records.some(record=>record.type==='childList'))schedule();
    }).observe(root,{childList:true,subtree:true});
    sync();
  }
  function scan(){document.querySelectorAll('.sx-live-projects').forEach(mount)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
  if(window.jQuery)window.jQuery(window).on('elementor/frontend/init',()=>{
    if(window.elementorFrontend)window.elementorFrontend.hooks.addAction('frontend/element_ready/global',scan);
  });
})();
