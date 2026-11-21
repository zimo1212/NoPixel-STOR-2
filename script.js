
const loader=document.querySelector('.loader');
window.addEventListener('load',()=>setTimeout(()=>loader?.classList.add('hide'),850));
const menu=document.querySelector('.menu'),links=document.querySelector('.navlinks');
menu?.addEventListener('click',()=>links.classList.toggle('open'));
const c=document.getElementById('particles');
if(c){const ctx=c.getContext('2d');let dots=[];function resize(){c.width=innerWidth*devicePixelRatio;c.height=innerHeight*devicePixelRatio;ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);dots=Array.from({length:75},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight,r:Math.random()*1.8+.4,s:Math.random()*.55+.15,a:Math.random()*.65+.15}))}function draw(){ctx.clearRect(0,0,innerWidth,innerHeight);for(const d of dots){d.y-=d.s;d.x+=Math.sin(d.y*.008)*.18;if(d.y< -5){d.y=innerHeight+5;d.x=Math.random()*innerWidth}ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);ctx.fillStyle=`rgba(229,174,75,${d.a})`;ctx.shadowBlur=8;ctx.shadowColor='#d9a441';ctx.fill()}requestAnimationFrame(draw)}addEventListener('resize',resize);resize();draw()}




// Elegant reveal animation repeats whenever elements re-enter the viewport.
(() => {
  const targets = document.querySelectorAll(
    'main > *, main section, .grid > *, .tile, .panel, .page-title, .payments-section'
  );
  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('is-visible'));
    return;
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('is-visible');
      else entry.target.classList.remove('is-visible');
    });
  }, { threshold: 0.10, rootMargin: '0px 0px -25px 0px' });
  targets.forEach((el, index) => {
    el.classList.add('reveal-on-scroll');
    el.style.transitionDelay = `${(index % 4) * 70}ms`;
    observer.observe(el);
  });
})();

// Discourage casual copying, text highlighting and image dragging.
document.addEventListener('contextmenu', event => {
  if (!event.target.closest('input, textarea, [contenteditable="true"]')) event.preventDefault();
});
document.addEventListener('copy', event => {
  if (!event.target.closest('input, textarea, [contenteditable="true"]')) event.preventDefault();
});
document.addEventListener('cut', event => {
  if (!event.target.closest('input, textarea, [contenteditable="true"]')) event.preventDefault();
});
document.addEventListener('dragstart', event => {
  if (event.target.matches('img, a')) event.preventDefault();
});
