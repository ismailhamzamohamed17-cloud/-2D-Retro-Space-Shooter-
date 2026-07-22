import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FPS Space", layout="centered")
st.title("🚀 First-Person Space Shooter")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        #board { position: relative; width: 320px; height: 350px; background: radial-gradient(circle, #111 10%, #000 90%); border: 3px solid #333; overflow: hidden; margin: auto; border-radius: 8px; }
        /* 3D FPS Crosshair styling */
        #crosshair { position: absolute; bottom: 155px; left: 140px; width: 40px; height: 40px; border: 2px dashed lime; border-radius: 50%; will-change: left; z-index: 5; }
        #crosshair::after { content: ''; position: absolute; top: 19px; left: 19px; width: 2px; height: 2px; background: lime; }
        .btn { padding: 18px 35px; font-size: 18px; margin: 5px 10px; background: #222; color: white; border-radius: 8px; border: 1px solid #555; font-weight: bold; min-width: 120px; }
        #scoreTxt { position: absolute; top: 10px; left: 10px; color: white; font-weight: bold; font-size: 16px; z-index: 10; }
        .retry-btn { margin-top: 15px; padding: 12px 25px; background: #238636; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 4px; }
    </style>
</head>
<body>

    <div id="board" onmousedown="handleScreenTap(event)" ontouchstart="handleScreenTap(event)">
        <div id="scoreTxt">Score: 0</div>
        <div id="crosshair"></div>
    </div>

    <div style="text-align: center; margin-top: 15px;">
        <button class="btn" onmousedown="startMove(-1)" onmouseup="stopMove()" ontouchstart="event.preventDefault(); startMove(-1)" ontouchend="event.preventDefault(); stopMove()">◀ Aim Left</button>
        <button class="btn" onmousedown="startMove(1)" onmouseup="stopMove()" ontouchstart="event.preventDefault(); startMove(1)" ontouchend="event.preventDefault(); stopMove()">Aim Right ▶</button>
    </div>

<script>
    let aimX = 140; let score = 0; let gameOver = false;
    let moveDirection = 0; const aimSpeed = 6;
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

    // Generates continuous, retro sci-fi background space music dynamically
    function startBackgroundMusic() {
        try {
            bgOsc1 = audioCtx.createOscillator(); bgOsc2 = audioCtx.createOscillator();
            let bgGain = audioCtx.createGain();
            
            bgOsc1.type = "triangle"; bgOsc1.frequency.setValueAtTime(73.42, audioCtx.currentTime); // D2 note
            bgOsc2.type = "sine"; bgOsc2.frequency.setValueAtTime(110.00, audioCtx.currentTime); // A2 minor chord depth
            
            bgGain.gain.setValueAtTime(0.05, audioCtx.currentTime); // Low volume background layer
            
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
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + duration);
    }

    function startMove(dir) { if (gameOver) return; moveDirection = dir; }
    function stopMove() { moveDirection = 0; }

    function updatePhysicsLoop() {
        if (!gameOver && moveDirection !== 0) {
            aimX = Math.max(0, Math.min(280, aimX + (moveDirection * aimSpeed)));
            if(globalThis.crosshair) globalThis.crosshair.style.left = aimX + "px";
        }
        requestAnimationFrame(updatePhysicsLoop);
    }

    window.handleScreenTap = function(e) {
        if (gameOver) return;
        if (e.target.classList.contains('retry-btn')) return;
        e.preventDefault();
        shoot();
    }

    function shoot() {
        if (gameOver) return;
        initAudio(); playSound(587.33, 293.66, 0.12, "sawtooth"); // Deep laser discharge sound
        
        // Flash crosshair red instantly to indicate firing confirmation
        crosshair.style.borderColor = "red";
        setTimeout(() => { if(!gameOver) crosshair.style.borderColor = "lime"; }, 60);

        // FPS Hit Check: Check if crosshair is centered over any oncoming scaling target
        activeEnemies.forEach((e) => {
            let eX = parseFloat(e.style.left) || 0;
            let eWidth = parseFloat(e.style.width) || 0;
            let centerOfEnemy = eX + (eWidth / 2);
            let centerOfAim = aimX + 20;

            // If target is close enough to center vision and large enough, blow it up
            if (Math.abs(centerOfAim - centerOfEnemy) < (eWidth / 2 + 10) && eWidth > 15) {
                playSound(120, 30, 0.2, "triangle");
                score += 10;
                if(globalThis.scoreTxt) scoreTxt.innerText = "Score: " + score;
                if(e.intervalId) clearInterval(e.intervalId);
                e.remove();
                activeEnemies = activeEnemies.filter(item => item !== e);
            }
        });
    }

    function restartGame() {
        stopBackgroundMusic();
        if(spawnInt) clearInterval(spawnInt);
        activeEnemies.forEach(e => { if(e.intervalId) clearInterval(e.intervalId); e.remove(); });
        
        activeEnemies = []; score = 0; aimX = 140; moveDirection = 0; gameOver = false;
        
        board.innerHTML = '<div id="scoreTxt">Score: 0</div><div id="crosshair" style="left: 140px;"></div>';
        setTimeout(() => {
            globalThis.scoreTxt = document.getElementById("scoreTxt");
            globalThis.crosshair = document.getElementById("crosshair");
            if(audioCtx) startBackgroundMusic();
            startSpawner();
        }, 50);
    }

    function startSpawner() {
        spawnInt = setInterval(() => {
            if (gameOver) { clearInterval(spawnInt); return; }
            
            let e = document.createElement("div");
            // Random trajectory targets heading outward from background depth
            let targetX = Math.random() * 260 + 20; 
            let currentSize = 4; // Spawns tiny in the distance
            
            e.style.cssText = `position:absolute; top:160px; left:160px; width:${currentSize}px; height:${currentSize}px; background:red; border-radius:50%; box-shadow: 0 0 8px red;`;
            board.appendChild(e); activeEnemies.push(e);
            
            let steps = 0;
            let eInt = setInterval(() => {
                if (gameOver) { clearInterval(eInt); return; }
                steps += 1;
                currentSize += 0.8; // Scales up towards screen perspective layout
                
                // Track 3D physics movement vectors outwards towards screen boundary perimeter
                let speedX = (targetX - 160) / 80;
                let currentX = 160 + (speedX * steps) - (currentSize / 2);
                let currentY = 160 + (1.2 * steps) - (currentSize / 2);
                
                e.style.width = currentSize + "px";
                e.style.height = currentSize + "px";
                e.style.left = currentX + "px";
                e.style.top = currentY + "px";
                e.intervalId = eInt;
                
                // Game Over trigger if enemy scaling breaches screen boundary context
                if (currentSize > 65) {
                    triggerGameOver();
                    clearInterval(eInt);
                }
            }, 25);
        }, 1000);
    }

    function triggerGameOver() {
        gameOver = true; moveDirection = 0;
        stopBackgroundMusic();
        playSound(90, 10, 0.6, "sawtooth");
        board.innerHTML = `
            <div style='color:red; font-size:32px; font-weight:bold; text-align:center; margin-top:90px;'>
                CRASH / OVER<br>
                <span style='color:white; font-size:18px; font-weight:normal;'>Final Score: ${score}</span><br>
                <button class='retry-btn' onclick='restartGame()'>RETRY 🔄</button>
            </div>`;
    }

    window.addEventListener("keydown", (e) => {
        if (e.repeat) return;
        if(e.key === "ArrowLeft" || e.key === "a") startMove(-1);
        if(e.key === "ArrowRight" || e.key === "d") startMove(1);
        if(e.key === " " || e.key === "Enter") { if(gameOver) restartGame(); else shoot(); }
    });

    window.addEventListener("keyup", (e) => {
        if((e.key === "ArrowLeft" || e.key === "a") && moveDirection === -1) stopMove();
        if((e.key === "ArrowRight" || e.key === "d") && moveDirection === 1) stopMove();
    });

    globalThis.scoreTxt = scoreTxt; globalThis.crosshair = crosshair;
    startSpawner(); updatePhysicsLoop();
</script>
</body>
</html>
"""

components.html(game_html, height=450)
