import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Virtua Tactical: Hampi Jericho Chronicles", layout="centered")
st.title("⚡ Virtua Tactical: Hampi Jericho - Chapter 2 Infiltration")

game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        #gameArea { 
            position: relative; width: 380px; height: 480px; 
            background: #010206; border: 4px solid #1e293b; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none;
            box-shadow: 0 24px 60px rgba(0,0,0,0.95);
        }

        /* 🎬 FILM GRAIN + CRITICAL PULSE DAMAGE LENS VIGNETTE */
        #gameArea::after {
            content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 28;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://w3.org id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.065'/%3E%3C/svg%3E");
            background-size: auto;
            box-shadow: inset 0 0 90px rgba(0, 0, 0, 0.95), inset 0 0 160px rgba(0, 0, 0, 0.85);
            background-color: rgba(220, 20, 20, 0);
            transition: box-shadow 0.12s ease-out, background-color 0.12s ease-out;
        }

        #gameArea.taking-damage::after {
            background-color: rgba(220, 20, 20, 0.26);
            box-shadow: inset 0 0 120px rgba(220, 20, 20, 0.98), inset 0 0 200px rgba(180, 0, 0, 0.98);
        }
        #gameArea.critical-pulse::after { animation: fullViewportLowHpPulse 0.5s ease-in-out infinite alternate; }
        @keyframes fullViewportLowHpPulse {
            0% { background-color: rgba(220, 20, 20, 0.04); box-shadow: inset 0 0 90px rgba(160, 0, 0, 0.75); }
            100% { background-color: rgba(220, 20, 20, 0.28); box-shadow: inset 0 0 130px rgba(254, 0, 0, 0.98), inset 0 0 190px rgba(180, 0, 0, 0.9); }
        }

        canvas { position: absolute; top: 0; left: 0; width: 380px; height: 480px; z-index: 1; }
        #weapon { position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%) scale(1.1); width: 100px; height: 160px; pointer-events: none; z-index: 25; will-change: transform; display: none; }
        .w-slide { position: absolute; top: 40px; left: 24px; width: 52px; height: 50px; background: linear-gradient(to right, #09090b 0%, #27272a 30%, #18181b 50%, #27272a 70%, #09090b 100%); border-radius: 6px 6px 2px 2px; border-top: 1.5px solid #52525b; box-shadow: 0 16px 30px rgba(0,0,0,0.9), inset 0 2px 4px rgba(255,255,255,0.12); }
        .w-holo-sight { position: absolute; top: 2px; left: 29px; width: 42px; height: 38px; border: 3.5px solid #27272a; border-bottom: none; border-radius: 6px 6px 0 0; background: linear-gradient(to bottom, rgba(0,240,255,0.15), rgba(0,240,255,0.03)); box-shadow: inset 0 0 10px rgba(0,240,255,0.2); }
        .w-holo-sight::after { content: ''; position: absolute; bottom: 5px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: #ff0055; border-radius: 50%; box-shadow: 0 0 12px 3px #ff0055; }
        .w-grip-back { position: absolute; top: 90px; left: 32px; width: 36px; height: 70px; background: linear-gradient(to right, #09090b, #18181b, #020202); border-radius: 3px; }
        #flash { position: absolute; top: 12px; left: 26px; width: 48px; height: 48px; background: radial-gradient(circle, #ffffff 20%, #ff4500 55%, transparent 85%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 12px #ff4500); }

        .target-ring { position: absolute; border: 3px dashed #ff2266; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-50%, -50%); display: block; box-shadow: 0 0 12px #ff2266; opacity: 0; transition: opacity 0.15s ease; }
        #sight { position: absolute; width: 32px; height: 32px; border: 2px solid #00f0ff; border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); z-index: 20; box-shadow: 0 0 10px #00f0ff; display: none; }

        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.88); padding: 4px 14px; border-radius: 6px; border: 2px solid #3f3f46; text-shadow: 0 0 6px #ffea00; display: none; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-family: sans-serif; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.88); padding: 6px 12px; border-radius: 6px; border: 1px solid #3f3f46; letter-spacing: 1px; display: none; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3366; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.88); padding: 3px 8px; border-radius: 4px; display: none; }
        #healthCounter { position: absolute; bottom: 12px; left: 12px; color: #ff3355; font-weight: bold; font-family: 'Courier New', monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.92); padding: 5px 12px; border-radius: 4px; border: 2px solid #ef4444; text-shadow: 0 0 5px #ff0000; display: none; }

        #overScreen, #winScreen { position: absolute; inset: 0; background: rgba(2, 6, 23, 0.94); z-index: 40; display: none; flex-direction: column; align-items: center; justify-content: center; }
        .retry-btn, .win-btn { margin-top: 20px; padding: 10px 24px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; }
        .win-btn { background: #eab308; color: #020617; }

        #chapterOverlay { position: absolute; inset: 0; background: #000000; z-index: 49; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    <div id="gameArea">
        <!-- 🎬 CHAPTER TWO INTERMISSION DIVISIONS -->
        <div id="chapterOverlay">
            <div id="overlayChapterTitle" style="color:white; font-family:monospace; font-size:18px; font-weight:bold; letter-spacing:3px;">CHAPTER 2</div>
            <div id="overlayChapterSubtitle" style="color:#eab308; font-family:sans-serif; font-size:11px; margin-top:5px; letter-spacing:1px; text-transform: uppercase;">AIRPORT TERMINAL & AIRCRAFT RECOVERY</div>
        </div>
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CH 2: INTERNATIONAL TERMINAL</div>
        <div id="targetTracker">SECTOR K: 0/4</div>
        <div id="healthCounter">HP: 100</div>
        
        <canvas id="gameCanvas" width="380" height="480"></canvas>
        
        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div> <div class="w-slide"></div> <div class="w-holo-sight"></div> <div class="w-grip-back"></div>
        </div>

        <div id="overScreen">
            <div style="color:#ef4444; font-size:32px; font-weight:bold; text-shadow:0 0 12px #000; font-family:monospace; letter-spacing:1px;">MISSION FAILURE</div>
            <div id="finalScore" style="color:white; font-size:16px; margin-top:10px;">Final Score Log: 200</div>
            <button class="retry-btn" onclick="resetArcadeEngine(true)">REDEPLOY OPERATIVE 🔄</button>
        </div>

        <div id="winScreen">
            <div style="color:#eab308; font-size:26px; font-weight:bold; text-shadow: 0 0 12px #eab308; text-align:center;">✈️ CAMPAIGN COMPLETE ✈️</div>
            <div style="color:white; font-size:13px; text-align:center; margin-top:15px; max-width:320px; line-height:1.5;">EXCELLENT WORK JERICHO!<br>Flight deck secured and hostage cells released!</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">REPLAY CAMPAIGN 🎮</button>
        </div>
    </div>

<script>
    let currentX = 190, currentY = 240, score = 200, isOver = false;
    let threatsList = []; let playerHp = 100;
    let spawnTimerId = null, runLoopTimerId = null, heartbeatIntervalId = null;
    let audioCtx = null;

    let currentChapter = 2; // Fixed on Chapter 2 state boundaries
    let currentSector = "K"; let sectorKills = 0;
    
    // 🎬 DEFINED: 10 SEPARATE SECTORS FOR THE AIRPORT & AIRCRAFT FLIGHT DECK
    const sectorsList = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"];
    const sectorRequirements = { 
        "K":4, "L":4, "M":4, "N":4, // Airport Main Terminal Tracks
        "O":5,                       // Boarding Skybridge Pipeline
        "P":5, "Q":5, "R":5, "S":5, // Inside the Passenger Cabin
        "T":6                        // Flight Deck / Cockpit Breach Door
    };

    let isMoving = false;
    let perspectiveMode3rdPerson = false; 
    let cameraFlyInProgressDist = 1.5; 

    const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
    let cameraZ = 0, targetCameraZ = 0; let cameraX = 0, targetCameraX = 0; let cycleTick = 0;
    function setupAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }

    function sound(type) {
        setupAudio(); if (!audioCtx) return; let osc = audioCtx.createOscillator(), gain = audioCtx.createGain(); osc.connect(gain); gain.connect(audioCtx.destination);
        if (type === "zap") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(620, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.14); gain.gain.setValueAtTime(0.35, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.14); }
        else if (type === "ding") { osc.type = "sine"; osc.frequency.setValueAtTime(1050, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(1450, audioCtx.currentTime + 0.08); gain.gain.setValueAtTime(0.18, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.08); }
        else if (type === "boom") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(120, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(15, audioCtx.currentTime + 0.4); gain.gain.setValueAtTime(0.45, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        else if (type === "level") { osc.type = "sine"; osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); osc.frequency.setValueAtTime(698.46, audioCtx.currentTime + 0.1); osc.frequency.setValueAtTime(880.00, audioCtx.currentTime + 0.2); gain.gain.setValueAtTime(0.2, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        else if (type === "bullet_crack") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(220, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(40, audioCtx.currentTime + 0.1); gain.gain.setValueAtTime(0.25, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.1); }
        else if (type === "heartbeat") { osc.type = "sine"; osc.frequency.setValueAtTime(55, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.2); gain.gain.setValueAtTime(0.4, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.2); }
    }
    function project3D(x, y, z) {
        let relativeX = x - cameraX;
        let activePerspectiveZ = z - cameraZ;
        
        if (activePerspectiveZ <= 0.1) return null;
        let fovScale = 400 / activePerspectiveZ;
        return { x: 190 + (relativeX * fovScale), y: 240 - ((y - 1.6) * fovScale), size: fovScale };
    }

    function render3DSceneGrid() {
        if (document.getElementById("chapterOverlay").style.display === "flex") return;

        cycleTick += 0.05; cameraZ += (targetCameraZ - cameraZ) * 0.07; cameraX += (targetCameraX - cameraX) * 0.07;
        if (isMoving && Math.abs(cameraZ - targetCameraZ) < 0.1) { isMoving = false; }
        
        if (!spawnTimerId && !isOver) {
            spawnTimerId = setInterval(spawn3DThreatUnit, 1300);
        }
        // --- 🛫 STAGE REGISTRY: CALCULATE GEOMETRY PHASES ---
        let isSkybridge = (currentSector === "O");
        let isInsideAircraft = ["P", "Q", "R", "S", "T"].includes(currentSector);

        if (!isInsideAircraft) {
            // A: Deep Dark Apron Terminal Horizon Sky
            let skyGrd = ctx.createLinearGradient(0, 0, 0, 240);
            skyGrd.addColorStop(0, "#010104"); skyGrd.addColorStop(0.7, "#03040f"); skyGrd.addColorStop(1, "#0a0a16");
            ctx.fillStyle = skyGrd; ctx.fillRect(0, 0, 380, 240);
            
            // B: Twinkling Airfield Tower Beacons
            ctx.fillStyle = "rgba(255,255,255,0.8)";
            for (let i = 1; i <= 15; i++) {
                let starX = (i * 97) % 380; let starY = (i * 23) % 150;
                let pulse = Math.abs(Math.sin(cycleTick + i)) * 1.5;
                ctx.fillRect(starX, starY, pulse, pulse);
            }
            
            // C: Distant Hangar Outlines
            ctx.fillStyle = "#05070e";
            ctx.fillRect(40 - (cameraX * 15), 210, 80, 30);
            ctx.fillRect(260 - (cameraX * 15), 215, 90, 25);
        } else {
            // Commercial Aircraft Interior Background
            ctx.fillStyle = "#0c0f14"; ctx.fillRect(0, 0, 380, 480);
        }

        // --- 🏗️ PERSPECTIVE RUNWAY & CABIN PAVEMENT LOOPS ---
        for (let z = 84; z >= 0; z -= 3) {
            let zPos = Math.floor(cameraZ) + z; zPos = zPos - (zPos % 3);
            let pNear = project3D(0, 0, zPos); let pFar = project3D(0, 0, zPos + 3); if (!pNear || !pFar) continue;
            let fogOpacity = Math.min(1, z / 65); let lightScale = 1 - fogOpacity;
            
            // Floor coloration changes dynamically depending on tarmac vs cabin carpet states
            let floorColor = "rgba(" + Math.floor(22 * lightScale) + "," + Math.floor(26 * lightScale) + "," + Math.floor(35 * lightScale) + ",1)";
            if (isInsideAircraft) {
                floorColor = "rgba(" + Math.floor(16 * lightScale) + "," + Math.floor(24 * lightScale) + "," + Math.floor(48 * lightScale) + ",1)"; // Aisle Blue Carpet
            }
            ctx.fillStyle = floorColor; ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            
            // Draw realistic center taxiway lines / carpet guiding grids
            ctx.strokeStyle = isInsideAircraft ? "rgba(234, 179, 8, 0.15)" : "rgba(234, 179, 8, 0.45)";
            ctx.lineWidth = Math.max(1, pNear.size * 0.02);
            ctx.beginPath(); ctx.moveTo(190, 240 + (1.6 * pNear.size)); ctx.lineTo(190, 240 + (1.6 * pFar.size)); ctx.stroke();
            // --- 🛫 DETAILED STRUCTURAL SIDE PANEL PAINTERS ---
            let isRidgeFold = Math.floor(zPos * 2.5) % 2 === 0;
            
            if (isInsideAircraft) {
                // Curved White Airplane Fuselage Ribs
                ctx.fillStyle = "rgba(" + Math.floor(140*lightScale) + "," + Math.floor(145*lightScale) + "," + Math.floor(155*lightScale) + ",1)";
                ctx.beginPath(); ctx.moveTo(190 - (2.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.quadraticCurveTo(190 - (4.5 * pNear.size), 240 - (0.5 * pNear.size), 190 - (3.5 * pNear.size), 240 - (2.4 * pNear.size));
                ctx.lineTo(190 - (3.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.quadraticCurveTo(190 - (4.5 * pFar.size), 240 - (0.5 * pFar.size), 190 - (2.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
                
                ctx.beginPath(); ctx.moveTo(190 + (2.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.quadraticCurveTo(190 + (4.5 * pNear.size), 240 - (0.5 * pNear.size), 190 + (3.5 * pNear.size), 240 - (2.4 * pNear.size));
                ctx.lineTo(190 + (3.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.quadraticCurveTo(190 + (4.5 * pFar.size), 240 - (0.5 * pFar.size), 190 + (2.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            } 
            else if (isSkybridge) {
                // Glass Boarding Tube Window Framework
                ctx.fillStyle = "rgba(6, 182, 212, " + (0.12 * lightScale) + ")";
                ctx.fillRect(190 - (4.5 * pNear.size), 240 - (2.4 * pNear.size), 1.5 * pNear.size, 4.0 * pNear.size);
                ctx.fillRect(190 + (3.0 * pNear.size), 240 - (2.4 * pNear.size), 1.5 * pNear.size, 4.0 * pNear.size);
                ctx.strokeStyle = "rgba(100, 116, 139, 0.4)"; ctx.strokeRect(190 - (4.5 * pNear.size), 240 - (2.4 * pNear.size), 1.5 * pNear.size, 4.0 * pNear.size);
                ctx.strokeRect(190 + (3.0 * pNear.size), 240 - (2.4 * pNear.size), 1.5 * pNear.size, 4.0 * pNear.size);
            } 
            else {
                // Silver Airport Runway Terminal Terminal Gate Blocks
                ctx.fillStyle = "rgba(" + (isRidgeFold ? Math.floor(70*lightScale) : Math.floor(90*lightScale)) + "," + (isRidgeFold ? Math.floor(75*lightScale) : Math.floor(95*lightScale)) + "," + (isRidgeFold ? Math.floor(85*lightScale) : Math.floor(105*lightScale)) + ",1)";
                ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 - (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
                ctx.beginPath(); ctx.moveTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            }
        }
        let depthDrawQueue = [];
        staticAirportObstacles.forEach(b => {
            // Render luggage bins inside terminal, and airplane row clusters inside cabin
            if (isInsideAircraft && !b.isCabinAsset) return;
            if (!isInsideAircraft && b.isCabinAsset) return;
            if (b.z >= cameraZ) depthDrawQueue.push({ type: "crate", z: b.z, data: b });
        });
        threatsList.forEach(t => { if (!t.isDying && t.z >= cameraZ) depthDrawQueue.push({ type: "enemy", z: t.z, data: t }); });
        depthDrawQueue.sort((a, b) => b.z - a.z);

        depthDrawQueue.forEach(item => {
            if (item.type === "crate") {
                let b = item.data; let p = project3D(b.x, b.y, b.z); if (!p) return; let w = b.w * p.size; let h = b.h * p.size;
                ctx.fillStyle = b.baseColor; ctx.fillRect(p.x - w/2, p.y - h/2, w, h); ctx.fillStyle = b.shadowColor; ctx.fillRect(p.x - w/2 + (w*0.08), p.y - h/2 + (h*0.08), w * 0.84, h * 0.84);
                ctx.strokeStyle = "rgba(0,0,0,0.5)"; ctx.lineWidth = Math.max(1, p.size * 0.02); ctx.strokeRect(p.x - w/2, p.y - h/2, w, h);
            } 
            else if (item.type === "enemy") {
                let t = item.data; if (!isMoving) t.loopTick++;
                let smoothSinPeekFactor = (Math.sin(t.loopTick * 0.05) + 1) / 2; let isActivelyOut = (smoothSinPeekFactor > 0.45); 
                let p = project3D(t.x, t.y, t.z); if (!p) return; let s = p.size * 0.4;
                let currentVisualX = p.x - (s * 1.5) + (s * 1.5 * smoothSinPeekFactor);
                t.currentScreenX = currentVisualX; t.currentScreenY = p.y - (s * 0.5); t.currentRadius = s * 1.15;

                if (isActivelyOut) { t.ring.style.opacity = "1"; t.age++; } else { t.ring.style.opacity = "0"; }
                if (t.age > 0 && t.age % 42 === 0 && !isMoving && isActivelyOut) { t.isFlashing = true; triggerEnemyDamageStrike(); setTimeout(() => { t.isFlashing = false; }, 70); }

                // Hijackers wear grey urban camouflage vests inside terminal tracks
                ctx.fillStyle = isInsideAircraft ? "#1e1b4b" : "#343a40";
                ctx.fillRect(currentVisualX - s/2, p.y - s, s, s * 1.3); ctx.strokeStyle = "#000"; ctx.lineWidth = 1.5; ctx.strokeRect(currentVisualX - s/2, p.y - s, s, s * 1.3);
                ctx.fillStyle = "#212529"; ctx.fillRect(currentVisualX - s/3, p.y - s * 0.9, s * 0.66, s * 0.7);
                ctx.fillStyle = "#e0a96d"; ctx.beginPath(); ctx.arc(currentVisualX, p.y - s * 1.3, s * 0.35, 0, Math.PI*2); ctx.fill(); ctx.stroke();
                ctx.fillStyle = "#1c1d21"; ctx.beginPath(); ctx.arc(currentVisualX, p.y - s * 1.4, s * 0.36, Math.PI, 0); ctx.fill(); ctx.stroke();
                ctx.fillRect(currentVisualX - s/3, p.y + s * 0.3, s * 0.22, s * 0.8); ctx.fillRect(currentVisualX + s/8, p.y + s * 0.3, s * 0.22, s * 0.8);
                ctx.fillStyle = "#ffc107"; ctx.fillRect(currentVisualX + s/6, p.y - s/3, s * 0.75, s * 0.18);

                if (t.isFlashing && isActivelyOut) { let flashGrd = ctx.createRadialGradient(currentVisualX + s * 0.9, p.y - s/4, 1, currentVisualX + s * 0.9, p.y - s/4, s * 0.55); flashGrd.addColorStop(0, "#ffffff"); flashGrd.addColorStop(0.5, "#ffc107"); flashGrd.addColorStop(1, "transparent"); ctx.fillStyle = flashGrd; ctx.beginPath(); ctx.arc(currentVisualX + s * 0.9, p.y - s/4, s * 0.55, 0, Math.PI*2); ctx.fill(); ctx.closePath(); }
                
                t.ring.style.left = currentVisualX + "px"; t.ring.style.top = (p.y - s/2) + "px"; 
                let dynamicCircleRadius = Math.max(14, Math.min(110, 95 * (1.3 - (t.age / 40)))); 
                t.ring.style.width = dynamicCircleRadius + "px"; t.ring.style.height = dynamicCircleRadius + "px";
            }
        });
    }
    function aim(e) {
        if (isOver || document.getElementById("chapterOverlay").style.display === "flex") return;
        let evt = e; if (e.touches && e.touches.length > 0) { evt = e.touches; } else if (e.changedTouches && e.changedTouches.length > 0) { evt = e.changedTouches; }
        let bounds = gameArea.getBoundingClientRect(); currentX = evt.clientX - bounds.left; currentY = evt.clientY - bounds.top;
        
        let mappedThreatZ = 12; threatsList.forEach(t => { if(!t.isDying) mappedThreatZ = t.z - cameraZ; });
        let dynamicallyAdjustedSize = Math.max(16, Math.min(60, (400 / mappedThreatZ) * 0.95));
        sight.style.width = dynamicallyAdjustedSize + "px"; sight.style.height = dynamicallyAdjustedSize + "px";
        
        sight.style.display = "block"; sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        let swayX = (currentX - 190) / 10; let swayY = (currentY - 240) / 12;
        weapon.style.transform = "translateX(-50%) scale(1.1) rotate(" + swayX + "deg) translateY(" + swayY + "px)";
    }
    gameArea.addEventListener("mousemove", aim);
    gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });

    function triggerMouseCoordinateFire(e) {
        setupAudio(); 
        let bounds = gameArea.getBoundingClientRect();
        currentX = e.clientX - bounds.left; currentY = e.clientY - bounds.top;
        triggerFire();
    }
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerMouseCoordinateFire(e); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); setupAudio(); aim(e); triggerFire(); } }, { passive: false });

    function triggerSectorPathMovement() {
        if (isMoving) return; isMoving = true;
        let idx = sectorsList.indexOf(currentSector);
        
        if (idx >= 0 && idx < sectorsList.length - 1) {
            currentSector = sectorsList[idx + 1]; sectorKills = 0; targetCameraZ = (idx + 1) * 16;
            let rollingPathRoll = Math.random();
            if (rollingPathRoll < 0.33) { targetCameraX = -1.5; } else if (rollingPathRoll < 0.66) { targetCameraX = 1.5; } else { targetCameraX = 0.0; }
            
            // Dynamic text updates matching realistic airport structural layers
            if (["K","L","M","N"].includes(currentSector)) { document.getElementById("chapterTxt").innerText = "CH 2: INTERNATIONAL TERMINAL TARMAC"; }
            else if (currentSector === "O") { document.getElementById("chapterTxt").innerText = "CH 2: BOARDING JET-BRIDGE TUBE"; }
            else if (["P","Q","R","S"].includes(currentSector)) { document.getElementById("chapterTxt").innerText = "CH 2: RECOVREING PASSENGER CABIN"; }
            else if (currentSector === "T") { document.getElementById("chapterTxt").innerText = "CH 2: FLIGHT DECK COMMAND BREACH"; }
        } else {
            clearInterval(spawnTimerId); clearInterval(runLoopTimerId); isOver = true;
            if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
            document.getElementById("winScreen").style.display = "flex"; return;
        }
        let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
        sound("level");
    }
    function triggerEnemyDamageStrike() {
        if (isOver || document.getElementById("winScreen").style.display === "flex" || isMoving || document.getElementById("chapterOverlay").style.display === "flex") return;
        playerHp -= 20; if (playerHp < 0) playerHp = 0; healthCounter.innerText = `HP: ${playerHp}`; sound("bullet_crack");
        gameArea.classList.add("taking-damage"); setTimeout(() => gameArea.classList.remove("taking-damage"), 130);
        if (playerHp <= 20 && !heartbeatIntervalId) { gameArea.classList.add("critical-pulse"); heartbeatIntervalId = setInterval(() => { sound("heartbeat"); }, 550); }
        if (playerHp <= 0) { isOver = true; sound("boom"); clearInterval(spawnTimerId); clearInterval(runLoopTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); gameArea.classList.remove("critical-pulse"); heartbeatIntervalId = null; } finalScore.innerText = "Final Score Log: " + score; overScreen.style.display = "flex"; }
    }

    function triggerFire() {
        if (isOver || document.getElementById("winScreen").style.display === "flex" || isMoving || document.getElementById("chapterOverlay").style.display === "flex") return;
        sound("zap"); flash.style.display = "block"; setTimeout(() => { flash.style.display = "none"; }, 60);
        let hitTarget = null; let lowestDistance = Infinity;
        threatsList.forEach(t => {
            if (t.isDying) return;
            let d = Math.hypot(currentX - t.currentScreenX, currentY - t.currentScreenY);
            if (d < t.currentRadius && d < lowestDistance) { lowestDistance = d; hitTarget = t; }
        });
        if (hitTarget) {
            hitTarget.isDying = true; sound("boom"); score += 150; scoreCounter.innerText = String(score).padStart(5, '0'); sectorKills += 1;
            let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
            hitTarget.ring.remove(); threatsList = threatsList.filter(item => item !== hitTarget);
            if (sectorKills >= needed) { document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = []; setTimeout(triggerSectorPathMovement, 400); }
        }
    }

    // Mapped Stationary Airport Luggage Carts & Airplane Blue Seats
    const staticAirportObstacles = [
        { id: "a1", x: -2.0, y: 0.5, z: 15, w: 1.8, h: 1.5, baseColor: "#475569", shadowColor: "#334155", isCabinAsset: false },
        { id: "a2", x: 2.1, y: 0.5, z: 32, w: 1.9, h: 2.0, baseColor: "#cbd5e1", shadowColor: "#94a3b8", isCabinAsset: false },
        { id: "a3", x: -2.2, y: 0.5, z: 48, w: 1.8, h: 1.6, baseColor: "#475569", shadowColor: "#334155", isCabinAsset: false },
        { id: "p1", x: -2.3, y: 0.7, z: 12, w: 1.2, h: 2.4, baseColor: "#1d4ed8", shadowColor: "#1e3a8a", isCabinAsset: true }, // Airplane Seats Aisle Left
        { id: "p2", x: 2.3, y: 0.7, z: 26, w: 1.2, h: 2.4, baseColor: "#1d4ed8", shadowColor: "#1e3a8a", isCabinAsset: true }  // Airplane Seats Aisle Right
    ];

    function spawn3DThreatUnit() {
        if (isOver || threatsList.length >= 2 || isMoving || document.getElementById("winScreen").style.display === "flex" || document.getElementById("chapterOverlay").style.display === "flex") return;
        let idx = sectorsList.indexOf(currentSector); let spawnZ = cameraZ + 12 + (idx * 0.5); let spawnX = cameraX + (Math.random() * 2.4) - 1.2;
        let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);
        threatsList.push({ x: spawnX, y: 0.2, z: spawnZ, age: 0, loopTick: Math.floor(Math.random()*60), isDying: false, isFlashing: false, ring: ring, currentScreenX: 0, currentScreenY: 0, currentRadius: 24 });
        sound("ding");
    }

    function initializeActiveArcadeGameplay() {
        document.getElementById("chapterOverlay").style.display = "none";
        document.getElementById("scoreCounter").style.display = "block";
        document.getElementById("chapterTxt").style.display = "block";
        document.getElementById("targetTracker").style.display = "block";
        document.getElementById("healthCounter").style.display = "block";
        document.getElementById("sight").style.display = "block";
        document.getElementById("weapon").style.display = "block";
        runLoopTimerId = setInterval(render3DSceneGrid, 1000 / 45);
    }

    window.resetArcadeEngine = function(fullReset) {
        if (spawnTimerId) { clearInterval(spawnTimerId); spawnTimerId = null; }
        clearInterval(runLoopTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
        document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = [];
        cameraZ = 0; targetCameraZ = 0; cameraX = 0; targetCameraX = 0; currentSector = "K"; sectorKills = 0; playerHp = 100; score = 200; isMoving = false; isOver = false;
        document.getElementById("winScreen").style.display = "none"; document.getElementById("overScreen").style.display = "none";
        gameArea.className = ""; healthCounter.innerText = "HP: 100"; scoreCounter.innerText = "00200"; document.getElementById("chapterTxt").innerText = "CH 2: INTERNATIONAL TERMINAL";
        let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
        
        document.getElementById("chapterOverlay").style.display = "flex";
        document.getElementById("scoreCounter").style.display = "none";
        document.getElementById("chapterTxt").style.display = "none";
        document.getElementById("targetTracker").style.display = "none";
        document.getElementById("healthCounter").style.display = "none";
        document.getElementById("sight").style.display = "none";
        document.getElementById("weapon").style.display = "none";
        setTimeout(initializeActiveArcadeGameplay, 3000);
    };

    setTimeout(initializeActiveArcadeGameplay, 3000);
</script>
</body>
</html>
'''

cb_id = random.randint(100000, 999999)
st.markdown(f'<!-- Airport Vector Injector Anchor ID: {cb_id} -->', unsafe_allow_html=True)
components.html(game_html, height=560, scrolling=False)
