import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Cop: 3D Campaign", layout="centered")
st.title("🚓 Virtua Arcade: Elite Campaign")

game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: 'Arial Black', sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        /* Main 3D Viewport View */
        #gameArea { 
            position: relative; width: 380px; height: 480px; 
            background: linear-gradient(to bottom, #4a777a 0%, #a1c4fd 40%, #727d8c 41%, #3a4454 100%); 
            border: 4px solid #444; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none;
            box-shadow: 0 16px 40px rgba(0,0,0,0.7); perspective: 600px;
        }

        /* 🌆 PURE 3D ARCHITECTURE MAPPING LAYER */
        #sceneryContainer { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 1; }
        
        .b-3d-left { position: absolute; top: 40px; left: 0; width: 120px; height: 160px; background: linear-gradient(135deg, #1b263b, #0d1b2a); border-right: 4px solid #000; box-shadow: 10px 0 20px rgba(0,0,0,0.5); }
        .b-3d-right { position: absolute; top: 30px; right: 0; width: 110px; height: 170px; background: linear-gradient(225deg, #14213d, #000814); border-left: 4px solid #000; box-shadow: -10px 0 20px rgba(0,0,0,0.5); }
        
        .roadway { position: absolute; bottom: 0; left: 0; width: 100%; height: 280px; background: linear-gradient(to bottom, #434952, #2c3036); clip-path: polygon(45% 0%, 55% 0%, 100% 100%, 0% 100%); z-index: 2; }
        .roadway::before { content: ''; position: absolute; top: 0; left: 50%; width: 8px; height: 100%; background: repeating-linear-gradient(to bottom, #e5e5e5 0px, #e5e5e5 25px, transparent 25px, transparent 50px); transform: translateX(-50%); opacity: 0.4; }

        /* Chapter 2: Shaded 3D Trees */
        .tree-3d { position: absolute; bottom: 160px; width: 50px; height: 130px; transform-style: preserve-3d; }
        .tree-trunk { position: absolute; bottom: 0; left: 21px; width: 8px; height: 45px; background: linear-gradient(to right, #4a2c11, #2b1704); }
        .tree-foliage { position: absolute; bottom: 40px; left: 0; width: 50px; height: 90px; background: radial-gradient(circle at center, #2d6a4f, #1b4332); border-radius: 50%; box-shadow: inset -4px -4px 10px rgba(0,0,0,0.4), 0 8px 12px rgba(0,0,0,0.3); }

        /* Chapter 5: Shipping Container Blocks */
        .cargo-box { position: absolute; bottom: 140px; width: 75px; height: 55px; background: linear-gradient(135deg, #ae2012, #6a040f); border: 2px solid #222; border-radius: 4px; box-shadow: -5px 8px 15px rgba(0,0,0,0.4); }
        .cargo-ribs { width: 100%; height: 100%; background: repeating-linear-gradient(to right, transparent, transparent 6px, rgba(0,0,0,0.4) 6px, rgba(0,0,0,0.4) 8px); }

        /* Chapter 8: Supermarket Shelves */
        .shelf-3d { position: absolute; bottom: 130px; width: 65px; height: 130px; background: linear-gradient(to right, #bc4749, #6a040f); border: 2px solid #222; box-shadow: -6px 6px 12px rgba(0,0,0,0.4); }
        .shelf-row { width: 100%; height: 25%; border-bottom: 2px solid #ddd; background: repeating-linear-gradient(to right, #f77f00 0px, #f77f00 6px, #fcbf49 6px, #fcbf49 12px); }
                /* 🚗 TRUE 3D PROFILED SUV WITH ACTIVE MECHANICAL OPENING DOORS */
        #car {
            position: absolute; top: 175px; left: 110px; width: 160px; height: 105px;
            background: linear-gradient(to bottom, #2b2d42, #1d1e2c, #0d0e15); border-radius: 12px 12px 6px 6px;
            box-shadow: 0 20px 35px rgba(0,0,0,0.6); z-index: 4;
            border: 1px solid #15161e; will-change: transform, left, top; transform-origin: center bottom;
        }
        .window { position: absolute; top: 12px; left: 15px; width: 130px; height: 35px; background: linear-gradient(180deg, rgba(142,202,230,0.7), rgba(2,48,71,0.6)); border-radius: 8px 8px 2px 2px; border: 2px solid #050505; }
        
        /* 3D Wheel Profile Layout */
        .wheel { position: absolute; background: #0e0e0e; border-radius: 4px; box-shadow: inset 0 0 8px #000; border: 1.5px solid #252525; }
        .w-front-l { bottom: 12px; left: -8px; width: 10px; height: 28px; transform: rotate(-5deg); }
        .w-front-r { bottom: 12px; right: -8px; width: 10px; height: 28px; transform: rotate(5deg); }
        .w-rear-l { bottom: -12px; left: 16px; width: 34px; height: 18px; }
        .w-rear-r { bottom: -12px; right: 16px; width: 34px; height: 18px; }
        
        /* Left and Right Side Mechanical Wings (Swing open dynamically when parked) */
        .suv-door {
            position: absolute; top: 48px; width: 22px; height: 45px; 
            background: linear-gradient(to bottom, #1d1e2c, #0d0e15); border: 1.5px solid #000;
            z-index: 5; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            will-change: transform;
        }
        .door-l { left: -5px; border-radius: 4px 0 0 4px; transform-origin: right center; }
        .door-r { right: -5px; border-radius: 0 4px 4px 0; transform-origin: left center; }
        
        /* Trigger states executed via Javascript engine injection classes */
        #car.parked-open .door-l { transform: rotateY(-75deg) skewY(10deg); box-shadow: -8px 8px 15px rgba(0,0,0,0.6); }
        #car.parked-open .door-r { transform: rotateY(75deg) skewY(-10deg); box-shadow: 8px 8px 15px rgba(0,0,0,0.6); }

        .light-l { position: absolute; bottom: 22px; left: 12px; width: 24px; height: 12px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 14px #ff4d6d; }
        .light-r { position: absolute; bottom: 22px; right: 12px; width: 24px; height: 14px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 14px #ff4d6d; }

        /* 🔫 3D-SHADED AUTOMATIC WEAPON INTERFACE LAYER */
        #weapon { position: absolute; bottom: -35px; right: 45px; width: 95px; height: 190px; transform: rotate(0deg); transform-origin: bottom center; pointer-events: none; z-index: 25; will-change: transform; }
        .w-slide { position: absolute; top: 10px; left: -32px; width: 115px; height: 28px; background: linear-gradient(to bottom, #444 0%, #1c1c1c 45%, #0a0a0a 100%); border-radius: 5px 2px 2px 2px; border-bottom: 2px solid #000; box-shadow: -5px 6px 12px rgba(0,0,0,0.6), inset 0 2px 3px rgba(255,255,255,0.2); }
        .w-slide::before { content: ''; position: absolute; left: -4px; top: 6px; width: 4px; height: 10px; background: #000; }
        .w-grip { position: absolute; top: 36px; left: 26px; width: 36px; height: 115px; background: repeating-linear-gradient(45deg, #2b1e17, #2b1e17 2px, #140d0a 2px, #140d0a 4px); border: 3px solid #050505; border-radius: 5px 6px 14px 6px; transform: rotate(-9deg); box-shadow: -8px 8px 16px rgba(0,0,0,0.6); }
        .w-frame { position: absolute; top: 34px; left: -16px; width: 52px; height: 26px; background: #1c1c1c; border-radius: 0 0 10px 4px; }
        .w-guard { position: absolute; top: 32px; left: -6px; width: 24px; height: 24px; border: 3px solid #1c1c1c; border-radius: 50%; }
        #flash { position: absolute; top: -12px; left: -38px; width: 40px; height: 40px; background: radial-gradient(circle, #ffffff 10%, #ffea00 50%, transparent 75%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 8px #ffea00); }

        #sight { position: absolute; top: 218px; left: 168px; width: 32px; height: 32px; border: 2px solid #00f0ff; border-radius: 50%; pointer-events: none; z-index: 20; box-shadow: 0 0 8px rgba(0,240,255,0.6); }
        #sight::before { content: ''; position: absolute; top: 15px; left: 0; width: 32px; height: 1px; background: #00f0ff; }
        #sight::after { content: ''; position: absolute; top: 0; left: 15px; width: 1px; height: 32px; background: #00f0ff; }
        .target-ring { position: absolute; width: 90px; height: 90px; border: 3px dashed #ffea00; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-30px, -30px); }

        /* 🏃 3D ARCADE THREAT STYLING */
        .threat { position: absolute; width: 45px; height: 75px; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; transform-origin: center bottom; will-change: transform, top, left, opacity; transition: transform 0.4s ease-out, top 0.4s ease-out, opacity 0.4s ease-out; }
        .t-head { background: linear-gradient(135deg, #e0a96d, #b57a53); border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #111; position: relative; }
        .t-head::before { content: ''; position: absolute; top: -2px; left: -1px; width: 26px; height: 10px; background: #2b1a08; border-radius: 12px 12px 0 0; }
        .t-eyes { position: absolute; top: 11px; left: 4px; width: 14px; height: 4px; display: flex; justify-content: space-between; }
        .t-eyes::before, .t-eyes::after { content: ''; width: 3.5px; height: 3.5px; background: #000; border-radius: 50%; border-top: 1px solid #ff0000; }
        .t-torso { background: linear-gradient(to right, #1d3557, #457b9d, #1d3557); width: 32px; height: 36px; border-radius: 4px; border: 1.5px solid #111; position: relative; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .t-arm { position: absolute; top: 6px; width: 26px; height: 11px; background: #1d3557; border: 1.5px solid #111; border-radius: 3px; transform-origin: right center; }
        .arm-l { left: -16px; transform: rotate(-15deg); }
        .arm-r { right: -16px; transform: rotate(15deg); transform-origin: left center; }
        .t-weapon { position: absolute; top: -2px; width: 14px; height: 11px; background: linear-gradient(to bottom, #444, #111); border-radius: 2px; border-bottom: 1.5px solid #000; }
        .arm-l .t-weapon { left: -12px; } .arm-r .t-weapon { right: -12px; }
        .t-legs { display: flex; justify-content: space-around; width: 28px; height: 16px; margin-top: auto; }
        .t-leg { background: #212529; width: 9px; height: 100%; border-radius: 2px; border: 1px solid #000; animation: walkCycle 0.22s ease-in-out infinite alternate; }
        .t-leg:nth-child(2) { animation-delay: 0.11s; }
        @keyframes walkCycle { 0% { transform: translateY(0); } 100% { transform: translateY(-5px); } }

        /* 🩸 RAGDOLL SPRAY PARTICLES & BLOOD POOLS */
        .blood-drop { position: absolute; width: 4px; height: 4px; background: #94000d; border-radius: 50%; z-index: 12; pointer-events: none; animation: explodeBlood 0.35s ease-out forwards; }
        @keyframes explodeBlood { 0% { transform: translate(0, 0) scale(1); opacity: 1; } 100% { transform: translate(var(--vx), var(--vy)) scale(0.3); opacity: 0; } }
        .blood-pool { position: absolute; width: 50px; height: 14px; background: radial-gradient(circle, #7a0006 20%, #4a0002 70%, transparent 100%); border-radius: 50%; z-index: 3; pointer-events: none; animation: spreadPool 1s ease-out forwards; }
        @keyframes spreadPool { 0% { transform: scale(0.1); opacity: 0; } 100% { transform: scale(1); opacity: 0.85; } }

        /* HUD Panels */
        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; text-shadow: 0 0 5px #ffea00; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.75); padding: 5px 12px; border-radius: 6px; border: 1px solid #444; }
        #targetTracker { position: absolute; top: 50px; right: 12px; color: #ff3333; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.75); padding: 3px 8px; border-radius: 4px; }

        #overScreen, #winScreen, #intermissionScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
        #overScreen { background: rgba(0,0,0,0.9); }
        #intermissionScreen { background: rgba(0,0,0,0.85); }
        #winScreen { background: linear-gradient(135deg, rgba(29,53,87,0.95), rgba(69,123,157,0.95)); }
        
        .retry-btn { padding: 12px 28px; background: #e63946; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(230,57,70,0.5); }
        .win-btn { padding: 12px 28px; background: #ffea00; color: #000; font-size: 16px; font-weight: 'Arial Black'; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(255,234,0,0.5); }
        .intermission-title { color: #ffea00; font-size: 26px; font-weight: bold; text-shadow: 0 0 10px #ffea00; text-align: center; }
    </style>
</head>
<body>
    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CH. 1: CITY STREETS</div>
        <div id="targetTracker">TARGETS CLEAR: 0/5</div>
        
        <div id="sceneryContainer"></div>
        <div class="roadway"></div>
        
        <div id="car">
            <div class="wheel w-front-l"></div>
            <div class="wheel w-front-r"></div>
            <div class="suv-door door-l"></div> <!-- Left mechanical swinging wing -->
            <div class="window"></div>
            <div class="light-l"></div>
            <div class="light-r"></div>
            <div class="suv-door door-r"></div> <!-- Right mechanical swinging wing -->
            <div class="wheel w-rear-l"></div>
            <div class="wheel w-rear-r"></div>
        </div>

        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div>
            <div class="w-slide"></div>
            <div class="w-frame"></div>
            <div class="w-guard"></div>
            <div class="w-grip"></div>
        </div>

        <div id="overScreen">
            <div style="color:#ffea00; font-size:32px; font-weight:bold; text-shadow:0 0 8px red;">OUTPOST OVERRUN</div>
            <button class="retry-btn" onclick="resetArcadeEngine(true)">REDEPLOY FROM CH. 1 🔄</button>
        </div>

        <div id="intermissionScreen">
            <div class="intermission-title">MISSION ACCOMPLISHED! 🎉</div>
            <button class="win-btn" onclick="advanceToNextChapter()">CONTINUE MISSION ➡️</button>
        </div>

        <div id="winScreen">
            <div style="color:#ffea00; font-size:28px; font-weight:bold; text-shadow: 0 0 10px #ffea00;">👑 CAMPAIGN VICTORY 👑</div>
            <div style="color:white; font-size:15px; text-align:center; margin-top:15px; max-width:300px; line-height:1.5;">CONGRATULATIONS OFFICER!<br>All 8 Sectors cleared and restored to order!</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">PLAY CAMPAIGN AGAIN 🎮</button>
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
        
        if (type === "zap") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.14);
            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.14);
        } else if (type === "ding") {
            osc.type = "sine"; osc.frequency.setValueAtTime(950, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1300, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.08);
        } else if (type === "boom") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(120, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(25, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.45, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.35);
        } else if (type === "level") {
            osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime);
            osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1);
            osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.4);
        } else if (type === "shout_aaa") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(280, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(190, audioCtx.currentTime + 0.28);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.28);
        }
    }

    function aim(e) {
        if (isOver || intermissionScreen.style.display === "flex") return;
        let evt = e.touches ? e.touches[0] : e;
        let bounds = gameArea.getBoundingClientRect();
        currentX = Math.max(-10, Math.min(350, evt.clientX - bounds.left - 16));
        currentY = Math.max(-10, Math.min(450, evt.clientY - bounds.top - 16));
        sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        
        let rotationAngle = (currentX - 168) / 14;
        let horizontalShift = (currentX - 168) / 7;
        let verticalShift = (currentY - 218) / 10;
        weapon.style.transform = `rotate(${rotationAngle}deg) translateX(${horizontalShift}px) translateY(${verticalShift}px)`;
    }

    gameArea.addEventListener("mousemove", aim);
    gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); triggerFire(); } });
        // FIXED: Complete 8-Chapter dictionary table handles independent map layers flawlessly
        // UPDATED CAMPAIGN MATRIX: Explicitly defines whether an environment is an outdoor road layout or indoor/craft zone
    const mapChapters = {
        1: { name: "CITY STREETS", bg: "linear-gradient(to bottom, #4a777a, #a1c4fd 40%, #727d8c 41%, #3a4454)", road: "none", isRoad: true, code: "city" },
        2: { name: "DARK FOREST", bg: "linear-gradient(to bottom, #132a13, #3f5e30 40%, #283618 41%, #061105)", road: "brightness(0.5) sepia(0.4) hue-rotate(50deg)", isRoad: true, code: "tree" },
        3: { name: "CARGO SHIP TARMAC", bg: "linear-gradient(to bottom, #1d2d44, #3e5c76 40%, #0d1b2a 41%, #010813)", road: "brightness(0.4) contrast(1.2)", isRoad: false, code: "ship" },
        4: { name: "COMMERCIAL AIRPLANE", bg: "linear-gradient(to bottom, #74a4bc, #b3d1ff 40%, #ffffff 41%, #d0e1fd)", road: "none", isRoad: false, code: "plane" },
        5: { name: "SHIPPING DOCKS", bg: "linear-gradient(to bottom, #000814, #001d3d 40%, #003566 41%, #001d3d)", road: "brightness(0.4) contrast(1.1)", isRoad: true, code: "docks" },
        6: { name: "HOTEL PENTHOUSE SUITE", bg: "linear-gradient(to bottom, #3a0ca3, #7209b7 40%, #150029 41%, #0a0014)", road: "none", isRoad: false, code: "hotel" },
        7: { name: "HOSPITAL WARD", bg: "linear-gradient(to bottom, #d8f3dc, #b7e4c7 40%, #74c69d 41%, #40916c)", road: "none", isRoad: false, code: "hospital" },
        8: { name: "HUGE SUPERMARKET", bg: "linear-gradient(to bottom, #ffccd5, #ffb3c1 40%, #c9184a 41%, #800f2f)", road: "none", isRoad: false, code: "market" }
    };

    function updateLevelAtmosphere() {
        let meta = mapChapters[activeChapter];
        let maxNeeded = 5 + (activeChapter - 1) * 2;
        chapterTxt.innerText = `CH. ${activeChapter}: ${meta.name}`;
        targetTracker.innerText = `TARGETS CLEAR: ${chapterKills}/${maxNeeded}`;
        gameArea.style.background = meta.bg;
        
        let roadwayEl = document.querySelector(".roadway");
        let carEl = document.getElementById("car");

        // --- ASSET HIDING MECHANICS: HIDES ROAD AND SUV OUTSIDE CHAPTERS 1, 2, AND 5 ---
        if (meta.isRoad) {
            roadwayEl.style.display = "block";
            roadwayEl.style.filter = meta.road;
            carEl.style.display = "block";
        } else {
            roadwayEl.style.display = "none"; // Delete road lane mesh instantly
            carEl.style.display = "none";     // Strip getaway vehicle chassis out completely
        }
        
        sceneryContainer.innerHTML = "";
        
        // Render detailed customized indoor 3D structures based on the map matrix code
        if (meta.code === "city") {
            sceneryContainer.innerHTML = '<div class="b-3d-left"></div><div class="b-3d-right"></div>';
        } else if (meta.code === "tree") {
            sceneryContainer.innerHTML = '<div class="tree-3d" style="left:25px;"><div class="tree-trunk"></div><div class="tree-foliage"></div></div><div class="tree-3d" style="right:25px; bottom:120px;"><div class="tree-trunk"></div><div class="tree-foliage"></div></div>';
        } else if (meta.code === "ship") {
            sceneryContainer.innerHTML = '<div style="position:absolute; bottom:0; left:0; width:100%; height:200px; background:#4f5d75; border-top:6px solid #2d3142; z-index:2;"><div style="width:100%; height:20px; background:#ef8354; margin-top:20px; border-bottom:4px solid #000;"></div></div>';
        } else if (meta.code === "plane") {
            sceneryContainer.innerHTML = '<div style="position:absolute; inset:0; background:repeating-linear-gradient(to right, #e0e1dd 0px, #e0e1dd 30px, #778da9 30px, #778da9 35px); z-index:1;"><div style="position:absolute; top:80px; left:0; width:100%; height:80px; background:linear-gradient(to bottom, #1b263b, transparent); display:flex; justify-content:space-around; align-items:center; padding:0 20px;"><div style="width:25px; height:20px; background:#8ecae6; border-radius:5px 5px 0 0;"></div><div style="width:25px; height:20px; background:#8ecae6; border-radius:5px 5px 0 0;"></div><div style="width:25px; height:20px; background:#8ecae6; border-radius:5px 5px 0 0;"></div></div></div>';
        } else if (meta.code === "docks") {
            sceneryContainer.innerHTML = '<div class="cargo-box" style="left:20px; bottom:120px;"><div class="cargo-ribs"></div></div><div class="cargo-box" style="right:15px; bottom:140px; background:linear-gradient(135deg,#005f73,#0a9396);"><div class="cargo-ribs"></div></div>';
        } else if (meta.code === "hotel") {
            sceneryContainer.innerHTML = '<div style="position:absolute; inset:0; background:#3d0066; z-index:1;"><div style="position:absolute; bottom:0; left:10%; width:80%; height:120px; background:#e0a96d; border-radius:8px 8px 0 0; border:4px solid #1a0033;"><div style="width:100%; height:30px; background:#fff; border-bottom:2px solid #000;"></div></div></div>';
        } else if (meta.code === "hospital") {
            sceneryContainer.innerHTML = '<div style="position:absolute; inset:0; background:#f4f9f4; z-index:1;"><div style="position:absolute; bottom:100px; left:30px; width:65px; height:45px; background:#fff; border:2px solid #95d5b2; border-radius:4px; box-shadow:0 6px 12px rgba(0,0,0,0.1);"><div style="width:10px; height:45px; background:#74c69d; float:left;"></div></div></div>';
        } else if (meta.code === "market") {
            sceneryContainer.innerHTML = '<div style="position:absolute; inset:0; background:#fffdf7; z-index:1;"><div class="shelf-3d" style="left:15px; bottom:20px;"><div class="shelf-row"></div><div class="shelf-row"></div></div><div class="shelf-3d" style="right:15px; bottom:20px;"><div class="shelf-row"></div><div class="shelf-row"></div></div></div>';
        }
    }


    function updateLevelAtmosphere() {
        let meta = mapChapters[activeChapter];
        let maxNeeded = 5 + (activeChapter - 1) * 2;
        chapterTxt.innerText = `CH. ${activeChapter}: ${meta.name}`;
        targetTracker.innerText = `TARGETS CLEAR: ${chapterKills}/${maxNeeded}`;
        gameArea.style.background = meta.bg;
        document.querySelector(".roadway").style.filter = meta.road;
        
        // FIXED: Clear out former elements before painting alternative 3D projections
        sceneryContainer.innerHTML = "";
        if (meta.code === "city") {
            sceneryContainer.innerHTML = '<div class="b-3d-left"></div><div class="b-3d-right"></div>';
        } else if (meta.code === "tree") {
            sceneryContainer.innerHTML = '<div class="tree-3d" style="left:25px;"><div class="tree-trunk"></div><div class="tree-foliage"></div></div><div class="tree-3d" style="right:25px; bottom:120px;"><div class="tree-trunk"></div><div class="tree-foliage"></div></div>';
        } else if (meta.code === "docks") {
            sceneryContainer.innerHTML = '<div class="cargo-box" style="left:20px; bottom:120px;"><div class="cargo-ribs"></div></div><div class="cargo-box" style="right:15px; bottom:140px; background:linear-gradient(135deg,#005f73,#0a9396);"><div class="cargo-ribs"></div></div>';
        } else if (meta.code === "market") {
            sceneryContainer.innerHTML = '<div class="shelf-3d" style="left:15px; bottom:110px;"><div class="shelf-row"></div><div class="shelf-row"></div></div><div class="shelf-3d" style="right:15px; bottom:110px;"><div class="shelf-row"></div><div class="shelf-row"></div></div>';
        } else if (meta.code === "hospital") {
            sceneryContainer.innerHTML = '<div style="position:absolute; bottom:120px; left:25px; width:55px; height:35px; background:#fff; border:2px solid #bbb; border-radius:4px; z-index:3; box-shadow:0 6px 12px rgba(0,0,0,0.15);"></div>';
        } else if (meta.code === "carnival") {
            sceneryContainer.innerHTML = '<div style="position:absolute; top:40px; left:50%; transform:translateX(-50%); color:#fff; font-size:11px; letter-spacing:4px; text-shadow:0 0 8px #ff00ff; z-index:2;">★ CARNIVAL ★</div>';
        }
    }

    function spawnBloodSpit(x, y) {
        for (let i = 0; i < 10; i++) {
            let drop = document.createElement("div"); drop.className = "blood-drop";
            drop.style.left = x + "px"; drop.style.top = y + "px";
            let vx = (Math.random() * 50 - 25); let vy = (Math.random() * -40 - 5);
            drop.style.setProperty('--vx', vx + 'px'); drop.style.setProperty('--vy', vy + 'px');
            gameArea.appendChild(drop);
            setTimeout(() => drop.remove(), 350);
        }
        let pool = document.createElement("div"); pool.className = "blood-pool";
        pool.style.left = (x - 25) + "px"; pool.style.top = (y + 25) + "px";
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
                t.el.style.transform += " rotate(85deg)"; 
                t.el.style.top = (parseFloat(t.el.style.top) + 25) + "px"; 
                
                // Chapter 6 Hotel: Shifts viewpoint target lanes on impact
                if(mapChapters[activeChapter].code === "hotel") {
                    setTimeout(() => { carPos = Math.random() * 80 + 70; }, 150);
                }

                if (chapterKills >= maxNeeded) {
                    clearInterval(spawnTimerId); clearInterval(physicsTimerId);
                    if (activeChapter >= 8) { winScreen.style.display = "flex"; return; }
                    sound("level");
                    intermissionScreen.style.display = "flex";
                }
            }
        });
    }

    function runEngineLoops() {
                // 1. Core Scenery & Target Pin Synchronization 3D Loop
        physicsTimerId = setInterval(() => {
            if (isOver) return;
            
            let meta = mapChapters[activeChapter];

            if (meta.isRoad) {
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
            } else {
                // If it is an indoor room layout or craft deck, bypass car movement tracking entirely
                carParked = true;
                distanceScale = 1.0; // Force full sizing scale on room targets instantly
            }

            let currentTopY = 165 + (distanceScale * 45);

            threatsList.forEach((t) => {
                if (t.isDying) return;
                
                // Map coordinates adapt flawlessly depending on outdoor road speeds or stationary rooms
                let updatedX = meta.isRoad ? (carPos + (t.sideOffset * distanceScale)) : (140 + t.sideOffset);
                let threatY = meta.isRoad ? (currentTopY + (t.baseTopY - 195) * distanceScale) : t.baseTopY;
                
                t.el.style.transform = `scale(${distanceScale})`;
                t.el.style.left = updatedX + "px"; 
                t.el.style.top = threatY + "px";
                
                t.ring.style.width = (90 * (1.3 - (t.age / 40))) + "px";
                t.ring.style.height = (90 * (1.3 - (t.age / 40))) + "px";
                let rSize = 90 * (1.3 - (t.age / 40));
                t.ring.style.left = (updatedX + (20 * distanceScale) - (rSize / 2) + 15) + "px";
                t.ring.style.top = (threatY + (15 * distanceScale) - (rSize / 2) + 30) + "px";
                t.age += 1;
            });
        }, 30);


                 spawnTimerId = setInterval(() => {
            // FIXED: Automatically scales the maximum simultaneous screen capacity relative to the level formula!
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
        activeChapter += 1; 
        chapterKills = 0;
        intermissionScreen.style.display = "none";
        clearDeadBodiesAndBlood();
        resetArcadeEngine(false);
    };

    window.resetArcadeEngine = function(resetFullCampaign) {
        clearInterval(spawnTimerId); 
        clearInterval(physicsTimerId);
        clearDeadBodiesAndBlood();
        
        if (resetFullCampaign) { 
            score = 200; 
            activeChapter = 1; 
            chapterKills = 0; 
            scoreCounter.innerText = "00200"; 
        }
        
        updateLevelAtmosphere();
        isOver = false; 
        distanceScale = 0.2; 
        carParked = false;
        car.classList.remove("parked-open"); // Seal wings on drive boot
        carPos = Math.random() * 80 + 70;
        
        sight.style.left = "168px"; 
        sight.style.top = "218px";
        weapon.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
        overScreen.style.display = "none"; 
        winScreen.style.display = "none";
        
        runEngineLoops();
    };

    updateLevelAtmosphere();
    runEngineLoops();
</script>
</body>
</html>
'''

components.html(game_html, height=560)




