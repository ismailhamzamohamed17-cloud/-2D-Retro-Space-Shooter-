import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Desert Outpost FPS", layout="centered")
st.title("🏜️ Outpost Sniper Defense")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        /* 1. Maximized Screen Sizing Container Optimized for iPhone 17 Pro Max */
        #board { 
            position: relative; 
            width: 380px; 
            height: 480px; 
            background: linear-gradient(to bottom, #ff9e7d 0%, #feb47b 40%, #e07a5f 70%, #d88060 100%); 
            border: 3px solid #555; 
            overflow: hidden; 
            margin: auto; 
            border-radius: 16px; 
            touch-action: none;
            box-shadow: 0 12px 32px rgba(0,0,0,0.6);
        }
        
        /* Deep background canyons and ground trenches */
        #board::before {
            content: ''; position: absolute; bottom: 0; left: -40px; width: 260px; height: 160px; background: #c2593f; clip-path: polygon(0% 100%, 60% 30%, 100% 100%); opacity: 0.8; z-index: 1; border-top: 2px solid #e07a5f;
        }
        #board::after {
            content: ''; position: absolute; bottom: 0; right: -40px; width: 280px; height: 130px; background: #a64630; clip-path: polygon(0% 100%, 35% 15%, 100% 100%); opacity: 0.9; z-index: 2; border-top: 2px solid #c2593f;
        }
        
        /* Underground Trench Lip Mask Overlay */
        .trench-floor {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 110px; background: #8c3523; z-index: 3; border-top: 4px solid #5e2114;
        }
        
        /* 2. Massive, Detailed Prominent 3D-Style Sniper Rifle Stock */
        #gun {
            position: absolute;
            bottom: -35px;
            right: 25px;
            width: 60px;
            height: 220px;
            transform: rotate(28deg);
            transform-origin: bottom right;
            pointer-events: none;
            z-index: 25;
            will-change: transform;
        }
        .gun-barrel {
            position: absolute; top: -65px; left: 24px; width: 12px; height: 110px; 
            background: linear-gradient(to right, #1a1a1a, #555, #2d2d2d); border-radius: 3px;
        }
        .gun-muzzle {
            position: absolute; top: -80px; left: 21px; width: 18px; height: 16px; 
            background: #0a0a0a; border-radius: 2px;
        }
        .gun-receiver {
            position: absolute; top: 40px; left: 10px; width: 38px; height: 100px; 
            background: linear-gradient(to right, #222, #3d3d3d, #1a1a1a); border-radius: 6px;
            box-shadow: -8px 8px 16px rgba(0,0,0,0.7);
        }
        .gun-scope-tube {
            position: absolute; top: 15px; left: -4px; width: 16px; height: 65px; 
            background: linear-gradient(to right, #111, #444, #222); border-radius: 3px;
        }
        .gun-stock {
            position: absolute; top: 140px; left: 16px; width: 32px; height: 80px; 
            background: linear-gradient(to right, #151515, #2a2a2a); border-radius: 4px;
        }

        /* Green Tactical Sniper Crosshair Scope Circle */
        #crosshair { 
            position: absolute; 
            top: 218px; 
            left: 168px; 
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
        
        #scoreTxt { position: absolute; top: 12px; left: 12px; color: #00ff66; font-weight: bold; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.75); padding: 4px 10px; border: 1px solid #444; border-radius: 6px; }
        .retry-btn { margin-top: 30px; padding: 12px 28px; background: #e76f51; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 12px rgba(231,111,81,0.4); }
        
        /* 3. Code-Generated Realistic Human Sapper Enemies */
        .humanoid { 
            position: absolute; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; will-change: left, top, width, height;
        }
        /* Caucasian / Desert camouflage skin-tone mapping elements */
        .human-head { background: #e0a96d; border-radius: 50%; width: 100%; height: 25%; box-shadow: inset -1px -1px 2px rgba(0,0,0,0.2); }
        /* Combat fatigue torso clothing layer */
        .human-torso { background: #4f5d2f; width: 65%; height: 50%; border-radius: 3px; margin-top: 3%; position: relative; }
        /* Moving human arms arms */
        .human-arm-l { position: absolute; left: -35%; top: 10%; width: 35%; height: 90%; background: #4f5d2f; transform: rotate(20deg); transform-origin: top right; border-radius: 2px; }
        .human-arm-r { position: absolute; right: -35%; top: 10%; width: 35%; height: 90%; background: #4f5d2f; transform: rotate(-20deg); transform-origin: top left; border-radius: 2px; }
        /* Combat trousers & boots legs structure */
        .human-legs { display: flex; justify-content: space-around; width: 65%; height: 22%; margin-top: auto; }
        .human-leg { background: #35401b; width: 40%; height: 100%; border-radius: 1px; }
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
        <div class="trench-floor"></div> <!-- Structural ground line barrier -->
    </div>

    <p style="text-align: center; color: #8b949e; font-size: 13px; margin-top: 15px; font-family: sans-serif; line-height: 1.4; padding: 0 10px;">
        🎮 <b>Drag anywhere inside the box</b> to sweep your close-up sniper rifle scope.<br>
        🎯 <b>Tap cleanly once without dragging</b> to eliminate targets running from trenches!
    </p>

<script>
    let aimX = 168; let aimY = 218; let score = 0; let gameOver = false;
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
            osc1.type = "sine"; osc1.frequency.setValueAtTime(60.00, audioCtx.currentTime);
            osc2.type = "sine"; osc2.frequency.setValueAtTime(90.00, audioCtx.currentTime);
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
            osc.frequency.setValueAtTime(700, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.2);
        } 
        else if (type === "shout") { // Aggressive soldier shout warning indicator frequencies
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(220, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(340, audioCtx.currentTime + 0.08);
            osc.frequency.linearRampToValueAtTime(180, audioCtx.currentTime + 0.25);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.25);
        }
        else if (type === "hit") {
            osc.type = "triangle";
            osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15);
        }
    }

    function updatePosition(e) {
        if (gameOver) return;
        let pointer = e.touches ? e.touches[0] : e;
        let boardRect = board.getBoundingClientRect();
        
        aimX = Math.max(-10, Math.min(345, pointer.clientX - boardRect.left - 22));
        aimY = Math.max(-10, Math.min(445, pointer.clientY - boardRect.top - 22));
        
        if(crosshair) {
            crosshair.style.left = aimX + "px";
            crosshair.style.top = aimY + "px";
        }
                // Massive immersive recoil sweep linking rifle rotation to aiming vector parameters
        if (gun) {
            gun.style.transform = `rotate(${28 + (aimX - 168) / 20}deg) translateX(${(aimX - 168) / 12}px) translateY(${(aimY - 218) / 18}px)`;
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

            if (Math.abs(centerScopeX - centerTargetX) < (eW / 2 + 16) && Math.abs(centerScopeY - centerTargetY) < (eH / 2 + 16) && eW > 6) {
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
        aimX = 168; 
        aimY = 218; 
        isMovingCrosshair = false; 
        gameOver = false;

        // Re-inject pristine clean layout structural frames
        board.innerHTML = `
            <div id="scoreTxt">Score: 0</div> 
            <div id="crosshair" style="left: 168px; top: 218px;"></div> 
            <div id="gun"> 
                <div class="gun-muzzle"></div> 
                <div class="gun-barrel"></div> 
                <div class="gun-scope-tube"></div> 
                <div class="gun-receiver"></div> 
                <div class="gun-stock"></div> 
            </div> 
            <div class="trench-floor"></div>`;
            
        setTimeout(() => {
            registerDeviceListeners();
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
            h.innerHTML = '<div class="human-head"></div><div class="human-torso"><div class="human-arm-l"></div><div class="human-arm-r"></div></div><div class="human-legs"><div class="human-leg"></div><div class="human-leg"></div></div>';
            
            let finalTrajectoryX = Math.random() * 280 + 40;
            let currentWidth = 8; 
            let currentHeight = 16;
            
            // FIXED: Enemies spawn underground inside trench horizons (top:370px instead of sky top:190px)
            h.style.cssText = `position:absolute; top:370px; left:190px; width:${currentWidth}px; height:${currentHeight}px;`;
            
            // Append target nodes underneath trench lip barrier to make them rise up realistically
            board.insertBefore(h, document.querySelector(".trench-floor"));
            activeEnemies.push(h);
            
            playSoundFX("shout");
            
            let steps = 0;
            let hInt = setInterval(() => {
                if (gameOver) { 
                    clearInterval(hInt); 
                    return; 
                }
                
                steps += 1;
                // Continuous 3D perspective scaling vectors running upwards/outwards towards screen
                currentWidth += 0.55; 
                currentHeight += 1.1;
                
                let speedX = (finalTrajectoryX - 190) / 85;
                let positionX = 190 + (speedX * steps) - (currentWidth / 2);
                // Moves upwards and out from underground trench parameters dynamically
                let positionY = 370 - (2.2 * steps) - (currentHeight / 2);
                
                h.style.width = currentWidth + "px";
                h.style.height = currentHeight + "px";
                h.style.left = positionX + "px";
                h.style.top = positionY + "px";
                h.intervalId = hInt;
                
                // If a human sapper breaks your defensive threshold perimeter context line, fail mission
                if (positionY < 120) {
                    triggerGameOver();
                    clearInterval(hInt);
                }
            }, 30);
        }, 1400);
    }

    function triggerGameOver() {
        gameOver = true; 
        isMovingCrosshair = false;
        stopSynthAmbientMusic();
        board.innerHTML = `
            <div style='color:#b7094c; font-size:26px; font-weight:bold; text-align:center; position:relative; z-index:40; text-shadow: 2px 2px #000; padding-top:140px;'> 
                OUTPOST OVERRUN<br> 
                <span style='color:white; font-size:16px; font-weight:normal;'>Enemies Neutralized: ${score / 10}</span><br> 
                <button class='retry-btn' onclick='restartGame()'>DEPLOY AGAIN 🔄</button> 
            </div>`;
    }

    registerDeviceListeners();
    startSpawner();
</script>
</body>
</html>
"""

components.html(game_html, height=560)

        
