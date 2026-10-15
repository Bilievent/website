(()=>{
function init(root){
 if(root.dataset.sxReady)return;
 const track=root.querySelector('.sx-track'), cards=Array.from(root.querySelectorAll('.sx-card')), status=root.querySelector('.sx-status');
 if(!track||!cards.length||!status)return;
 root.dataset.sxReady='1';let index=2;
 function select(next,scroll){index=(next+cards.length)%cards.length;cards.forEach((card,i)=>card.classList.toggle('sx-active',i===index));status.textContent=String(index+1).padStart(2,'0')+' / '+String(cards.length).padStart(2,'0');if(scroll&&matchMedia('(max-width:600px)').matches){track.scrollTo({left:cards[index].offsetLeft-track.offsetLeft,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});}}
 root.querySelector('.sx-prev').addEventListener('click',()=>select(index-1,true));root.querySelector('.sx-next').addEventListener('click',()=>select(index+1,true));
 cards.forEach((card,i)=>{card.addEventListener('mouseenter',()=>{if(matchMedia('(hover:hover)').matches)select(i,false)});card.addEventListener('focusin',()=>select(i,false));});
 track.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();select(index+(e.key==='ArrowRight'?1:-1),true)}});
 let frame;track.addEventListener('scroll',()=>{if(!matchMedia('(max-width:600px)').matches)return;cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{let nearest=0;cards.forEach((c,i)=>{if(Math.abs(c.offsetLeft-track.offsetLeft-track.scrollLeft)<Math.abs(cards[nearest].offsetLeft-track.offsetLeft-track.scrollLeft))nearest=i});select(nearest,false)})},{passive:true});
 track.setAttribute('tabindex','0');track.setAttribute('role','region');track.setAttribute('aria-label','Selected projects. Use left and right arrow keys to browse.');select(2,false);
 if(matchMedia('(max-width:600px)').matches)select(0,false);
}
function scan(){document.querySelectorAll('.syncs-projects').forEach(init)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
if(window.jQuery)window.jQuery(window).on('elementor/frontend/init',()=>{if(window.elementorFrontend)window.elementorFrontend.hooks.addAction('frontend/element_ready/global',scan)});
})();