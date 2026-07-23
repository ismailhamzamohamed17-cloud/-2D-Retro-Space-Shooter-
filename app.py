import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Virtua Tactical: Hampi Jericho Chronicles", layout="centered")
st.title("⚡ Virtua Tactical: Hampi Jericho Campaign")

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
        #chapterOverlay { position: absolute; inset: 0; background: #000000; z-index: 49; display: flex; flex-direction: column; align-items: center; justify-content: center; }

        /* --- 🎯 DISPLAY VISIBILITY FIXED PERMANENTLY TO PREVENT IFRAME DROPOUT CRASHES --- */
        #weapon { position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%) scale(1.1); width: 100px; height: 160px; pointer-events: none; z-index: 25; will-change: transform; display: block; }
        .w-slide { position: absolute; top: 40px; left: 24px; width: 52px; height: 50px; background: linear-gradient(to right, #09090b 0%, #27272a 30%, #18181b 50%, #27272a 70%, #09090b 100%); border-radius: 6px 6px 2px 2px; border-top: 1.5px solid #52525b; box-shadow: 0 16px 30px rgba(0,0,0,0.9), inset 0 2px 4px rgba(255,255,255,0.12); }
        .w-holo-sight { position: absolute; top: 2px; left: 29px; width: 42px; height: 38px; border: 3.5px solid #27272a; border-bottom: none; border-radius: 6px 6px 0 0; background: linear-gradient(to bottom, rgba(0,240,255,0.15), rgba(0,240,255,0.03)); box-shadow: inset 0 0 10px rgba(0,240,255,0.2); }
        .w-grip-back { position: absolute; top: 90px; left: 32px; width: 36px; height: 70px; background: linear-gradient(to right, #09090b, #18181b, #020202); border-radius: 3px; }
        #flash { position: absolute; top: 12px; left: 26px; width: 48px; height: 48px; background: radial-gradient(circle, #ffffff 20%, #ff4500 55%, transparent 85%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 12px #ff4500); }
        .target-ring { position: absolute; border: 3px dashed #ff2266; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-50%, -50%); display: block; box-shadow: 0 0 12px #ff2266; opacity: 0; transition: opacity 0.15s ease; }
        #sight { position: absolute; width: 32px; height: 32px; border: 2px solid #00f0ff; border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); z-index: 20; box-shadow: 0 0 10px #00f0ff; display: block; }
        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.88); padding: 4px 14px; border-radius: 6px; border: 2px solid #3f3f46; text-shadow: 0 0 6px #ffea00; display: block; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-family: sans-serif; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.88); padding: 6px 12px; border-radius: 6px; border: 1px solid #3f3f46; letter-spacing: 1px; display: block; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3366; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.88); padding: 3px 8px; border-radius: 4px; display: block; }
        #healthCounter { position: absolute; bottom: 12px; left: 12px; color: #ff3355; font-weight: bold; font-family: 'Courier New', monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.92); padding: 5px 12px; border-radius: 4px; border: 2px solid #ef4444; text-shadow: 0 0 5px #ff0000; display: block; }
        #overScreen, #winScreen { position: absolute; inset: 0; background: rgba(2, 6, 23, 0.94); z-index: 40; display: none; flex-direction: column; align-items: center; justify-content: center; }
        .retry-btn, .win-btn { margin-top: 20px; padding: 10px 24px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; }
        .win-btn { background: #eab308; color: #020617; }
    </style>
</head>
<body style="background:#010409;">
    <div id="gameArea">
        <div id="chapterOverlay">
            <div id="overlayChapterTitle" style="color:white; font-family:monospace; font-size:18px; font-weight:bold; letter-spacing:3px;">CHAPTER 1</div>
            <div id="overlayChapterSubtitle" style="color:#64748b; font-family:sans-serif; font-size:11px; margin-top:5px; letter-spacing:1px;">PORT TERMINAL SANITIZATION</div>
        </div>
        <div id="scoreCounter">00200</div> <div id="chapterTxt">CH 1: 3D CONTAINER PORT</div> <div id="targetTracker">SECTOR A: 0/3</div> <div id="healthCounter">HP: 100</div>
        <canvas id="gameCanvas" width="380" height="480"></canvas>
        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div> <div class="w-slide"></div> <div class="w-holo-sight"></div> <div class="w-grip-back"></div>
        </div>
        <div id="overScreen">
            <div style="color:#ef4444; font-size:32px; font-weight:bold; text-shadow:0 0 12px #0 black; font-family:monospace; letter-spacing:1px;">MISSION FAILURE</div>
            <div id="finalScore" style="color:white; font-size:16px; margin-top:10px;">Final Score Log: 200</div>
            <button class="retry-btn" onclick="resetArcadeEngine(true)">REDEPLOY OPERATIVE 🔄</button>
        </div>
        <div id="winScreen">
            <div style="color:#eab308; font-size:28px; font-weight:bold; text-shadow: 0 0 12px #eab308;">👑 CAMPAIGN SECURED 👑</div>
            <div style="color:white; font-size:14px; text-align:center; margin-top:15px; max-width:320px; line-height:1.5;">CONGRATULATIONS JERICHO!<br>All terminals and flight decks successfully secured!</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">REPLAY CAMPAIGN 🎮</button>
        </div>
    </div>
<script>
    let currentX = 190, currentY = 240, score = 200, isOver = false; let threatsList = []; let playerHp = 100;
    let spawnTimerId = null, runLoopTimerId = null, heartbeatIntervalId = null; let audioCtx = null;
    let currentChapter = 1; let currentSector = "A"; let sectorKills = 0;
    const ch1Sectors = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]; const ch2Sectors = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"];
    const ch1Requirements = { "A":3, "B":3, "C":3, "D":3, "E":4, "F":4, "G":4, "H":4, "I":4, "J":5 }; const ch2Requirements = { "K":4, "L":4, "M":4, "N":4, "O":5, "P":5, "Q":5, "R":5, "S":5, "T":6 };
    let isMoving = false; const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
    let cameraZ = 0, targetCameraZ = 0; let cameraX = 0, targetCameraX = 0; let cycleTick = 0;
    function setupAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
    function sound(type) {
        setupAudio(); if (!audioCtx) return; let osc = audioCtx.createOscillator(), gain = audioCtx.createGain(); osc.connect(gain); gain.connect(audioCtx.destination);
        if (type === "zap") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(540, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(45, audioCtx.currentTime + 0.15); gain.gain.setValueAtTime(0.4, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.15); }
        else if (type === "ding") { osc.type = "sine"; osc.frequency.setValueAtTime(950, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(1350, audioCtx.currentTime + 0.08); gain.gain.setValueAtTime(0.2, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.08); }
        else if (type === "boom") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(110, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.38); gain.gain.setValueAtTime(0.5, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.38); }
        else if (type === "level") { osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2); gain.gain.setValueAtTime(0.25, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        else if (type === "bullet_crack") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(190, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(30, audioCtx.currentTime + 0.12); gain.gain.setValueAtTime(0.3, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.12); }
        else if (type === "heartbeat") { osc.type = "sine"; osc.frequency.setValueAtTime(60, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(25, audioCtx.currentTime + 0.18); gain.gain.setValueAtTime(0.45, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.18); }
    }
    function project3D(x, y, z) { let rX = x - cameraX; let aZ = z - cameraZ; if (aZ <= 0.1) return null; let f = 400 / aZ; return { x: 190 + (rX * f), y: 240 - ((y - 1.6) * f), size: f }; }

    function render3DSceneGrid() {
        if (document.getElementById("chapterOverlay").style.display === "flex") return;
        cycleTick += 0.05; cameraZ += (targetCameraZ - cameraZ) * 0.07; cameraX += (targetCameraX - cameraX) * 0.07;
        if (isMoving && Math.abs(cameraZ - targetCameraZ) < 0.1) { isMoving = false; }
        if (!spawnTimerId && !isOver) { spawnTimerId = setInterval(spawn3DThreatUnit, 1350); }
        let isCh1Outdoor = (currentChapter === 1 && ["E","F","G","H","I","J"].includes(currentSector));
        let isCh2Aircraft = (currentChapter === 2 && ["P","Q","R","S"].includes(currentSector)); let isCh2Cockpit = (currentChapter === 2 && currentSector === "T");

        if (currentChapter === 1) {
            if (isCh1Outdoor) {
                let skyGrd = ctx.createLinearGradient(0, 0, 0, 240); skyGrd.addColorStop(0, "#010103"); skyGrd.addColorStop(0.6, "#040514"); skyGrd.addColorStop(1, "#110b1c"); ctx.fillStyle = skyGrd; ctx.fillRect(0, 0, 380, 240);
                ctx.fillStyle = "rgba(255,255,255,0.75)"; for (let i = 1; i <= 25; i++) { ctx.fillRect((i * 73) % 380, (i * 37) % 190, 1.5, 1.5); }
                ctx.fillStyle = "#04060c"; let sX = 140 - (cameraX * 25); ctx.beginPath(); ctx.moveTo(sX, 230); ctx.lineTo(sX + 65, 230); ctx.lineTo(sX + 55, 240); ctx.lineTo(sX - 5, 240); ctx.closePath(); ctx.fill();
                let seaGrd = ctx.createLinearGradient(0, 240, 0, 480); seaGrd.addColorStop(0, "#04060c"); seaGrd.addColorStop(1, "#011116"); ctx.fillStyle = seaGrd; ctx.fillRect(0, 240, 380, 480);
            } else { ctx.fillStyle = "#010206"; ctx.fillRect(0, 0, 380, 480); }
        } else { ctx.fillStyle = (isCh2Aircraft || isCh2Cockpit) ? "#090b10" : "#010205"; ctx.fillRect(0, 0, 380, 480); }

        for (let z = 84; z >= 0; z -= 3) {
            let zPos = Math.floor(cameraZ) + z; zPos = zPos - (zPos % 3); let pNear = project3D(0, 0, zPos); let pFar = project3D(0, 0, zPos + 3); if (!pNear || !pFar) continue;
            let lightScale = 1 - Math.min(1, z / 65);
            ctx.fillStyle = "rgba(" + Math.floor(18 * lightScale) + "," + Math.floor(24 * lightScale) + "," + Math.floor(38 * lightScale) + ",1)";
            ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            ctx.strokeStyle = (isCh2Aircraft || isCh2Cockpit) ? "rgba(6, 182, 212, 0.2)" : "rgba(20, 184, 166, 0.25)"; ctx.lineWidth = Math.max(1, pNear.size * 0.03);
            ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.stroke();

            if (currentChapter === 1 && isCh1Outdoor) continue;
            if (isCh2Cockpit) {
                let w = pNear.size; ctx.fillStyle = "rgba(55,60,70,1)"; ctx.fillRect(190 - (4.5 * w), 240 - (0.4 * w), 9.0 * w, 2.0 * w);
                ctx.fillStyle = "#022c22"; ctx.fillRect(190 - (0.8 * w), 240 + (0.1 * w), 1.6 * w, 0.9 * w);
            } else if (isCh2Aircraft) {
                ctx.fillStyle = "rgba(" + Math.floor(190*lightScale) + ",195,205,1)";
                ctx.beginPath(); ctx.moveTo(190 - (2.2 * pNear.size), 240 + (1.6 * pNear.size)); ctx.quadraticCurveTo(190 - (4.4 * pNear.size), 240 - (0.4 * pNear.size), 190 - (2.6 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 - (2.6 * pFar.size), 240 - (2.4 * pFar.size)); ctx.quadraticCurveTo(190 - (4.4 * pFar.size), 240 - (0.4 * pFar.size), 190 - (2.2 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
                ctx.beginPath(); ctx.moveTo(190 + (2.2 * pNear.size), 240 + (1.6 * pNear.size)); ctx.quadraticCurveTo(190 + (4.4 * pNear.size), 240 - (0.4 * pNear.size), 190 + (2.6 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 + (2.6 * pFar.size), 240 - (2.4 * pFar.size)); ctx.quadraticCurveTo(190 + (4.4 * pFar.size), 240 - (0.4 * pFar.size), 190 + (2.2 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            } else {
                ctx.fillStyle = (currentChapter === 1) ? "rgba(13,148,136,1)" : "rgba(71,85,105,1)";
                ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.lineTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.fill();
                ctx.beginPath(); ctx.moveTo(190 + (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.fill();
            }
        }
        let depthDrawQueue = []; let activeObstacleRegistry = (currentChapter === 1) ? ch1Obstacles : ch2Obstacles;
        activeObstacleRegistry.forEach(b => { if ((isCh2Aircraft || isCh2Cockpit) ? b.isCabinAsset : !b.isCabinAsset) { if (b.z >= cameraZ) depthDrawQueue.push({ type: "crate", z: b.z, data: b }); } });
        threatsList.forEach(t => { if (!t.isDying && t.z >= cameraZ) depthDrawQueue.push({ type: "enemy", z: t.z, data: t }); });
        depthDrawQueue.sort((a, b) => b.z - a.z);

        depthDrawQueue.forEach(item => {
            if (item.type === "crate") {
                let b = item.data; let p = project3D(b.x, b.y, b.z); if (!p) return;
                if (b.isCabinAsset) {
                    let w = 1.3 * p.size; let h = 2.1 * p.size; ctx.fillStyle = "#1e40af"; ctx.fillRect(p.x - w/2, p.y + (h * 0.1), w, h * 0.4);
                    ctx.fillStyle = "#1d4ed8"; ctx.fillRect(p.x - w/2 + (w * 0.08), p.y - h/2, w * 0.84, h * 0.6);
                } else {
                    let w = 1.9 * p.size; let h = 2.2 * p.size; ctx.fillStyle = b.baseColor; ctx.fillRect(p.x - w/2, p.y - h/2, w, h);
                }
            } else if (item.type === "enemy") {
                let t = item.data; if (!isMoving) t.loopTick++; let smooth = (Math.sin(t.loopTick * 0.05) + 1) / 2; let active = (smooth > 0.45);
                let p = project3D(t.x, t.y, t.z); if (!p) return; let s = p.size * 0.4; let cX = p.x - (s * 1.5) + (s * 1.5 * smooth);
                t.currentScreenX = cX; t.currentScreenY = p.y - (s * 0.5); t.currentRadius = s * 1.15;
                if (active) { t.ring.style.opacity = "1"; t.age++; } else { t.ring.style.opacity = "0"; }
                if (t.age > 0 && t.age % 42 === 0 && !isMoving && active) { t.isFlashing = true; triggerEnemyDamageStrike(); setTimeout(() => { t.isFlashing = false; }, 70); }
                ctx.fillStyle = (currentChapter === 1) ? "#1e291b" : "#2d1f3d"; ctx.fillRect(cX - s/2, p.y - s, s, s * 1.3);
                ctx.fillStyle = "#d4b38a"; ctx.beginPath(); ctx.arc(cX, p.y - s * 1.3, s * 0.35, 0, Math.PI*2); ctx.fill();
                t.ring.style.left = cX + "px"; t.ring.style.top = (p.y - s/2) + "px"; let rSize = Math.max(14, Math.min(110, 95 * (1.3 - (t.age / 40)))); t.ring.style.width = rSize + "px"; t.ring.style.height = rSize + "px";
            }
        });
    }
    // --- 📱 FIXED: IMMERSIVE ACCELERATED MOBILE TOUCH LISTENERS CORE ---
    function executeAdaptiveInputSweep(e) {
        setupAudio();
        // Locks native page dragging so swipe-aiming operates perfectly on mobile views
        if (e.cancelable) e.preventDefault();
        
        let targetEventSource = e.touches ? e.touches[0] : e;
        if (e.type === "touchend" || e.type === "touchcancel") {
            if (e.changedTouches && e.changedTouches.length > 0) targetEventSource = e.changedTouches[0];
        }
        
        let bounds = gameArea.getBoundingClientRect();
        currentX = targetEventSource.clientX - bounds.left;
        currentY = targetEventSource.clientY - bounds.top;
        
        // Force clamp pointer values inside the mobile frame box boundary dimensions
        if (currentX < 0) currentX = 0; if (currentX > 380) currentX = 380;
        if (currentY < 0) currentY = 0; if (currentY > 480) currentY = 480;

        sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        let swayX = (currentX - 190) / 10; let swayY = (currentY - 240) / 12;
        weapon.style.transform = "translateX(-50%) scale(1.1) rotate(" + swayX + "deg) translateY(" + swayY + "px)";
    }

    // Bind clean listener tracks across desktop mouse boards and mobile screens synchronously
    gameArea.addEventListener("mousemove", executeAdaptiveInputSweep);
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") { executeAdaptiveInputSweep(e); triggerFire(); } });
    
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { executeAdaptiveInputSweep(e); triggerFire(); } }, { passive: false });
    gameArea.addEventListener("touchmove", executeAdaptiveInputSweep, { passive: false });
    gameArea.addEventListener("touchend", executeAdaptiveInputSweep, { passive: false });

    function triggerSectorPathMovement() {
        if (isMoving) return; isMoving = true;
        let activeSectorList = (currentChapter === 1) ? ch1Sectors : ch2Sectors;
        let activeRequirementMap = (currentChapter === 1) ? ch1Requirements : ch2Requirements;
        let idx = activeSectorList.indexOf(currentSector);
        
        if (idx >= 0 && idx < activeSectorList.length - 1) {
            currentSector = activeSectorList[idx + 1]; sectorKills = 0; targetCameraZ = (idx + 1) * 16;
            let rollingPathRoll = Math.random();
            if (rollingPathRoll < 0.33) { targetCameraX = -1.6; } else if (rollingPathRoll < 0.66) { targetCameraX = 1.6; } else { targetCameraX = 0.0; }
            if (currentChapter === 1) {
                if (["E","F","G","H","I","J"].includes(currentSector)) { document.getElementById("chapterTxt").innerText = "CH 1: OUTSIDE CARGO TERMINAL"; }
            } else {
                if (["K","L","M","N"].includes(currentSector)) { document.getElementById("chapterTxt").innerText = "CH 2: AIRPORT TARMAC AIRSIDE"; }
                else if (currentSector === "O") { document.getElementById("chapterTxt").innerText = "CH 2: GLASS BOARDING BRIDGE"; }
                else if (["P","Q","R","S"].includes(currentSector)) { document.getElementById("chapterTxt").innerText = "CH 2: IMMERSIVE PASSENGER CABIN"; }
                else if (currentSector === "T") { document.getElementById("chapterTxt").innerText = "CH 2: COCKPIT CONTROL RECOVERY"; }
            }
        } else {
            if (currentChapter === 1) {
                currentChapter = 2; currentSector = "K"; sectorKills = 0; cameraZ = 0; targetCameraZ = 0;
                document.getElementById("overlayChapterTitle").innerText = "CHAPTER 2";
                document.getElementById("overlayChapterSubtitle").innerText = "AIRPORT TERMINAL & AIRCRAFT RECOVERY";
                document.getElementById("chapterOverlay").style.display = "flex";
                document.getElementById("chapterTxt").innerText = "CH 2: INTERNATIONAL RUNWAY APRON";
                setTimeout(initializeActiveArcadeGameplay, 3000); return;
            } else {
                clearInterval(spawnTimerId); clearInterval(runLoopTimerId); isOver = true;
                document.getElementById("winScreen").style.display = "flex"; return;
            }
        }
        let needed = activeRequirementMap[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`; sound("level");
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
        threatsList.forEach(t => { if (t.isDying) return; let d = Math.hypot(currentX - t.currentScreenX, currentY - t.currentScreenY); if (d < t.currentRadius && d < lowestDistance) { lowestDistance = d; hitTarget = t; } });
        if (hitTarget) {
            hitTarget.isDying = true; sound("boom"); score += 100; scoreCounter.innerText = String(score).padStart(5, '0'); sectorKills += 1;
            let activeRequirementMap = (currentChapter === 1) ? ch1Requirements : ch2Requirements; let needed = activeRequirementMap[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
            hitTarget.ring.remove(); threatsList = threatsList.filter(item => item !== hitTarget);
            if (sectorKills >= needed) { document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = []; setTimeout(triggerSectorPathMovement, 400); }
        }
    }

    const ch1Obstacles = [ { id: "c1", x: -2.0, y: 0.5, z: 15, baseColor: "#0d9488", shadowColor: "#115e59", isCabinAsset: false }, { id: "c2", x: 2.1, y: 0.5, z: 31, baseColor: "#dc2626", shadowColor: "#991b1b", isCabinAsset: false } ];
    const ch2Obstacles = [ { id: "b1", x: -2.0, y: 0.5, z: 16, baseColor: "#475569", shadowColor: "#334155", isCabinAsset: false }, { id: "p1", x: -1.8, y: 0.5, z: 12, isCabinAsset: true }, { id: "p2", x: 1.8, y: 0.5, z: 24, isCabinAsset: true } ];

    function spawn3DThreatUnit() {
        if (isOver || threatsList.length >= 2 || isMoving || document.getElementById("winScreen").style.display === "flex" || document.getElementById("chapterOverlay").style.display === "flex") return;
        let activeSectorList = (currentChapter === 1) ? ch1Sectors : ch2Sectors;
        let idx = activeSectorList.indexOf(currentSector); let spawnZ = cameraZ + 12 + (idx * 0.5); let spawnX = cameraX + (Math.random() * 2.6) - 1.3;
        let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);
        threatsList.push({ x: spawnX, y: 0.2, z: spawnZ, age: 0, loopTick: Math.floor(Math.random()*60), isDying: false, isFlashing: false, ring: ring, currentScreenX: 0, currentScreenY: 0, currentRadius: 24 });
        sound("ding");
    }

    function initializeActiveArcadeGameplay() { document.getElementById("chapterOverlay").style.display = "none"; if (!runLoopTimerId) runLoopTimerId = setInterval(render3DSceneGrid, 1000 / 45); }

    window.resetArcadeEngine = function(fullReset) {
        if (spawnTimerId) { clearInterval(spawnTimerId); spawnTimerId = null; } clearInterval(runLoopTimerId); runLoopTimerId = null; if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
        document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = []; cameraZ = 0; targetCameraZ = 0; cameraX = 0; targetCameraX = 0; currentChapter = 1; currentSector = "A"; sectorKills = 0; playerHp = 100; score = 200; isMoving = false; isOver = false;
        document.getElementById("winScreen").style.display = "none"; document.getElementById("overScreen").style.display = "none"; gameArea.className = ""; healthCounter.innerText = "HP: 100"; scoreCounter.innerText = "00200"; document.getElementById("chapterTxt").innerText = "CH 1: 3D CONTAINER PORT";
        document.getElementById("overlayChapterTitle").innerText = "CHAPTER 1"; document.getElementById("overlayChapterSubtitle").innerText = "PORT TERMINAL SANITIZATION"; document.getElementById("chapterOverlay").style.display = "flex";
        setTimeout(initializeActiveArcadeGameplay, 3000);
    };
    setTimeout(initializeActiveArcadeGameplay, 3000);
</script>
</body>
</html>
'''
cb_id = random.randint(100000, 999999)
st.markdown(f'<!-- Mobile Touch Fixed Frame ID: {cb_id} -->', unsafe_allow_html=True)
components.html(game_html, height=560, scrolling=False)
