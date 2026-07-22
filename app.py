import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Sniper FPS", layout="centered")
st.title("🎯 3D Desert Sniper")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
    
    /* Layered 3D Desert Horizon (No external images) */
    #board { 
        position: relative; 
        width: 320px; 
        height: 350px; 
        background: linear-gradient(to bottom, #ff9e7d 0%, #feb47b 40%, #e07a5f 70%, #d88060 100%); 
        border: 3px solid #444; 
        overflow: hidden; 
        margin: auto; 
        border-radius: 12px; 
        touch-action: none;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    
    /* Realistic CSS Sand Dunes */
    #board::before {
        content: ''; position: absolute; bottom: 0; left: -40px; width: 220px; height: 120px; background: #c2593f; clip-path: polygon(0% 100%, 60% 15%, 100% 100%); opacity: 0.8; z-index: 1;
    }
    #board::after {
        content: ''; position: absolute; bottom: 0; right: -40px; width: 240px; height: 100px; background: #a64630; clip-path: polygon(0% 100%, 35% 5%, 100% 100%); opacity: 0.9; z-index: 2;
    }
    
    /* 3D Realistic Gun Shape on the Right Side */
    #gun {
        position: absolute;
        bottom: -10px;
        right: 10px;
        width: 30px;
        height: 140px;
        background: linear-gradient(to right, #222, #111, #333);
        transform: rotate(35deg);
        transform-origin: bottom right;
        pointer-events: none;
        z-index: 25;
        border-radius: 4px;
        box-shadow: -5px 5px 10px rgba(0,0,0,0.5);
        will-change: transform;
    }
    #gun::after {
        content: ''; position: absolute; top: -30px; left: 8px; width: 14px; height: 50px; background: #000; border-radius: 2px;
    }

    /* Green Tactical Crosshair Scope */
    #crosshair { 
        position: absolute; 
        top: 153px; 
        left: 138px; 
        width: 44px; 
        height: 44px; 
        border: 2px solid #00ff66; 
        border-radius: 50%; 
        will-change: left, top; 
        z-index: 15; 
        pointer-events: none;
    }
    #crosshair::before { content: ''; position: absolute; top: 22px; left: 0; width: 44px; height: 1px; background: #00ff66; }
    #crosshair::after { content: ''; position: absolute; top: 0; left: 22px; width: 1px; height: 44px; background: #00ff66; }
    
    #scoreTxt { position: absolute; top: 10px; left: 10px; color: black; font-weight: bold; font-size: 16px; z-index: 30; background: rgba(255,255,255,0.7); padding: 3px 8px; border-radius: 4px; }
    .retry-btn { margin-top: 20px; padding: 12px 25px; background: #e76f51; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; }
    
    /* Code-Generated Realistic Humanoid Figure Target */
    .humanoid { 
        position: absolute; 
        z-index: 5; 
        pointer-events: none; 
        display: flex;
        flex-direction: column;
        align-items: center;
        will-change: left, top, width, height;
    }
    .head { background: #1d1e2c; border-radius: 50%; width: 100%; height: 25%; }
    .torso { background: #1d1e2c; width: 60%; height: 50%; border-radius: 4px; margin-top: 5%; position: relative; }
    .limb-l { position: absolute; left: -30%; top: 10%; width: 30%; height: 80%; background: #1d1e2c; transform: rotate(15deg); }
    .limb-r { position: absolute; right: -30%; top: 10%; width: 30%; height: 80%; background: #1d1e2c; transform: rotate(-15deg); }
    .legs { display: flex; justify-content: space-around; width: 60%; height: 20%; margin-top: auto; }
    .leg { background: #1d1e2c; width: 35%; height: 100%; }
</style>
</head>
<body>

    <div id="board">
        <div id="scoreTxt">Score: 0</div>
        <div id="crosshair"></div>
        <div id="gun"></div> <!-- Sniper rifle placeholder block -->
    </div>

    <p style="text-align: center; color: #8b949e; font-size: 13px; margin-top: 12px; font-family: sans-serif; line-height: 1.4;">
        🎮 <b>Drag anywhere inside the box</b> to guide your weapon sight.<br>
        🎯 <b>Tap cleanly once without dragging</b> to fire!
    </p>

<script>
    let aimX = 138; let aimY = 153; let score = 0; let gameOver = false;
    let isMovingCrosshair = false;
    let touchMovedFlag = false;
    
    const board = document.getElementById("board");
    const crosshair = document.getElementById("crosshair");
    const scoreTxt = document.getElementById("scoreTxt");
    const gun = document.getElementById("gun");
    
    let activeEnemies = [];
    let audioCtx = null; let spawnInt = null; let bgLoop = null;

    function initAudio() {
        if (audioCtx) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        startSynthAmbientMusic();
    }

    function startSynthAmbientMusic() {
        try {
            let osc1 = audioCtx.createOscillator(); let osc2 = audioCtx.createOscillator();
            bgLoop = audioCtx.createGain();
            osc1.type = "sine"; osc1.frequency.setValueAtTime(55.00, audioCtx.currentTime);
            osc2.type = "triangle"; osc2.frequency.setValueAtTime(82.41, audioCtx.currentTime);
            bgLoop.gain.setValueAtTime(0.04, audioCtx.currentTime);
            osc1.connect(bgLoop); osc2.connect(bgLoop);
            bgLoop.connect(audioCtx.destination);
            osc1.start(); osc2.start();
        } catch(e) {}
    }

    function stopSynthAmbientMusic() {
        if (bgLoop) { try { audioCtx.close(); audioCtx = null; } catch(e){} }
    }

    function playSoundFX(type) {
        initAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);

        if (type === "sniper") {
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(900, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(150, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15);
        } 
        else if (type === "shout") {
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(260, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(420, audioCtx.currentTime + 0.1);
            osc.frequency.linearRampToValueAtTime(200, audioCtx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.3);
        }
        else if (type === "hit") {
            osc.type = "triangle";
            osc.frequency.setValueAtTime(180, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.2);
        }
    }

    // FIXED: Streamlit Frame Independent Touch Positioning Formulas
    function updatePosition(e) {
        if (gameOver) return;
        let pointer = e.touches ? e.touches[0] : e;
        let boardRect = board.getBoundingClientRect();
        
        // Maps absolute finger touch values relative to container boundaries
        aimX = Math.max(-10, Math.min(288, pointer.clientX - boardRect.left - 22));
        aimY = Math.max(-10, Math.min(316, pointer.clientY - boardRect.top - 22));
        
        crosshair.style.left = aimX + "px";
        crosshair.style.top = aimY + "px";
        
        // Makes the rifle match your aim crosshair subtly for extreme realism
        gun.style.transform = `rotate(${-15 + (aimX - 138)/30}deg) translateX(${(aimX - 138)/20}px)`;
    }

    function onStart(e) {
        if (gameOver) return;
        initAudio();
        isMovingCrosshair = true;
        touchMovedFlag = false;
        updatePosition(e);
    }

    function onMove(e) {
        if (!isMovingCrosshair || gameOver) return;
        if(e.touches) e.preventDefault(); // Disables vertical browser container pull bouncing
        touchMovedFlag = true;
        updatePosition(e);
    }

    function onEnd(e) {
        if (!isMovingCrosshair || gameOver) return;
        isMovingCrosshair = false;
        if (!touchMovedFlag) {
            fireSniperRifle();
        }
    }

    board.addEventListener("touchstart", onStart, {passive: false});
    window.addEventListener("touchmove", onMove, {passive: false});
    window.addEventListener("touchend", onEnd);
    board.addEventListener("mousedown", onStart);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onEnd);

    function fireSniperRifle() {
        if (gameOver) return;
        playSoundFX("sniper");
        
        crosshair.style.borderColor = "red";
        setTimeout(() => { if(!gameOver) crosshair.style.borderColor = "#00ff66"; }, 70);

        activeEnemies.forEach((e) => {
            let eX = parseFloat(e.style.left) || 0;
            let eY = parseFloat(e.style.top) || 0;
            let eW = parseFloat(e.style.width) || 0;
            let eH = parseFloat(e.style.height) || 0;
            
            let centerTargetX = eX + (eW / 2);
            let centerTargetY = eY + (eH / 2);
            let centerScopeX = aimX + 22;
            let centerScopeY = aimY + 22;

            if (Math.abs(centerScopeX - centerTargetX) < (eW / 2 + 15) && Math.abs(centerScopeY - centerTargetY) < (eH / 2 + 15) && eW > 8) {
                playSoundFX("hit");
                score += 10;
                scoreTxt.innerText = "Score: " + score;
                if(e.intervalId) clearInterval(e.intervalId);
                e.remove();
                activeEnemies = activeEnemies.filter(item => item !== e);
            }
        });
    }

    function restartGame() {
        stopSynthAmbientMusic();
        if(spawnInt) clearInterval(spawnInt);
        activeEnemies.forEach(e => { if(e.intervalId) clearInterval(e.intervalId); e.remove(); });
        
        activeEnemies = []; score = 0; aimX = 138; aimY = 153; isMovingCrosshair = false; gameOver = false;
        
        board.innerHTML = '<div id="scoreTxt">Score: 0</div><div id="crosshair" style="left: 138px; top: 153px;"></div><div id="gun"></div>';
        setTimeout(() => {
            globalThis.scoreTxt = document.getElementById("scoreTxt");
            globalThis.crosshair = document.getElementById("crosshair");
            globalThis.gun = document.getElementById("gun");
            initAudio();
            startSpawner();
        }, 60);
    }

     function startSpawner() {
        spawnInt = setInterval(() => {
            if (gameOver) { clearInterval(spawnInt); return; }
            
            // Build the humanoid target assembly using code shape nodes
            let h = document.createElement("div");
            h.className = "humanoid";
            h.innerHTML = '<div class="head"></div><div class="torso"><div class="limb-l"></div><div class="limb-r"></div></div><div class="legs"><div class="leg"></div><div class="leg"></div></div>';
            
            let finalTrajectoryX = Math.random() * 240 + 30;
            let currentWidth = 6; let currentHeight = 12;
            
            // Set starting location at the desert horizon ridge line
            h.style.cssText = `position:absolute; top:190px; left:160px; width:${currentWidth}px; height:${currentHeight}px;`;
            board.appendChild(h); activeEnemies.push(h);
            
            playSoundFX("shout");

            let steps = 0;
            let hInt = setInterval(() => {
                if (gameOver) { clearInterval(hInt); return; }
                steps += 1;
                
                // Continuous 3D scaling loops
                currentWidth += 0.45; currentHeight += 0.9;
                
                let speedX = (finalTrajectoryX - 160) / 95;
                let positionX = 160 + (speedX * steps) - (currentWidth / 2);
                let positionY = 190 + (1.1 * steps) - (currentHeight / 2);
                
                h.style.width = currentWidth + "px";
                h.style.height = currentHeight + "px";
                h.style.left = positionX + "px";
                h.style.top = positionY + "px";
                h.intervalId = hInt;
                
                if (currentHeight > 85) {
                    triggerGameOver();
                    clearInterval(hInt);
                }
            }, 30);
        }, 1300);
    }

    function triggerGameOver() {
        gameOver = true; isMovingCrosshair = false;
        stopSynthAmbientMusic();
        board.innerHTML = `
            <div style='color:#7a1f1d; font-size:28px; font-weight:bold; text-align:center; position:relative; z-index:40; text-shadow: 2px 2px #000; padding-top:40px;'>
                MISSION FAILURE<br>
                <span style='color:white; font-size:18px; font-weight:normal;'>Score achieved: ${score}</span><br>
                <button class='retry-btn' onclick='restartGame()'>DEPLOY AGAIN 🔄</button>
            </div>`;
    }

    globalThis.scoreTxt = scoreTxt; 
    globalThis.crosshair = crosshair; 
    globalThis.gun = gun;
    startSpawner();
</script>
</body>
</html>
"""

components.html(game_html, height=450)

                
