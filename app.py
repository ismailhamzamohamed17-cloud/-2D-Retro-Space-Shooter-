import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Tactical: 3D Rail Shooter", layout="centered")
st.title("⚡ Virtua Tactical: 3D Operations")

game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        #gameArea { 
            position: relative; width: 380px; height: 480px; 
            background: #020617; border: 4px solid #1a1f26; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none;
            box-shadow: 0 24px 60px rgba(0,0,0,0.9);
        }

        /* FILM GRAIN + DYNAMIC FULL-SCREEN TACTICAL DAMAGE FLASH */
        #gameArea::after {
            content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 28;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://w3.org id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.045'/%3E%3C/svg%3E");
            background-size: auto;
            box-shadow: inset 0 0 80px rgba(0, 0, 0, 0.95), inset 0 0 140px rgba(0, 0, 0, 0.85);
            background-color: rgba(220, 20, 20, 0);
            transition: box-shadow 0.1s ease-out, background-color 0.1s ease-out;
        }

        #gameArea.taking-damage::after {
            background-color: rgba(220, 20, 20, 0.22);
            box-shadow: inset 0 0 110px rgba(220, 20, 20, 0.95), inset 0 0 180px rgba(180, 0, 0, 0.95);
        }
        #gameArea.critical-pulse::after { animation: fullViewportLowHpPulse 0.55s ease-in-out infinite alternate; }
        @keyframes fullViewportLowHpPulse {
            0% { background-color: rgba(220, 20, 20, 0.05); box-shadow: inset 0 0 85px rgba(160, 0, 0, 0.7); }
            100% { background-color: rgba(220, 20, 20, 0.25); box-shadow: inset 0 0 115px rgba(240, 0, 0, 0.95), inset 0 0 170px rgba(200, 0, 0, 0.85); }
        }

        canvas { position: absolute; top: 0; left: 0; width: 380px; height: 480px; z-index: 1; }
        #weapon { position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%) scale(1.1); width: 100px; height: 160px; pointer-events: none; z-index: 25; will-change: transform; }
        .w-slide { position: absolute; top: 40px; left: 24px; width: 52px; height: 50px; background: linear-gradient(to right, #111 0%, #2a2a2a 30%, #0d0d0d 50%, #2a2a2a 70%, #111 100%); border-radius: 6px 6px 2px 2px; border-top: 1px solid #444; box-shadow: 0 12px 25px rgba(0,0,0,0.8), inset 0 2px 3px rgba(255,255,255,0.1); }
        .w-holo-sight { position: absolute; top: 2px; left: 29px; width: 42px; height: 38px; border: 3.5px solid #1c1c1c; border-bottom: none; border-radius: 6px 6px 0 0; background: linear-gradient(to bottom, rgba(0,240,255,0.1), rgba(0,240,255,0.02)); box-shadow: inset 0 0 8px rgba(0,240,255,0.15); }
        .w-holo-sight::after { content: ''; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: #ff003c; border-radius: 50%; box-shadow: 0 0 10px 2px #ff003c; }
        .w-grip-back { position: absolute; top: 90px; left: 32px; width: 36px; height: 70px; background: linear-gradient(to right, #0a0a0a, #1a1a1a, #050505); border-radius: 3px; }
        #flash { position: absolute; top: 15px; left: 30px; width: 40px; height: 40px; background: radial-gradient(circle, #ffffff 15%, #ff3c00 60%, transparent 80%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 10px #ff3c00); }

        /* FIXED: Added pointer-events: none so tracking rings never intercept bullet touch points */
        .target-ring { position: absolute; border: 3px dashed #ff2222; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-50%, -50%); display: block; box-shadow: 0 0 10px #ff2222; }
        #sight { position: absolute; width: 32px; height: 32px; border: 2px solid #00ffff; border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); z-index: 20; box-shadow: 0 0 8px #00ffff; display: none; }

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
        <div id="chapterTxt">CH 1: 3D CONTAINER PORT</div>
        <div id="targetTracker">SECTOR A: 0/3</div>
        <div id="healthCounter">HP: 100</div>
        
        <canvas id="gameCanvas" width="380" height="480"></canvas>
        
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
            <div class="intermission-title">CAMPAIGN ACCOMPLISHED! 🎉</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">PLAY AGAIN 🎮</button>
        </div>
    </div>

<script>
    let currentX = 190, currentY = 240, score = 200, isOver = false;
    let threatsList = []; let playerHp = 100;
    let audioCtx = null, spawnTimerId = null, runLoopTimerId = null, heartbeatIntervalId = null;

    let currentSector = "A"; let sectorKills = 0;
    const sectorRequirements = { "A": 3, "B": 3, "C": 4 };

    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let cameraZ = 0, targetCameraZ = 0;
    let cameraX = 0, targetCameraX = 0;

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
    function aim(e) {
        if (isOver) return;
        let evt = e; if (e.touches && e.touches.length > 0) { evt = e.touches; } else if (e.changedTouches && e.changedTouches.length > 0) { evt = e.changedTouches; }
        let bounds = gameArea.getBoundingClientRect();
        currentX = evt.clientX - bounds.left; currentY = evt.clientY - bounds.top;
        
        sight.style.display = "block"; sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        let swayX = (currentX - 190) / 10; let swayY = (currentY - 240) / 12;
        weapon.style.transform = "translateX(-50%) scale(1.1) rotate(" + swayX + "deg) translateY(" + swayY + "px)";
    }
    gameArea.addEventListener("mousemove", aim); gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); aim(e); triggerFire(); } }, { passive: false });

    function project3D(x, y, z) {
        let relativeX = x - cameraX;
        let relativeZ = z - cameraZ;
        if (relativeZ <= 0.1) return null;
        let fovScale = 400 / relativeZ;
        let px = 190 + (relativeX * fovScale);
        let py = 240 - ((y - 1.6) * fovScale);
        return { x: px, y: py, size: fovScale };
    }

    const static3DObstacles = [
        { x: -1.8, y: 0.5, z: 15, color: "#7c2d12" },
        { x: 1.8, y: 0.5, z: 30, color: "#1e3a8a" },
        { x: -1.5, y: 0.5, z: 45, color: "#065f46" }
    ];
    function render3DSceneGrid() {
        ctx.fillStyle = "#0a0f1d"; ctx.fillRect(0, 0, 380, 480);

        cameraZ += (targetCameraZ - cameraZ) * 0.07;
        cameraX += (targetCameraX - cameraX) * 0.07;

        for (let z = 80; z >= 0; z -= 4) {
            let zPos = Math.floor(cameraZ) + z;
            zPos = zPos - (zPos % 4); 

            let pNear = project3D(0, 0, zPos);
            let pFar = project3D(0, 0, zPos + 4);
            if (!pNear || !pFar) continue;

            let fogOpacity = Math.min(1, z / 60);
            ctx.strokeStyle = "rgba(30, 41, 59, " + (1 - fogOpacity) + ")";
            ctx.lineWidth = Math.max(1, pNear.size / 60);

            ctx.beginPath();
            ctx.moveTo(190 - (4 * pNear.size), 240 + (1.6 * pNear.size));
            ctx.lineTo(190 + (4 * pNear.size), 240 + (1.6 * pNear.size));
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(190 - (4 * pNear.size), 240 + (1.6 * pNear.size));
            ctx.lineTo(190 - (4 * pNear.size), 240 - (2.4 * pNear.size));
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(190 + (4 * pNear.size), 240 + (1.6 * pNear.size));
            ctx.lineTo(190 + (4 * pNear.size), 240 - (2.4 * pNear.size));
            ctx.stroke();
        }

        static3DObstacles.forEach(b => {
            let p = project3D(b.x, b.y, b.z);
            if (!p || b.z < cameraZ) return;
            let w = 1.8 * p.size; let h = 2.0 * p.size;
            ctx.fillStyle = b.color; ctx.fillRect(p.x - w/2, p.y - h/2, w, h);
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.strokeRect(p.x - w/2, p.y - h/2, w, h);
        });

        threatsList.forEach(t => {
            if (t.isDying) return;
            t.age++;
            
            if (t.age > 0 && t.age % 35 === 0) {
                t.isFlashing = true; triggerEnemyDamageStrike();
                setTimeout(() => { t.isFlashing = false; }, 70);
            }

            let p = project3D(t.x, t.y, t.z);
            if (!p) return;

            let s = p.size * 0.4;
            t.currentScreenX = p.x; 
            // FIXED: Shifted structural hitbox center point down to match visual torso configurations perfectly
            t.currentScreenY = p.y - (s / 2); 
            t.currentRadius = s * 0.95; // Expanded hit radius to ensure first shots connect reliably

            ctx.fillStyle = "#14532d"; ctx.fillRect(p.x - s/2, p.y - s, s, s * 1.3);
            ctx.strokeStyle = "#000"; ctx.strokeRect(p.x - s/2, p.y - s, s, s * 1.3);
            ctx.fillStyle = "#cdba96"; ctx.beginPath(); ctx.arc(p.x, p.y - s * 1.3, s * 0.35, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "#1c210e"; ctx.fillRect(p.x - s/3, p.y + s * 0.3, s * 0.22, s * 0.8); ctx.fillRect(p.x + s/8, p.y + s * 0.3, s * 0.22, s * 0.8);
            ctx.fillStyle = "#111111"; ctx.fillRect(p.x + s/4, p.y - s/4, s * 0.7, s * 0.2);

            if (t.isFlashing) {
                let flashGrd = ctx.createRadialGradient(p.x + s, p.y - s/6, 1, p.x + s, p.y - s/6, s * 0.5);
                flashGrd.addColorStop(0, "#ffffff"); flashGrd.addColorStop(0.4, "#ffaa00"); flashGrd.addColorStop(1, "transparent");
                ctx.fillStyle = flashGrd; ctx.beginPath(); ctx.arc(p.x + s, p.y - s/6, s * 0.5, 0, Math.PI*2); ctx.fill(); ctx.closePath();
            }

            t.ring.style.left = p.x + "px"; t.ring.style.top = (p.y - s/2) + "px";
            let rSize = Math.max(0, 95 * (1.3 - (t.age / 40)));
            t.ring.style.width = rSize + "px"; t.ring.style.height = rSize + "px";
        });
    }
    function triggerSectorPathMovement() {
        if (currentSector === "A") {
            currentSector = "B"; sectorKills = 0; targetCameraZ = 16; targetCameraX = 1.2;
        } else if (currentSector === "B") {
            currentSector = "C"; sectorKills = 0; targetCameraZ = 32; targetCameraX = -1.2;
        } else if (currentSector === "C") {
            clearInterval(spawnTimerId); clearInterval(runLoopTimerId); isOver = true;
            if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); heartbeatIntervalId = null; }
            intermissionScreen.style.display = "flex"; return;
        }
        let needed = sectorRequirements[currentSector];
        targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
        sound("level");
    }

    function triggerEnemyDamageStrike() {
        if (isOver || intermissionScreen.style.display === "flex") return;
        playerHp -= 20; if (playerHp < 0) playerHp = 0; healthCounter.innerText = `HP: ${playerHp}`; sound("bullet_crack");
        gameArea.classList.add("taking-damage"); setTimeout(() => gameArea.classList.remove("taking-damage"), 130);
        if (playerHp <= 20 && !heartbeatIntervalId) { gameArea.classList.add("critical-pulse"); heartbeatIntervalId = setInterval(() => { sound("heartbeat"); }, 550); }
        if (playerHp <= 0) { isOver = true; sound("boom"); clearInterval(spawnTimerId); clearInterval(runLoopTimerId); if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); gameArea.classList.remove("critical-pulse"); heartbeatIntervalId = null; } finalScore.innerText = "Final Operation Score: " + score; overScreen.style.display = "flex"; }
    }

    function triggerFire() {
        if (isOver || intermissionScreen.style.display === "flex") return;
        sound("zap"); flash.style.display = "block"; setTimeout(() => { flash.style.display = "none"; }, 60);

        let hitTarget = null; let lowestDistance = Infinity;
        threatsList.forEach(t => {
            if (t.isDying) return;
            let d = Math.hypot(currentX - t.currentScreenX, currentY - t.currentScreenY);
            if (d < t.currentRadius && d < lowestDistance) { lowestDistance = d; hitTarget = t; }
        });

        if (hitTarget) {
            hitTarget.isDying = true; sound("shout_aaa");
            score += 100; scoreCounter.innerText = String(score).padStart(5, '0');
            sectorKills += 1;
            
            let needed = sectorRequirements[currentSector];
            targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
            hitTarget.ring.remove();
            threatsList = threatsList.filter(item => item !== hitTarget);

            if (sectorKills >= needed) {
                document.querySelectorAll(".target-ring").forEach(el => el.remove());
                threatsList = []; setTimeout(triggerSectorPathMovement, 500);
            }
        }
    }

    function spawn3DThreatUnit() {
        let maxSimultaneous = 2; if (isOver || threatsList.length >= maxSimultaneous) return;

        // FIXED: Anchored spawner depth equations relative to the active camera sector zone milestones
        let spawnZ = 12;
        if (currentSector === "B") spawnZ = 28;
        if (currentSector === "C") spawnZ = 44;

        let spawnX = cameraX + (Math.random() * 2.8) - 1.4;
        let ring = document.createElement("div"); ring.className = "target-ring"; gameArea.appendChild(ring);

        threatsList.push({
            x: spawnX, y: 0.2, z: spawnZ, age: 0, isDying: false, isFlashing: false, ring: ring,
            currentScreenX: 0, currentScreenY: 0, currentRadius: 24
        });
        sound("ding");
    }

    window.resetArcadeEngine = function(fullReset) { location.reload(); };

    runLoopTimerId = setInterval(render3DSceneGrid, 1000 / 45);
    spawnTimerId = setInterval(spawn3DThreatUnit, 1300);
</script>
</body>
</html>
'''

st.markdown('<div class="cab">', unsafe_allow_html=True)
components.html(game_html, height=560, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)
