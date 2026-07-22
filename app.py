import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hamza shooting game", layout="centered")
st.title("🚓 Shooting game made by Hamza")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
    
    #gameArea { 
        position: relative; 
        width: 380px; 
        height: 480px; 
        background: linear-gradient(to bottom, #4a777a 0%, #a1c4fd 40%, #727d8c 41%, #3a4454 100%); 
        border: 4px solid #444; 
        overflow: hidden; 
        margin: auto; 
        border-radius: 16px; 
        touch-action: none;
        box-shadow: 0 12px 32px rgba(0,0,0,0.6);
    }
    
    .building-l { position: absolute; top: 50px; left: 0; width: 130px; height: 150px; background: repeating-linear-gradient(to bottom, #1b263b 0px, #1b263b 14px, transparent 14px, transparent 20px), #0d1b2a; z-index: 1; }
    .building-r { position: absolute; top: 40px; right: 0; width: 110px; height: 160px; background: repeating-linear-gradient(to bottom, #14213d 0px, #14213d 10px, transparent 10px, transparent 16px), #000814; z-index: 1; }
    .roadway { position: absolute; bottom: 0; left: 0; width: 100%; height: 280px; background: linear-gradient(to bottom, #434952, #2c3036); clip-path: polygon(42% 0%, 58% 0%, 100% 100%, 0% 100%); z-index: 2; }
    .roadway::before { content: ''; position: absolute; top: 0; left: 50%; width: 8px; height: 100%; background: repeating-linear-gradient(to bottom, #e5e5e5 0px, #e5e5e5 25px, transparent 25px, transparent 50px); transform: translateX(-50%); opacity: 0.4; }

    /* Moving Vehicle Styling */
    #car {
        position: absolute; top: 195px; left: 110px; width: 160px; height: 95px;
        background: linear-gradient(to bottom, #3a3d40, #181a1b, #0f1012); border-radius: 14px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.6); z-index: 4;
        border: 1px solid #232526;
        transition: left 0.1s linear;
    }
    .window { position: absolute; top: 12px; left: 14px; width: 132px; height: 32px; background: linear-gradient(180deg, rgba(142,202,230,0.6), rgba(2,48,71,0.5)); border-radius: 6px; border: 2px solid #000; }
    .light-l { position: absolute; bottom: 18px; left: 12px; width: 24px; height: 14px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; }
    .light-r { position: absolute; bottom: 18px; right: 12px; width: 24px; height: 14px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; }

    /* 🔫 DETAILED SEMI-AUTOMATIC PISTOL (MATCHES REFERENCE PHOTO PROFILE) */
    #weapon {
        position: absolute; 
        bottom: -35px; 
        right: 50px; /* Aligned right exactly like reference photo */
        width: 90px; 
        height: 180px; 
        transform: rotate(0deg); 
        pointer-events: none; 
        z-index: 25;
        will-change: transform;
    }
    /* Heavy straight metallic top slide block */
    .w-slide { 
        position: absolute; top: 10px; left: -40px; width: 120px; height: 30px; 
        background: linear-gradient(to bottom, #2b2b2b, #151515, #222); 
        border-radius: 4px 2px 2px 2px; border-bottom: 3px solid #0d0d0d; 
    }
    /* Front sight and muzzle tip */
    .w-slide::before { content: ''; position: absolute; left: -4px; top: 6px; width: 4px; height: 10px; background: #000; }
    /* Checkered vertical frame texture handle */
    .w-grip { 
        position: absolute; top: 38px; left: 35px; width: 36px; height: 115px; 
        background: repeating-linear-gradient(45deg, #3d2b1f, #3d2b1f 2px, #241911 2px, #241911 4px); 
        border: 3px solid #0a0a0a; border-radius: 4px 6px 12px 6px; transform: rotate(-8deg); 
        box-shadow: -6px 6px 12px rgba(0,0,0,0.6); 
    }
    .w-frame { position: absolute; top: 36px; left: -20px; width: 60px; height: 25px; background: #1a1a1a; border-radius: 0 0 10px 4px; }
    .w-guard { position: absolute; top: 34px; left: -8px; width: 24px; height: 24px; border: 3px solid #1a1a1a; border-radius: 50%; }

    #flash { position: absolute; top: -10px; left: -35px; width: 40px; height: 45px; background: radial-gradient(circle, #fff 10%, #ffea00 50%, transparent 70%); border-radius: 50%; display: none; z-index: 26; }
    #sight { position: absolute; top: 218px; left: 168px; width: 32px; height: 32px; border: 2px solid #00f0ff; border-radius: 50%; pointer-events: none; z-index: 20; box-shadow: 0 0 6px rgba(0,240,255,0.5); }
    #sight::before { content: ''; position: absolute; top: 15px; left: 0; width: 32px; height: 1px; background: #00f0ff; }
    #sight::after { content: ''; position: absolute; top: 0; left: 15px; width: 1px; height: 32px; background: #00f0ff; }
    .target-ring { position: absolute; width: 90px; height: 90px; border: 3px dashed #ffea00; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-30px, -30px); transition: width 1.3s linear, height 1.3s linear, transform 1.3s linear; }

    /* 🏃 REALISTIC HUMANOIDS: HAIR, LEGS, EYES & EMOTIONS */
    .threat { position: absolute; width: 45px; height: 75px; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; }
    
    /* Head structure with eyes and hair geometry */
    .t-head { 
        background: #e0a96d; border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #111; position: relative; 
    }
    /* Hair layer styling */
    .t-head::before { 
        content: ''; position: absolute; top: -3px; left: -1px; width: 26px; height: 10px; background: #4a2c11; border-radius: 12px 12px 0 0; 
    }
    /* Expressive eyes with built-in angry emotion state styling */
    .t-eyes { 
        position: absolute; top: 10px; left: 3px; width: 16px; height: 4px; display: flex; justify-content: space-between; 
    }
    .t-eyes::before, .t-eyes::after { 
        content: ''; width: 4px; height: 4px; background: #000; border-radius: 50%; border-top: 1.5px solid red; /* Angry brow look */
    }
    /* Torso and jacket styling */
    .t-torso { background: linear-gradient(to right, #1d3557, #457b9d, #1d3557); width: 32px; height: 34px; border-radius: 4px; border: 1.5px solid #111; position: relative; }
    .t-arm { position: absolute; top: 4px; width: 24px; height: 10px; background: #1d3557; border: 1.5px solid #111; border-radius: 2px; }
    .arm-l { left: -14px; transform: rotate(-10deg); }
    .arm-r { right: -14px; transform: rotate(10deg); }
    
    /* Moving lower leg nodes */
    .t-legs { 
        display: flex; justify-content: space-around; width: 28px; height: 16px; margin-top: auto; 
    }
    .t-leg { 
        background: #111; width: 8px; height: 100%; border-radius: 2px; 
        animation: legWalk 0.3s ease-in-out infinite alternate; 
    }
    .t-leg:nth-child(2) { animation-delay: 0.15s; }
    
    @keyframes legWalk { 
        0% { transform: translateY(0); } 100% { transform: translateY(-4px); } 
    }

    #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; }
    #overScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
    .retry-btn { padding: 12px 28px; background: #e63946; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(230,57,70,0.5); }
</style>
</head>
<body>

    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div class="building-l"></div>
        <div class="building-r"></div>
        <div class="roadway"></div>
        
        <div id="car">
            <div class="window"></div>
            <div class="light-l"></div>
            <div class="light-r"></div>
        </div>

        <div id="sight"></div>
        
        <div id="weapon">
            <div id="flash"></div>
            <div class="w-slide"></div>
            <div class="w-frame"></div>
            <div class="w-guard"></div>
            <div class="w-grip"></div>
        </div>

        <!-- Stable Dedicated Death Interface Context -->
        <div id="overScreen">
            <div style="color:#ffea00; font-size:32px; font-weight:bold; font-family:monospace; text-shadow:0 0 8px red;">GAME OVER</div>
            <div id="finalScore" style="color:white; font-size:18px; margin-top:10px;">Score: 200</div>
            <button class="retry-btn" onclick="resetArcadeEngine()">CONTINUE 🪙</button>
        </div>
    </div>

<script>
    let currentX = 168, currentY = 218, score = 200, isOver = false;
    let carPos = 110, carDir = 2;
    let threatsList = [];
    let audioCtx = null, spawnTimerId = null, physicsTimerId = null;

    const gameArea = document.getElementById("gameArea");
    const sight = document.getElementById("sight");
    const weapon = document.getElementById("weapon");
    const flash = document.getElementById("flash");
    const car = document.getElementById("car");
    const scoreCounter = document.getElementById("scoreCounter");
    const overScreen = document.getElementById("overScreen");
    const finalScore = document.getElementById("finalScore");

    function setupAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function sound(type) {
        setupAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);
        
        if (type === "zap") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(580, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.12);
            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.12);
        } else if (type === "ding") {
            osc.type = "sine"; osc.frequency.setValueAtTime(900, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.08);
        } else if (type === "boom") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(100, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.4);
            gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.4);
        }
    }
    // Bulletproof Aiming Engine: Snaps directly to finger coordinates instantly
    function aim(e) {
        if (isOver) return;
        let evt = e.touches ? e.touches[0] : e;
        let bounds = gameArea.getBoundingClientRect();
        
        currentX = Math.max(-10, Math.min(350, evt.clientX - bounds.left - 16));
        currentY = Math.max(-10, Math.min(450, evt.clientY - bounds.top - 16));
        
        sight.style.left = currentX + "px";
        sight.style.top = currentY + "px";
        
        // Realistic Pistol sway linked directly to target locations
        let sway = (currentX - 168) / 12;
        weapon.style.transform = `rotate(${15 + sway}deg) translateY(${(currentY - 218) / 15}px)`;
    }

    // Connect movement listeners cleanly to container tracking layers
    gameArea.addEventListener("mousemove", aim);
    gameArea.addEventListener("touchmove", (e) => { 
        e.preventDefault(); 
        aim(e); 
    }, { passive: false });

    // Tap / Click action fires pistol instantly
    gameArea.addEventListener("mousedown", (e) => { 
        if (e.target.className !== "retry-btn") triggerFire(); 
    });
    gameArea.addEventListener("touchstart", (e) => { 
        if (e.target.className !== "retry-btn") { 
            e.preventDefault(); 
            triggerFire(); 
        } 
    });

    function triggerFire() {
        if (isOver) return;
        sound("zap");
        
        // Visual Snappy Kick Recoil Animation
        flash.style.display = "block";
        weapon.style.bottom = "-45px";
        setTimeout(() => { 
            flash.style.display = "none"; 
            weapon.style.bottom = "-30px"; 
        }, 60);

        let hitCenterXTarg = currentX + 16;
        let hitCenterYTarg = currentY + 16;

        // Check if shot box coordinates overlap any spawned threats
        threatsList.forEach((t, index) => {
            let tRect = t.el.getBoundingClientRect();
            let areaRect = gameArea.getBoundingClientRect();
            let tX = tRect.left - areaRect.left;
            let tY = tRect.top - areaRect.top;

            if (hitCenterXTarg >= tX && hitCenterXTarg <= tX + 40 && hitCenterYTarg >= tY && hitCenterYTarg <= tY + 60) {
                sound("ding");
                score += 100;
                scoreCounter.innerText = String(score).padStart(5, '0');
                
                t.el.remove();
                t.ring.remove();
                threatsList.splice(index, 1);
            }
        });
    }

    function runEngineLoops() {
        // 1. Core Vehicle & Threat Pin Synchronization Clock Loop
        physicsTimerId = setInterval(() => {
            if (isOver) return;
            
            // Move car side to side smoothly
            carPos += carDir;
            if (carPos > 180 || carPos < 40) carDir *= -1;
            car.style.left = carPos + "px";

            // Safely anchor out criminals and tracking rings right onto the car frame coordinates
            threatsList.forEach((t) => {
                let updatedX = carPos + t.sideOffset;
                t.el.style.left = updatedX + "px";
                t.ring.style.left = (updatedX + 20) + "px";
            });
        }, 30);

        // 2. High-Speed Threat Generator Clock Loop
        spawnTimerId = setInterval(() => {
            if (isOver || threatsList.length >= 4) return;

            let el = document.createElement("div");
            el.className = "threat";
            
            let roll = Math.random();
            let sideOffset, topY, armClass;
            
            if (roll < 0.25) { sideOffset = -25; topY = 185; armClass = "arm-l"; }
            else if (roll < 0.5) { sideOffset = 145; topY = 185; armClass = "arm-r"; }
            else if (roll < 0.75) { sideOffset = -15; topY = 210; armClass = "arm-l"; }
            else { sideOffset = 135; topY = 210; armClass = "arm-r"; }

             el.innerHTML = `
                <div class="t-head">
                    <div class="t-eyes"></div>
                </div>
                <div class="t-torso">
                    <div class="t-arm ${armClass}"></div>
                </div>
                <div class="t-legs">
                    <div class="t-leg"></div>
                    <div class="t-leg"></div>
                </div>`;
            el.style.left = (carPos + sideOffset) + "px";
            el.style.top = topY + "px";
            gameArea.appendChild(el);

            let ring = document.createElement("div");
            ring.className = "target-ring";
            ring.style.left = (carPos + sideOffset + 20) + "px";
            ring.style.top = (topY + 15) + "px";
            gameArea.appendChild(ring);

            let threatObj = { el: el, ring: ring, sideOffset: sideOffset };
            threatsList.push(threatObj);

            // Command locking ring shrinkage instantly
            setTimeout(() => {
                if (ring.parentNode) {
                    ring.style.width = "35px"; 
                    ring.style.height = "35px";
                    ring.style.transform = "translate(-2px, -2px)";
                }
            }, 50);

            // Timer monitoring lock closure: if countdown reaches 0, execute Game Over
            setTimeout(() => {
                if (!isOver && el.parentNode) {
                    isOver = true;
                    sound("boom");
                    clearInterval(spawnTimerId);
                    clearInterval(physicsTimerId);
                    
                    finalScore.innerText = "Arcade Score: " + score;
                    overScreen.style.display = "flex";
                }
            }, 1350);

        }, 1000); // Fast arcade generation cadence
    }

    window.resetArcadeEngine = function() {
        // Pure variable cleanup routines
        clearInterval(spawnTimerId);
        clearInterval(physicsTimerId);
        
        threatsList.forEach(t => { t.el.remove(); t.ring.remove(); });
        threatsList = [];
        
        score = 200;
        isOver = false;
        carPos = 110;
        carDir = 2;
        currentX = 168;
        currentY = 218;

        scoreCounter.innerText = "00200";
        sight.style.left = "168px";
        sight.style.top = "218px";
        weapon.style.transform = "rotate(15deg)";
        overScreen.style.display = "none";

        runEngineLoops();
    };

    // Spin up engine immediately upon app boot layout load
    runEngineLoops();
</script>
</body>
</html>
"""

components.html(game_html, height=560)

