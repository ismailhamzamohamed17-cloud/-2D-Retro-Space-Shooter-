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
    <style>
    body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
    
    /* 3D Horizon Space Desert Viewport */
    #board { 
        position: relative; 
        width: 320px; 
        height: 350px; 
        background: linear-gradient(to bottom, #11001c 0%, #240046 30%, #3c096c 60%, #7b2cbf 100%); 
        border: 3px solid #555; 
        overflow: hidden; 
        margin: auto; 
        border-radius: 12px; 
        touch-action: none;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    }
    
    /* Neon glowing alien sand structures */
    #board::before {
        content: ''; position: absolute; bottom: 0; left: -40px; width: 220px; height: 110px; background: #3c096c; clip-path: polygon(0% 100%, 60% 15%, 100% 100%); opacity: 0.8; z-index: 1; border-top: 1px solid #9d4edd;
    }
    #board::after {
        content: ''; position: absolute; bottom: 0; right: -40px; width: 240px; height: 95px; background: #240046; clip-path: polygon(0% 100%, 35% 5%, 100% 100%); opacity: 0.9; z-index: 2; border-top: 1px solid #7b2cbf;
    }
    
    /* Highly Detailed 3D-Look Tactical Sniper Rifle Model Assembly */
    #gun {
        position: absolute;
        bottom: -20px;
        right: 15px;
        width: 45px;
        height: 160px;
        transform: rotate(40deg);
        transform-origin: bottom right;
        pointer-events: none;
        z-index: 25;
        will-change: transform;
    }
    /* Long Sniper Metal Barrel extension */
    .gun-barrel {
        position: absolute; top: -45px; left: 18px; width: 8px; height: 75px; 
        background: linear-gradient(to right, #111, #444, #222); border-radius: 2px;
    }
    /* Heavy Muzzle Brake Tip */
    .gun-muzzle {
        position: absolute; top: -55px; left: 16px; width: 12px; height: 12px; 
        background: #0d0d0d; border-radius: 1px;
    }
    /* Rifle Receiver & Dynamic Scope Mount Body */
    .gun-receiver {
        position: absolute; top: 30px; left: 10px; width: 24px; height: 70px; 
        background: linear-gradient(to right, #1a1a1a, #2b2b2b, #111); border-radius: 4px;
        box-shadow: -5px 5px 12px rgba(0,0,0,0.6);
    }
    /* Sniper Scope Tube attached to rifle upper receiver */
    .gun-scope-tube {
        position: absolute; top: 15px; left: -2px; width: 10px; height: 45px; 
        background: linear-gradient(to right, #0a0a0a, #333, #1a1a1a); border-radius: 2px;
    }
    /* Heavy Sniper Stock handle */
    .gun-stock {
        position: absolute; top: 100px; left: 14px; width: 20px; height: 60px; 
        background: linear-gradient(to right, #111, #222); border-radius: 3px;
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
    
    #scoreTxt { position: absolute; top: 10px; left: 10px; color: #00ff66; font-weight: bold; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.7); padding: 3px 8px; border: 1px solid #333; border-radius: 4px; }
    .retry-btn { margin-top: 25px; padding: 12px 25px; background: #9d4edd; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; box-shadow: 0 0 10px #9d4edd; }
    
    /* 3D Radiant Neon-Green Extraterrestrial Alien Invader Target Model */
    .humanoid { 
        position: absolute; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; will-change: left, top, width, height;
    }
    /* Glowing extended macro alien skull head */
    .alien-head { background: #39ff14; border-radius: 50% 50% 40% 40%; width: 100%; height: 35%; box-shadow: 0 0 8px #39ff14; position: relative; }
    /* Giant black insectoid glowing eyes */
    .alien-head::before { content: ''; position: absolute; top: 40%; left: 15%; width: 25%; height: 25%; background: #000; border-radius: 50% 50% 30% 30%; transform: rotate(-10deg); }
    .alien-head::after { content: ''; position: absolute; top: 40%; right: 15%; width: 25%; height: 25%; background: #000; border-radius: 50% 50% 30% 30%; transform: rotate(10deg); }
    /* Slender fluid torso section */
    .alien-torso { background: #39ff14; width: 45%; height: 40%; border-radius: 2px; margin-top: 4%; position: relative; box-shadow: 0 0 6px #39ff14; }
    /* Long trailing space alien arms */
    .alien-arm-l { position: absolute; left: -50%; top: 10%; width: 50%; height: 110%; background: #39ff14; transform: rotate(35deg); transform-origin: top right; border-radius: 2px; }
    .alien-arm-r { position: absolute; right: -50%; top: 10%; width: 50%; height: 110%; background: #39ff14; transform: rotate(-35deg); transform-origin: top left; border-radius: 2px; }
    /* Shifting lower tentacles / legs structure */
    .alien-legs { display: flex; justify-content: space-between; width: 70%; height: 20%; margin-top: auto; }
    .alien-leg { background: #39ff14; width: 25%; height: 100%; border-radius: 1px; box-shadow: 0 0 4px #39ff14; }
</style>
</head>
<body>

    <div id="board">
        <div id="scoreTxt">Score: 0</div>
        <div id="crosshair"></div>
        <div id="gun">
            <div class="gun-muzzle"></div>
            <div class="gun-barrel"></div>
            <div class="gun-scope-tube"></div>
            <div class="gun-receiver"></div>
            <div class="gun-stock"></div>
        </div>
    </div>

    <p style="text-align: center; color: #8b949e; font-size: 13px; margin-top: 12px; font-family: sans-serif; line-height: 1.4;">
        🎮 <b>Drag anywhere inside the box</b> to sweep your weapon scope sight.<br>
        🛸 <b>Tap cleanly once without dragging</b> to eliminate oncoming alien invaders!
    </p>

<script>
    let aimX = 138; let aimY = 153; let score = 0; let gameOver = false;
    let isMovingCrosshair = false;
    let touchMovedFlag = false;
    
    let board = document.getElementById("board");
    let crosshair = document.getElementById("crosshair");
    let scoreTxt = document.getElementById("scoreTxt");
    let gun = document.getElementById("gun");
    
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
            osc1.type = "sine"; osc1.frequency.setValueAtTime(45.00, audioCtx.currentTime);
            osc2.type = "sawtooth"; osc2.frequency.setValueAtTime(65.41, audioCtx.currentTime);
            bgLoop.gain.setValueAtTime(0.03, audioCtx.currentTime);
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
            osc.frequency.setValueAtTime(850, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.18);
            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.18);
        } 
        else if (type === "shout") { // Extraterrestrial frequency shriek screech
            osc.type = "sine";
            osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + 0.15);
            osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.3);
        }
        else if (type === "hit") {
            osc.type = "triangle";
            osc.frequency.setValueAtTime(220, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.22);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.22);
        }
    }

    function updatePosition(e) {
        if (gameOver) return;
        let pointer = e.touches ? e.touches[0] : e;
        let boardRect = board.getBoundingClientRect();
        
        aimX = Math.max(-10, Math.min(288, pointer.clientX - boardRect.left - 22));
        aimY = Math.max(-10, Math.min(316, pointer.clientY - boardRect.top - 22));
        
        if(crosshair) {
            crosshair.style.left = aimX + "px";
            crosshair.style.top = aimY + "px";
        }
        
        // Dynamic sniper rifle barrel pivot calculation matrix matching scope movements
        if(gun) {
            gun.style.transform = `rotate(${40 + (aimX - 138)/25}deg) translateX(${(aimX - 138)/18}px) translateY(${(aimY - 153)/25}px)`;
        }
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
        if (e.touches) e.preventDefault();
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

    // Explicit structural event connection pipeline function
    function registerDeviceListeners() {
        board = document.getElementById("board");
        crosshair = document.getElementById("crosshair");
        scoreTxt = document.getElementById("scoreTxt");
        gun = document.getElementById("gun");
        
        board.addEventListener("touchstart", onStart, { passive: false });
        board.addEventListener("mousedown", onStart);
    }

    window.addEventListener("touchmove", onMove, { passive: false });
    window.addEventListener("touchend", onEnd);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onEnd);

    function fireSniperRifle() {
        if (gameOver) return;
        playSoundFX("sniper");
        
        if (crosshair) crosshair.style.borderColor = "#ff0055";
        setTimeout(() => { 
            if (!gameOver && crosshair) crosshair.style.borderColor = "#00ff66"; 
        }, 70);

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
                if (scoreTxt) scoreTxt.innerText = "Score: " + score;
                if (e.intervalId) clearInterval(e.intervalId);
                e.remove();
                activeEnemies = activeEnemies.filter(item => item !== e);
            }
        });
    }

    function restartGame() {
        stopSynthAmbientMusic();
        if (spawnInt) clearInterval(spawnInt);
        
        activeEnemies.forEach(e => { 
            if (e.intervalId) clearInterval(e.intervalId); 
            e.remove(); 
        });
        
        activeEnemies = []; 
        score = 0; 
        aimX = 138; 
        aimY = 153; 
        isMovingCrosshair = false; 
        gameOver = false;

        // FULLY FIXED: Injection re-build resets raw layout properties and forces structural variable re-binding hooks
        board.innerHTML = `
            <div id="scoreTxt">Score: 0</div>
            <div id="crosshair" style="left: 138px; top: 153px;"></div>
            <div id="gun">
                <div class="gun-muzzle"></div>
                <div class="gun-barrel"></div>
                <div class="gun-scope-tube"></div>
                <div class="gun-receiver"></div>
                <div class="gun-stock"></div>
            </div>`;
            
        setTimeout(() => {
            registerDeviceListeners(); // Force-inject event hooks immediately to fix freezing bugs
            initAudio();
            startSpawner();
        }, 60);
    }

    function startSpawner() {
        spawnInt = setInterval(() => {
            if (gameOver) { 
                clearInterval(spawnInt); 
                return; 
            }
            
            let h = document.createElement("div");
            h.className = "humanoid";
            h.innerHTML = '<div class="alien-head"></div><div class="alien-torso"><div class="alien-arm-l"></div><div class="alien-arm-r"></div></div><div class="alien-legs"><div class="alien-leg"></div><div class="alien-leg"></div></div>';
            
            let finalTrajectoryX = Math.random() * 240 + 30;
            let currentWidth = 6; 
            let currentHeight = 12;
            
            h.style.cssText = `position:absolute; top:190px; left:160px; width:${currentWidth}px; height:${currentHeight}px;`;
            board.appendChild(h); 
            activeEnemies.push(h);
            
            playSoundFX("shout");

            let steps = 0;
            let hInt = setInterval(() => {
                if (gameOver) { 
                    clearInterval(hInt); 
                    return; 
                }
                
                steps += 1;
                currentWidth += 0.45; 
                currentHeight += 0.9;
                
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
        gameOver = true; 
        isMovingCrosshair = false;
        stopSynthAmbientMusic();
        board.innerHTML = `
            <div style='color:#dc2f02; font-size:26px; font-weight:bold; text-align:center; position:relative; z-index:40; text-shadow: 2px 2px #000; padding-top:55px;'>
                OUTPOST OVERRUN<br>
                <span style='color:white; font-size:16px; font-weight:normal;'>Aliens Eliminated: ${score/10}</span><br>
                <button class='retry-btn' onclick='restartGame()'>DEPLOY AGAIN 🔄</button>
            </div>`;
    }

    // Run primary initializer routine
    registerDeviceListeners();
    startSpawner();
</script>
</body>
</html>
"""

components.html(game_html, height=450)

                
