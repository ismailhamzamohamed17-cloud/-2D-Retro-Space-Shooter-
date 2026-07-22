import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Arcade FPS", layout="centered")
st.title("🚓 Virtua Arcade Shooter")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        /* 1. Maximized Screen Sizing Container Optimized for Arcade Layout */
        #board { 
            position: relative; 
            width: 380px; 
            height: 480px; 
            background: linear-gradient(to bottom, #7ca1d9 0%, #a1c4fd 40%, #8397a6 41%, #4e5d6c 100%); 
            border: 3px solid #555; 
            overflow: hidden; 
            margin: auto; 
            border-radius: 16px; 
            touch-action: none;
            box-shadow: 0 12px 32px rgba(0,0,0,0.6);
        }
        
        /* City Grid Architecture Layout (Retro Skyscrapers & Road Perspective) */
        .skyline-left {
            position: absolute; top: 80px; left: 0; width: 140px; height: 120px;
            background: repeating-linear-gradient(to bottom, #2b3a4a 0px, #2b3a4a 12px, transparent 12px, transparent 18px), #1e2936;
            border-right: 4px solid #151d26; z-index: 1;
        }
        .skyline-right {
            position: absolute; top: 60px; right: 0; width: 120px; height: 140px;
            background: repeating-linear-gradient(to right, #243b34 0px, #243b34 8px, #1a2924 8px, #1a2924 16px);
            border-left: 4px solid #111; z-index: 1;
        }
        .road-surface {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 280px;
            background: #555e6b; clip-path: polygon(40% 0%, 60% 0%, 100% 100%, 0% 100%); z-index: 2;
        }
        /* Road lane dash indicators */
        .road-surface::before {
            content: ''; position: absolute; top: 0; left: 50%; width: 6px; height: 100%;
            background: repeating-linear-gradient(to bottom, #fff 0px, #fff 20px, transparent 20px, transparent 40px);
            transform: translateX(-30%) skewX(-10deg); opacity: 0.6;
        }

        /* 2. Getaway Enemy Vehicle in the Center Lane */
        #getawayCar {
            position: absolute; top: 190px; left: 110px; width: 160px; height: 90px;
            background: linear-gradient(to bottom, #222, #111); border-radius: 8px 8px 4px 4px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5); z-index: 4; will-change: transform;
        }
        /* Windshield / Windows zone */
        .car-window {
            position: absolute; top: 10px; left: 10px; width: 140px; height: 30px;
            background: rgba(135, 206, 235, 0.4); border-radius: 4px; border: 2px solid #000;
        }
        /* Red brake taillights */
        .car-light-l { position: absolute; bottom: 15px; left: 10px; width: 25px; height: 10px; background: red; border-radius: 2px; }
        .car-light-r { position: absolute; bottom: 15px; right: 10px; width: 25px; height: 10px; background: red; border-radius: 2px; }

        /* 3. Gun Positioned at the Bottom-Left Corner pointing up and right */
        #gun {
            position: absolute;
            bottom: -30px;
            left: 30px;
            width: 80px;
            height: 180px;
            transform: rotate(-15deg);
            transform-origin: bottom left;
            pointer-events: none;
            z-index: 25;
            will-change: transform;
        }
        .gun-slide {
            position: absolute; top: 10px; left: -10px; width: 110px; height: 26px; 
            background: linear-gradient(to bottom, #333, #1f1f1f, #2b2b2b); border-radius: 2px 4px 2px 2px; border-bottom: 2px solid #111;
        }
        .gun-hammer {
            position: absolute; top: 6px; left: -14px; width: 10px; height: 14px; background: #111; border-radius: 50% 50% 0 0; transform: rotate(-35deg);
        }
        .gun-grip {
            position: absolute; top: 34px; left: 10px; width: 34px; height: 110px; 
            background: repeating-linear-gradient(45deg, #4a3319, #4a3319 2px, #332211 2px, #332211 4px);
            border: 3px solid #1a1a1a; border-radius: 6px 4px 6px 12px; transform: rotate(10deg);
        }
        .gun-frame {
            position: absolute; top: 32px; left: 10px; width: 50px; height: 25px; background: #1f1f1f;
        }
        .gun-trigger-guard {
            position: absolute; top: 30px; left: 35px; width: 22px; height: 22px; border: 3px solid #1f1f1f; border-radius: 50%;
        }

        /* Tactical Crosshair Scope Circle */
        #crosshair { 
            position: absolute; top: 218px; left: 168px; width: 30px; height: 30px; 
            border: 2px solid #388bfd; border-radius: 50%; will-change: left, top; z-index: 15; pointer-events: none;
        }
        #crosshair::before { content: ''; position: absolute; top: 14px; left: 0; width: 30px; height: 1px; background: #388bfd; }
        #crosshair::after { content: ''; position: absolute; top: 0; left: 14px; width: 1px; height: 30px; background: #388bfd; }
        
        /* 4. Virtua Cop Retro Yellow Locking Target Ring */
        .lockon-ring {
            position: absolute; border: 3px dashed #ffea00; border-radius: 50%;
            pointer-events: none; z-index: 10; animation: shrinkLock 1.5s linear infinite;
            will-change: width, height, left, top;
        }
        @keyframes shrinkLock {
            0% { width: 90px; height: 90px; transform: translate(-30px, -30px); opacity: 1; }
            100% { width: 35px; height: 35px; transform: translate(-2px, -2px); opacity: 0.8; }
        }

        /* 5. Arcade Criminal / Threat Target leaning out of car */
        .humanoid { 
            position: absolute; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; will-change: left, top;
        }
        .human-head { background: #e0a96d; border-radius: 50%; width: 24px; height: 24px; border: 1px solid #000; }
        .human-torso { background: #d90429; width: 32px; height: 40px; border-radius: 4px; margin-top: 2px; position: relative; border: 1px solid #000; }
        /* Arms pointing weapon toward player */
        .human-arm { position: absolute; left: -15px; top: 5px; width: 25px; height: 10px; background: #d90429; border: 1px solid #000; transform: rotate(-10deg); }
        .human-weapon { position: absolute; left: -24px; top: 0px; width: 12px; height: 10px; background: #222; }

        #scoreTxt { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: monospace; font-size: 20px; z-index: 30; background: rgba(0,0,0,0.8); padding: 4px 12px; border-radius: 4px; border: 2px solid #555; }
        .retry-btn { margin-top: 30px; padding: 12px 28px; background: #d90429; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 12px rgba(217,4,41,0.5); }
    </style>
</head>
<body>

    <div id="board">
        <div id="scoreTxt">00200</div>
        <div class="skyline-left"></div>
        <div class="skyline-right"></div>
        <div class="road-surface"></div>
        
        <!-- Getaway Car Setup -->
        <div id="getawayCar">
            <div class="car-window"></div>
            <div class="car-light-l"></div>
            <div class="car-light-r"></div>
        </div>

        <div id="crosshair"></div>
        <div id="gun">
            <div class="gun-hammer"></div>
            <div class="gun-slide"></div>
            <div class="gun-frame"></div>
            <div class="gun-trigger-guard"></div>
            <div class="gun-grip"></div>
        </div>
    </div>

    <p style="text-align: center; color: #8b949e; font-size: 13px; margin-top: 15px; font-family: sans-serif; line-height: 1.4;">
        🕹️ <b>Drag anywhere inside the box</b> to guide your weapon sight scope.<br>
        💥 <b>Tap cleanly once without dragging</b> to shoot targets before the ring locks!
    </p>

<script>
    let aimX = 168; let aimY = 218; let score = 200; let gameOver = false;
    let isMovingCrosshair = false;
    let touchMovedFlag = false;
    
    let board = document.getElementById("board");
    let crosshair = document.getElementById("crosshair");
    let scoreTxt = document.getElementById("scoreTxt");
    let gun = document.getElementById("gun");
    let car = document.getElementById("getawayCar");
    
    let activeEnemies = [];
    let audioCtx = null; let spawnInt = null; let carXOffset = 0; let carDirection = 1;

    function initAudio() {
        if (audioCtx) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function playSoundFX(type) {
        initAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);

        if (type === "shoot") { // Arcade gun snap explosion discharge
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(60, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15);
        } 
        else if (type === "hit") { // Retro point score indicator echo sound wave
            osc.type = "sine";
            osc.frequency.setValueAtTime(880, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }
        else if (type === "damage") { // Heavy synth hit alert crash
            osc.type = "sawtooth";
                        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            osc.start(); 
            osc.stop(audioCtx.currentTime + 0.3);
        }
    }

    function updatePosition(e) {
        if (gameOver) return;
        let pointer = e.touches ? e.touches[0] : e;
        let boardRect = board.getBoundingClientRect();
        
        aimX = Math.max(-10, Math.min(345, pointer.clientX - boardRect.left - 15));
        aimY = Math.max(-10, Math.min(445, pointer.clientY - boardRect.top - 15));
        
        if (crosshair) {
            crosshair.style.left = aimX + "px";
            crosshair.style.top = aimY + "px";
        }
        
        // Pivot weapon barrel on the bottom left corner to point directly at your crosshair
        if (gun) {
            let dx = aimX - 50;
            let dy = 450 - aimY;
            let angle = Math.atan2(dy, dx) * (180 / Math.PI);
            gun.style.transform = `rotate(${-90 + angle}deg)`;
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
            fireArcadePistol();
        }
    }

    function registerDeviceListeners() {
        board = document.getElementById("board");
        crosshair = document.getElementById("crosshair");
        scoreTxt = document.getElementById("scoreTxt");
        gun = document.getElementById("gun");
        car = document.getElementById("getawayCar");
        
        board.addEventListener("touchstart", onStart, { passive: false });
        board.addEventListener("mousedown", onStart);
    }

    window.addEventListener("touchmove", onMove, { passive: false });
    window.addEventListener("touchend", onEnd);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onEnd);

    function fireArcadePistol() {
        if (gameOver) return;
        playSoundFX("shoot");
        
        if (crosshair) crosshair.style.borderColor = "white";
        setTimeout(() => { 
            if (!gameOver && crosshair) crosshair.style.borderColor = "#388bfd"; 
        }, 70);

        activeEnemies.forEach((enemyObj) => {
            let e = enemyObj.element;
            let r = enemyObj.ring;
            let boardRect = board.getBoundingClientRect();
            let eRect = e.getBoundingClientRect();
            
            let eX = eRect.left - boardRect.left;
            let eY = eRect.top - boardRect.top;
            
            let centerScopeX = aimX + 15;
            let centerScopeY = aimY + 15;

            // Box collision parameters to verify accurate arcade hit bounds
            if (centerScopeX >= eX && centerScopeX <= eX + 40 && centerScopeY >= eY && centerScopeY <= eY + 60) {
                playSoundFX("hit");
                score += 100;
                if (scoreTxt) scoreTxt.innerText = String(score).padStart(5, '0');
                if (enemyObj.timeoutId) clearTimeout(enemyObj.timeoutId);
                e.remove();
                r.remove();
                activeEnemies = activeEnemies.filter(item => item !== enemyObj);
            }
        });
    }

    function restartGame() {
        if (spawnInt) clearInterval(spawnInt);
        activeEnemies.forEach(obj => { 
            obj.element.remove(); 
            obj.ring.remove(); 
        });
        
        activeEnemies = []; 
        score = 200; 
        aimX = 168; 
        aimY = 218; 
        isMovingCrosshair = false; 
        gameOver = false;
        
        board.innerHTML = `
            <div id="scoreTxt">00200</div> 
            <div class="skyline-left"></div> 
            <div class="skyline-right"></div> 
            <div class="road-surface"></div> 
            <div id="getawayCar"> 
                <div class="car-window"></div> 
                <div class="car-light-l"></div> 
                <div class="car-light-r"></div> 
            </div> 
            <div id="crosshair" style="left:168px; top:218px;"></div> 
            <div id="gun"> 
                <div class="gun-hammer"></div> 
                <div class="gun-slide"></div> 
                <div class="gun-frame"></div> 
                <div class="gun-trigger-guard"></div> 
                <div class="gun-grip"></div> 
            </div>`;
            
        setTimeout(() => {
            registerDeviceListeners();
            initAudio();
            startSpawner();
        }, 60);
    }

    // Horizontal car drifting vector mechanics engine loop
    setInterval(() => {
        if (gameOver || !car) return;
        carXOffset += carDirection * 1.5;
        if (carXOffset > 70) carDirection = -1;
        if (carXOffset < -70) carDirection = 1;
        car.style.transform = `translateX(${carXOffset}px)`;
    }, 30);

    function startSpawner() {
        spawnInt = setInterval(() => {
            if (gameOver) { 
                clearInterval(spawnInt); 
                return; 
            }
            if (activeEnemies.length >= 2) return; // Cap maximum simultaneous criminal window spawns
            
            let enemy = document.createElement("div");
            enemy.className = "humanoid";
            enemy.innerHTML = '<div class="human-head"></div><div class="human-torso"><div class="human-arm"></div><div class="human-weapon"></div></div>';
            
            // Randomly lean criminal model left or right out of car trunk windows
            let side = Math.random() > 0.5 ? -25 : 145;
            let currentX = 110 + carXOffset + side;
            let currentY = 185;
            
            enemy.style.cssText = `position:absolute; top:${currentY}px; left:${currentX}px; width:40px; height:60px; z-index: 5;`;
            board.appendChild(enemy);
            
            // Build retro yellow locking ring layer around spawned target element
            let ring = document.createElement("div");
            ring.className = "lockon-ring";
            ring.style.cssText = `top:${currentY + 15}px; left:${currentX + 20}px;`;
            board.appendChild(ring);
            
            let enemyObj = { element: enemy, ring: ring, side: side };
            activeEnemies.push(enemyObj);
            
            // Continuously pin criminals and rings securely onto the moving car frame coords
            let trackingInterval = setInterval(() => {
                if (gameOver || !enemy.parentNode) { 
                    clearInterval(trackingInterval); 
                    return; 
                }
                let updatedX = 110 + carXOffset + side;
                enemy.style.left = updatedX + "px";
                ring.style.left = (updatedX + 2) + "px";
            }, 30);
            
            // Timer countdown checking lock state: if loop reaches zero, take structural damage
            enemyObj.timeoutId = setTimeout(() => {
                if (gameOver || !enemy.parentNode) return;
                playSoundFX("damage");
                triggerGameOver();
            }, 1500);
        }, 1800);
    }

    function triggerGameOver() {
        gameOver = true; 
        isMovingCrosshair = false;
        activeEnemies.forEach(obj => { 
            if (obj.timeoutId) clearTimeout(obj.timeoutId); 
        });
        
        board.innerHTML = `
            <div style='color:#ffea00; font-size:28px; font-weight:bold; text-align:center; position:relative; z-index:40; text-shadow: 2px 2px #000; padding-top:140px; font-family:monospace;'> 
                GAME OVER<br> 
                <span style='color:white; font-size:16px; font-weight:normal;'>Arcade Score: ${score}</span><br> 
                <button class='retry-btn' onclick='restartGame()'>CONTINUE 🪙</button> 
            </div>`;
    }

    registerDeviceListeners();
    startSpawner();
</script>
</body>
</html>
"""

components.html(game_html, height=560)
