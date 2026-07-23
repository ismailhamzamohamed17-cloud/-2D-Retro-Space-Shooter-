import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Tactical: Special Ops", layout="centered")
st.title("⚡ Virtua Tactical: Elite Operations")

game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        /* Photorealistic 3D Arcade Cinematic Frame Box Container */
        #gameArea { 
            position: relative; width: 380px; height: 480px; 
            background: linear-gradient(to bottom, #111a24 0%, #2a3a4a 40%, #1c232e 41%, #0b0f14 100%); 
            border: 4px solid #333; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none;
            box-shadow: 0 24px 50px rgba(0,0,0,0.85); perspective: 700px;
            transition: background 1s cubic-bezier(0.25, 1, 0.5, 1);
        }

        /* 🌆 VOLUMETRIC SCENERY LAYER MATRIX */
        #sceneryContainer { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 1; }
        
        /* Chapter 1: European City streets architecture with overhead wire meshes */
        .city-facade-l { position: absolute; top: 30px; left: 0; width: 125px; height: 170px; background: linear-gradient(135deg, #2b2b2b, #121212); border-right: 3px solid #000; box-shadow: inset -5px 0 15px rgba(0,0,0,0.5), 12px 0 25px rgba(0,0,0,0.6); }
        .city-facade-r { position: absolute; top: 20px; right: 0; width: 115px; height: 180px; background: linear-gradient(225deg, #242424, #0d0d0d); border-left: 3px solid #000; box-shadow: inset 5px 0 15px rgba(0,0,0,0.5), -12px 0 25px rgba(0,0,0,0.6); }
        .overhead-wires { position: absolute; top: 0; left: 0; width: 100%; height: 120px; background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(255,255,255,0.04) 40px, rgba(255,255,255,0.04) 42px); opacity: 0.7; }

        /* Chapter 3: Rain-Slicked Cargo Port Terminal elements */
        .port-crane { position: absolute; top: 10px; left: 15px; width: 85px; height: 140px; background: linear-gradient(to right, #1a222d, #0b0f14); border-radius: 4px; box-shadow: 8px 8px 20px rgba(0,0,0,0.5); }
        .cargo-vessel { position: absolute; top: 60px; right: -20px; width: 140px; height: 110px; background: linear-gradient(to bottom, #111a24, #05080c); border-radius: 50% 12px 12px 50%; box-shadow: -15px 15px 30px rgba(0,0,0,0.7); }
        .puddle-reflection { position: absolute; bottom: 15px; left: 25%; width: 90px; height: 25px; background: radial-gradient(ellipse at center, rgba(161,196,253,0.15) 0%, transparent 70%); border-radius: 50%; mix-blend-mode: screen; filter: blur(1px); }

        /* Aspalt road with advanced perspective clip paths */
        .roadway { position: absolute; bottom: 0; left: 0; width: 100%; height: 280px; background: linear-gradient(to bottom, #32373f, #1b1e22); clip-path: polygon(46% 0%, 54% 0%, 100% 100%, 0% 100%); z-index: 2; transition: filter 1s ease; }
        .roadway::before { content: ''; position: absolute; top: 0; left: 50%; width: 6px; height: 100%; background: repeating-linear-gradient(to bottom, #bfcaa7 0px, #bfcaa7 25px, transparent 25px, transparent 55px); transform: translateX(-50%); opacity: 0.35; }

        /* 🚗 PHOTO-STYLE TACTICAL TRANSPORT VAN WITH SWINGING SIDE WINGS */
        #car {
            position: absolute; top: 172px; left: 105px; width: 170px; height: 110px;
            background: linear-gradient(to bottom, #342a45 0%, #1e172a 45%, #0a0812 100%); border-radius: 16px 16px 8px 8px;
            box-shadow: 0 25px 45px rgba(0,0,0,0.8), inset 0 3px 5px rgba(255,255,255,0.12); z-index: 4;
            border: 1px solid #130f1c; will-change: transform, left, top; transform-origin: center bottom;
        }
        .window { position: absolute; top: 14px; left: 16px; width: 138px; height: 38px; background: linear-gradient(180deg, rgba(120,165,220,0.5) 0%, rgba(10,25,50,0.6) 100%); border-radius: 8px 8px 3px 3px; border: 2.5px solid #050505; box-shadow: inset 0 4px 6px rgba(255,255,255,0.15); }
        
        .wheel { position: absolute; background: #0c0c0c; border-radius: 5px; box-shadow: inset 0 0 10px #000; border: 2px solid #202020; }
        .w-front-l { bottom: 14px; left: -9px; width: 11px; height: 30px; transform: rotate(-3deg); }
        .w-front-r { bottom: 14px; right: -9px; width: 11px; height: 30px; transform: rotate(3deg); }
        .w-rear-l { bottom: -14px; left: 18px; width: 36px; height: 20px; }
        .w-rear-r { bottom: -14px; right: 18px; width: 36px; height: 20px; }
        
        /* Mechanical Side doors swinging open on parking stops */
        .suv-door { position: absolute; top: 52px; width: 24px; height: 48px; background: linear-gradient(to bottom, #251c30, #0a0812); border: 2px solid #000; z-index: 5; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); will-change: transform; }
        .door-l { left: -6px; border-radius: 4px 0 0 4px; transform-origin: right center; }
        .door-r { right: -6px; border-radius: 0 4px 4px 0; transform-origin: left center; }
        #car.parked-open .door-l { transform: rotateY(-80deg) skewY(8deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.6); }
        #car.parked-open .door-r { transform: rotateY(80deg) skewY(-8deg); box-shadow: 10px 10px 20px rgba(0,0,0,0.6); }

        .light-l { position: absolute; bottom: 26px; left: 14px; width: 20px; height: 16px; background: radial-gradient(circle, #ff334b, #900); border-radius: 2px; box-shadow: 0 0 16px #ff334b; }
        .light-r { position: absolute; bottom: 26px; right: 14px; width: 20px; height: 16px; background: radial-gradient(circle, #ff334b, #900); border-radius: 2px; box-shadow: 0 0 16px #ff334b; }

        /* 🔫 PHOTO-STYLE POLYMER TACTICAL HANDGUN + HOLOGRAPHIC RED-DOT RETICLE SIGHT */
        #weapon {
            position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%) scale(1.1);
            width: 100px; height: 160px; pointer-events: none; z-index: 25; will-change: transform;
        }
        /* Heavy polymer rear receiver slide positioned front-and-center */
        .w-slide { 
            position: absolute; top: 40px; left: 24px; width: 52px; height: 50px; 
            background: linear-gradient(to right, #1a1a1a 0%, #3a3a3a 30%, #151515 50%, #3a3a3a 70%, #1a1a1a 100%);
            border-radius: 6px 6px 2px 2px; border-top: 1px solid #555;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7), inset 0 2px 4px rgba(255,255,255,0.15);
        }
        /* Centered square Holographic Glass Optic frame bracket */
        .w-holo-sight {
            position: absolute; top: 2px; left: 29px; width: 42px; height: 38px;
            border: 3.5px solid #222; border-bottom: none; border-radius: 6px 6px 0 0;
            background: linear-gradient(to bottom, rgba(0,240,255,0.12), rgba(0,240,255,0.03));
            box-shadow: inset 0 0 8px rgba(0,240,255,0.2);
        }
        /* Glowing miniature bright red core laser emitter node dot inside the optic lens */
        .w-holo-sight::after {
            content: ''; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%);
            width: 4px; height: 4px; background: #ff003c; border-radius: 50%; box-shadow: 0 0 10px 2px #ff003c;
        }
        .w-grip-back { position: absolute; top: 90px; left: 32px; width: 36px; height: 70px; background: linear-gradient(to right, #111, #222, #0d0d0d); border-radius: 3px; }
        #flash { position: absolute; top: 15px; left: 30px; width: 40px; height: 40px; background: radial-gradient(circle, #ffffff 15%, #ff3c00 60%, transparent 80%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 10px #ff3c00); }

        /* --- 🏃 3D CINEMATIC THREAT SOLDIER STYLING --- */
        .threat { position: absolute; width: 45px; height: 75px; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; transform-origin: center bottom; will-change: transform, top, left, opacity; transition: transform 0.4s ease-out, top 0.4s ease-out, opacity 0.4s ease-out; }
        .t-head { background: linear-gradient(135deg, #e0a96d, #b57a53); border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #111; position: relative; }
        .t-head::before { content: ''; position: absolute; top: -3px; left: -1px; width: 26px; height: 10px; background: #1a1e16; border-radius: 4px 4px 0 0; } /* Camo helmet cap */
        .t-eyes { position: absolute; top: 11px; left: 4px; width: 14px; height: 4px; display: flex; justify-content: space-between; }
        .t-eyes::before, .t-eyes::after { content: ''; width: 3.5px; height: 3.5px; background: #000; border-radius: 50%; border-top: 1px solid #ff0000; }
        .t-torso { background: linear-gradient(to right, #3a472e, #5c6b42, #3a442d); width: 34px; height: 38px; border-radius: 4px; border: 1.5px solid #111; position: relative; box-shadow: 0 5px 8px rgba(0,0,0,0.4); }
        .t-arm { position: absolute; top: 6px; width: 26px; height: 11px; background: #4a573a; border: 1.5px solid #111; border-radius: 3px; }
        .arm-l { left: -16px; transform: rotate(-15deg); transform-origin: right center; }
        .arm-r { right: -16px; transform: rotate(15deg); transform-origin: left center; }
        .t-weapon { position: absolute; top: -2px; width: 15px; height: 11px; background: #222; border-radius: 2px; }
        .arm-l .t-weapon { left: -12px; } .arm-r .t-weapon { right: -12px; }
        .t-legs { display: flex; justify-content: space-around; width: 28px; height: 16px; margin-top: auto; }
        .t-leg { background: #2b3321; width: 9px; height: 100%; border-radius: 2px; border: 1px solid #000; animation: walkCycle 0.22s ease-in-out infinite alternate; }
        .t-leg:nth-child(2) { animation-delay: 0.11s; }
        @keyframes walkCycle { 0% { transform: translateY(0); } 100% { transform: translateY(-5px); } }

        /* Blood Splatters and Pools */
        .blood-drop { position: absolute; width: 4px; height: 4px; background: #8a0007; border-radius: 50%; z-index: 12; pointer-events: none; animation: explodeBlood 0.35s ease-out forwards; }
        @keyframes explodeBlood { 0% { transform: translate(0, 0) scale(1); opacity: 1; } 100% { transform: translate(var(--vx), var(--vy)) scale(0.3); opacity: 0; } }
        .blood-pool { position: absolute; width: 52px; height: 14px; background: radial-gradient(circle, #6f0003 20%, #3f0001 70%, transparent 100%); border-radius: 50%; z-index: 3; pointer-events: none; animation: spreadPool 1s ease-out forwards; }
        @keyframes spreadPool { 0% { transform: scale(0.1); opacity: 0; } 100% { transform: scale(1); opacity: 0.8; } }

        /* UI Panels */
        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; text-shadow: 0 0 5px #ffea00; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.8); padding: 6px 12px; border-radius: 6px; border: 1px solid #444; letter-spacing: 1px; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3333; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.8); padding: 3px 8px; border-radius: 4px; }

        #overScreen, #winScreen, #intermissionScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
        #overScreen { background: rgba(0,0,0,0.92); }
        #intermissionScreen { background: rgba(0,0,0,0.85); }
        #winScreen { background: linear-gradient(135deg, rgba(20,35,60,0.95), rgba(40,65,95,0.95)); }
        
        .retry-btn { padding: 12px 28px; background: #e63946; color: white; font-size: 15px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(230,57,70,0.5); }
        .win-btn { padding: 12px 28px; background: #ffea00; color: #000; font-size: 15px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(255,234,0,0.5); }
        .intermission-title { color: #ffea00; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #ffea00; text-align: center; }
    </style>
</head>
<body>
    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CHAPTER 1: CITY STREETS</div>
        <div id="targetTracker">TARGETS CLEAR: 0/5</div>
        
        <div id="sceneryContainer"></div>
        <div class="roadway"></div>
        
        <div id="car">
            <div class="wheel w-front-l"></div>
            <div class="wheel w-front-r"></div>
            <div class="suv-door door-l"></div>
            <div class="window"></div>
            <div class="light-l"></div>
            <div class="light-r"></div>
            <div class="suv-door door-r"></div>
            <div class="wheel w-rear-l"></div>
            <div class="wheel w-rear-r"></div>
        </div>

        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div>
            <div class="w-slide"></div>
            <div class="w-holo-sight"></div>
            <div class="w-frame"></div>
            <div class="w-guard"></div>
            <div class="w-grip-back"></div>
        </div>

        <div id="overScreen">
            <div style="color:#ffea00; font-size:30px; font-weight:bold; text-shadow:0 0 8px red; font-family:monospace;">OPERATIONS FAILURE</div>
            <button class="retry-btn" onclick="resetArcadeEngine(true)">RESTART CAMPAIGN 🔄</button>
        </div>

        <div id="intermissionScreen">
            <div class="intermission-title">MISSION ACCOMPLISHED! 🎉</div>
            <button class="win-btn" onclick="advanceToNextChapter()">CONTINUE TO NEXT CHAPTER ➡️</button>
        </div>

        <div id="winScreen">
            <div style="color:#ffea00; font-size:28px; font-weight:bold; text-shadow: 0 0 10px #ffea00;">👑 COMPLETE CAMPAIGN VICTORY 👑</div>
            <div style="color:white; font-size:14px; text-align:center; margin-top:15px; max-width:320px; line-height:1.5;">EXCELLENT WORK OFFICER!<br>All special operations sectors have been thoroughly secured!</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">REPLAY CAMPAIGN 🎮</button>
        </div>
    </div>

<script>
    let currentX = 168, currentY = 218, score = 200, isOver = false, activeChapter = 1;
    let carPos = 110, distanceScale = 0.2, carParked = false;
    let threatsList = []; let chapterKills = 0;
    let audioCtx = null, spawnTimerId = null, physicsTimerId = null;

    const gameArea = document.getElementById("gameArea");
    const sight = document.getElementById("sight");
    const weapon = document.getElementById("weapon");
    const flash = document.getElementById("flash");
    const car = document.getElementById("car");
    const scoreCounter = document.getElementById("scoreCounter");
    const chapterTxt = document.getElementById("chapterTxt");
    const targetTracker = document.getElementById("targetTracker");
    const sceneryContainer = document.getElementById("sceneryContainer");
    const overScreen = document.getElementById("overScreen");
    const winScreen = document.getElementById("winScreen");
    const intermissionScreen = document.getElementById("intermissionScreen");

    function setupAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function sound(type) {
        setupAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);
        
        if (type === "zap") { // Heavy snapping muzzle blast discharge
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(540, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(45, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15);
        } else if (type === "ding") {
            osc.type = "sine"; osc.frequency.setValueAtTime(950, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1350, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.08);
        } else if (type === "boom") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(110, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.38);
            gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.38);
        } else if (type === "level") {
            osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime);
            osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1);
            osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.4);
        } else if (type === "shout_aaa") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(260, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(180, audioCtx.currentTime + 0.26);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.26);
        }
    }

    function aim(e) {
        if (isOver || intermissionScreen.style.display === "flex") return;
        let evt = e.touches ? e.touches[0] : e;
        let bounds = gameArea.getBoundingClientRect();
        currentX = Math.max(-10, Math.min(350, evt.clientX - bounds.left - 16));
        currentY = Math.max(-10, Math.min(450, evt.clientY - bounds.top - 16));
        sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        
        // Weapon pivot formulas mapping subtle recoil shifts to center front red dot
        let swayX = (currentX - 168) / 10;
        let swayY = (currentY - 218) / 12;
        weapon.style.transform = `translateX(-50%) scale(1.1) rotate(${swayX}deg) translateY(${swayY}px)`;
    }

    gameArea.addEventListener("mousemove", aim);
    gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); triggerFire(); } });
    // REDUCED CAMPAIGN ARRAY: Curated to strictly execute Chapter 1, Chapter 2, and Chapter 3 Harbor Terminal
    const mapChapters = {
        1: { name: "CITY STREETS", bg: "linear-gradient(to bottom, #2b3a4a 0%, #4a5a6b 40%, #1c222b 41%, #0c1016)", road: "none", code: "city" },
        2: { name: "DARK FOREST", bg: "linear-gradient(to bottom, #061105, #142413 40%, #1a2219 41%, #030802)", road: "brightness(0.4) sepia(0.5) hue-rotate(60deg)", code: "tree" },
        3: { name: "CARGO PORT TERMINAL", bg: "linear-gradient(to bottom, #000814, #00152e 40%, #0c1017 41%, #02060c)", road: "brightness(0.45) contrast(1.25)", code: "port" }
    };

    function updateLevelAtmosphere() {
        let meta = mapChapters[activeChapter];
        let maxNeeded = 5 + (activeChapter - 1) * 2;
        chapterTxt.innerText = `CH. ${activeChapter}: ${meta.name}`;
        targetTracker.innerText = `TARGETS CLEAR: ${chapterKills}/${maxNeeded}`;
        gameArea.style.background = meta.bg;
        document.querySelector(".roadway").style.filter = meta.road;
        
        sceneryContainer.innerHTML = "";
        if (meta.code === "city") {
            sceneryContainer.innerHTML = '<div class="city-facade-l"></div><div class="overhead-wires"></div><div class="city-facade-r"></div>';
        } else if (meta.code === "tree") {
            sceneryContainer.innerHTML = '<div class="tree-3d" style="left:20px;"><div class="tree-trunk"></div><div class="tree-foliage"></div></div><div class="tree-3d" style="right:25px; bottom:110px;"><div class="tree-trunk"></div><div class="tree-foliage"></div></div>';
        } else if (meta.code === "port") {
            sceneryContainer.innerHTML = '<div class="port-crane"></div><div class="puddle-reflection"></div><div class="cargo-vessel"></div><div class="cargo-box" style="left:115px; bottom:140px;"><div class="cargo-ribs"></div></div>';
        }
    }

    function spawnBloodSpit(x, y) {
        for (let i = 0; i < 10; i++) {
            let drop = document.createElement("div"); drop.className = "blood-drop";
            drop.style.left = x + "px"; drop.style.top = y + "px";
            let vx = (Math.random() * 50 - 25); let vy = (Math.random() * -35 - 5);
            drop.style.setProperty('--vx', vx + 'px'); drop.style.setProperty('--vy', vy + 'px');
            gameArea.appendChild(drop);
            setTimeout(() => drop.remove(), 350);
        }
        let pool = document.createElement("div"); pool.className = "blood-pool";
        pool.style.left = (x - 26) + "px"; pool.style.top = (y + 26) + "px";
        gameArea.appendChild(pool);
    }

    function triggerFire() {
        if (isOver || intermissionScreen.style.display === "flex") return;
        sound("zap"); flash.style.display = "block";
        setTimeout(() => { flash.style.display = "none"; }, 60);
        let hitCenterX = currentX + 16; let hitCenterY = currentY + 16;

        threatsList.forEach((t) => {
            if (t.isDying) return;
            let tRect = t.el.getBoundingClientRect(); let areaRect = gameArea.getBoundingClientRect();
            let tX = tRect.left - areaRect.left; let tY = tRect.top - areaRect.top;

            if (hitCenterX >= tX && hitCenterX <= tX + tRect.width && hitCenterY >= tY && hitCenterY <= tY + tRect.height) {
                t.isDying = true; sound("shout_aaa"); spawnBloodSpit(hitCenterX, hitCenterY);
                score += 100; scoreCounter.innerText = String(score).padStart(5, '0'); chapterKills += 1;
                let maxNeeded = 5 + (activeChapter - 1) * 2;
                targetTracker.innerText = `TARGETS CLEAR: ${chapterKills}/${maxNeeded}`;

                t.ring.remove();
                
                // --- RAGDOLL PHYSICS: GRAVITY LEAN DEATH DROP CODES ---
                t.el.style.transform += " rotate(85deg)"; 
                t.el.style.top = (parseFloat(t.el.style.top) + 26) + "px"; 
                t.el.style.opacity = "0";

                setTimeout(() => {
                    t.el.remove();
                    threatsList = threatsList.filter(item => item !== t);
                }, 400);

                if (chapterKills >= maxNeeded) {
                    clearInterval(spawnTimerId); clearInterval(physicsTimerId);
                    if (activeChapter >= 3) { winScreen.style.display = "flex"; return; }
                    sound("level");
                    intermissionScreen.style.display = "flex";
                }
            }
        });
    }

    function runEngineLoops() {
        physicsTimerId = setInterval(() => {
            if (isOver) return;
            if (!carParked) {
                distanceScale += 0.015;
                if (distanceScale >= 1.0) { 
                    distanceScale = 1.0; 
                    carParked = true; 
                    car.classList.add("parked-open"); 
                }
            }

            let currentTopY = 165 + (distanceScale * 45); 
            car.style.transform = `scale(${distanceScale})`;
            car.style.left = carPos + "px"; car.style.top = currentTopY + "px";

            threatsList.forEach((t) => {
                if (t.isDying) return; 
                let updatedX = carPos + (t.sideOffset * distanceScale);
                let threatY = currentTopY + (t.baseTopY - 195) * distanceScale;
                
                t.el.style.transform = `scale(${distanceScale})`;
                t.el.style.left = updatedX + "px"; t.el.style.top = threatY + "px";
                
                t.ring.style.width = (90 * (1.3 - (t.age / 40))) + "px";
                t.ring.style.height = (90 * (1.3 - (t.age / 40))) + "px";
                let rSize = 90 * (1.3 - (t.age / 40));
                t.ring.style.left = (updatedX + (20 * distanceScale) - (rSize / 2) + 15) + "px";
                t.ring.style.top = (threatY + (15 * distanceScale) - (rSize / 2) + 30) + "px";
                t.age += 1;
            });
        }, 30);

        spawnTimerId = setInterval(() => {
            let maxSimultaneous = 5 + (activeChapter - 1) * 2;
            if (isOver || threatsList.length >= maxSimultaneous || !carParked) return;

            let el = document.createElement("div"); el.className = "threat";
            let roll = Math.random(); let sideOffset, topY, armClass;
            
            if (roll < 0.25) { sideOffset = -30; topY = 190; armClass = "arm-l"; }
            else if (roll < 0.5) { sideOffset = 150; topY = 185; armClass = "arm-r"; }
            else if (roll < 0.75) { sideOffset = -15; topY = 210; armClass = "arm-l"; }
            else { sideOffset = 130; topY = 210; armClass = "arm-r"; }

            el.innerHTML = '<div class="t-head"><div class="t-eyes"></div></div><div class="t-torso"><div class="t-arm ' + armClass + '"><div class="t-weapon"></div></div></div><div class="t-legs"><div class="t-leg"></div><div class="t-leg"></div></div>';
                
            let updatedX = carPos + (sideOffset * distanceScale);
            let threatY = (165 + (distanceScale * 45)) + (topY - 195) * distanceScale;
            
            el.style.left = updatedX + "px"; el.style.top = threatY + "px"; el.style.transform = `scale(${distanceScale})`;
            gameArea.appendChild(el);

            let ring = document.createElement("div"); ring.className = "target-ring";
            gameArea.appendChild(ring);

            let threatObj = { el: el, ring: ring, sideOffset: sideOffset, baseTopY: topY, age: 0, isDying: false };
            threatsList.push(threatObj);
            sound("ding");

            setTimeout(() => {
                if (!isOver && el.parentNode && !threatObj.isDying) {
                    isOver = true; sound("boom");
                    clearInterval(spawnTimerId); clearInterval(physicsTimerId);
                    finalScore.innerText = "Final Campaign Score: " + score;
                    overScreen.style.display = "flex";
                }
            }, 1400);
        }, 1100);
    }

    function clearDeadBodiesAndBlood() {
        document.querySelectorAll(".threat, .target-ring, .blood-pool, .blood-drop").forEach(el => el.remove());
        threatsList = [];
    }

    window.advanceToNextChapter = function() {
        activeChapter += 1; chapterKills = 0;
        intermissionScreen.style.display = "none";
        clearDeadBodiesAndBlood();
        resetArcadeEngine(false);
    }

    window.resetArcadeEngine = function(resetFullCampaign) {
        clearInterval(spawnTimerId); clearInterval(physicsTimerId);
        clearDeadBodiesAndBlood();
        if (resetFullCampaign) { score = 200; activeChapter = 1; chapterKills = 0; scoreCounter.innerText = "00200"; }
        
        updateLevelAtmosphere();
        isOver = false; distanceScale = 0.2; carParked = false; 
        car.classList.remove("parked-open"); 
        carPos = Math.random() * 80 + 70;
        
        sight.style.left = "168px"; sight.style.top = "218px";
        weapon.style.transform = "translateX(-50%) scale(1.1) rotate(0deg) translateY(0px)";
        overScreen.style.display = "none"; winScreen.style.display = "none";
        
        runEngineLoops();
    };

    updateLevelAtmosphere();
    runEngineLoops();
</script>
</body>
</html>
'''

components.html(game_html, height=560)

