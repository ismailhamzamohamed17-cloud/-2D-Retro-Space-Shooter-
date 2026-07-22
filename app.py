import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Space Shooter", layout="centered")
st.title("🚀 Mobile Space Shooter")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; }
        #board { position: relative; width: 320px; height: 350px; background: black; border: 3px solid #333; overflow: hidden; margin: auto; border-radius: 8px; cursor: crosshair; }
        #ship { position: absolute; bottom: 10px; left: 140px; width: 40px; height: 40px; background: lime; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); will-change: left; }
        .btn { padding: 18px 35px; font-size: 18px; margin: 5px 10px; background: #222; color: white; border-radius: 8px; border: 1px solid #555; font-weight: bold; min-width: 120px; touch-action: manipulation; }
        #scoreTxt { position: absolute; top: 10px; left: 10px; color: white; font-weight: bold; font-size: 16px; z-index: 10; }
        .retry-btn { margin-top: 15px; padding: 12px 25px; background: #238636; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>

    <!-- Tap directly inside this container on your phone screen to fire lasers -->
    <div id="board" onmousedown="handleScreenTap(event)" ontouchstart="handleScreenTap(event)">
        <div id="scoreTxt">Score: 0</div>
        <div id="ship"></div>
    </div>

    <!-- Simplified movement controls -->
    <div style="text-align: center; margin-top: 15px;">
        <button class="btn" 
                onmousedown="startMove(-1)" onmouseup="stopMove()" ontouchstart="event.preventDefault(); startMove(-1)" ontouchend="event.preventDefault(); stopMove()">◀ Left</button>
        <button class="btn" 
                onmousedown="startMove(1)" onmouseup="stopMove()" ontouchstart="event.preventDefault(); startMove(1)" ontouchend="event.preventDefault(); stopMove()">Right ▶</button>
    </div>

<script>
    let shipX = 140; let score = 0; let gameOver = false;
    let moveDirection = 0;
    const shipSpeed = 6;

    const board = document.getElementById("board");
    const ship = document.getElementById("ship");
    const scoreTxt = document.getElementById("scoreTxt");
    
    let activeBullets = []; let activeEnemies = [];
    let audioCtx = null;
    let spawnInt = null;

    function initAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
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

    function startMove(dir) {
        if (gameOver) return;
        moveDirection = dir;
    }

    function stopMove() {
        moveDirection = 0;
    }

    function updatePhysicsLoop() {
        if (!gameOver && moveDirection !== 0) {
            shipX = Math.max(0, Math.min(280, shipX + (moveDirection * shipSpeed)));
            if(globalThis.ship) globalThis.ship.style.left = shipX + "px";
        }
        requestAnimationFrame(updatePhysicsLoop);
    }

    // Handles screening triggers for touchscreen taps & mouse clicks
    window.handleScreenTap = function(e) {
        if (gameOver) return;
        
        // Safety check to prevent firing when clicking the retry button itself
        if (e.target.classList.contains('retry-btn')) return;
        
        e.preventDefault();
        shoot();
    }

    function shoot() {
        if (gameOver) return;
        initAudio(); playSound(500, 150, 0.08, "sawtooth");
        
        let b = document.createElement("div");
        b.style.cssText = "position:absolute; bottom:50px; left:"+(shipX+17)+"px; width:6px; height:15px; background:cyan; border-radius:2px;";
        board.appendChild(b); activeBullets.push(b);
        
        let bY = 50;
        let bInt = setInterval(() => {
            if (gameOver) { clearInterval(bInt); return; }
            bY += 8; b.style.bottom = bY + "px";
            if(bY > 350) { 
                clearInterval(bInt); b.remove(); 
                activeBullets = activeBullets.filter(item => item !== b);
            }
        }, 20);
    }

    function restartGame() {
        if(spawnInt) clearInterval(spawnInt);
        activeBullets.forEach(b => b.remove());
        activeEnemies.forEach(e => { if(e.intervalId) clearInterval(e.intervalId); e.remove(); });
        
        activeBullets = [];
        activeEnemies = [];
        score = 0;
        shipX = 140;
        moveDirection = 0;
        gameOver = false;
        
        board.innerHTML = '<div id="scoreTxt">Score: 0</div><div id="ship" style="left: 140px;"></div>';
        setTimeout(() => {
            globalThis.scoreTxt = document.getElementById("scoreTxt");
            globalThis.ship = document.getElementById("ship");
            startSpawner();
        }, 50);
    }

    function startSpawner() {
        spawnInt = setInterval(() => {
            if (gameOver) { clearInterval(spawnInt); return; }
            
            let e = document.createElement("div");
            let eX = Math.random() * 295;
            e.style.cssText = "position:absolute; top:0px; left:"+eX+"px; width:25px; height:25px; background:red; border-radius:4px;";
            board.appendChild(e); activeEnemies.push(e);
            
            let eY = 0;
            let eInt = setInterval(() => {
                if (gameOver) { clearInterval(eInt); return; }
                eY += 3; e.style.top = eY + "px";
                e.intervalId = eInt;
                
                if (eY > 300 && Math.abs(eX - shipX) < 30) {
                    triggerGameOver();
                    clearInterval(eInt);
                }

                activeBullets.forEach((b) => {
                    let bLeft = parseInt(b.style.left) || 0;
                    let bBottom = parseInt(b.style.bottom) || 0;
                    let bTop = 350 - bBottom;
                    
                    if (Math.abs(bLeft - eX) < 25 && bTop < (eY + 25) && bTop > eY) {
                        playSound(150, 40, 0.15, "triangle");
                        score += 10;
                        if(globalThis.scoreTxt) scoreTxt.innerText = "Score: " + score;
                        
                        clearInterval(eInt); e.remove(); 
                        activeEnemies = activeEnemies.filter(item => item !== e);
                        b.remove(); 
                        activeBullets = activeBullets.filter(item => item !== b);
                    }
                });

                if(eY > 350) { 
                    clearInterval(eInt); e.remove(); 
                    activeEnemies = activeEnemies.filter(item => item !== e);
                }
            }, 20);
        }, 1200);
    }

    function triggerGameOver() {
        gameOver = true;
        moveDirection = 0;
        playSound(100, 20, 0.4, "sawtooth");
        board.innerHTML = `
            <div style='color:red; font-size:32px; font-weight:bold; text-align:center; margin-top:90px;'>
                GAME OVER<br>
                <span style='color:white; font-size:18px; font-weight:normal;'>Final Score: ${score}</span><br>
                <button class='retry-btn' onclick='restartGame()'>RETRY 🔄</button>
            </div>`;
    }

    window.addEventListener("keydown", (e) => {
        if (e.repeat) return;
        if(e.key === "ArrowLeft" || e.key === "a") startMove(-1);
        if(e.key === "ArrowRight" || e.key === "d") startMove(1);
        if(e.key === " " || e.key === "Enter") {
            if(gameOver) restartGame();
            else shoot();
        }
    });

    window.addEventListener("keyup", (e) => {
        if((e.key === "ArrowLeft" || e.key === "a") && moveDirection === -1) stopMove();
        if((e.key === "ArrowRight" || e.key === "d") && moveDirection === 1) stopMove();
    });

    globalThis.scoreTxt = scoreTxt;
    globalThis.ship = ship;
    startSpawner();
    updatePhysicsLoop();
</script>
</body>
</html>
"""

components.html(game_html, height=450)
