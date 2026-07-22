import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Space Shooter",
    page_icon="🚀",
    layout="wide" # Bypasses standard narrow container constraints
)

st.title("🚀 Mobile Space Shooter with Sound")
st.write("Turn your sound up! Press **FIRE / ◀ / ▶** on mobile or **WASD / Space** on PC to play.")

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
    let gameStarted = false; // Fixes blank browser safety state
    let gameOver = false;
    let spawnTimeout = null;
    
    const inputs = { left: false, right: false };
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

    function handleInteractionStart() {
        if (!gameStarted) {
            gameStarted = true;
            resetGame();
            return true;
        }
        if (gameOver) {
            resetGame();
            return true;
        }
        return false;
    }

    // Keyboard Bindings
    window.addEventListener("keydown", (e) => {
        if (!gameStarted || gameOver) {
            if (e.key === "Enter" || e.key === " ") {
                handleInteractionStart();
            }
            return;
        }
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") inputs.left = true;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") inputs.right = true;
        if (e.key === " " || e.key === "Spacebar") fireBullet();
    });

    window.addEventListener("keyup", (e) => {
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") inputs.left = false;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") inputs.right = false;
    });

    // Touch and Click Interactions
    function setupTouch(elementId, stateProperty) {
        const btn = document.getElementById(elementId);
        btn.addEventListener("touchstart", (e) => {
            e.preventDefault();
            if (handleInteractionStart()) return;
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
        if (handleInteractionStart()) return;
        fireBullet();
    }, { passive: false });

    // PC Click Handler / Mobile Canvas Fallback
    canvas.addEventListener("mousedown", (e) => {
        handleInteractionStart();
    });
    canvas.addEventListener("touchstart", (e) => {
        e.preventDefault();
        handleInteractionStart();
    }, { passive: false });

    function spawnEnemy() {
        if (!gameStarted || gameOver) return;
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
    }

      function drawLoop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (!gameStarted) {
            // Draw a bright green box to show the game engine is alive
            ctx.fillStyle = "#238636";
            ctx.fillRect(40, 125, 320, 200);
            
            // Draw a bright blue triangle (start arrow) instead of text strings
            ctx.fillStyle = "#58a6ff";
            ctx.beginPath();
            ctx.moveTo(200, 180);
            ctx.lineTo(170, 240);
            ctx.lineTo(230, 240);
            ctx.closePath();
            ctx.fill();
            
            requestAnimationFrame(drawLoop);
            return;
        }

        if (gameOver) {
            ctx.fillStyle = "#da3633";
            ctx.fillRect(50, 150, 300, 200);
            
            ctx.fillStyle = "#ffffff";
            ctx.font = "24px Arial";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width / 2, 230);
            ctx.font = "14px Arial";
            ctx.fillText("CLICK TO RESTART", canvas.width / 2, 290);
            return;
        }

        if (inputs.left && player.x > 0) player.x -= player.speed;
        if (inputs.right && player.x < canvas.width - player.width) player.x += player.speed;

        // Render Green Player Ship
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(player.x + player.width / 2, player.y);
        ctx.lineTo(player.x, player.y + player.height);
        ctx.lineTo(player.x + player.width, player.y + player.height);
        ctx.closePath();
        ctx.fill();

        // Projectiles Controller
        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= bullets[i].speed;
            if (bullets[i].y < 0) {
                bullets.splice(i, 1);
                continue;
            }
            ctx.fillStyle = bullets[i].color;
            ctx.fillRect(bullets[i].x, bullets[i].y, bullets[i].width, bullets[i].height);
        }

        // Hostiles Controller
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

        // Render Score Counter Text
        ctx.fillStyle = "#ffffff";
        ctx.font = "16px Arial";
        ctx.textAlign = "left";
        ctx.fillText("Score: " + score, 15, 30);
    }



requestAnimationFrame(drawLoop);
}
// Start rendering the title screen immediately
    // Force browser engine loop inside Streamlit container structures
    setInterval(drawLoop, 1000 / 60);
</script>


"""

_, center_column, _ = st.columns([1, 4, 1])

with center_column:
    components.html(game_html, height=900, scrolling=False)
