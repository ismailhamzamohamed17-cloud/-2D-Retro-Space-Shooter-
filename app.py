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
        
        /* Enhanced Screen Sizing Container Optimized for Arcade Layout */
        #board { 
            position: relative; 
            width: 380px; 
            height: 480px; 
            background: linear-gradient(to bottom, #4a777a 0%, #a1c4fd 40%, #727d8c 41%, #3a4454 100%); 
            border: 3px solid #555; 
            overflow: hidden; 
            margin: auto; 
            border-radius: 16px; 
            touch-action: none;
            box-shadow: 0 12px 32px rgba(0,0,0,0.6);
        }
        
        /* 3D City Boulevard Layout (Retro Skyscrapers & Road Perspective) */
        .skyline-left {
            position: absolute; top: 50px; left: 0; width: 130px; height: 150px;
            background: repeating-linear-gradient(to bottom, #1b263b 0px, #1b263b 14px, transparent 14px, transparent 20px), #0d1b2a;
            border-right: 4px solid #0d1b2a; z-index: 1; opacity: 0.95;
        }
        .skyline-right {
            position: absolute; top: 40px; right: 0; width: 110px; height: 160px;
            background: repeating-linear-gradient(to bottom, #14213d 0px, #14213d 10px, transparent 10px, transparent 16px), #000814;
            border-left: 4px solid #000814; z-index: 1; opacity: 0.95;
        }
        .road-surface {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 280px;
            background: linear-gradient(to bottom, #434952, #2c3036); clip-path: polygon(42% 0%, 58% 0%, 100% 100%, 0% 100%); z-index: 2;
        }
        /* Road lane dash indicators */
        .road-surface::before {
            content: ''; position: absolute; top: 0; left: 50%; width: 8px; height: 100%;
            background: repeating-linear-gradient(to bottom, #e5e5e5 0px, #e5e5e5 25px, transparent 25px, transparent 50px);
            transform: translateX(-50%); opacity: 0.4;
        }

        /* --- HIGHLY REALISTIC 3D-SHADED GETAWAY SUV VEHICLE --- */
        #getawayCar {
            position: absolute; top: 195px; left: 110px; width: 160px; height: 95px;
            background: linear-gradient(to bottom, #3a3d40, #181a1b, #0f1012); border-radius: 14px 14px 8px 8px;
            box-shadow: 0 16px 28px rgba(0,0,0,0.7), inset 0 2px 4px rgba(255,255,255,0.2); z-index: 4; will-change: transform;
            border: 1px solid #232526;
        }
        /* Rear Windshield Glass Shading */
        .car-window {
            position: absolute; top: 12px; left: 14px; width: 132px; height: 32px;
            background: linear-gradient(180deg, rgba(142, 202, 230, 0.6) 0%, rgba(33, 158, 188, 0.3) 70%, rgba(2, 48, 71, 0.5) 100%); 
            border-radius: 6px; border: 2px solid #070808;
            box-shadow: inset 0 4px 6px rgba(255,255,255,0.15);
        }
        /* Chrome bumper bar styling */
        #getawayCar::after {
            content: ''; position: absolute; bottom: 8px; left: 10px; width: 140px; height: 6px;
            background: linear-gradient(to bottom, #e5e5e5, #b5b5b5, #666); border-radius: 3px;
        }
        /* Glowing taillight pods */
        .car-light-l { position: absolute; bottom: 18px; left: 12px; width: 24px; height: 14px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; border: 1px solid #800f2f; }
        .car-light-r { position: absolute; bottom: 18px; right: 12px; width: 24px; height: 14px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; border: 1px solid #800f2f; }

        /* REPOSITIONED & OVERHAULED GUN ON THE RIGHT SIDE */
        #gun {
            position: absolute; bottom: -35px; right: 40px; width: 80px; height: 180px;
            transform: rotate(0deg); transform-origin: bottom center; pointer-events: none; z-index: 25; will-change: transform;
        }
        .gun-slide {
            position: absolute; top: 10px; left: -30px; width: 110px; height: 26px; 
            background: linear-gradient(to bottom, #2b2b2b, #151515, #222);
            border-radius: 4px 2px 2px 2px; border-bottom: 2px solid #0d0d0d;
            box-shadow: -4px 4px 10px rgba(0,0,0,0.5);
        }
        .gun-slide::before { content: ''; position: absolute; left: -4px; top: 6px; width: 4px; height: 10px; background: #000; border-radius: 1px; }
        .gun-hammer { position: absolute; top: 6px; right: -36px; width: 10px; height: 14px; background: #0d0d0d; border-radius: 50% 50% 0 0; transform: rotate(35deg); }
        .gun-grip {
            position: absolute; top: 34px; left: 25px; width: 34px; height: 110px; 
            background: repeating-linear-gradient(45deg, #3d2b1f, #3d2b1f 2px, #241911 2px, #241911 4px);
            border: 3px solid #0a0a0a; border-radius: 4px 6px 12px 6px; transform: rotate(-10deg);
            box-shadow: -6px 6px 12px rgba(0,0,0,0.6);
        }
        .gun-frame { position: absolute; top: 32px; left: -15px; width: 50px; height: 25px; background: #1a1a1a; border-radius: 0 0 10px 4px; }
        .gun-trigger-guard { position: absolute; top: 30px; left: -5px; width: 22px; height: 22px; border: 3px solid #1a1a1a; border-radius: 50%; }

        /* Blue Tactical Crosshair Scope Circle */
        #crosshair { 
            position: absolute; top: 218px; left: 168px; width: 30px; height: 30px; 
            border: 2px solid #00f0ff; border-radius: 50%; will-change: left, top; z-index: 15; pointer-events: none;
            box-shadow: 0 0 6px rgba(0,240,255,0.4);
        }
        #crosshair::before { content: ''; position: absolute; top: 14px; left: 0; width: 30px; height: 1px; background: #00f0ff; }
        #crosshair::after { content: ''; position: absolute; top: 0; left: 14px; width: 1px; height: 30px; background: #00f0ff; }
        
        /* Virtua Cop Yellow Locking Target Ring */
        .lockon-ring {
            position: absolute; border: 3px dashed #ffea00; border-radius: 50%;
            pointer-events: none; z-index: 10; animation: shrinkLock 1.3s linear infinite;
            will-change: width, height, left, top;
            box-shadow: 0 0 8px rgba(255,234,0,0.3);
        }
        @keyframes shrinkLock {
            0% { width: 95px; height: 95px; transform: translate(-32px, -32px); opacity: 1; }
            100% { width: 35px; height: 35px; transform: translate(-2px, -2px); opacity: 0.9; }
        }

        /* --- HIGHLY DETAILED REALISTIC ARCADE CRIMINAL HUMANOID TARGETS --- */
        .humanoid { 
            position: absolute; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; will-change: left, top;
        }
        /* Shaded head with 3D profile depth hair layer */
        .human-head { 
            background: linear-gradient(135deg, #e0a96d 0%, #c48b53 100%); border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #111; 
            box-shadow: inset -2px -2px 3px rgba(0,0,0,0.3), 0 4px 6px rgba(0,0,0,0.3); position: relative;
        }
        .human-head::before {
            content: ''; position: absolute; top: -2px; left: 2px; width: 20px; height: 8px; background: #2b1d0c; border-radius: 4px 4px 0 0;
        }
        /* Tactical vest shaded clothing torso body design */
        .human-torso { 
            background: linear-gradient(to right, #1d3557 0%, #457b9d 50%, #1d3557 100%); width: 32px; height: 42px; border-radius: 5px; margin-top: 1px; position: relative; border: 1.5px solid #111; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        }
        /* Shaded arms tracking and aiming a handgun directly at user cockpit views */
        .human-arm { 
            position: absolute; top: 6px; width: 28px; height: 12px; 
            background: linear-gradient(to bottom, #457b9d, #1d3557); border: 1.5px solid #111; border-radius: 3px; 
        }
        .arm-left-side { left: -18px; transform: rotate(-15deg); transform-origin: right center; }
        .arm-right-side { right: -18px; transform: rotate(15deg); transform-origin: left center; }
        
        .human-weapon { position: absolute; top: -2px; width: 15px; height: 11px; background: linear-gradient(to bottom, #444, #111); border-radius: 2px; border-bottom: 2px solid #000; }
        .weapon-left-side { left: -28px; }
        .weapon-right-side { right: -28px; }

        #scoreTxt { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; text-shadow: 0 0 5px #ffea00; }
        .retry-btn { margin-top: 30px; padding: 12px 28px; background: #e63946; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 12px rgba(230,57,70,0.5); }
    </style>
</head>
<body>

    <div id="board">
        <div id="scoreTxt">00200</div>
        <div class="skyline-left"></div>
        <div class="skyline-right"></div>
        <div class="road-surface"></div>
        
        <div id="getawayCar">
            <div class="car-window"></div>
            <div class="car-light-l"></div>
            <div class="car-light-r"></div>
        </div>

        <div id="crosshair"></div>
        <div id="gun">
            <div class="gun-slide"></div>
            <div class="gun-hammer"></div>
            <div class="gun-frame"></div>
            <div class="gun-trigger-guard"></div>
            <div class="gun-grip"></div>
        </div>
    </div>
     let aimX = 168; 
    let aimY = 218; 
    let score = 200; 
    let gameOver = false;
    let isMovingCrosshair = false;
    let touchMovedFlag = false;
    
    let board = document.getElementById("board");
    let crosshair = document.getElementById("crosshair");
    let scoreTxt = document.getElementById("scoreTxt");
    let gun = document.getElementById("gun");
    let car = document.getElementById("getawayCar");
    
    let activeEnemies = [];
    let audioCtx = null; 
    let spawnInt = null; 
    let carXOffset = 0; 
    let carDirection = 1;

    function initAudio() {
        if (audioCtx) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function playSoundFX(type) {
        initAudio(); 
        if (!audioCtx) return;
        let osc = audioCtx.createOscillator(); 
        let gain = audioCtx.createGain();
        osc.connect(gain); 
        gain.connect(audioCtx.destination);
        
        if (type === "shoot") {
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(550, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.14);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            osc.start(); 
            osc.stop(audioCtx.currentTime + 0.14);
        }
        else if (type === "hit") {
            osc.type = "sine";
            osc.frequency.setValueAtTime(950, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1300, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); 
            osc.stop(audioCtx.currentTime + 0.08);
        }
        else if (type === "damage") {
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(100, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(25, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.45, audioCtx.currentTime);
            osc.start(); 
            osc.stop(audioCtx.currentTime + 0.35);
        }
    }

    function updatePosition(e) {
        if (gameOver) return;
        let pointer = e.touches ? e.touches : e;
        let boardRect = board.getBoundingClientRect();
        
        aimX = Math.max(-10, Math.min(345, pointer.clientX - boardRect.left - 15));
        aimY = Math.max(-10, Math.min(445, pointer.clientY - boardRect.top - 15));
        
        if (crosshair) {
            crosshair.style.left = aimX + "px";
            crosshair.style.top = aimY + "px";
        }
        
        if (gun) {
            let rotationAngle = (aimX - 168) / 15;
            let horizontalShift = (aimX - 168) / 8;
            let verticalShift = (aimY - 218) / 12;
            gun.style.transform = `rotate(${rotationAngle}deg) translateX(${horizontalShift}px) translateY(${verticalShift}px)`;
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
            if (!gameOver && crosshair) crosshair.style.borderColor = "#00f0ff";
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
                <div class="gun-slide"></div>
                <div class="gun-hammer"></div>
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

    setInterval(() => {
        if (gameOver || !car) return;
        carXOffset += carDirection * 1.5;
        if (carXOffset > 70) carDirection = -1;
        if (carXOffset < -70) carDirection = 1;
        car.style.transform = `translateX(${carXOffset}px)`;
    }, 30);

    function startSpawner() {
        // --- UPGRADED ARCADE COOLDOWN SPAWNER ACTION ---
        spawnInt = setInterval(() => {
            if (gameOver) { clearInterval(spawnInt); return; }
            if (activeEnemies.length >= 4) return;
            
            // Randomize spatial positioning variants across vehicle segments
            let positionRoll = Math.random();
            let side, currentY, innerHTML;
            
            if (positionRoll < 0.25) { // Left-side driver window
                side = -25; currentY = 185;
                innerHTML = '<div class="human-head"></div><div class="human-torso"><div class="human-arm arm-left-side"></div><div class="human-weapon weapon-left-side"></div></div>';
            } else if (positionRoll < 0.50) { // Right-side passenger window
                side = 145; currentY = 185;
                innerHTML = '<div class="human-head"></div><div class="human-torso"><div class="human-arm arm-right-side"></div><div class="human-weapon weapon-right-side"></div></div>';
            } else if (positionRoll < 0.75) { // Low left door position
                side = -15; currentY = 210;
                innerHTML = '<div class="human-head"></div><div class="human-torso"><div class="human-arm arm-left-side"></div><div class="human-weapon weapon-left-side"></div></div>';
            } else { // Low right door position
                side = 135; currentY = 210;
                innerHTML = '<div class="human-head"></div><div class="human-torso"><div class="human-arm arm-right-side"></div><div class="human-weapon weapon-right-side"></div></div>';
            }
            
            let enemy = document.createElement("div");
            enemy.className = "humanoid";
            enemy.innerHTML = innerHTML;
            
            let currentX = 110 + carXOffset + side;
            enemy.style.cssText = `position:absolute; top:${currentY}px; left:${currentX}px; width:40px; height:60px; z-index: 5;`;
            board.appendChild(enemy);
            
            let ring = document.createElement("div");
            ring.className = "lockon-ring";
            ring.style.cssText = `top:${currentY + 15}px; left:${currentX + 20}px;`;
            board.appendChild(ring);
            
            let enemyObj = { element: enemy, ring: ring, side: side, currentY: currentY };
            activeEnemies.push(enemyObj);
            
            let trackingInterval = setInterval(() => {
                if (gameOver || !enemy.parentNode) {
                    clearInterval(trackingInterval);
                    return;
                }
                let updatedX = 110 + carXOffset + side;
                enemy.style.left = updatedX + "px";
                ring.style.left = (updatedX + 2) + "px";
            }, 30);
            
            enemyObj.timeoutId = setTimeout(() => {
                if (gameOver || !enemy.parentNode) return;
                playSoundFX("damage");
                triggerGameOver();
            }, 1400);
        }, 1100);
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
    
