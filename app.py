import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Streamlit Retro Arcade",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🚀 Mobile Space Shooter with Sound")
st.write("Turn your sound up! Press **FIRE / ◀ / ▶** on mobile to play and restart.")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body {
            margin: 0;
            background-color: #010409;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            overflow: hidden;
            touch-action: none;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }
        #gameContainer {
            position: relative;
            width: 100vw;
            max-width: 450px;
            height: 65vh;
            max-height: 500px;
            margin-top: 5px;
        }
        canvas {
            width: 100%;
            height: 100%;
            background-color: #000000;
            border: 2px solid #30363d;
            border-radius: 8px;
            display: block;
        }
        #controls {
            display: flex;
            width: 100vw;
            max-width: 450px;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            box-sizing: border-box;
            height: 25vh;
        }
        .nav-cluster {
            display: flex;
            gap: 15px;
        }
        .btn {
            background-color: #21262d;
            border: 2px solid #30363d;
            color: white;
            font-weight: bold;
            font-size: 28px;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            -webkit-user-select: none;
        }
        .btn:active {
            background-color: #388bfd;
            transform: scale(0.9);
        }
        #fireBtn {
            background-color: #da3633;
            border-color: #f85149;
            width: 85px;
            height: 85px;
            font-size: 18px;
        }
        #fireBtn:active {
            background-color: #f85149;
        }
    </style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas"></canvas>
</div>

<div id="controls">
    <div class="nav-cluster">
        <div id="leftBtn" class="btn">◀</div>
        <div id="rightBtn" class="btn">▶</div>
    </div>
    <div id="fireBtn" class="btn">FIRE</div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 400;
    canvas.height = 500;

    const player = { x: canvas.width / 2 - 20, y: canvas.height - 60, width: 40, height: 40, speed: 6, color: "#238636" };
    const bullets = [];
    const enemies = [];
    let score = 0;
    let gameOver = false;
    let spawnTimeout = null;
    
    const inputs = { left: false, right: false };

    // Web Audio Synthesizer Engine
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    function playLaserSound() {
        initAudio();
        if (!audioCtx) return;
        
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(440, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(110, audioCtx.currentTime + 0.15);
        
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    }

    function playExplosionSound() {
        initAudio();
        if (!audioCtx) return;

        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();

        osc.type = "triangle";
        osc.frequency.setValueAtTime(150, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.3);

        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
    }

    // Centralized Restart Function
    function checkAndRestart() {
        if (gameOver) {
            resetGame();
            return true;
        }
        return false;
    }

    // Keyboard Bindings
    window.addEventListener("keydown", (e) => {
        if (gameOver && e.key === "Enter") { resetGame(); return; }
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") inputs.left = true;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") inputs.right = true;
        if (e.key === " " || e.key === "Spacebar") {
            if (!gameOver) fireBullet();
        }
    });

    window.addEventListener("keyup", (e) => {
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") inputs.left = false;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") inputs.right = false;
    });

    // Device Touch Bindings
    function setupTouch(elementId, stateProperty) {
        const btn = document.getElementById(elementId);
        
        btn.addEventListener("touchstart", (e) => {
            e.preventDefault();
            initAudio(); 
            if (checkAndRestart()) return;
            inputs[stateProperty] = true;
        }, { passive: false });

        btn.addEventListener("touchend", (e) => {
            e.preventDefault();
            inputs[stateProperty] = false;
        }, { passive: false });
    }

    setupTouch("leftBtn", "left");
    setupTouch("rightBtn", "right");

    function fireBullet() {
        bullets.push({ x: player.x + player.width / 2 - 3, y: player.y, width: 6, height: 15, speed: 9, color: "#58a6ff" });
        playLaserSound();
    }

    document.getElementById("fireBtn").addEventListener("touchstart", (e) => {
        e.preventDefault();
        initAudio();
        if (checkAndRestart()) return;
        fireBullet();
    }, { passive: false });

    canvas.addEventListener("touchstart", (e) => {
        e.preventDefault();
        initAudio();
        checkAndRestart();
    }, { passive: false });

    function spawnEnemy() {
        if (gameOver) return;
        const size = Math.random() * 15 + 20;
        const x = Math.random() * (canvas.width - size);
        enemies.push({ x: x, y: -size, width: size, height: size, speed: Math.random() * 1.5 + 1.5, color: "#f85149" });
        
        const nextSpawn = Math.max(500, 1200 - score * 6);
        spawnTimeout = setTimeout(spawnEnemy, nextSpawn);
    }

    function resetGame() {
        if (spawnTimeout) clearTimeout(spawnTimeout);
        score = 0;
        bullets.length = 0;
        enemies.length = 0;
        player.x = canvas.width / 2 - 20;
        gameOver = false;
        inputs.left = false;
        inputs.right = false;
        spawnEnemy();
        update();
    }

    function update() {
        if (gameOver) {
            ctx.fillStyle = "rgba(1, 4, 9, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#f85149";
            ctx.font = "bold 28px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);
            ctx.fillStyle = "#ffffff";
            ctx.font = "16px sans-serif";
            ctx.fillText("Tap ANY Button to Restart", canvas.width / 2, canvas.height / 2 + 20);
            return;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (inputs.left && player.x > 0) player.x -= player.speed;
        if (inputs.right && player.x < canvas.width - player.width) player.x += player.speed;

        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(player.x + player.width / 2, player.y);
        ctx.lineTo(player.x, player.y + player.height);
        ctx.lineTo(player.x + player.width, player.y + player.height);
        ctx.closePath();
        ctx.fill();

        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= bullets[i].speed;
            if (bullets[i].y < 0) {
                bullets.splice(i, 1);
                continue;
            }
            ctx.fillStyle = bullets[i].color;
            ctx.fillRect(bullets[i].x, bullets[i].y, bullets[i].width, bullets[i].height);
        }

        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].y += enemies[i].speed;
            
            if (enemies[i].y > canvas.height) {
                gameOver = true;
                playExplosionSound();
            }

            ctx.fillStyle = enemies[i].color;
            ctx.fillRect(enemies[i].x, enemies[i].y, enemies[i].width, enemies[i].height);

            if (enemies[i].x < player.x + player.width &&
                enemies[i].x + enemies[i].width > player.x &&
                enemies[i].y < player.y + player.height &&
                enemies[i].y + enemies[i].height > player.y) {
                gameOver = true;
                playExplosionSound();
            }

            for (let j = bullets.length - 1; j >= 0; j--) {
            if (bullets[j].x < enemies[i].x + enemies[i].width &&
bullets[j].x + bullets[j].width > enemies[i].x &&
bullets[j].y < enemies[i].y + enemies[i].height &&
bullets[j].y + bullets[j].height > enemies[i].y) {

enemies.splice(i, 1);
bullets.splice(j, 1);
score += 10;
playExplosionSound();
break;
}
}
}

ctx.fillStyle = "#ffffff";
ctx.font = "bold 18px sans-serif";
ctx.textAlign = "left";
ctx.fillText(Score: ${score}, 15, 30);

requestAnimationFrame(update);
}

resetGame();


"""

components.html(game_html, height=750, scrolling=False)
            
            

