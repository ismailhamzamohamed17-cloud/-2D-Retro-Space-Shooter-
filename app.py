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
    
    /* 1. Real Image Desert Horizon Viewport */
    #board { 
        position: relative; 
        width: 320px; 
        height: 350px; 
        background: url('https://unsplash.com') center bottom/cover no-repeat; 
        border: 3px solid #444; 
        overflow: hidden; 
        margin: auto; 
        border-radius: 12px; 
        touch-action: none;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    
    /* 2. Realistic Sniper Rifle stock image overlay on the right side */
    #gun {
        position: absolute;
        bottom: -20px;
        right: -10px;
        width: 160px;
        height: 180px;
        background: url('https://unsplash.com') center center/contain no-repeat;
        transform: rotate(-15deg);
        pointer-events: none;
        z-index: 25;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.7)) brightness(0.4);
    }

    /* Green Tactical Crosshair Scope Circle */
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
    .retry-btn { margin-top: 100px; padding: 12px 25px; background: #e76f51; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; }
    
    /* 3. Realistic Moving Soldier Sprite Target */
    .humanoid { 
        position: absolute; 
        z-index: 5; 
        pointer-events: none; 
        background: url('https://unsplash.com') center center/cover no-repeat;
        border-radius: 4px;
        filter: brightness(0.6) drop-shadow(0 4px 6px rgba(0,0,0,0.5));
    }
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
            
            let h = document.createElement("div");
            h.className = "humanoid";
            
            let finalTrajectoryX = Math.random() * 240 + 30;
            let currentWidth = 4; let currentHeight = 8;
            
            // Horizon lineup elevation starting points
            h.style.cssText = `position:absolute; top:190px; left:160px; width:${currentWidth}px; height:${currentHeight}px;`;
            board.appendChild(h); activeEnemies.push(h);
            
            playSoundFX("shout");

            let steps = 0;
            let hInt = setInterval(() => {
                if (gameOver) { clearInterval(hInt); return; }
                steps += 1;
                
                // Realistic 3D perspective sizing adjustments
                currentWidth += 0.5; currentHeight += 1.0;
                
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

                
