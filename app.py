import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Virtua Tactical: Hampi Jericho Ops", layout="centered")
st.title("⚡ Virtua Tactical: Hampi Jericho Chronicles")

game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        #gameArea { position: relative; width: 380px; height: 480px; background: #010206; border: 4px solid #1e293b; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none; box-shadow: 0 24px 60px rgba(0,0,0,0.95); }
        #gameArea::after { content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 28; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://w3.org id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.065'/%3E%3C/svg%3E"); background-size: auto; box-shadow: inset 0 0 90px rgba(0, 0, 0, 0.95), inset 0 0 160px rgba(0, 0, 0, 0.85); background-color: rgba(220, 20, 20, 0); transition: box-shadow 0.12s ease-out, background-color 0.12s ease-out; }
        #gameArea.taking-damage::after { background-color: rgba(220, 20, 20, 0.26); box-shadow: inset 0 0 120px rgba(220, 20, 20, 0.98), inset 0 0 200px rgba(180, 0, 0, 0.98); }
        #gameArea.critical-pulse::after { animation: fullViewportLowHpPulse 0.5s ease-in-out infinite alternate; }
        @keyframes fullViewportLowHpPulse { 0% { background-color: rgba(220, 20, 20, 0.04); box-shadow: inset 0 0 90px rgba(160, 0, 0, 0.75); } 100% { background-color: rgba(220, 20, 20, 0.28); box-shadow: inset 0 0 130px rgba(254, 0, 0, 0.98), inset 0 0 190px rgba(180, 0, 0, 0.9); } }
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
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.88); padding: 6px 12px; border-radius: 6px; border: 1px solid #3f3f46; letter-spacing: 1px; display: none; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3366; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.88); padding: 3px 8px; border-radius: 4px; display: none; }
        #healthCounter { position: absolute; bottom: 12px; left: 12px; color: #ff3355; font-weight: bold; font-family: 'Courier New', monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.92); padding: 5px 12px; border-radius: 4px; border: 2px solid #ef4444; text-shadow: 0 0 5px #ff0000; display: none; }
        #overScreen, #winScreen { position: absolute; inset: 0; background: rgba(2, 6, 23, 0.94); z-index: 40; display: none; flex-direction: column; align-items: center; justify-content: center; }
        .retry-btn, .win-btn { margin-top: 20px; padding: 10px 24px; background: #ef4444; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; }
        .win-btn { background: #eab308; color: #020617; }
        #chapterOverlay { position: absolute; inset: 0; background: #000000; z-index: 49; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        @keyframes flashPulse { 0% { opacity: 0.6; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div id="gameArea">
        <div id="chapterOverlay">
            <div id="overlayChTitle" style="color:white; font-family:monospace; font-size:18px; font-weight:bold; letter-spacing:3px;">CHAPTER 1</div>
            <div id="overlayChSubtitle" style="color:#64748b; font-family:sans-serif; font-size:11px; margin-top:5px; letter-spacing:1px;">PORT TERMINAL SANITIZATION</div>
        </div>
        
        <div id="tutorialPopup" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: #ff2266; font-family: monospace; font-size: 15px; font-weight: bold; background: rgba(0,0,0,0.85); border: 2px solid #ff2266; padding: 10px 16px; border-radius: 8px; z-index: 35; text-align: center; box-shadow: 0 0 15px rgba(255, 34, 102, 0.4); animation: flashPulse 1s infinite alternate; pointer-events: none; display: none;">
            CLICK RED CIRCLE TO SHOOT
        </div>

        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CH 1: 3D CONTAINER PORT</div>
        <div id="targetTracker">SECTOR A: 0/3</div>
        <div id="healthCounter">HP: 100</div>
        
        <canvas id="gameCanvas" width="380" height="480"></canvas>
        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div> <div class="w-slide"></div> <div class="w-holo-sight"></div> <div class="w-grip-back"></div>
        </div>

        <div id="overScreen">
            <div style="color:#ef4444; font-size:32px; font-weight:bold; text-shadow:0 0 12px #000; font-family:monospace; letter-spacing:1px;">MISSION FAILURE</div>
            <div id="finalScore" style="color:white; font-size:16px; margin-top:10px;">Final Score Log: 200</div>
            <button class="retry-btn" onclick="window.resetArcadeEngine(true)">REDEPLOY OPERATIVE 🔄</button>
        </div>

        <div id="winScreen">
            <div id="winHeader" style="color:#eab308; font-size:28px; font-weight:bold; text-shadow: 0 0 12px #eab308;">👑 CAMPAIGN SECURED 👑</div>
            <div id="winSub" style="color:white; font-size:14px; text-align:center; margin-top:15px; max-width:320px; line-height:1.5;">EXCELLENT WORK JERICHO!<br>All terminals cleared successfully.</div>
            <button class="win-btn" id="winBtnAction" onclick="window.resetArcadeEngine(true)">REPLAY CAMPAIGN 🎮</button>
        </div>
    </div>
<script>
    let currentX = 190, currentY = 240, score = 200, isOver = false;
    let threatsList = []; let playerHp = 100;
    let spawnTimerId = null, runLoopTimerId = null, heartbeatIntervalId = null;
    let audioCtx = null;

    let currentChapter = 1; 
    let currentSector = "A"; let sectorKills = 0;
    const sectorsList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
    const sectorRequirements = { "A":3, "B":3, "C":3, "D":3, "E":4, "F":4, "G":4, "H":4, "I":4, "J":5 };
    let isMoving = false;
    let cockpitDoorOpened = false;

    const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
    let cameraZ = 0, targetCameraZ = 0; let cameraX = 0, targetCameraX = 0; let cycleTick = 0;

    const gameArea = document.getElementById("gameArea");
    const weapon = document.getElementById("weapon");
    const sight = document.getElementById("sight");
    const scoreCounter = document.getElementById("scoreCounter");
    const chapterTxt = document.getElementById("chapterTxt");
    const targetTracker = document.getElementById("targetTracker");
    const healthCounter = document.getElementById("healthCounter");
    const overScreen = document.getElementById("overScreen");
    const winScreen = document.getElementById("winScreen");
    const finalScore = document.getElementById("finalScore");
    const flash = document.getElementById("flash");

    const static3DObstacles = [
        { id: "c1", x: -2.0, y: 0.5, z: 15, baseColor: "#0d9488", shadowColor: "#115e59" }, 
        { id: "c2", x: 2.1, y: 0.5, z: 31, baseColor: "#dc2626", shadowColor: "#991b1b" },
        { id: "c3", x: -1.9, y: 0.5, z: 47, baseColor: "#2563eb", shadowColor: "#1e40af" }, 
        { id: "c4", x: 2.0, y: 0.5, z: 63, baseColor: "#ba8b02", shadowColor: "#785a01" }
    ];
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
    
    function project3D(x, y, z) {
        let relativeX = x - cameraX; let activePerspectiveZ = z - cameraZ;
        if (activePerspectiveZ <= 0.1) return null;
        let fovScale = 400 / activePerspectiveZ;
        return { x: 190 + (relativeX * fovScale), y: 240 - ((y - 1.6) * fovScale), size: fovScale };
    }

    function spawn3DThreatUnit() {
        if (isOver || threatsList.length >= 2 || isMoving || document.getElementById("winScreen").style.display === "flex" || document.getElementById("chapterOverlay").style.display === "flex") return;
        let idx = sectorsList.indexOf(currentSector); let spawnZ = cameraZ + 12 + (idx * 0.5); let spawnX = cameraX + (Math.random() * 2.6) - 1.3;
        if (currentChapter === 2 && idx >= 7 && !cockpitDoorOpened) return; 
        
        let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);
        threatsList.push({ x: spawnX, y: 0.2, z: spawnZ, age: 0, loopTick: Math.floor(Math.random()*60), isDying: false, isFlashing: false, ring: ring, currentScreenX: 0, currentScreenY: 0, currentRadius: 24 });
        sound("ding");
    }
    function aim(e) {
        if (isOver || document.getElementById("chapterOverlay").style.display === "flex") return;
        let targetPoint = e; 
        if (e.touches && e.touches.length > 0) { targetPoint = e.touches; } 
        else if (e.changedTouches && e.changedTouches.length > 0) { targetPoint = e.changedTouches; }
        
        let bounds = gameArea.getBoundingClientRect(); 
        currentX = targetPoint.clientX - bounds.left; 
        currentY = targetPoint.clientY - bounds.top;
        
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
        setupAudio(); let bounds = gameArea.getBoundingClientRect();
        currentX = e.clientX - bounds.left; currentY = e.clientY - bounds.top;
        triggerFire();
    }
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerMouseCoordinateFire(e); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); setupAudio(); aim(e); triggerFire(); } }, { passive: false });
    function updateMapLevelLabels() {
        let secIdx = sectorsList.indexOf(currentSector);
        if (currentChapter === 1) {
            chapterTxt.innerText = secIdx >= 4 ? "CH 1: OUTSIDE CARGO TERMINAL" : "CH 1: 3D CONTAINER PORT";
        } else {
            if (secIdx >= 7) { chapterTxt.innerText = "CH 2: AIRPLANE COCKPIT DECK"; }
            else if (secIdx >= 4) { chapterTxt.innerText = "CH 2: COMMERCIAL CABIN FLIGHT"; }
            else { chapterTxt.innerText = "CH 2: INTERNATIONAL RUNWAY AIRPORT"; }
        }
    }

    function triggerSectorPathMovement() {
        if (isMoving) return; isMoving = true;
        let idx = sectorsList.indexOf(currentSector);
        
        if (idx >= 0 && idx < sectorsList.length - 1) {
            currentSector = sectorsList[idx + 1]; sectorKills = 0; targetCameraZ = (idx + 1) * 16;
            let rollingPathRoll = Math.random();
            if (rollingPathRoll < 0.33) { targetCameraX = -1.3; } else if (rollingPathRoll < 0.66) { targetCameraX = 1.3; } else { targetCameraX = 0.0; }
            
            updateMapLevelLabels();
            document.getElementById("tutorialPopup").style.display = "none";
        } else {
            handleChapterTransition();
            return;
        }
        let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
        sound("level");
    }

    function handleChapterTransition() {
        if (currentChapter === 1) {
            currentChapter = 2; currentSector = "A"; sectorKills = 0;
            cameraZ = 0; targetCameraZ = 0; cameraX = 0; targetCameraX = 0; threatsList = [];
            isMoving = false; cockpitDoorOpened = false;
            
            document.querySelectorAll(".target-ring").forEach(el => el.remove());
            if (spawnTimerId) clearInterval(spawnTimerId); spawnTimerId = null;
            
            document.getElementById("overlayChTitle").innerText = "CHAPTER 2";
            document.getElementById("overlayChSubtitle").innerText = "AIRPORT RUNWAY & CABIN SECURING";
            document.getElementById("chapterOverlay").style.display = "flex";
            
            scoreCounter.style.display = "none"; chapterTxt.style.display = "none"; targetTracker.style.display = "none"; healthCounter.style.display = "none"; sight.style.display = "none"; weapon.style.display = "none";
            setTimeout(initializeActiveArcadeGameplay, 3000);
        } else {
            if (spawnTimerId) clearInterval(spawnTimerId); clearInterval(runLoopTimerId); isOver = true;
            document.getElementById("winHeader").innerText = "👑 CAMPAIGN SECURED 👑";
            document.getElementById("winSub").innerHTML = "ALL SECTORS SECURED!<br>Jericho Ops cleared the cockpit terminal.";
            document.getElementById("winBtnAction").innerText = "RESET SYSTEM 🔄";
            winScreen.style.display = "flex";
        }
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
        document.getElementById("tutorialPopup").style.display = "none";
        sound("zap"); flash.style.display = "block"; setTimeout(() => { flash.style.display = "none"; }, 60);
        
        if (currentChapter === 2 && currentSector === "J" && !cockpitDoorOpened) {
            if (Math.hypot(currentX - 190, currentY - 250) < 40) {
                cockpitDoorOpened = true; sound("level"); sound("boom");
                let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);
                threatsList.push({ x: 0.0, y: 0.4, z: cameraZ + 10, age: 10, loopTick: 20, isDying: false, isFlashing: false, ring: ring, currentScreenX: 190, currentScreenY: 210, currentRadius: 35 });
                return;
            }
        }

        let hitTarget = null; let lowestDistance = Infinity;
        threatsList.forEach(t => {
            if (t.isDying) return;
            let d = Math.hypot(currentX - t.currentScreenX, currentY - t.currentScreenY);
            if (d < t.currentRadius && d < lowestDistance) { lowestDistance = d; hitTarget = t; }
        });
        
        if (hitTarget) {
            hitTarget.isDying = true; sound("boom"); score += 100; scoreCounter.innerText = String(score).padStart(5, '0'); sectorKills += 1;
            let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
            if(t.ring) t.ring.remove(); threatsList = threatsList.filter(item => item !== hitTarget);
            if (sectorKills >= needed) { document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = []; setTimeout(triggerSectorPathMovement, 400); }
        }
    }
    function render3DSceneGrid() {
        if (document.getElementById("chapterOverlay").style.display === "flex") return;

        cycleTick += 0.05; cameraZ += (targetCameraZ - cameraZ) * 0.07; cameraX += (targetCameraX - cameraX) * 0.07;
        if (isMoving && Math.abs(cameraZ - targetCameraZ) < 0.1) { isMoving = false; }
        if (!spawnTimerId && !isOver) { spawnTimerId = setInterval(spawn3DThreatUnit, 1350); }

        ctx.clearRect(0, 0, 380, 480);
        let secIdx = sectorsList.indexOf(currentSector);

        if (currentChapter === 1 || (currentChapter === 2 && secIdx < 4)) {
            let isOutdoor = (currentChapter === 1 && secIdx >= 4) || currentChapter === 2;
            let skyGrd = ctx.createLinearGradient(0, 0, 0, 240); skyGrd.addColorStop(0, "#010103"); skyGrd.addColorStop(1, "#110b1c"); ctx.fillStyle = skyGrd; ctx.fillRect(0, 0, 380, 240);
            let floorGrd = ctx.createLinearGradient(0, 240, 0, 480); floorGrd.addColorStop(0, "#04060c"); floorGrd.addColorStop(1, "#011116"); ctx.fillStyle = floorGrd; ctx.fillRect(0, 240, 380, 240);

            for (let z = 84; z >= 0; z -= 3) {
                let zPos = Math.floor(cameraZ) + z; zPos = zPos - (zPos % 3);
                let pNear = project3D(0, 0, zPos); let pFar = project3D(0, 0, zPos + 3); if (!pNear || !pFar) continue;
                let fogOpacity = Math.min(1, z / 65); let lightScale = 1 - fogOpacity;
                
                let floorColor = "rgba(" + Math.floor((currentChapter==2?32:18) * lightScale) + "," + Math.floor((currentChapter==2?34:24) * lightScale) + "," + Math.floor((currentChapter==2?42:38) * lightScale) + ",1)";
                ctx.fillStyle = floorColor; ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
                
                if (isOutdoor) continue;
                let isRidgeFold = Math.floor(zPos * 2.5) % 2 === 0;
                ctx.fillStyle = "rgba(" + (isRidgeFold ? Math.floor(13*lightScale) : Math.floor(19*lightScale)) + "," + (isRidgeFold ? Math.floor(148*lightScale) : Math.floor(94*lightScale)) + "," + (isRidgeFold ? Math.floor(136*lightScale) : Math.floor(89*lightScale)) + ",1)";
                ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 - (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
                ctx.beginPath(); ctx.moveTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            }
        } else if (currentChapter === 2 && secIdx >= 4 && secIdx < 7) {
            ctx.fillStyle = "#0f172a"; ctx.fillRect(0, 0, 380, 480);
            for (let z = 70; z >= 0; z -= 4) {
                let zPos = Math.floor(cameraZ) + z; let p = project3D(0, 0, zPos); if (!p) continue;
                let scale = 1 - (z / 70);
                ctx.fillStyle = "rgba(" + Math.floor(30*scale) + "," + Math.floor(41*scale) + "," + Math.floor(59*scale) + ",1)";
                ctx.fillRect(190 - (3.8 * p.size), 240, 1.2 * p.size, 0.8 * p.size); 
                ctx.fillRect(190 + (2.6 * p.size), 240, 1.2 * p.size, 0.8 * p.size); 
                
                ctx.fillStyle = "rgba(" + Math.floor(212*scale) + "," + Math.floor(163*scale) + "," + Math.floor(115*scale) + ",1)";
                ctx.beginPath(); ctx.arc(190 - (3.2 * p.size), 240 + (0.2*p.size), p.size * 0.12, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(190 + (3.2 * p.size), 240 + (0.2*p.size), p.size * 0.12, 0, Math.PI*2); ctx.fill();
            }
        } else if (currentChapter === 2 && secIdx >= 7) {
            ctx.fillStyle = "#020617"; ctx.fillRect(0, 0, 380, 480);
            ctx.fillStyle = "#0f172a"; ctx.fillRect(20, 260, 340, 220);
            ctx.fillStyle = "#22c55e"; ctx.fillRect(60, 310, 50, 40); 
            ctx.fillStyle = "#38bdf8"; ctx.fillRect(270, 310, 50, 40); 
            
            if (currentSector === "J" && !cockpitDoorOpened) {
                ctx.fillStyle = "rgba(0,0,0,0.95)"; ctx.fillRect(0, 0, 380, 480);
                ctx.fillStyle = "#dc2626"; ctx.font = "bold 13px monospace"; ctx.fillText("COCKPIT ACCESS DOOR SECURITY LOCKED", 50, 190);
                ctx.fillStyle = "#1e293b"; ctx.fillRect(150, 220, 80, 60);
                ctx.strokeStyle = "#ef4444"; ctx.strokeRect(150, 220, 80, 60);
                ctx.fillStyle = "#ffffff"; ctx.font = "10px sans-serif"; ctx.fillText("TAP TO BREACH", 154, 255);
            }
        }

        let depthDrawQueue = [];
        static3DObstacles.forEach(b => { if (b.z >= cameraZ) depthDrawQueue.push({ type: "crate", z: b.z, data: b }); });
        threatsList.forEach(t => { if (!t.isDying && t.z >= cameraZ) depthDrawQueue.push({ type: "enemy", z: t.z, data: t }); });
        depthDrawQueue.sort((a, b) => b.z - a.z);

        depthDrawQueue.forEach(item => {
            if (item.type === "crate" && (currentChapter === 1 || (currentChapter === 2 && sectorsList.indexOf(currentSector) < 4))) {
                let b = item.data; let p = project3D(b.x, b.y, b.z); if (!p) return; let w = 1.9 * p.size; let h = 2.2 * p.size;
                ctx.fillStyle = b.baseColor; ctx.fillRect(p.x - w/2, p.y - h/2, w, h);
            } else if (item.type === "enemy") {
                let t = item.data; if (!isMoving) t.loopTick++;
                let smoothSinPeekFactor = (Math.sin(t.loopTick * 0.05) + 1) / 2; let isActivelyOut = (smoothSinPeekFactor > 0.45); 
                let p = project3D(t.x, t.y, t.z); if (!p) return; let s = p.size * 0.4;
                let currentVisualX = p.x - (s * 1.5) + (s * 1.5 * smoothSinPeekFactor);
                
                t.currentScreenX = currentVisualX; t.currentScreenY = p.y - (s * 0.5); t.currentRadius = s * 1.15;
                if (isActivelyOut) { t.ring.style.opacity = "1"; t.age++; } else { t.ring.style.opacity = "0"; }
                if (t.age > 0 && t.age % 42 === 0 && !isMoving && isActivelyOut) { t.isFlashing = true; triggerEnemyDamageStrike(); setTimeout(() => { t.isFlashing = false; }, 70); }

                // 🎬 HIGH-DETAILED CHARACTER MODEL GRAPHICS RENDER MESHES RESTORED
                ctx.fillStyle = "#1e291b"; ctx.fillRect(currentVisualX - s/2, p.y - s, s, s * 1.3); // Body Vest
                ctx.fillStyle = "#3f3f46"; ctx.fillRect(currentVisualX - s/3, p.y - s * 0.9, s * 0.66, s * 0.7); // Terrorist Mask Gear
                ctx.fillStyle = "#d4b38a"; ctx.beginPath(); ctx.arc(currentVisualX, p.y - s * 1.3, s * 0.35, 0, Math.PI*2); ctx.fill(); // Skin Node Head
                ctx.fillStyle = "#27272a"; ctx.beginPath(); ctx.arc(currentVisualX, p.y - s * 1.4, s * 0.36, Math.PI, 0); ctx.fill(); // Combat Helmet Cap
                
                if (t.isFlashing && isActivelyOut) { let flashGrd = ctx.createRadialGradient(currentVisualX + s * 0.9, p.y - s/4, 1, currentVisualX + s * 0.9, p.y - s/4, s * 0.55); flashGrd.addColorStop(0, "#ffffff"); flashGrd.addColorStop(0.5, "#eab308"); flashGrd.addColorStop(1, "transparent"); ctx.fillStyle = flashGrd; ctx.beginPath(); ctx.arc(currentVisualX + s * 0.9, p.y - s/4, s * 0.55, 0, Math.PI*2); ctx.fill(); }
                
                t.ring.style.left = currentVisualX + "px"; t.ring.style.top = (p.y - s/2) + "px"; 
                let dynamicCircleRadius = Math.max(14, Math.min(110, 95 * (1.3 - (t.age / 40)))); 
                t.ring.style.width = dynamicCircleRadius + "px"; t.ring.style.height = dynamicCircleRadius + "px";
            }
        });
    }
    function initializeActiveArcadeGameplay() {
        document.getElementById("chapterOverlay").style.display = "none";
        if (currentSector === "A" && sectorKills === 0 && currentChapter === 1) { 
            document.getElementById("tutorialPopup").style.display = "block"; 
        }
        scoreCounter.style.display = "block"; chapterTxt.style.display = "block"; targetTracker.style.display = "block"; healthCounter.style.display = "block"; sight.style.display = "block"; weapon.style.display = "block";
        updateMapLevelLabels();
        
        if (runLoopTimerId) clearInterval(runLoopTimerId);
        runLoopTimerId = setInterval(render3DSceneGrid, 1000 / 45);
    }

    window.resetArcadeEngine = function(fullReset) {
        if (spawnTimerId) { clearInterval(spawnTimerId); spawnTimerId = null; }
        clearInterval(runLoopTimerId); runLoopTimerId = null; if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
        document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = [];
        cameraZ = 0; targetCameraZ = 0; cameraX = 0; targetCameraX = 0; currentSector = "A"; sectorKills = 0; playerHp = 100; score = 200; isMoving = false; isOver = false; cockpitDoorOpened = false;
        
        if (fullReset) { currentChapter = 1; }
        document.getElementById("winScreen").style.display = "none"; document.getElementById("overScreen").style.display = "none"; gameArea.className = "";
        healthCounter.innerText = "HP: 100"; scoreCounter.innerText = "00200"; 
        
        document.getElementById("overlayChTitle").innerText = currentChapter === 1 ? "CHAPTER 1" : "CHAPTER 2";
        document.getElementById("overlayChSubtitle").innerText = currentChapter === 1 ? "PORT TERMINAL SANITIZATION" : "AIRPORT RUNWAY & CABIN SECURING";
        document.getElementById("chapterOverlay").style.display = "flex";
        
        scoreCounter.style.display = "none"; chapterTxt.style.display = "none"; targetTracker.style.display = "none"; healthCounter.style.display = "none"; sight.style.display = "none"; weapon.style.display = "none";
        setTimeout(initializeActiveArcadeGameplay, 3000);
    };

    setTimeout(initializeActiveArcadeGameplay, 3000);
</script>
</body>
</html>
'''

cb_id = random.randint(100000, 999999)
st.markdown(f'<!-- Full Care Mesh Restored Frame: {cb_id} -->', unsafe_allow_html=True)
components.html(game_html, height=560, scrolling=False)
