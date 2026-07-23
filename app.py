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
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.88); padding: 6px 12px; border-radius: 6px; border: 1px solid #3f3f46; letter-spacing: 1px; display: none; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3366; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.88); padding: 3px 8px; border-radius: 4px; display: none; }
        #healthCounter { position: absolute; bottom: 12px; left: 12px; color: #ff3355; font-weight: bold; font-family: 'Courier New', monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.92); padding: 5px 12px; border-radius: 4px; border: 2px solid #ef4444; text-shadow: 0 0 5px #ff0000; display: none; }

        .blink-prompt { font-size: 13px; font-weight: bold; color: #06b6d4; margin-top: 15px; letter-spacing: 2px; text-shadow: 0 0 8px rgba(6,182,212,0.6); animation: textFadeBlink 0.75s ease-in-out infinite alternate; display: none; }
        @keyframes textFadeBlink { 0% { opacity: 0.1; } 100% { opacity: 1; } }
        #coverScreen { position: absolute; inset: 0; background: linear-gradient(135deg, #0f172a, #020617); z-index: 50; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; text-align: center; }
        #chapterOverlay { position: absolute; inset: 0; background: #000000; z-index: 49; display: none; flex-direction: column; align-items: center; justify-content: center; }
        
        .story-scroller { max-width: 340px; color: #e2e8f0; font-size: 13px; font-weight: 500; line-height: 1.55; margin-bottom: 20px; max-height: 220px; overflow-y: hidden; text-align: center; border: 1.5px solid #1e293b; padding: 16px; background: rgba(2, 6, 23, 0.75); border-radius: 12px; box-shadow: inset 0 4px 20px rgba(0,0,0,0.6); }
        .load-bar-track { width: 240px; height: 6px; background: #1e293b; border-radius: 4px; overflow: hidden; margin-top: 10px; }
        .load-bar-fluid { width: 0%; height: 100%; background: #06b6d4; transition: width 0.04s linear; }

        .audio-start-btn { padding: 12px 32px; background: #06b6d4; color: #020617; font-size: 14px; font-weight: bold; letter-spacing: 2px; border: none; border-radius: 8px; cursor: pointer; margin-bottom: 15px; box-shadow: 0 0 15px rgba(6,182,212,0.6); transition: transform 0.1s ease; }
        .audio-start-btn:active { transform: scale(0.96); }
    </style>
</head>
<body>
    <div id="gameArea">
        <!-- BRIEFING PANEL LAYOUT CARD -->
        <div id="coverScreen">
            <div style="color:#06b6d4; font-size:26px; font-weight:bold; letter-spacing:1px; text-shadow:0 0 12px rgba(6,182,212,0.5);">HAMPI JERICHO</div>
            <div style="color:#e2e8f0; font-size:11px; font-weight:700; letter-spacing:4px; margin-bottom:15px; color:#94a3b8;">💥 PORT TERMINAL OPERATIONS 💥</div>
            
            <button class="audio-start-btn" id="voiceTriggerBtn">ACTIVATE AUDIO BRIEFING 🔊</button>

            <div class="story-scroller" id="briefContentText">The city sleeps, but the docks are alive with terror. A ruthless criminal syndicate has hijacked the container port terminal, threatening to hold the city's supply lines hostage. Standard law enforcement has been completely compromised. Enter Hampi Jericho—an elite, rogue tactical operative armed with custom high-precision polymer weapons. Slipping between cargo bays, Jericho must execute a precise tactical cleanup across 10 danger zones to restore safety to the metropolis.</div>
            <div id="loadPercent" style="color:#06b6d4; font-family:monospace; font-size:14px; font-weight:bold; display:none;">INITIALIZING JERICHO MATRIX: 0%</div>
            <div class="load-bar-track" id="barTrack" style="display:none;"><div class="load-bar-fluid" id="loadBar"></div></div>
            <div id="tapPrompt" class="blink-prompt">PRESS SCREEN TO CONTINUE</div>
        </div>

        <!-- PITCH-BLACK CHAPTER ONE INTERMISSION PLATE -->
        <div id="chapterOverlay">
            <div style="color:white; font-family:monospace; font-size:18px; font-weight:bold; letter-spacing:3px;">CHAPTER 1</div>
            <div style="color:#64748b; font-family:sans-serif; font-size:11px; margin-top:5px; letter-spacing:1px;">PORT TERMINAL SANITIZATION</div>
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
            <button class="retry-btn" onclick="resetArcadeEngine(true)">REDEPLOY OPERATIVE 🔄</button>
        </div>

        <div id="winScreen">
            <div style="color:#eab308; font-size:28px; font-weight:bold; text-shadow: 0 0 12px #eab308;">👑 COMPLETE CAMPAIGN VICTORY 👑</div>
            <div style="color:white; font-size:14px; text-align:center; margin-top:15px; max-width:320px; line-height:1.5;">EXCELLENT WORK JERICHO!<br>All 10 campaign sectors successfully secured!</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">REPLAY CAMPAIGN 🎮</button>
        </div>
    </div>

<script>
    let currentX = 190, currentY = 240, score = 200, isOver = false;
    let threatsList = []; let playerHp = 100;
    let audioCtx = null, spawnTimerId = null, runLoopTimerId = null, heartbeatIntervalId = null;

    let currentSector = "A"; let sectorKills = 0;
    const sectorsList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
    const sectorRequirements = { "A":3, "B":3, "C":3, "D":3, "E":4, "F":4, "G":4, "H":4, "I":4, "J":5 };
    let isMoving = false; let loaderFinished = false;
    
    let perspectiveMode3rdPerson = true; 
    let cameraFlyInProgressDist = 65; 

    const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d");
    let cameraZ = 0, targetCameraZ = 0; let cameraX = 0, targetCameraX = 0; let cycleTick = 0;

    // --- 🔊 CRASH-PROOF: NATURAL UTTERANCE FEMALE AI VOICE CHANNELS ---
    function executeNaturalFemaleVoiceBrief() {
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel(); 
        
        let narrativeBriefText = document.getElementById("briefContentText").textContent;
        let speakUtterance = new SpeechSynthesisUtterance(narrativeBriefText);
        let systemVoiceRegistry = window.speechSynthesis.getVoices();
        
        // Scan the browser to enforce an explicit female voice mapping layout
        let perfectFemaleAcoustic = systemVoiceRegistry.find(v => 
            v.name.toLowerCase().includes("female") || 
            v.name.toLowerCase().includes("zira") || 
            v.name.toLowerCase().includes("hazel") ||
            v.name.toLowerCase().includes("google us english") ||
            v.name.toLowerCase().includes("natural") ||
            (v.lang.startsWith("en") && !v.name.toLowerCase().includes("male") && !v.name.toLowerCase().includes("david"))
        );
        
        if (perfectFemaleAcoustic) speakUtterance.voice = perfectFemaleAcoustic;
        speakUtterance.rate = 0.94; speakUtterance.pitch = 1.15; speakUtterance.volume = 1.0;
        window.speechSynthesis.speak(speakUtterance);
    }

    document.getElementById("voiceTriggerBtn").addEventListener("click", function launchRegulatedEngine() {
        document.getElementById("voiceTriggerBtn").style.display = "none";
        document.getElementById("loadPercent").style.display = "block";
        document.getElementById("barTrack").style.display = "block";
        
        executeNaturalFemaleVoiceBrief();
        executeMatrixLoadingSequence();
    });
    function executeMatrixLoadingSequence() {
        let percentage = 0; let barFluid = document.getElementById("loadBar"); let txtPercent = document.getElementById("loadPercent");
        let loadInterval = setInterval(() => {
            percentage += 2;
            if (barFluid) barFluid.style.width = percentage + "%";
            if (txtPercent) txtPercent.textContent = "INITIALIZING JERICHO MATRIX: " + percentage + "%";
            
            if (percentage >= 100) {
                clearInterval(loadInterval); loaderFinished = true;
                document.getElementById("tapPrompt").style.display = "block";
                
                const coverElement = document.getElementById("coverScreen");
                coverElement.addEventListener("click", function triggerCinematicTransition() {
                    // Turn off text synthesis instantly on continue touch gesture
                    if (window.speechSynthesis) window.speechSynthesis.cancel();
                    
                    coverElement.style.display = "none";
                    document.getElementById("chapterOverlay").style.display = "flex";
                    
                    // Suspend the frame black overlay for exactly 3 seconds (3000ms) before canvas initialization
                    setTimeout(() => {
                        document.getElementById("chapterOverlay").style.display = "none";
                        document.getElementById("scoreCounter").style.display = "block";
                        document.getElementById("chapterTxt").style.display = "block";
                        document.getElementById("targetTracker").style.display = "block";
                        document.getElementById("healthCounter").style.display = "block";
                        
                        perspectiveMode3rdPerson = true; cameraFlyInProgressDist = 65; 
                        runLoopTimerId = setInterval(render3DSceneGrid, 1000 / 45);
                    }, 3000);
                });
            }
        }, 22);
    }

    function setupAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
    // --- 🎬 UNIFIED FIXED 3D CAMERA ENGINE ---
    function project3D(x, y, z) {
        let relativeX = x - cameraX;
        let activePerspectiveZ = z - cameraZ;
        
        // FIXED PERSPECTIVE ALIGNMENT LINK: Ties world depth layers forward together to handle camera pans smoothly
        if (perspectiveMode3rdPerson) {
            activePerspectiveZ = z + (cameraFlyInProgressDist - 1.5);
        }
        
        if (activePerspectiveZ <= 0.1) return null;
        let fovScale = 400 / activePerspectiveZ;
        return { x: 190 + (relativeX * fovScale), y: 240 - ((y - 1.6) * fovScale), size: fovScale };
    }

    function render3DSceneGrid() {
        cycleTick += 0.05; cameraZ += (targetCameraZ - cameraZ) * 0.07; cameraX += (targetCameraX - cameraX) * 0.07;
        if (isMoving && Math.abs(cameraZ - targetCameraZ) < 0.1) { isMoving = false; }
        
        // Smooth Cinematic Third Person Panning Zoom
        if (perspectiveMode3rdPerson) {
            cameraFlyInProgressDist -= (cameraFlyInProgressDist - 1.5) * 0.038; 
            if (cameraFlyInProgressDist <= 2.2) {
                perspectiveMode3rdPerson = false;
                document.getElementById("weapon").style.display = "block";
                if (!spawnTimerId) spawnTimerId = setInterval(spawn3DThreatUnit, 1350);
            }
        }

        let isOutdoorSector = ["E","F","G","H","I","J"].includes(currentSector);
        ctx.fillStyle = "#010206"; ctx.fillRect(0, 0, 380, 480);

        // --- 🏗️ FIXED CANVAS DRAW BOUNDS: ALL CALLS EXPLICITLY BOUND TO CONTEXT ARRAYS ---
        for (let z = 84; z >= 0; z -= 3) {
            let zPos = Math.floor(cameraZ) + z; zPos = zPos - (zPos % 3);
            let pNear = project3D(0, 0, zPos); let pFar = project3D(0, 0, zPos + 3); if (!pNear || !pFar) continue;
            let fogOpacity = Math.min(1, z / 65); let lightScale = 1 - fogOpacity;
            
            let floorColor = "rgba(" + Math.floor(18 * lightScale) + "," + Math.floor(24 * lightScale) + "," + Math.floor(38 * lightScale) + ",1)";
            ctx.fillStyle = floorColor; ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            
            ctx.strokeStyle = "rgba(20, 184, 166, 0.25)"; ctx.lineWidth = Math.max(1, pNear.size * 0.03); 
            ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); 
            ctx.stroke(); // BOUND CORRECTLY TO ACTIVE LAYER VARIABLE CONTEXT
            
            let isRidgeFold = Math.floor(zPos * 2.5) % 2 === 0;
            ctx.fillStyle = "rgba(" + (isRidgeFold ? Math.floor(13*lightScale) : Math.floor(19*lightScale)) + "," + (isRidgeFold ? Math.floor(148*lightScale) : Math.floor(94*lightScale)) + "," + (isRidgeFold ? Math.floor(136*lightScale) : Math.floor(89*lightScale)) + ",1)";
            ctx.beginPath(); ctx.moveTo(190 - (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 - (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 - (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
            ctx.beginPath(); ctx.moveTo(190 + (4.5 * pNear.size), 240 + (1.6 * pNear.size)); ctx.lineTo(190 + (4.5 * pNear.size), 240 - (2.4 * pNear.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 - (2.4 * pFar.size)); ctx.lineTo(190 + (4.5 * pFar.size), 240 + (1.6 * pFar.size)); ctx.fill();
        }
        let depthDrawQueue = [];
        static3DObstacles.forEach(b => { if (b.z >= cameraZ) depthDrawQueue.push({ type: "crate", z: b.z, data: b }); });
        if (!perspectiveMode3rdPerson) {
            threatsList.forEach(t => { if (!t.isDying && t.z >= cameraZ) depthDrawQueue.push({ type: "enemy", z: t.z, data: t }); });
        }
        depthDrawQueue.sort((a, b) => b.z - a.z);

        depthDrawQueue.forEach(item => {
            if (item.type === "crate") {
                let b = item.data; let p = project3D(b.x, b.y, b.z); if (!p) return; let w = 1.9 * p.size; let h = 2.2 * p.size;
                ctx.fillStyle = b.baseColor; ctx.fillRect(p.x - w/2, p.y - h/2, w, h); ctx.fillStyle = b.shadowColor; ctx.fillRect(p.x - w/2 + (w*0.08), p.y - h/2 + (h*0.08), w * 0.84, h * 0.84);
                ctx.strokeStyle = "rgba(0,0,0,0.6)"; ctx.lineWidth = Math.max(1.5, p.size * 0.04); ctx.strokeRect(p.x - w/2, p.y - h/2, w, h);
            } 
            else if (item.type === "enemy") {
                let t = item.data; if (!isMoving) t.loopTick++;
                let smoothSinPeekFactor = (Math.sin(t.loopTick * 0.05) + 1) / 2; let isActivelyOut = (smoothSinPeekFactor > 0.45); 
                let p = project3D(t.x, t.y, t.z); if (!p) return; let s = p.size * 0.4;
                let currentVisualX = p.x - (s * 1.5) + (s * 1.5 * smoothSinPeekFactor);
                t.currentScreenX = currentVisualX; t.currentScreenY = p.y - (s * 0.5); t.currentRadius = s * 1.15;

                if (isActivelyOut) { t.ring.style.opacity = "1"; t.age++; } else { t.ring.style.opacity = "0"; }
                if (t.age > 0 && t.age % 42 === 0 && !isMoving && isActivelyOut) { t.isFlashing = true; triggerEnemyDamageStrike(); setTimeout(() => { t.isFlashing = false; }, 70); }

                ctx.fillStyle = "#1e291b"; ctx.fillRect(currentVisualX - s/2, p.y - s, s, s * 1.3); ctx.strokeStyle = "#000"; ctx.lineWidth = 1.5; ctx.strokeRect(currentVisualX - s/2, p.y - s, s, s * 1.3);
                ctx.fillStyle = "#3f3f46"; ctx.fillRect(currentVisualX - s/3, p.y - s * 0.9, s * 0.66, s * 0.7);
                ctx.fillStyle = "#d4b38a"; ctx.beginPath(); ctx.arc(currentVisualX, p.y - s * 1.3, s * 0.35, 0, Math.PI*2); ctx.fill(); ctx.stroke();
                ctx.fillStyle = "#27272a"; ctx.beginPath(); ctx.arc(currentVisualX, p.y - s * 1.4, s * 0.36, Math.PI, 0); ctx.fill(); ctx.stroke();
                ctx.fillRect(currentVisualX - s/3, p.y + s * 0.3, s * 0.22, s * 0.8); ctx.fillRect(currentVisualX + s/8, p.y + s * 0.3, s * 0.22, s * 0.8);
                ctx.fillStyle = "#09090b"; ctx.fillRect(currentVisualX + s/6, p.y - s/3, s * 0.75, s * 0.18);

                if (t.isFlashing && isActivelyOut) { let flashGrd = ctx.createRadialGradient(currentVisualX + s * 0.9, p.y - s/4, 1, currentVisualX + s * 0.9, p.y - s/4, s * 0.55); flashGrd.addColorStop(0, "#ffffff"); flashGrd.addColorStop(0.5, "#eab308"); flashGrd.addColorStop(1, "transparent"); ctx.fillStyle = flashGrd; ctx.beginPath(); ctx.arc(currentVisualX + s * 0.9, p.y - s/4, s * 0.55, 0, Math.PI*2); ctx.fill(); ctx.closePath(); }
                t.ring.style.left = currentVisualX + "px"; t.ring.style.top = (p.y - s/2) + "px"; let rSize = Math.max(0, 95 * (1.3 - (t.age / 40))); t.ring.style.width = rSize + "px"; t.ring.style.height = rSize + "px";
            }
        });

        // --- 🏗️ DETAILED MULTI-TIERED 3D DESIGN FOR HAMPI JERICHO ---
        if (perspectiveMode3rdPerson) {
            let jX = 190; let jY = 380; let scaleSize = 56; 
            let legWalkCycleSway = Math.sin(cycleTick * 1.8) * (scaleSize * 0.24);

            // A: Long Leg Trousers Pants Pants
            ctx.fillStyle = "#0d1321"; 
            ctx.fillRect(jX - (scaleSize * 0.28), jY, scaleSize * 0.20, scaleSize * 1.1 + legWalkCycleSway);
            ctx.fillRect(jX + (scaleSize * 0.08), jY, scaleSize * 0.20, scaleSize * 1.1 - legWalkCycleSway);
            ctx.strokeStyle = "#000000"; ctx.lineWidth = 1.5;
            ctx.strokeRect(jX - (scaleSize * 0.28), jY, scaleSize * 0.20, scaleSize * 1.1 + legWalkCycleSway);
            ctx.strokeRect(jX + (scaleSize * 0.08), jY, scaleSize * 0.20, scaleSize * 1.1 - legWalkCycleSway);

            // B: Strong Broad Shoulders Jacket Torso Frame Shell
            ctx.fillStyle = "#1e293b"; ctx.fillRect(jX - (scaleSize * 0.55), jY - (scaleSize * 1.1), scaleSize * 1.1, scaleSize * 1.15);
            ctx.strokeRect(jX - (scaleSize * 0.55), jY - (scaleSize * 1.1), scaleSize * 1.1, scaleSize * 1.15);

            // C: Tactical Kevlar Trauma Vest Overlapping Harness Plates
            ctx.fillStyle = "#0f766e"; ctx.fillRect(jX - (scaleSize * 0.4), jY - (scaleSize * 0.95), scaleSize * 0.8, scaleSize * 0.8);
            ctx.fillStyle = "#115e59"; ctx.fillRect(jX - (scaleSize * 0.35), jY - (scaleSize * 0.85), scaleSize * 0.18, scaleSize * 0.7); ctx.fillRect(jX + (scaleSize * 0.18), jY - (scaleSize * 0.85), scaleSize * 0.18, scaleSize * 0.7);

            // D: Camouflage Helmet Cap Unit
            ctx.fillStyle = "#cdba96"; ctx.beginPath(); ctx.arc(jX, jY - (scaleSize * 1.3), scaleSize * 0.26, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "#14532d"; ctx.beginPath(); ctx.arc(jX, jY - (scaleSize * 1.4), scaleSize * 0.28, Math.PI, 0); ctx.fill(); ctx.stroke();
        }
    }
    function aim(e) {
        if (isOver || document.getElementById("coverScreen").style.display === "flex" || perspectiveMode3rdPerson) return;
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

    function triggerMouseCoordinateFire(e) {
        let bounds = gameArea.getBoundingClientRect();
        currentX = e.clientX - bounds.left; currentY = e.clientY - bounds.top;
        triggerFire();
    }
    gameArea.addEventListener("mousedown", (e) => { if(!loaderFinished || perspectiveMode3rdPerson) return; if(e.target.tagName !== "BUTTON") triggerMouseCoordinateFire(e); });
    gameArea.addEventListener("touchstart", (e) => { if(!loaderFinished || perspectiveMode3rdPerson) return; if(e.target.tagName !== "BUTTON") { e.preventDefault(); aim(e); triggerFire(); } }, { passive: false });

    function triggerSectorPathMovement() {
        if (isMoving) return; isMoving = true;
        let idx = sectorsList.indexOf(currentSector);
        if (idx >= 0 && idx < sectorsList.length - 1) {
            currentSector = sectorsList[idx + 1]; sectorKills = 0; targetCameraZ = (idx + 1) * 16;
            let rollingPathRoll = Math.random();
            if (rollingPathRoll < 0.33) { targetCameraX = -1.6; } else if (rollingPathRoll < 0.66) { targetCameraX = 1.6; } else { targetCameraX = 0.0; }
            if (["E","F","G","H","I","J"].includes(currentSector)) { document.getElementById("chapterTxt").innerText = "CH 1: OUTSIDE CARGO TERMINAL"; }
        } else {
            clearInterval(spawnTimerId); clearInterval(runLoopTimerId); isOver = true;
            if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
            document.getElementById("winScreen").style.display = "flex"; return;
        }
        let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
    }

    function triggerEnemyDamageStrike() {
        if (isOver || document.getElementById("winScreen").style.display === "flex" || isMoving || perspectiveMode3rdPerson) return;
        playerHp -= 20; if (playerHp < 0) playerHp = 0; healthCounter.innerText = `HP: ${playerHp}`;
        gameArea.classList.add("taking-damage"); setTimeout(() => gameArea.classList.remove("taking-damage"), 130);
        if (playerHp <= 20 && !heartbeatIntervalId) { gameArea.classList.add("critical-pulse"); }
        if (playerHp <= 0) { isOver = true; clearInterval(spawnTimerId); clearInterval(runLoopTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); gameArea.classList.remove("critical-pulse"); heartbeatIntervalId = null; } finalScore.innerText = "Final Score Log: " + score; overScreen.style.display = "flex"; }
    }

    function triggerFire() {
        if (isOver || document.getElementById("winScreen").style.display === "flex" || isMoving || perspectiveMode3rdPerson) return;
        flash.style.display = "block"; setTimeout(() => { flash.style.display = "none"; }, 60);
        let hitTarget = null; let lowestDistance = Infinity;
        threatsList.forEach(t => {
            if (t.isDying) return;
            let d = Math.hypot(currentX - t.currentScreenX, currentY - t.currentScreenY);
            if (d < t.currentRadius && d < lowestDistance) { lowestDistance = d; hitTarget = t; }
        });
        if (hitTarget) {
            hitTarget.isDying = true; score += 100; scoreCounter.innerText = String(score).padStart(5, '0'); sectorKills += 1;
            let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
            hitTarget.ring.remove(); threatsList = threatsList.filter(item => item !== hitTarget);
            if (sectorKills >= needed) { document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = []; setTimeout(triggerSectorPathMovement, 400); }
        }
    }

    function spawn3DThreatUnit() {
        if (isOver || threatsList.length >= 2 || isMoving || document.getElementById("winScreen").style.display === "flex" || perspectiveMode3rdPerson) return;
        let idx = sectorsList.indexOf(currentSector); let spawnZ = cameraZ + 12 + (idx * 0.5); let spawnX = cameraX + (Math.random() * 2.6) - 1.3;
        let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);
        threatsList.push({ x: spawnX, y: 0.2, z: spawnZ, age: 0, loopTick: Math.floor(Math.random()*60), isDying: false, isFlashing: false, ring: ring, currentScreenX: 0, currentScreenY: 0, currentRadius: 24 });
    }

    window.resetArcadeEngine = function(fullReset) {
        if (spawnTimerId) { clearInterval(spawnTimerId); spawnTimerId = null; }
        clearInterval(runLoopTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
        document.querySelectorAll(".target-ring").forEach(el => el.remove()); threatsList = [];
        cameraZ = 0; targetCameraZ = 0; cameraX = 0; targetCameraX = 0; currentSector = "A"; sectorKills = 0; playerHp = 100; score = 200; isMoving = false; isOver = false;
        document.getElementById("winScreen").style.display = "none"; document.getElementById("overScreen").style.display = "none";
        gameArea.className = ""; healthCounter.innerText = "HP: 100"; scoreCounter.innerText = "00200"; document.getElementById("chapterTxt").innerText = "CH 1: 3D CONTAINER PORT";
        let needed = sectorRequirements[currentSector]; targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
        perspectiveMode3rdPerson = true; cameraFlyInProgressDist = 65; document.getElementById("weapon").style.display = "none";
        runLoopTimerId = setInterval(render3DSceneGrid, 1000 / 45);
    };
</script>
</body>
</html>
'''

import base64
encoded_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
iframe_src_str = f"data:text/html;base64,{encoded_html}"

cb_id = random.randint(100000, 999999)
st.markdown(f'<!-- Fresh Matrix Deploy Anchor ID: {cb_id} -->', unsafe_allow_html=True)
components.iframe(src=iframe_src_str, height=560, scrolling=False)
