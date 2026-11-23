/* HD Events: continuous luminous strands. No images or video used for motion. */
(()=>{
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const ribbons=[...document.querySelectorAll('[data-ribbon]')].map((el,index)=>({el,index,canvas:el.querySelector('canvas'),ctx:el.querySelector('canvas').getContext('2d'),visible:false,w:0,h:0,dirty:true}));
 let clock=0,last=0,lastPaint=0,scrollPhase=0,targetScroll=scrollY,previousScroll=scrollY,velocity=0;
 const rand=n=>{const q=Math.sin(n*127.1+311.7)*43758.5453;return q-Math.floor(q)};
 const colors=['#05dff8','#00ffff','#4089ff','#7d44ff','#bd47ff','#5f69ff','#02f4ff'];
 function resize(r){const rect=r.el.getBoundingClientRect();r.w=rect.width;r.h=rect.height;const d=Math.min(devicePixelRatio||1,1.5);r.canvas.width=Math.round(r.w*d);r.canvas.height=Math.round(r.h*d);r.ctx.setTransform(d,0,0,d,0,0);r.dirty=true;}
 const ro=new ResizeObserver(es=>{for(const e of es){const r=ribbons.find(r=>r.el===e.target);if(r)resize(r)}});
 const io=new IntersectionObserver(es=>{for(const e of es){const r=ribbons.find(r=>r.el===e.target);r.visible=e.isIntersecting;if(r.visible)r.dirty=true;}},{rootMargin:'100px'});
 ribbons.forEach(r=>{resize(r);ro.observe(r.el);io.observe(r.el)});
 addEventListener('scroll',()=>{targetScroll=scrollY},{passive:true});
 // Smooth non-repeating envelopes: quiet ripples, broad peaks and local twists.
 const noise=x=>{const i=Math.floor(x),f=x-i,t=f*f*(3-2*f);return rand(i)*(1-t)+rand(i+1)*t};
 function point(r,u,strand,phase){
  const closing=r.index===3,mobile=r.w<800;
  const base=closing?(mobile?.84:.76):.56;
  const scale=closing?r.h*.18:r.h*.30;
  const travel=phase*.19+r.index*8.3;
  const envelope=.16+.84*Math.pow(noise(u*3.1-travel*.36+12.4),1.25);
  // One travelling tall swell surrounded by smaller, independently evolving ripples.
  const peak=.59+.18*Math.sin(travel*.63+r.index);
  const swell=Math.exp(-Math.pow((u-peak)/.18,2));
  const amplitude=scale*(.20+envelope*.55+swell*.8);
  const angle=u*15.2-phase*.65+1.15*Math.sin(u*5.3+travel*.41)+.35*Math.sin(u*12.7-travel*.28);
  const width=Math.sin(angle)*amplitude;
  const spine=base*r.h-amplitude*.40+Math.sin(u*7.4-travel)*scale*.22;
  const twist=Math.sin(angle*1.03+.65)*strand*strand*amplitude*.12;
  return spine+Math.sin(angle+strand*.82)*amplitude+strand*amplitude*.25*Math.cos(angle*.61)+twist+Math.sin(u*23+phase*.22+strand*.4)*scale*.026;
 }
 function draw(r){
  const {ctx:g,w,h}=r;g.clearRect(0,0,w,h);
  const phase=clock*.42+scrollPhase*.0019+r.index*1.83;
  const gradient=g.createLinearGradient(0,0,w,0);colors.forEach((c,i)=>gradient.addColorStop(i/(colors.length-1),c));
  g.globalCompositeOperation='lighter';
  // Soft coloured light under the fine, distinct filaments.
  for(let j=0;j<3;j++){
   const u=.2+j*.31,y=point(r,u,0,phase),rad=Math.min(w*.25,h*.7);
   const glow=g.createRadialGradient(u*w,y,0,u*w,y,rad);glow.addColorStop(0,j===1?'#8640ff23':'#00ddff24');glow.addColorStop(1,'#00000000');g.fillStyle=glow;g.fillRect(u*w-rad,y-rad,rad*2,rad*2);
  }
  const steps=Math.ceil(w/6),lines=w<600?13:16;
  for(let pass=0;pass<2;pass++){
   g.strokeStyle=gradient;g.lineWidth=pass?1.15:5.5;g.globalAlpha=pass?.86:.045;
   for(let i=0;i<lines;i++){
    const strand=(i/(lines-1)-.5)*2;
    g.beginPath();for(let k=0;k<=steps;k++){const u=k/steps,x=u*(w+50)-25,y=point(r,u,strand,phase);if(k===0)g.moveTo(x,y);else g.lineTo(x,y)}g.stroke();
   }
  }
  // Birth positions follow the ribbon, then sparks detach and drift into darkness.
  const count=w<600?1500:2800;
  for(let i=0;i<count;i++){
   const seed=i+r.index*4000,life=2.5+rand(seed+2)*4;
   const age=(clock+rand(seed+7)*life)%life;
   const cycle=Math.floor((clock+rand(seed+7)*life)/life);
   const birth=rand(seed+cycle*.71)*1.12-.06;
   const edge=rand(seed+13)>.5?1:-1;
   const strand=i%3===0?(rand(seed+17)-.5)*2:edge*(.8+rand(seed+19)*.3);
   const u=birth+age*(.006+rand(seed+23)*.018);
   const emitPhase=phase-age*.42;
   const origin=point(r,birth,strand,emitPhase);
   const speed=(rand(seed+29)-.62)*(r.index===3?30:22);
   const y=origin+speed*age+Math.sin(age*1.4+seed)*age*2;
   const x=u*w;
   const fade=Math.sin(Math.PI*age/life)*Math.pow(1-age/life,.7);
   g.globalAlpha=fade*(.35+rand(seed+43)*.65);
   g.fillStyle=colors[Math.max(0,Math.min(colors.length-1,Math.floor(birth*(colors.length-1))))];
   const size=rand(seed+67)>.994?2:.35+rand(seed+71)*.85;
   g.beginPath();g.arc(x,y,size,0,Math.PI*2);g.fill();
   if(size>1.8){g.globalAlpha*=.13;g.beginPath();g.arc(x,y,5,0,Math.PI*2);g.fill()}
  }
  g.globalAlpha=1;g.globalCompositeOperation='source-over';r.dirty=false;
 }
 function frame(now){
  const dt=Math.min(.05,(now-(last||now))/1000);last=now;
  const stopped=reduced.matches||document.body.classList.contains('paused');
  if(!document.hidden){
   if(!stopped){clock+=dt*2.8;const delta=targetScroll-previousScroll;previousScroll=targetScroll;velocity+=(delta-velocity)*.15;scrollPhase+=(targetScroll-scrollPhase)*Math.min(1,dt*7);clock+=Math.min(Math.abs(velocity)*.0003,.015);}
   if(now-lastPaint>32){for(const r of ribbons)if(r.visible&&(!stopped||r.dirty))draw(r);lastPaint=now;}
  }
  requestAnimationFrame(frame);
 }
 reduced.addEventListener('change',()=>ribbons.forEach(r=>r.dirty=true));
 requestAnimationFrame(frame);
})();
