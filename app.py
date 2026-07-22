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
        #board { position: relative; width: 320px; height: 350px; background: black; border: 3px solid #333; overflow: hidden; margin: auto; border-radius: 8px; }
        #ship { position: absolute; bottom: 10px; left: 140px; width: 40px; height: 40px; background: lime; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); }
        .btn { padding: 15px 22px; font-size: 16px; margin: 5px; background: #222; color: white; border-radius: 8px; border: 1px solid #555; font-weight: bold; }
        #fire { background: red; border-color: #a00; }
        #scoreTxt { position: absolute; top: 10px; left: 10px; color: white; font-weight: bold; font-size: 16px; z-index: 10; }
    </style>
</head>
<body>

    <div id="board">
        <div id="scoreTxt">Score: 0</div>
        <div id="ship"></div>
    </div>

    <div style="text-align: center; margin-top: 15px;">
        <button class="btn" onclick="move(-25)">◀ Left</button>
        <button class="btn" onclick="move(25)">Right ▶</button>
        <button class="btn" id="fire" onclick="shoot()">FIRE</button>
    </div>

<script>
    let shipX = 140; let score = 0; let gameOver = false;
    const board = document.getElementById("board");
    const ship = document.getElementById("ship");
    const scoreTxt = document.getElementById("scoreTxt");
    
    const activeBullets = []; const activeEnemies = [];
    let audioCtx = null;

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

    function move(dir) {
        if (gameOver) { location.reload(); return; }
        shipX = Math.max(0, Math.min(280, shipX + dir));
        ship.style.left = shipX + "px";
    }

    function shoot() {
        if (gameOver) { location.reload(); return; }
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
                if(activeBullets.indexOf(b) > -1) activeBullets.splice(activeBullets.indexOf(b), 1); 
            }
        }, 20);
    }

    let spawnInt = setInterval(() => {
        if (gameOver) { clearInterval(spawnInt); return; }
        
        let e = document.createElement("div");
        let eX = Math.random() * 295;
        e.style.cssText = "position:absolute; top:0px; left:"+eX+"px; width:25px; height:25px; background:red; border-radius:4px;";
        board.appendChild(e); activeEnemies.push(e);
        
        let eY = 0;
        let eInt = setInterval(() => {
            if (gameOver) { clearInterval(eInt); return; }
            eY += 3; e.style.top = eY + "px";
            
            // 1. Crash Collision check (Enemies hitting player)
            if (eY > 300 && Math.abs(eX - shipX) < 30) {
                triggerGameOver();
            }

            // 2. Hit elimination check (Lasers hitting enemies)
            activeBullets.forEach((b) => {
                let bLeft = parseInt(b.style.left) || 0;
                let bBottom = parseInt(b.style.bottom) || 0;
                let bTop = 350 - bBottom;
                
                if (Math.abs(bLeft - eX) < 25 && bTop < (eY + 25) && bTop > eY) {
                    playSound(150, 40, 0.15, "triangle");
                    score += 10;
                    scoreTxt.innerText = "Score: " + score;
                    
                    clearInterval(eInt); e.remove(); 
                    if(activeEnemies.indexOf(e) > -1) activeEnemies.splice(activeEnemies.indexOf(e), 1);
                    b.remove(); 
                    if(activeBullets.indexOf(b) > -1) activeBullets.splice(activeBullets.indexOf(b), 1);
                }
            });

            if(eY > 350) { 
                clearInterval(eInt); e.remove(); 
                if(activeEnemies.indexOf(e) > -1) activeEnemies.splice(activeEnemies.indexOf(e), 1); 
            }
        }, 20);
    }, 1200);

    function triggerGameOver() {
        gameOver = true;
        playSound(100, 20, 0.4, "sawtooth");
        board.innerHTML = "<div style='color:red; font-size:32px; font-weight:bold; text-align:center; margin-top:120px;'>GAME OVER<br><span style='color:white; font-size:14px; font-weight:normal;'>Score: "+score+"<br><br>Tap Any Control Button to Restart</span></div>";
    }

    // Keyboard support fallback for PC tests
    window.addEventListener("keydown", (e) => {
        if(e.key === "ArrowLeft" || e.key === "a") move(-25);
        if(e.key === "ArrowRight" || e.key === "d") move(25);
        if(e.key === " " || e.key === "Enter") shoot();
    });
</script>
</body>
</html>
"""

components.html(game_html, height=450)
