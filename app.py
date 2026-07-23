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
        
        #gameArea { 
            position: relative; width: 380px; height: 480px; 
            background: #0f131a; border: 4px solid #1a1f26; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none;
            box-shadow: 0 24px 60px rgba(0,0,0,0.9); perspective: 800px;
        }

        /* FILM GRAIN + DYNAMIC WHOLE-SCREEN DAMAGE RESIZE VIGNETTE */
        #gameArea::after {
            content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 28;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://w3.org id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.055'/%3E%3C/svg%3E");
            background-size: auto;
            box-shadow: inset 0 0 80px rgba(0, 0, 0, 0.95), inset 0 0 140px rgba(0, 0, 0, 0.85);
            background-color: rgba(220, 20, 20, 0);
            transition: box-shadow 0.1s ease-out, background-color 0.1s ease-out;
        }

        #gameArea.taking-damage::after {
            background-color: rgba(220, 20, 20, 0.22);
            box-shadow: inset 0 0 110px rgba(220, 20, 20, 0.95), inset 0 0 180px rgba(180, 0, 0, 0.9);
        }

        #gameArea.critical-pulse::after {
            animation: wholeScreenLowHpPulse 0.55s ease-in-out infinite alternate;
        }
        @keyframes wholeScreenLowHpPulse {
            0% { background-color: rgba(220, 20, 20, 0.05); box-shadow: inset 0 0 85px rgba(160, 0, 0, 0.7); }
            100% { background-color: rgba(220, 20, 20, 0.25); box-shadow: inset 0 0 115px rgba(240, 0, 0, 0.95), inset 0 0 170px rgba(200, 0, 0, 0.85); }
        }

        /* 🎬 FIXED: SMOOTH RAIL-SHOOTER CAMERA TRANSITION WRAPPER CONTAINER */
        #sceneryContainer { 
            position: absolute; width: 100%; height: 100%; top: 0; left: 0; 
            pointer-events: none; z-index: 1;
            transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1); /* Simulates dynamic character movement/turning */
            will-change: transform;
        }
        /* Chapter 1: European City street facade panel nodes */
        .city-facade-l { position: absolute; top: 15px; left: -40px; width: 140px; height: 220px; background: linear-gradient(135deg, #1c1c1c, #0a0a0a); border-right: 3px solid #000; box-shadow: 12px 0 25px rgba(0,0,0,0.8); z-index: 3; }
        .city-facade-r { position: absolute; top: 10px; right: -50px; width: 130px; height: 230px; background: linear-gradient(225deg, #161616, #070707); border-left: 3px solid #000; box-shadow: -12px 0 25px rgba(0,0,0,0.8); z-index: 3; }
        .overhead-wires { position: absolute; top: 0; left: -100px; width: 600px; height: 140px; background: repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(255,255,255,0.015) 35px, rgba(255,255,255,0.015) 36px); opacity: 0.6; z-index: 3; }

        /* Chapter 2: High-Density 3D Forest Tree Elements */
        .tree-3d { position: absolute; bottom: 200px; width: 65px; height: 160px; transform-origin: center bottom; z-index: 3; }
        .tree-trunk { position: absolute; bottom: 0; left: 27px; width: 10px; height: 50px; background: linear-gradient(to right, #241407, #0f0702); }
        .tree-foliage { position: absolute; bottom: 45px; left: 0; width: 65px; height: 115px; background: radial-gradient(circle at center, #0f2619, #050d08); border-radius: 50%; box-shadow: inset -5px -8px 15px rgba(0,0,0,0.6), 0 10px 15px rgba(0,0,0,0.4); }

        /* Chapter 3: Cinematic Cargo Pier Docks Container Ship & Terminal Elements */
        .dock-edge { position: absolute; bottom: -50px; left: -100px; width: 600px; height: 300px; background: linear-gradient(to bottom, #1b1e22, #0d0f12); z-index: 2; border-top: 8px solid #2d3142; box-shadow: inset 0 15px 30px rgba(0,0,0,0.5); }
        .port-crane-tower { position: absolute; top: 20px; left: -20px; width: 80px; height: 190px; background: linear-gradient(to right, #11161d, #05070a); border-right: 3px solid #000; z-index: 1; opacity: 0.5; }
        .cargo-vessel-hull { position: absolute; top: 80px; right: -80px; width: 220px; height: 140px; background: linear-gradient(to bottom, #090e14, #020406); border-radius: 50% 12px 12px 50%; z-index: 1; border-bottom: 4px solid #000; box-shadow: -15px 15px 30px rgba(0,0,0,0.8); }
        .cargo-container-stack { position: absolute; width: 75px; height: 55px; background: linear-gradient(135deg, #47120c, #1f0402); border: 2px solid #000; border-radius: 4px; box-shadow: 0 8px 16px rgba(0,0,0,0.6); z-index: 3; }
        .container-ribs { width: 100%; height: 100%; background: repeating-linear-gradient(to right, transparent, transparent 6px, rgba(0,0,0,0.4) 6px, rgba(0,0,0,0.4) 8px); }
        .wet-reflection { position: absolute; bottom: 40px; left: 10%; width: 200px; height: 30px; background: radial-gradient(ellipse at center, rgba(140,180,240,0.08) 0%, transparent 80%); border-radius: 50%; mix-blend-mode: screen; filter: blur(2px); z-index: 2; }

        /* 🗺️ DYNAMIC HIGHWAY STRIP CONTROLLERS */
        .roadway { position: absolute; bottom: 0; left: -100px; width: 600px; height: 280px; background: linear-gradient(to bottom, #1f2226, #0e1012); clip-path: polygon(46% 0%, 54% 0%, 100% 100%, 0% 100%); z-index: 2; transition: transform 0.8s ease-in-out; }
        .road-lines { position: absolute; top: 0; left: 50%; width: 6px; height: 100%; background: repeating-linear-gradient(to bottom, #727a69 0px, #727a69 25px, transparent 25px, transparent 60px); transform: translateX(-50%); opacity: 0.25; }
        #car { position: absolute; top: 172px; left: 105px; width: 170px; height: 100px; background: linear-gradient(to bottom, #2b331f 0%, #1c2413 45%, #0d1208 100%); border-radius: 6px; box-shadow: 0 25px 45px rgba(0,0,0,0.85); z-index: 4; border: 2px solid #141c0b; will-change: transform, left, top; transform-origin: center bottom; transition: transform 0.8s ease-in-out, left 0.8s, top 0.8s; }
        .window { position: absolute; top: 16px; left: 20px; width: 130px; height: 22px; background: linear-gradient(180deg, rgba(50,75,110,0.5) 0%, rgba(2,6,15,0.8) 100%); border: 2px solid #000; }
        .wheel { position: absolute; background: #080808; border-radius: 3px; border: 1.5px solid #1c1c1c; }
        .w-front-l { bottom: 10px; left: -6px; width: 8px; height: 32px; } .w-front-r { bottom: 10px; right: -6px; width: 8px; height: 32px; } .w-rear-l { bottom: -10px; left: 20px; width: 38px; height: 16px; } .w-rear-r { bottom: -10px; right: 20px; width: 38px; height: 16px; }
        .suv-door { position: absolute; top: 45px; width: 20px; height: 35px; background: #1c2413; border: 1.5px solid #000; z-index: 5; transition: transform 0.4s ease; }
        .door-l { left: -4px; transform-origin: right center; } .door-r { right: -4px; transform-origin: left center; }
        #car.parked-open .door-l { transform: rotateY(-85deg); } #car.parked-open .door-r { transform: rotateY(85deg); }
        .light-l { position: absolute; bottom: 20px; left: 10px; width: 16px; height: 12px; background: #d4c222; box-shadow: 0 0 15px #d4c222; } .light-r { position: absolute; bottom: 20px; right: 10px; width: 16px; height: 12px; background: #d4c222; box-shadow: 0 0 15px #d4c222; }

        #weapon { position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%) scale(1.1); width: 100px; height: 160px; pointer-events: none; z-index: 25; will-change: transform; }
        .w-slide { position: absolute; top: 40px; left: 24px; width: 52px; height: 50px; background: linear-gradient(to right, #111 0%, #2a2a2a 30%, #0d0d0d 50%, #2a2a2a 70%, #111 100%); border-radius: 6px 6px 2px 2px; border-top: 1px solid #444; box-shadow: 0 12px 25px rgba(0,0,0,0.8), inset 0 2px 3px rgba(255,255,255,0.1); }
        .w-holo-sight { position: absolute; top: 2px; left: 29px; width: 42px; height: 38px; border: 3.5px solid #1c1c1c; border-bottom: none; border-radius: 6px 6px 0 0; background: linear-gradient(to bottom, rgba(0,240,255,0.1), rgba(0,240,255,0.02)); box-shadow: inset 0 0 8px rgba(0,240,255,0.15); }
        .w-holo-sight::after { content: ''; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: #ff003c; border-radius: 50%; box-shadow: 0 0 10px 2px #ff003c; }
        .w-grip-back { position: absolute; top: 90px; left: 32px; width: 36px; height: 70px; background: linear-gradient(to right, #0a0a0a, #1a1a1a, #050505); border-radius: 3px; }
        #flash { position: absolute; top: 15px; left: 30px; width: 40px; height: 40px; background: radial-gradient(circle, #ffffff 15%, #ff3c00 60%, transparent 80%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 10px #ff3c00); }

        .threat { position: absolute; width: 45px; height: 83px; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; transform-origin: center bottom; will-change: transform, top, left, opacity; }
        .t-head { background: linear-gradient(135deg, #c48e58, #945d31); border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #000; position: relative; }
        .t-head::before { content: ''; position: absolute; top: -3px; left: -1px; width: 26px; height: 12px; background: repeating-linear-gradient(45deg, #2b331a, #2b331f 4px, #161a0d 4px, #161a0d 8px); border-radius: 6px 6px 0 0; border: 1.5px solid #000; } 
        .t-eyes { position: absolute; top: 12px; left: 4px; width: 14px; height: 4px; display: flex; justify-content: space-between; }
        .t-eyes::before, .t-eyes::after { content: ''; width: 3.5px; height: 3.5px; background: #000; border-radius: 50%; border-top: 1px solid #ff0000; }
        .t-torso { background: repeating-linear-gradient(to right, #323b20, #464f2e 6px, #1c210e 12px); width: 34px; height: 38px; border-radius: 4px; border: 1.5px solid #000; position: relative; box-shadow: 0 6px 10px rgba(0,0,0,0.5); }
        .t-arm { position: absolute; top: 6px; width: 26px; height: 11px; background: #323b20; border: 1.5px solid #000; border-radius: 3px; }
        .arm-l { left: -16px; transform: rotate(-15deg); transform-origin: right center; }
        .arm-r { right: -16px; transform: rotate(15deg); transform-origin: left center; }
        .t-legs { display: flex; justify-content: space-around; width: 28px; height: 24px; margin-top: auto; }
        .t-leg { background: #1c210e; width: 9px; height: 100%; border-radius: 2px; border: 1px solid #000; animation: walkCycle 0.22s ease-in-out infinite alternate; }
        .t-leg:nth-child(2) { animation-delay: 0.11s; }
        @keyframes walkCycle { 0% { transform: translateY(0); } 100% { transform: translateY(-5px); } }
        .dead-threat .t-leg { animation: none; transform: translateY(0) !important; }

        .t-weapon { position: absolute; top: -2px; width: 16px; height: 6px; background: #1a1a1a; border-radius: 2px; border-bottom: 2px solid #000; }
        .arm-l .t-weapon { left: -14px; } .arm-r .t-weapon { right: -14px; }
        .enemy-flash { position: absolute; width: 14px; height: 14px; background: radial-gradient(circle, #ffffff 20%, #ffbb00 60%, transparent 80%); border-radius: 50%; display: none; z-index: 6; filter: drop-shadow(0 0 6px #ff8800); }
        .arm-l .enemy-flash { left: -26px; top: -6px; } .arm-r .enemy-flash { right: -26px; top: -6px; }

        .target-ring { position: absolute; border: 3px dashed #ff2222; border-radius: 50%; pointer-events: none; z-index: 10; transform-origin: center center; display: block; box-shadow: 0 0 10px #ff2222; }
        .blood-drop { position: absolute; width: 4px; height: 4px; background: #6b0004; border-radius: 50%; z-index: 12; pointer-events: none; animation: explodeBlood 0.35s ease-out forwards; }
        @keyframes explodeBlood { 0% { transform: translate(0, 0) scale(1); opacity: 1; } 100% { transform: translate(var(--vx), var(--vy)) scale(0.3); opacity: 0; } }
        .blood-pool { position: absolute; width: 52px; height: 14px; background: radial-gradient(circle, #4a0002 20%, #240001 70%, transparent 100%); border-radius: 50%; z-index: 3; pointer-events: none; animation: spreadPool 1s ease-out forwards; }
        @keyframes spreadPool { 0% { transform: scale(0.1); opacity: 0; } 100% { transform: scale(1); opacity: 0.85; } }

        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; text-shadow: 0 0 5px #ffea00; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.85); padding: 6px 12px; border-radius: 6px; border: 1px solid #444; letter-spacing: 1px; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3333; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.85); padding: 3px 8px; border-radius: 4px; }
        #healthCounter { position: absolute; bottom: 12px; left: 12px; color: #ff3333; font-weight: bold; font-family: 'Courier New', monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.9); padding: 5px 12px; border-radius: 4px; border: 2px solid #ff2222; text-shadow: 0 0 4px #ff0000; }

        #overScreen, #winScreen, #intermissionScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
        #overScreen { background: rgba(0,0,0,0.95); } #intermissionScreen { background: rgba(0,0,0,0.85); } #winScreen { background: linear-gradient(135deg, rgba(10,20,35,0.95), rgba(25,40,65,0.95)); }
        .retry-btn { padding: 12px 28px; background: #b01a25; color: white; font-size: 15px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(176,26,37,0.5); }
        .win-btn { padding: 12px 28px; background: #ffea00; color: #000; font-size: 15px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(255,234,0,0.5); }
        .intermission-title { color: #ffea00; font-size: 26px; font-weight: bold; text-shadow: 0 0 12px #ffea00; text-align: center; }
    </style>
</head>
<body>
    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CHAPTER 1: CITY STREETS</div>
        <div id="targetTracker">SECTOR A: 0/3</div>
        <div id="healthCounter">HP: 100</div>
        
        <div id="sceneryContainer"></div>
        <div class="roadway"><div class="road-lines"></div></div>
        
        <div id="car">
            <div class="wheel w-front-l"></div> <div class="wheel w-front-r"></div>
            <div class="suv-door door-l"></div> <div class="window"></div> <div class="light-l"></div> <div class="light-r"></div>
            <div class="suv-door door-r"></div> <div class="wheel w-rear-l"></div> <div class="wheel w-rear-r"></div>
        </div>

        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div> <div class="w-slide"></div> <div class="w-holo-sight"></div> <div class="w-grip-back"></div>
        </div>

        <div id="overScreen">
            <div style="color:#b01a25; font-size:32px; font-weight:bold; text-shadow:0 0 10px #000; font-family:monospace; letter-spacing:1px;">MISSION FAILURE</div>
            <div id="finalScore" style="color:white; font-size:16px; margin-top:10px;">Final Operation Score: 200</div>
            <button class="retry-btn" onclick="resetArcadeEngine(true)">RETRY MISSION 🔄</button>
        </div>

        <div id="intermissionScreen">
            <div class="intermission-title">MISSION ACCOMPLISHED! 🎉</div>
            <button class="win-btn" onclick="advanceToNextChapter()">CONTINUE MISSION ➡️</button>
        </div>

        <div id="winScreen">
            <div style="color:#ffea00; font-size:28px; font-weight:bold; text-shadow: 0 0 10px #ffea00;">👑 COMPLETE CAMPAIGN VICTORY 👑</div>
            <div style="color:white; font-size:14px; text-align:center; margin-top:15px; max-width:320px; line-height:1.5;">EXCELLENT WORK OFFICER!<br>All operations zones cleared successfully!</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">REPLAY CAMPAIGN 🎮</button>
        </div>
    </div>

<script>
    let currentX = 168, currentY = 218, score = 200, isOver = false, activeChapter = 1;
    let carPos = 110, distanceScale = 0.2, carParked = false;
    let threatsList = []; let playerHp = 100;
    let audioCtx = null, spawnTimerId = null, physicsTimerId = null, heartbeatIntervalId = null;

    // --- 🎮 RAIL-SHOOTER ON-RAILS SECTOR MOTION VARIABLES ---
    let currentSector = "A"; // Progressive states: "A", "B", "C"
    let sectorKills = 0;
    const sectorRequirements = { "A": 3, "B": 3, "C": 4 }; // Kills needed per checkpoint section

    const gameArea = document.getElementById("gameArea"), sight = document.getElementById("sight"), weapon = document.getElementById("weapon"), flash = document.getElementById("flash"), car = document.getElementById("car"), scoreCounter = document.getElementById("scoreCounter"), chapterTxt = document.getElementById("chapterTxt"), targetTracker = document.getElementById("targetTracker"), healthCounter = document.getElementById("healthCounter"), sceneryContainer = document.getElementById("sceneryContainer"), overScreen = document.getElementById("overScreen"), winScreen = document.getElementById("winScreen"), intermissionScreen = document.getElementById("intermissionScreen"), finalScore = document.getElementById("finalScore");

    function setupAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
    
    function sound(type) {
        setupAudio(); if (!audioCtx) return; let osc = audioCtx.createOscillator(), gain = audioCtx.createGain(); osc.connect(gain); gain.connect(audioCtx.destination);
        if (type === "zap") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(540, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(45, audioCtx.currentTime + 0.15); gain.gain.setValueAtTime(0.4, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.15); }
        else if (type === "ding") { osc.type = "sine"; osc.frequency.setValueAtTime(950, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(1350, audioCtx.currentTime + 0.08); gain.gain.setValueAtTime(0.2, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.08); }
        else if (type === "boom") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(110, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.38); gain.gain.setValueAtTime(0.5, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.38); }
        else if (type === "level") { osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2); gain.gain.setValueAtTime(0.25, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        else if (type === "shout_aaa") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(260, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(180, audioCtx.currentTime + 0.26); gain.gain.setValueAtTime(0.25, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.26); }
        else if (type === "bullet_crack") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(190, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(30, audioCtx.currentTime + 0.12); gain.gain.setValueAtTime(0.3, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.12); }
        else if (type === "heartbeat") { osc.type = "sine"; osc.frequency.setValueAtTime(60, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(25, audioCtx.currentTime + 0.18); gain.gain.setValueAtTime(0.45, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.18); }
    }

    function aim(e) {
        if (isOver || intermissionScreen.style.display === "flex") return;
        let evt = e; if (e.touches && e.touches.length > 0) { evt = e.touches; } else if (e.changedTouches && e.changedTouches.length > 0) { evt = e.changedTouches; }
        let bounds = gameArea.getBoundingClientRect();
        currentX = Math.max(-10, Math.min(350, evt.clientX - bounds.left - 16)); currentY = Math.max(-10, Math.min(450, evt.clientY - bounds.top - 16));
        sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        let swayX = (currentX - 168) / 10; let swayY = (currentY - 218) / 12;
        weapon.style.transform = "translateX(-50%) scale(1.1) rotate(" + swayX + "deg) translateY(" + swayY + "px)";
    }
    gameArea.addEventListener("mousemove", aim); gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); aim(e); triggerFire(); } }, { passive: false });
    const mapChapters = {
        1: { name: "CITY STREETS", bg: "linear-gradient(to bottom, #172230 0%, #2f3e4f 40%, #151a21 41%, #090c12)", road: "none", code: "city" },
        2: { name: "DARK FOREST", bg: "linear-gradient(to bottom, #050d04, #0f1c0e 40%, #131a12 41%, #020501)", road: "brightness(0.35) sepia(0.6) hue-rotate(65deg)", code: "tree" },
        3: { name: "CARGO PORT TERMINAL", bg: "linear-gradient(to bottom, #00050d, #000f24 40%, #070a0f 41%, #010306)", road: "brightness(0.4) contrast(1.3)", code: "port" }
    };

    function updateLevelAtmosphere() {
        let meta = mapChapters[activeChapter]; let needed = sectorRequirements[currentSector];
        chapterTxt.innerText = `CH. ${activeChapter}: ${meta.name}`; 
        targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`; gameArea.style.background = meta.bg;
        
        let roadwayEl = document.querySelector(".roadway"), carEl = document.getElementById("car");
        if (meta.code === "port") { roadwayEl.style.display = "none"; carEl.style.display = "none"; carParked = true; } 
        else if (meta.code === "tree") { roadwayEl.style.display = "block"; roadwayEl.style.filter = meta.road; document.querySelector(".road-lines").style.display = "none"; carEl.style.display = "block"; } 
        else { roadwayEl.style.display = "block"; roadwayEl.style.filter = meta.road; document.querySelector(".road-lines").style.display = "block"; carEl.style.display = "block"; }
        
        sceneryContainer.innerHTML = "";
        if (meta.code === "city") { sceneryContainer.innerHTML = '<div class="city-facade-l"></div><div class="overhead-wires"></div><div class="city-facade-r"></div>'; } 
        else if (meta.code === "tree") { sceneryContainer.innerHTML = `<div class="tree-3d" style="left:15px; bottom:160px; transform:scale(0.85);"><div class="tree-trunk"></div><div class="tree-foliage"></div></div><div class="tree-3d" style="left:65px; bottom:180px; transform:scale(0.7);"><div class="tree-trunk"></div><div class="tree-foliage"></div></div><div class="tree-3d" style="right:20px; bottom:150px; transform:scale(0.9);"><div class="tree-trunk"></div><div class="tree-foliage"></div></div><div class="tree-3d" style="right:75px; bottom:175px; transform:scale(0.75);"><div class="tree-trunk"></div><div class="tree-foliage"></div></div>`; } 
        else if (meta.code === "port") { sceneryContainer.innerHTML = `<div class="dock-edge"></div><div class="port-crane-tower"></div><div class="wet-reflection"></div><div class="cargo-vessel-hull"></div><div class="cargo-container-stack" style="left:20px; bottom:115px; z-index:3;"><div class="container-ribs"></div></div><div class="cargo-container-stack" style="left:70px; bottom:130px; background:linear-gradient(135deg,#0a4447,#032021); z-index:3;"><div class="container-ribs"></div></div><div class="cargo-container-stack" style="right:35px; bottom:120px; background:linear-gradient(135deg,#5c4308,#241a02); z-index:3;"><div class="container-ribs"></div></div>`; }
    }

    function spawnBloodSpit(x, y) {
        for (let i = 0; i < 10; i++) {
            let drop = document.createElement("div"); drop.className = "blood-drop"; drop.style.left = x + "px"; drop.style.top = y + "px";
            let vx = (Math.random() * 50 - 25); let vy = (Math.random() * -35 - 5); drop.style.setProperty('--vx', vx + 'px'); drop.style.setProperty('--vy', vy + 'px');
            gameArea.appendChild(drop); setTimeout(() => drop.remove(), 350);
        }
        let pool = document.createElement("div"); pool.className = "blood-pool"; pool.style.left = (x - 26) + "px"; pool.style.top = (y + 26) + "px"; gameArea.appendChild(pool);
    }

    function triggerEnemyDamageStrike() {
        if (isOver || intermissionScreen.style.display === "flex") return;
        playerHp -= 20; if (playerHp < 0) playerHp = 0; healthCounter.innerText = `HP: ${playerHp}`; sound("bullet_crack");
        gameArea.classList.add("taking-damage"); setTimeout(() => gameArea.classList.remove("taking-damage"), 140);
        if (playerHp <= 20 && !heartbeatIntervalId) { gameArea.classList.add("critical-pulse"); heartbeatIntervalId = setInterval(() => { sound("heartbeat"); }, 550); }
        if (playerHp <= 0) { isOver = true; sound("boom"); clearInterval(spawnTimerId); clearInterval(physicsTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); gameArea.classList.remove("critical-pulse"); heartbeatIntervalId = null; } finalScore.innerText = "Final Operation Score: " + score; overScreen.style.display = "flex"; }
    }
    // --- 🎬 FIXED: ADVANCED VIRTUA COP ON-RAILS MOTION AND CAMERA CONTROLLER ENGINE ---
    function triggerSectorPathMovement() {
        if (currentSector === "A") {
            currentSector = "B"; sectorKills = 0;
            // Camera pans heavily to the right side layout of the map zone
            sceneryContainer.style.transform = "scale(1.2) translateX(-40px) translateY(10px)";
            if (document.querySelector(".roadway")) document.querySelector(".roadway").style.transform = "skewX(-15deg) translateX(-30px)";
        } else if (currentSector === "B") {
            currentSector = "C"; sectorKills = 0;
            // Camera pans up and scales out to simulate running deep inside the base
            sceneryContainer.style.transform = "scale(1.5) translateX(20px) translateY(30px)";
            if (document.querySelector(".roadway")) document.querySelector(".roadway").style.transform = "scale(0.8) translateY(40px)";
        } else if (currentSector === "C") {
            // Sector C is clear -> Entire chapter campaign area accomplished!
            if (activeChapter >= 3) { winScreen.style.display = "flex"; return; }
            sound("level"); intermissionScreen.style.display = "flex";
            return;
        }
        sound("level");
        updateLevelAtmosphere();
    }

    function triggerFire() {
        if (isOver || intermissionScreen.style.display === "flex") return;
        sound("zap"); flash.style.display = "block"; setTimeout(() => { flash.style.display = "none"; }, 60);
        let hitCenterX = currentX + 16; let hitCenterY = currentY + 16;

        threatsList.forEach((t) => {
            if (t.isDying) return;
            let tRect = t.el.getBoundingClientRect(); let areaRect = gameArea.getBoundingClientRect();
            let tX = tRect.left - areaRect.left; let tY = tRect.top - areaRect.top;

            if (hitCenterX >= tX && hitCenterX <= tX + tRect.width && hitCenterY >= tY && hitCenterY <= tY + tRect.height) {
                t.isDying = true; t.el.classList.add("dead-threat");
                sound("shout_aaa"); spawnBloodSpit(hitCenterX, hitCenterY);
                score += 100; scoreCounter.innerText = String(score).padStart(5, '0'); 
                
                sectorKills += 1;
                let needed = sectorRequirements[currentSector];
                targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;

                t.ring.remove(); t.el.style.transform += " rotate(85deg)"; t.el.style.top = (parseFloat(t.el.style.top) + 26) + "px"; 
                
                // FIXED: Character now automatically advances camera layers once the local sector quota is met
                if (sectorKills >= needed) {
                    // Instantly clear surviving ambient enemies before camera panning
                    document.querySelectorAll(".threat, .target-ring").forEach(el => el.remove());
                    threatsList = [];
                    setTimeout(triggerSectorPathMovement, 400);
                }
            }
        });
    }

    function runEngineLoops() {
        physicsTimerId = setInterval(() => {
            if (isOver) return; let meta = mapChapters[activeChapter];
            if (meta.code !== "port") {
                if (!carParked) { distanceScale += 0.015; if (distanceScale >= 1.0) { distanceScale = 1.0; carParked = true; car.classList.add("parked-open"); } }
                let currentTopY = 165 + (distanceScale * 45); car.style.transform = "scale(" + distanceScale + ")"; car.style.left = carPos + "px"; car.style.top = currentTopY + "px";
            }
            let currentTopY = 165 + (distanceScale * 45);

            threatsList.forEach((t) => {
                if (t.isDying) return; 
                if (t.age > 0 && t.age % 32 === 0) { 
                    let eFlashEl = t.el.querySelector(".enemy-flash");
                    if (eFlashEl) { eFlashEl.style.display = "block"; triggerEnemyDamageStrike(); setTimeout(() => { eFlashEl.style.display = "none"; }, 65); }
                }

                if (meta.code === "port") {
                    t.localScale += 0.024; if (t.localScale > 1.35) t.localScale = 1.35;
                    t.el.style.transform = "scale(" + t.localScale + ")"; t.el.style.left = (60 + t.sideOffset) + "px"; t.el.style.top = (130 + (t.baseTopY - 190) + (t.localScale * 45)) + "px";
                    let rSize = 90 * (1.3 - (t.age / 40)); t.ring.style.width = Math.max(0, rSize) + "px"; t.ring.style.height = Math.max(0, rSize) + "px";
                    t.ring.style.left = ((60 + t.sideOffset) + (20 * t.localScale) - (rSize / 2) + 15) + "px"; t.ring.style.top = ((130 + (t.baseTopY - 190) + (t.localScale * 45)) + (15 * t.localScale) - (rSize / 2) + 30) + "px";
                } else {
                    t.el.style.transform = "scale(" + distanceScale + ")"; t.el.style.left = (carPos + (t.sideOffset * distanceScale)) + "px"; t.el.style.top = (currentTopY + (t.baseTopY - 195) * distanceScale) + "px";
                    let rSize = 90 * (1.3 - (t.age / 40)); t.ring.style.width = Math.max(0, rSize) + "px"; t.ring.style.height = Math.max(0, rSize) + "px";
                    t.ring.style.left = ((carPos + (t.sideOffset * distanceScale)) + (20 * distanceScale) - (rSize / 2) + 15) + "px"; t.ring.style.top = ((currentTopY + (t.baseTopY - 195) * distanceScale) + (15 * distanceScale) - (rSize / 2) + 30) + "px";
                }
                t.age += 1;
            });
        }, 30);

        spawnTimerId = setInterval(() => {
            let maxSimultaneous = 3; if (isOver || threatsList.length >= maxSimultaneous || !carParked) return;
            let el = document.createElement("div"); el.className = "threat"; let roll = Math.random(); let sideOffset, topY, armClass;
            
            // Generate different position vectors based on which dynamic camera zone is active
            if (currentSector === "B") { sideOffset = roll < 0.5 ? -10 : 110; topY = 220; armClass = "arm-l"; }
            else if (currentSector === "C") { sideOffset = roll < 0.5 ? 20 : 140; topY = 170; armClass = "arm-r"; }
            else { if (roll < 0.25) { sideOffset = -30; topY = 190; armClass = "arm-l"; } else if (roll < 0.5) { sideOffset = 150; topY = 185; armClass = "arm-r"; } else if (roll < 0.75) { sideOffset = -15; topY = 210; armClass = "arm-l"; } else { sideOffset = 130; topY = 210; armClass = "arm-r"; } }

            el.innerHTML = '<div class="t-head"><div class="t-eyes"></div></div><div class="t-torso"><div class="t-arm ' + armClass + '"><div class="t-weapon"></div><div class="enemy-flash"></div></div></div><div class="t-legs"><div class="t-leg"></div><div class="t-leg"></div></div>';
            let initialScale = (mapChapters[activeChapter].code === "port") ? 0.25 : distanceScale;
            let updatedX = (mapChapters[activeChapter].code === "port") ? (60 + sideOffset) : (carPos + (sideOffset * distanceScale));
            let threatY = (mapChapters[activeChapter].code === "port") ? (130 + (topY - 190)) : ((165 + (distanceScale * 45)) + (topY - 195) * distanceScale);
            
            el.style.left = updatedX + "px"; el.style.top = threatY + "px"; el.style.transform = "scale(" + initialScale + ")";
            gameArea.appendChild(el); let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);

            let threatObj = { el: el, ring: ring, sideOffset: sideOffset, baseTopY: topY, age: 0, isDying: false, localScale: initialScale }; threatsList.push(threatObj); sound("ding");
        }, 1100);
    }

    function clearDeadBodiesAndBlood() { document.querySelectorAll(".threat, .target-ring, .blood-pool, .blood-drop").forEach(el => el.remove()); threatsList = []; }
    window.advanceToNextChapter = function() { activeChapter += 1; sectorKills = 0; currentSector = "A"; playerHp = 100; if(sceneryContainer) sceneryContainer.style.transform = "none"; intermissionScreen.style.display = "none"; clearDeadBodiesAndBlood(); resetArcadeEngine(false); };
    window.resetArcadeEngine = function(resetFullCampaign) {
        clearInterval(spawnTimerId); clearInterval(physicsTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); gameArea.classList.remove("critical-pulse"); heartbeatIntervalId = null; }
        clearDeadBodiesAndBlood();
        if (resetFullCampaign) { score = 200; activeChapter = 1; sectorKills = 0; currentSector = "A"; playerHp = 100; if(sceneryContainer) sceneryContainer.style.transform = "none"; scoreCounter.innerText = "00200"; }
        healthCounter.innerText = `HP: ${playerHp}`; updateLevelAtmosphere(); isOver = false; distanceScale = 0.2; carParked = (mapChapters[activeChapter].code === "port"); car.classList.remove("parked-open"); carPos = Math.random() * 80 + 70;
        currentX = 168; currentY = 218; sight.style.left = "168px"; sight.style.top = "218px"; weapon.style.transform = "translateX(-50%) scale(1.1) rotate(0deg) translateY(0px)"; overScreen.style.display = "none"; winScreen.style.display = "none"; runEngineLoops();
    };
    updateLevelAtmosphere(); runEngineLoops();
</script>
</body>
</html>
'''
st.markdown('<div class="cab">', unsafe_allow_html=True)
components.html(game_html, height=560, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)
