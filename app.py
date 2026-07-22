import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Desert FPS", layout="centered")
st.title("🏜️ Desert Sniper FPS")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        /* Layered Sunset Desert Canvas */
        #board { 
            position: relative; 
            width: 320px; 
            height: 350px; 
            background: linear-gradient(to bottom, #ff7e5f 0%, #feb47b 40%, #e07a5f 70%, #f4a261 100%); 
            border: 3px solid #555; 
            overflow: hidden; 
            margin: auto; 
            border-radius: 8px; 
            touch-action: none;
        }
        
        /* Distant background mountain ranges */
        #board::before {
            content: ''; position: absolute; bottom: 0; left: -50px; width: 250px; height: 120px; background: #c2593f; clip-path: polygon(0% 100%, 50% 20%, 100% 100%); opacity: 0.7; z-index: 1;
        }
        #board::after {
            content: ''; position: absolute; bottom: 0; right: -30px; width: 200px; height: 90px; background: #a64630; clip-path: polygon(0% 100%, 40% 10%, 100% 100%); opacity: 0.9; z-index: 2;
        }

        /* 3D FPS Tactical Scope Crosshair */
        #crosshair { 
            position: absolute; 
            top: 155px; 
            left: 140px; 
            width: 44px; 
            height: 44px; 
            border: 3px solid #ff0055; 
            border-radius: 50%; 
            will-change: left, top; 
            z-index: 15; 
            cursor: move;
            box-shadow: 0 0 0 999px rgba(0, 0, 0, 0.15); /* Scope tint effect */
        }
        #crosshair::before { content: ''; position: absolute; top: 21px; left: 0; width: 44px; height: 2px; background: #ff0055; }
        #crosshair::after { content: ''; position: absolute; top: 0; left: 21px; width: 2px; height: 44px; background: #ff0055; }
        
        #scoreTxt { position: absolute; top: 10px; left: 10px; color: black; font-weight: bold; font-size: 18px; z-index: 10; background: rgba(255,255,255,0.6); padding: 2px 8px; border-radius: 4px; }
        .retry-btn { margin-top: 15px; padding: 12px 25px; background: #e76f51; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 4px; }
        
        /* Humanoid Target Assembly Framework */
        .humanoid { position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; z-index: 5; pointer-events: none; }
        .head { border-radius: 50%; background: #2b2d42; width: 25%; height: 25%; }
        .torso { background: #2b2d42; width: 15%; height: 45%; margin-top: 2%; position: relative; }
        .arm-l { position: absolute; top: 10%; left: -150%; width: 150%; height: 20%; background: #2b2d42; transform: rotate(-30deg); transform-origin: right; }
        .arm-r { position: absolute; top: 10%; right: -150%; width: 150%; height: 20%; background: #2b2d42; transform: rotate(30deg); transform-origin: left; }
        .legs { display: flex; justify-content: space-between; width: 100%; height: 28%; }
        .leg { background: #2b2d42; width: 20%; height: 100%; }
    </style>
</head>
<body>

    <div id="board">
        <div id="scoreTxt">Score: 0</div>
        <div id="crosshair"></div>
    </div>

    <p style="text-align: center; color: #8b949e; font-size: 13px; margin-top: 10px; font-family: sans-serif;">
        🎯 <b>Drag the scope crosshair</b> directly with your finger to aim, and <b>lift your finger up</b> to shoot!
    </p>

<script>
    let aimX = 140; let aimY = 155; let score = 0; let gameOver = false;
    let isDragging = false;
    let touchStartX = 0; let touchStartY = 0;
    
    const board = document.getElementById("board");
    const crosshair = document.getElementById("crosshair");
    const scoreTxt = document.getElementById("scoreTxt");
    
    let activeEnemies = [];
    let audioCtx = null; let spawnInt = null; let bgOsc1 = null; let bgOsc2 = null;

    function initAudio() {
        if (audioCtx) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        startBackgroundMusic();
    }

    function startBackgroundMusic() {
        try {
            bgOsc1 = audioCtx.createOscillator(); bgOsc2 = audioCtx.createOscillator();
            let bgGain = audioCtx.createGain();
            bgOsc1.type = "sine"; bgOsc1.frequency.setValueAtTime(65.41, audioCtx.currentTime); // C2 background drone
            bgOsc2.type = "triangle"; bgOsc2.frequency.setValueAtTime(98.00, audioCtx.currentTime); // G2 sandstorm drone
            bgGain.gain.setValueAtTime(0.06, audioCtx.currentTime);
            bgOsc1.connect(bgGain); bgOsc2.connect(bgGain);
            bgGain.connect(audioCtx.destination);
            bgOsc1.start(); bgOsc2.start();
        } catch(e) {}
    }

    function stopBackgroundMusic() {
        if(bgOsc1) { try { bgOsc1.stop(); bgOsc2.stop(); } catch(e){} }
    }

    function playSound(fStart, fEnd, duration, type) {
        initAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
        osc.type = type; osc.frequency.setValueAtTime(fStart, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(fEnd, audioCtx.currentTime + duration);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + duration);
    }

    // Touch and Mouse Drag Implementation
      function onStart(e) {
        if (gameOver) return;
        let clientX = e.touches ? e.touches[0].clientX : e.clientX;
        let clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        let rect = crosshair.getBoundingClientRect();
        isDragging = true;
        touchStartX = clientX - aimX;
        touchStartY = clientY - aimY;
    }

    function onMove(e) {
        if (!isDragging || gameOver) return;
        if (e.touches) e.preventDefault(); // Prevents screen bouncing on mobile safari/chrome
        
        let clientX = e.touches ? e.touches[0].clientX : e.clientX;
        let clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        // Track finger dragging positions across the board
        aimX = Math.max(-10, Math.min(285, clientX - touchStartX));
        aimY = Math.max(-10, Math.min(315, clientY - touchStartY));
        
        crosshair.style.left = aimX + "px";
        crosshair.style.top = aimY + "px";
    }

    function onEnd() {
        if (!isDragging || gameOver) return;
        isDragging = false;
        shoot(); // Fire sniper automatically upon lifting finger
    }

    // Attach interaction events directly to your screen window
    crosshair.addEventListener("touchstart", onStart, {passive: false});
    window.addEventListener("touchmove", onMove, {passive: false});
    window.addEventListener("touchend", onEnd);
    crosshair.addEventListener("mousedown", onStart);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onEnd);
    // ---------------------------------------------

    function startSpawner() {
        spawnInt = setInterval(() => {
            if (gameOver) { 
                clearInterval(spawnInt); 
                return; 
            }
            
            // Generate full modular HTML vector assembly for the Humanoid target structures
            let h = document.createElement("div");
            h.className = "humanoid";
            h.innerHTML = '<div class="head"></div><div class="torso"><div class="arm-l"></div><div class="arm-r"></div></div><div class="legs"><div class="leg"></div><div class="leg"></div></div>';
            
            let targetX = Math.random() * 240 + 30;
            let targetY = 160 + (Math.random() * 40 - 20); 
            let currentW = 4; 
            let currentH = 8;
            
            // FIXED: Added mandatory backticks around string variables to prevent app engine crashing
            h.style.cssText = `position:absolute; top:160px; left:160px; width:${currentW}px; height:${currentH}px;`;
            board.appendChild(h); 
            activeEnemies.push(h);
            
            let steps = 0;
            let hInt = setInterval(() => {
                if (gameOver) { 
                    clearInterval(hInt); 
                    return; 
                }
                
                steps += 1;
                currentW += 0.5; 
                currentH += 1.0; 
                
                let speedX = (targetX - 160) / 90;
                let currentX = 160 + (speedX * steps) - (currentW / 2);
                let currentY = 160 + (1.3 * steps) - (currentH / 2);
                
                h.style.width = currentW + "px";
                h.style.height = currentH + "px";
                h.style.left = currentX + "px";
                h.style.top = currentY + "px";
                h.intervalId = hInt;
                
                if (currentH > 90) {
                    triggerGameOver();
                    clearInterval(hInt);
                }
            }, 25);
        }, 1100);
    }

    function triggerGameOver() {
        gameOver = true; 
        isDragging = false;
        stopBackgroundMusic();
        playSound(120, 10, 0.5, "sawtooth");
        board.innerHTML = `
            <div style='color:#7a1f1d; font-size:30px; font-weight:bold; text-align:center; margin-top:100px; position:relative; z-index:20; text-shadow: 1px 1px black;'>
                MISSION FAILED<br>
                <span style='color:black; font-size:18px; font-weight:normal;'>Score: ${score}</span><br>
                <button class='retry-btn' onclick='restartGame()'>REDEPLOY 🔄</button>
            </div>`;
    }

    globalThis.scoreTxt = scoreTxt; 
    globalThis.crosshair = crosshair;
    startSpawner();
"""

components.html(game_html, height=450)


