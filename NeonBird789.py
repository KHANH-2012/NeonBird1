
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NEON BIRD",
    page_icon="🐤",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #172554, #050816 75%);
    color: white;
}
header, footer, #MainMenu {visibility: hidden;}
.block-container {max-width: 1000px; padding-top: 1rem;}
h1 {
    text-align: center;
    font-size: 52px !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg,#22d3ee,#a78bfa,#f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🐤 NEON BIRD")
st.markdown("<p style='text-align:center;color:#94a3b8'>FLAP • SURVIVE • DOMINATE</p>",
            unsafe_allow_html=True)

modes = {
    "🟢 Dễ":          (205, 2.5, 0.25, -5.4, 112, "#4ade80"),
    "🔵 Bình thường": (170, 3.1, 0.30, -5.8, 100, "#38bdf8"),
    "🟠 Khó":         (143, 3.8, 0.34, -6.1, 91,  "#fb923c"),
    "🔴 Điên rồ":     (120, 4.6, 0.39, -6.5, 83,  "#fb7185"),
    "💀 Ác mộng":     (103, 5.3, 0.43, -6.9, 76,  "#c084fc"),
}

mode = st.selectbox("🎮 CHỌN CHẾ ĐỘ CHƠI", list(modes.keys()))
gap, speed, gravity, jump, spawn, color = modes[mode]

st.markdown(
    f"<p style='text-align:center;color:{color};font-weight:bold'>"
    f"{mode} · SPEED {speed} · PIPE GAP {gap}</p>",
    unsafe_allow_html=True
)

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
body{margin:0;background:#070d20;color:white;font-family:Arial}
.wrap{max-width:520px;margin:auto}
.hud{display:flex;justify-content:space-between;padding:14px 20px;
background:#111c35;border:1px solid #293858;border-radius:14px;
margin-bottom:10px}
.label{font-size:11px;color:#94a3b8;letter-spacing:2px}
.num{font-size:28px;font-weight:900;color:#67e8f9}
.frame{position:relative;border:1px solid #475569;border-radius:16px;
overflow:hidden;box-shadow:0 0 35px #22d3ee22}
canvas{width:100%;height:auto;display:block;touch-action:manipulation}
.overlay{position:absolute;inset:0;display:flex;flex-direction:column;
align-items:center;justify-content:center;text-align:center;
background:#071025aa;padding:20px}
.overlay.hide{display:none}
h2{font-size:36px;text-shadow:0 0 20px #22d3ee;margin:0 0 12px}
p{font-size:13px;line-height:1.8;color:#cbd5e1}
button{padding:14px 28px;border:0;border-radius:12px;
font-weight:900;letter-spacing:2px;background:linear-gradient(90deg,#67e8f9,#c4b5fd);
cursor:pointer;color:#0f172a;font-size:14px}
.hint{text-align:center;color:#94a3b8;font-size:12px;line-height:2;padding:12px}
</style>
</head>
<body>
<div class="wrap">
  <div class="hud">
    <div><div class="label">SCORE</div><div id="score" class="num">0</div></div>
    <div style="text-align:right"><div class="label">BEST</div>
      <div id="best" class="num">0</div></div>
  </div>
  <div class="frame">
    <canvas id="c" width="480" height="640"></canvas>
    <div id="ov" class="overlay">
      <h2 id="title">NEON BIRD</h2>
      <p id="msg">Bay qua những đường ống neon!<br>
      Nhấn SPACE hoặc chạm màn hình để bay.</p>
      <button id="btn">▶ BẮT ĐẦU</button>
    </div>
  </div>
  <div class="hint">SPACE / ↑ / CLICK / TAP để bay<br>Tránh ống · Tránh trần và mặt đất</div>
</div>

<script>
const W=480,H=640;
const GAP=__GAP__, SPEED=__SPEED__, GRAV=__GRAV__,
JUMP=__JUMP__, SPAWN=__SPAWN__, COLOR="__COLOR__";
const c=document.getElementById("c"),x=c.getContext("2d");
const ov=document.getElementById("ov"),btn=document.getElementById("btn");
const scoreEl=document.getElementById("score"),bestEl=document.getElementById("best");
const title=document.getElementById("title"),msg=document.getElementById("msg");

let bird,pipes,particles,score,best=0,tick=0,running=false,dead=false;
let stars=Array.from({length:65},()=>({
 x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.6+.3
}));

function reset(){
 bird={x:115,y:280,vy:0,r:14};
 pipes=[];particles=[];score=0;tick=0;
 scoreEl.textContent=0;running=true;dead=false;
 ov.classList.add("hide");
}
function burst(px,py,n=8){
 for(let i=0;i<n;i++){
  particles.push({x:px,y:py,vx:(Math.random()-.5)*5,
   vy:(Math.random()-.5)*5,life:25});
 }
}
function flap(){
 if(!running){if(dead||!bird){reset()}else{reset()}}
 bird.vy=JUMP;burst(bird.x,bird.y,5);
}
function gameOver(){
 if(!running)return;
 running=false;dead=true;burst(bird.x,bird.y,30);
 title.textContent="GAME OVER";
 msg.innerHTML="Điểm của bạn: <b style='color:#67e8f9;font-size:25px'>"+score+
 "</b><br>Hãy thử lại để lập kỷ lục mới!";
 btn.textContent="↻ CHƠI LẠI";ov.classList.remove("hide");
}
function pipe(){
 let margin=65;
 let top=margin+Math.random()*(H-2*margin-GAP-50);
 pipes.push({x:W+10,top,bottom:top+GAP,passed:false});
}
function background(){
 let g=x.createLinearGradient(0,0,0,H);
 g.addColorStop(0,"#111d42");g.addColorStop(1,"#40204f");
 x.fillStyle=g;x.fillRect(0,0,W,H);
 for(const s of stars){
  x.fillStyle="#dbeafe";x.globalAlpha=.3+.5*Math.abs(Math.sin(tick*.02+s.x));
  x.beginPath();x.arc(s.x,s.y,s.r,0,7);x.fill();
 }
 x.globalAlpha=1;
 x.fillStyle="#20264c";
 for(let i=0;i<14;i++){
  let xx=i*42-(tick*.3)%42;
  let h=50+(i*37%100);x.fillRect(xx,H-h-20,32,h+20);
 }
 x.fillStyle="#101329";x.fillRect(0,H-20,W,20);
 x.fillStyle=COLOR;x.fillRect(0,H-20,W,2);
}
function drawPipe(p){
 let g=x.createLinearGradient(p.x,0,p.x+58,0);
 g.addColorStop(0,"#063047");g.addColorStop(.4,COLOR);
 g.addColorStop(.6,"#d1fae5");g.addColorStop(1,"#063047");
 x.shadowColor=COLOR;x.shadowBlur=14;x.fillStyle=g;
 x.fillRect(p.x,0,54,p.top-12);
 x.fillRect(p.x-5,p.top-12,64,18);
 x.fillRect(p.x,p.bottom+12,54,H-p.bottom-32);
 x.fillRect(p.x-5,p.bottom-6,64,18);
 x.shadowBlur=0;
}
function drawBird(){
 x.save();x.translate(bird.x,bird.y);
 x.rotate(Math.max(-.5,Math.min(.8,bird.vy*.07)));
 x.shadowColor=COLOR;x.shadowBlur=18;
 let g=x.createLinearGradient(-15,-15,15,15);
 g.addColorStop(0,"#fef08a");g.addColorStop(1,"#f97316");
 x.fillStyle=g;x.beginPath();x.ellipse(0,0,17,14,0,0,7);x.fill();
 x.shadowBlur=0;
 x.fillStyle="#fb923c";x.beginPath();
 x.ellipse(-7,4+Math.sin(tick*.25)*3,9,6,-.4,0,7);x.fill();
 x.fillStyle="white";x.beginPath();x.arc(8,-5,5,0,7);x.fill();
 x.fillStyle="#111827";x.beginPath();x.arc(10,-5,2.5,0,7);x.fill();
 x.fillStyle="#fb7185";x.beginPath();
 x.moveTo(13,0);x.lineTo(24,4);x.lineTo(13,7);x.fill();
 x.restore();
}
function update(){
 tick++;
 if(!running)return;
 bird.vy+=GRAV;bird.y+=bird.vy;
 if(tick%SPAWN===0)pipe();
 for(const p of pipes){
  p.x-=SPEED;
  if(!p.passed&&p.x+55<bird.x){
   p.passed=true;score++;scoreEl.textContent=score;
   best=Math.max(best,score);bestEl.textContent=best;burst(bird.x,bird.y,10);
  }
  if(bird.x+11>p.x-5&&bird.x-11<p.x+59&&
    (bird.y-10<p.top||bird.y+10>p.bottom))gameOver();
 }
 pipes=pipes.filter(p=>p.x>-80);
 if(bird.y<0||bird.y+14>H-20)gameOver();
 for(const p of particles){
  p.x+=p.vx;p.y+=p.vy;p.life--;p.vy+=.04;
 }
 particles=particles.filter(p=>p.life>0);
}
function draw(){
 background();
 for(const p of pipes)drawPipe(p);
 if(bird)drawBird();
 for(const p of particles){
  x.globalAlpha=Math.max(0,p.life/25);x.fillStyle=COLOR;
  x.beginPath();x.arc(p.x,p.y,3,0,7);x.fill();
 }
 x.globalAlpha=1;
}
function loop(){update();draw();requestAnimationFrame(loop)}
btn.addEventListener("click",()=>{reset();bird.vy=JUMP;});
c.addEventListener("pointerdown",e=>{e.preventDefault();flap()});
window.addEventListener("keydown",e=>{
 if(["Space","ArrowUp","KeyW"].includes(e.code)){
  e.preventDefault();if(!e.repeat)flap();
 }
});
bird={x:115,y:280,vy:0,r:14};pipes=[];particles=[];
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

game = (game
    .replace("__GAP__", str(gap))
    .replace("__SPEED__", str(speed))
    .replace("__GRAV__", str(gravity))
    .replace("__JUMP__", str(jump))
    .replace("__SPAWN__", str(spawn))
    .replace("__COLOR__", color)
)

components.html(game, height=830, scrolling=False)

st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:12px'>"
    "NEON BIRD ARCADE · PYTHON + STREAMLIT + CANVAS</p>",
    unsafe_allow_html=True
)

/* ===== NEON BIRD AUDIO SYSTEM ===== */
let audioCtx = null;
let musicEnabled = true;
let sfxEnabled = true;
let musicTimer = null;
let musicStep = 0;

function initAudio() {
  if (!audioCtx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) audioCtx = new AC();
  }
  if (audioCtx && audioCtx.state === "suspended") {
    audioCtx.resume();
  }
}

function tone(freq, duration=0.12, type="sine", volume=0.08, delay=0) {
  if (!audioCtx || !sfxEnabled) return;

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  const start = audioCtx.currentTime + delay;

  osc.type = type;
  osc.frequency.setValueAtTime(freq, start);
  gain.gain.setValueAtTime(0.0001, start);
  gain.gain.exponentialRampToValueAtTime(volume, start + 0.015);
  gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);

  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(start);
  osc.stop(start + duration + 0.03);
}

// Sound when the bird flaps
function sfxFlap() {
  tone(520, 0.08, "triangle", 0.055);
  tone(760, 0.06, "sine", 0.025, 0.035);
}

// Sound when passing a pipe
function sfxScore() {
  tone(660, 0.10, "sine", 0.07);
  tone(880, 0.13, "sine", 0.06, 0.08);
  tone(1100, 0.16, "triangle", 0.045, 0.16);
}

// Game over sound
function sfxGameOver() {
  tone(300, 0.20, "sawtooth", 0.045);
  tone(220, 0.25, "sawtooth", 0.04, 0.18);
  tone(150, 0.42, "triangle", 0.05, 0.40);
}

// Original synthesized arcade background music.
// No external audio file or copyrighted game soundtrack is used.
const melody = [
  523,659,784,659,523,392,440,523,
  659,784,880,784,659,523,440,392,
  523,659,784,988,880,784,659,523,
  440,523,659,523,392,440,523,0
];

function musicTick() {
  if (!audioCtx || !musicEnabled) return;

  const t = audioCtx.currentTime;
  const note = melody[musicStep % melody.length];

  if (note > 0) {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = "triangle";
    osc.frequency.setValueAtTime(note, t);
    gain.gain.setValueAtTime(0.0001, t);
    gain.gain.linearRampToValueAtTime(0.022, t + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.19);

    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(t);
    osc.stop(t + 0.21);
  }

  // Soft synthesized bass beat
  if (musicStep % 4 === 0) {
    const bass = audioCtx.createOscillator();
    const bg = audioCtx.createGain();

    bass.type = "sine";
    bass.frequency.setValueAtTime(
      musicStep % 8 === 0 ? 110 : 82.4, t
    );
    bg.gain.setValueAtTime(0.035, t);
    bg.gain.exponentialRampToValueAtTime(0.0001, t + 0.15);

    bass.connect(bg);
    bg.connect(audioCtx.destination);
    bass.start(t);
    bass.stop(t + 0.16);
  }

  musicStep++;
}

function startMusic() {
  if (!audioCtx || !musicEnabled || musicTimer) return;
  musicTimer = setInterval(musicTick, 220);
}

function stopMusic() {
  if (musicTimer) clearInterval(musicTimer);
  musicTimer = null;
}

document.getElementById("musicBtn").addEventListener("click", () => {
  initAudio();
  musicEnabled = !musicEnabled;

  document.getElementById("musicBtn").textContent =
    musicEnabled ? "🎵 NHẠC: ON" : "🔇 NHẠC: OFF";

  if (musicEnabled) startMusic();
  else stopMusic();
});

document.getElementById("soundBtn").addEventListener("click", () => {
  sfxEnabled = !sfxEnabled;

  document.getElementById("soundBtn").textContent =
    sfxEnabled ? "🔊 SFX: ON" : "🔇 SFX: OFF";
});
