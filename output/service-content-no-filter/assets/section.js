/* Presentation only: native Elementor still owns requests, queries, languages and caching. */
(()=>{
  if(window.__syncsServiceContentV1){window.__syncsServiceContentV1.scan();return;}
  const states=new WeakMap();
  window.__syncsServiceContentV1={version:2,scan};
  const mobile=()=>matchMedia('(max-width:600px)').matches;
  const reduced=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
  const messages={
    en:{region:'Related content. Use left and right arrow keys to browse.',browse:'Browse related content',previous:'Previous item',next:'Next item',loading:'Loading content…'},
    ar:{region:'المحتوى المرتبط بالخدمة. استخدم سهمي اليمين واليسار للتنقل.',browse:'تصفح المحتوى المرتبط بالخدمة',previous:'العنصر السابق',next:'العنصر التالي',loading:'جارٍ تحميل المحتوى…'}
  };
  const setAttr=(node,name,value)=>{if(node&&node.getAttribute(name)!==value)node.setAttribute(name,value)};
  const language=root=>{const section=root.closest('.sx-service-section');if(section?.classList.contains('sx-lang-ar'))return 'ar';if(section?.classList.contains('sx-lang-en'))return 'en';return (root.closest('[lang]')?.getAttribute('lang')||document.documentElement.lang||'en').toLowerCase().split('-')[0]==='ar'?'ar':'en';};
  function mount(root){
    if(states.has(root))return;
    const state={track:null,items:[],all:[],active:null,frame:0,scrollFrame:0,seen:false,busy:false};
    states.set(root,state);
    function announce(){
      const controls=root.querySelector('.sx-service-controls');
      if(!controls)return;
      const lang=language(root),labels=messages[lang],numbers=new Intl.NumberFormat(lang);
      controls.hidden=state.items.length===0;
      setAttr(controls,'aria-label',labels.browse);
      const prev=controls.querySelector('.sx-service-prev'),next=controls.querySelector('.sx-service-next');
      setAttr(prev,'aria-label',labels.previous);setAttr(next,'aria-label',labels.next);
      const rtl=state.track?getComputedStyle(state.track).direction==='rtl':getComputedStyle(root).direction==='rtl';
      for(const [button,arrow] of [[prev,rtl?'→':'←'],[next,rtl?'←':'→']]){
        if(button&&button.textContent!==arrow)button.textContent=arrow;
        if(button)button.disabled=state.items.length<2||state.busy;
      }
      const status=controls.querySelector('[role=status]');
      const text=state.busy?labels.loading:`${numbers.format(Math.max(0,state.items.indexOf(state.active)+1))} / ${numbers.format(state.items.length)}`;
      if(status){setAttr(status,'dir','ltr');if(status.textContent!==text)status.textContent=text;}
      if(state.track)setAttr(state.track,'aria-label',labels.region);
    }
    function select(item,scroll=false){
      if(!item||!state.items.includes(item))return;
      state.active=item;
      // Clear the old selection from hidden results as well as visible ones.
      state.all.forEach(card=>{
        const selected=card===item;
        if(card.classList.contains('sx-service-active')!==selected)card.classList.toggle('sx-service-active',selected);
      });
      announce();
      if(scroll&&state.track){
        const rect=item.getBoundingClientRect(),trackRect=state.track.getBoundingClientRect();
        state.track.scrollBy({left:rect.left-trackRect.left-(state.track.clientWidth-rect.width)/2,behavior:reduced()?'instant':'smooth'});
      }
    }
    function sync(){
      const oldTrack=state.track,oldItems=state.items;
      const grid=root.querySelector('.sx-service-grid');
      const track=grid?.querySelector('.elementor-loop-container')||null;
      state.track=track;
      state.all=track?Array.from(track.children).filter(el=>el.matches('.e-loop-item')):[];
      state.items=state.all.filter(el=>{
        const style=getComputedStyle(el);
        return !el.hidden&&style.display!=='none'&&style.visibility==='visible'&&el.getClientRects().length>0;
      });
      state.busy=Boolean(grid?.closest('[aria-busy="true"]')||track?.closest('[aria-busy="true"]'));
      const changed=oldTrack!==track||oldItems.length!==state.items.length||oldItems.some((item,i)=>item!==state.items[i]);
      const appendOnly=oldTrack===track&&state.items.length>oldItems.length&&oldItems.length>0&&oldItems.every((item,i)=>item===state.items[i]);
      if(track){
        const slots=Math.max(1,Math.min(4,state.items.length));
        for(const [key,value] of [['--sx-count',String(slots)],['--sx-denom',String(slots+1.9)]]){
          if(track.style.getPropertyValue(key)!==value)track.style.setProperty(key,value);
        }
        setAttr(track,'tabindex','0');setAttr(track,'role','region');
      }
      if(changed&&state.seen&&!appendOnly){
        state.active=state.items[0]||null;
        if(track)track.scrollTo({left:0,behavior:'instant'});
      }else if(!state.items.includes(state.active)){
        state.active=state.items[!state.seen&&!mobile()?Math.min(2,state.items.length-1):0]||null;
      }
      if(state.active)select(state.active);
      else{state.all.forEach(item=>item.classList.remove('sx-service-active'));announce();}
      state.seen=true;
    }
    function schedule(){cancelAnimationFrame(state.frame);state.frame=requestAnimationFrame(sync)}
    function step(delta){
      // Visibility can change in the same frame as a click, before the observer callback.
      sync();
      if(state.busy||!state.items.length)return;
      select(state.items[(state.items.indexOf(state.active)+delta+state.items.length)%state.items.length],true);
    }
    root.addEventListener('click',event=>{
      const button=event.target.closest('.sx-service-prev,.sx-service-next');
      if(button&&button.closest('.sx-service-content')===root)step(button.matches('.sx-service-next')?1:-1);
    });
    root.addEventListener('pointerover',event=>{
      if(mobile()||state.busy||!matchMedia('(hover:hover)').matches)return;
      const item=event.target.closest('.e-loop-item');
      if(state.items.includes(item))select(item);
    });
    root.addEventListener('focusin',event=>{
      const item=event.target.closest('.e-loop-item');
      if(!state.busy&&state.items.includes(item))select(item);
    });
    root.addEventListener('keydown',event=>{
      if(event.target!==state.track||!['ArrowRight','ArrowLeft'].includes(event.key))return;
      event.preventDefault();
      step((event.key==='ArrowRight'?1:-1)*(getComputedStyle(state.track).direction==='rtl'?-1:1));
    });
    root.addEventListener('scroll',event=>{
      if(!mobile()||state.busy||event.target!==state.track)return;
      const scrolledTrack=state.track;
      cancelAnimationFrame(state.scrollFrame);
      state.scrollFrame=requestAnimationFrame(()=>{
        if(scrolledTrack!==state.track||!state.items.length)return;
        const rect=state.track.getBoundingClientRect(),center=rect.left+rect.width/2;
        const distance=item=>{const r=item.getBoundingClientRect();return Math.abs(r.left+r.width/2-center)};
        select(state.items.reduce((best,item)=>distance(item)<distance(best)?item:best));
      });
    },true);
    const withoutSizing=value=>{const style=document.createElement('div').style;style.cssText=value||'';style.removeProperty('--sx-count');style.removeProperty('--sx-denom');return style.cssText;};
    const withoutSelection=value=>(value||'').split(/\s+/).filter(c=>c&&c!=='sx-service-active').sort().join(' ');
    new MutationObserver(records=>{
      const relevant=records.some(record=>{
        const target=record.target;
        if(record.type==='childList'){
          if(target.closest?.('.elementor-loop-container'))return true;
          return [...record.addedNodes,...record.removedNodes].some(node=>node.nodeType===1&&(node.matches('.sx-service-grid,.elementor-loop-container,.e-loop-item')||node.querySelector('.sx-service-grid,.elementor-loop-container,.e-loop-item')));
        }
        // Ignore our selection class and track width variables to avoid observer feedback.
        if(record.attributeName==='class'&&withoutSelection(record.oldValue)===withoutSelection(target.getAttribute('class')))return false;
        if(record.attributeName==='style'&&target===state.track&&withoutSizing(record.oldValue)===withoutSizing(target.getAttribute('style')))return false;
        return target.matches?.('.e-loop-item')&&target.parentElement===state.track||target===root||target.contains?.(state.track);
      });
      if(relevant)schedule();
    }).observe(root,{childList:true,subtree:true,attributes:true,attributeOldValue:true,attributeFilter:['hidden','style','class','aria-busy','lang','dir']});
    // Language plugins may change lang/dir on ancestors without replacing the grid.
    const ancestors=new MutationObserver(schedule);
    for(let node=root.parentElement;node;node=node.parentElement)ancestors.observe(node,{attributes:true,attributeFilter:['lang','dir','hidden','class','style','aria-busy']});
    window.addEventListener('resize',schedule,{passive:true});
    sync();
  }
  function scan(){document.querySelectorAll('.sx-service-section .sx-service-content').forEach(mount)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
  if(window.jQuery)window.jQuery(window).on('elementor/frontend/init',()=>{
    if(window.elementorFrontend)window.elementorFrontend.hooks.addAction('frontend/element_ready/global',scan);
  });
})();
