import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit page layout to maximize screen real estate
st.set_page_config(
    page_title="Streamlit Space Shooter",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🚀 Mobile-Friendly Space Shooter")
st.write("Playing on desktop? Use **Arrow Keys / WASD** and **Spacebar**. Playing on mobile? Use the **on-screen touch controls** below!")

# Pure HTML5 / Canvas / Touch JavaScript Engine
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
            touch-action: none; /* Prevents double-tap zooming on mobile Safari/Chrome */
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }
        #gameContainer {
            position: relative;
            width: 100vw;
            max-width: 450px; /* Locked down mobile aspect aspect-ratio */
            height: 70vh;
            max-height: 550px;
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
        /* Touch Controls Area */
        #controls {
            display: flex;
            width: 100vw;
            max-width: 450px;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            box-sizing: border-box;
            height: 20vh;
        }
        .nav-cluster {
            display: flex;
            gap: 12px;
        }
        .btn {
            background-color: #21262d;
            border: 2px solid #30363d;
            color: white;
            font-weight: bold;
            font-size: 24px;
            border-radius: 50%;
            width: 65px;
            height: 65px;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            -webkit-user-select: none;
        }
        .btn:active {
            background-color: #388bfd;
            transform: scale(0.92);
        }
        #fireBtn {
            background-color: #da3633;
            border-color: #f85149;
            width: 75px;
            height: 75px;
            border-radius: 50%;
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

    // Internal Logical Game Resolution Setup
    canvas.width = 400;
    canvas.height = 500;

    const player = { x: canvas.width / 2 - 20, y: canvas.height - 60, width: 40, height: 40, speed: 6, color: "#238636" };
    const bullets = [];
    const enemies = [];
    let score = 0;
    let gameOver = false;
    
    // Combined State Tracker for Hardware Keys + Touch Controls
    const inputs = { left: false, right: false, fire: false };

    // Keyboard Bindings
    window.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") inputs.left = true;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") inputs.right = true;
        if (e.key === " " || e.key === "Spacebar") { inputs.fire = true; }
        if (e.key === "Enter" && gameOver) resetGame();
    });
    window.addEventListener("keyup", (e) => {
        if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") inputs.left = false;
        if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") inputs.right = false;
    });

    // Touch Event Helpers
    function setupTouch(elementId, stateProperty) {
        const btn = document.getElementById(elementId);
        
        btn.addEventListener("touchstart", (e) => {
            e.preventDefault();
            if (gameOver) {
                resetGame();
                return;
            }
            inputs[stateProperty] = true;
        }, { passive: false });

        btn.addEventListener("touchend", (e) => {
            e.preventDefault();
            inputs[stateProperty] = false;
        }, { passive: false });
    }

    setupTouch("leftBtn", "left");
    setupTouch("rightBtn", "right");

    // Standalone click handler logic specifically designed for tactical single-tap shooting
    document.getElementById("fireBtn").addEventListener("touchstart", (e) => {
        e.preventDefault();
        if (gameOver) {
            resetGame();
            return;
        }
        bullets.push({ x: player.x + player.width / 2 - 3, y: player.y, width: 6, height: 15, speed: 9, color: "#58a6ff" });
    }, { passive: false });

    // Allow canvas tapping to reset game on death overlay screen
    canvas.addEventListener("touchstart", (e) => {
        if (gameOver) resetGame();
    });

    function spawnEnemy() {
        if (gameOver) return;
        const size = Math.random() * 15 + 20;
        const x = Math.random() * (canvas.width - size);
        enemies.push({ x: x, y: -size, width: size, height: size, speed: Math.random() * 1.5 + 1.5, color: "#f85149" });
        setTimeout(spawnEnemy, Math.max(500, 1200 - score * 6));
    }

    function resetGame() {
        score = 0;
        bullets.length = 0;
        enemies.length = 0;
        player.x = canvas.width / 2 - 20;
        gameOver = false;
        inputs.left = false;
        inputs.right = false;
        inputs.fire = false;
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
            ctx.fillText("Tap Any Control Button to Restart", canvas.width / 2, canvas.height / 2 + 20);
            return;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Core Physics Calculation Handling
        if (inputs.left && player.x > 0) player.x -= player.speed;
        if (inputs.right && player.x < canvas.width - player.width) player.x += player.speed;

        // Draw Player Rocket Ship
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(player.x + player.width / 2, player.y);
        ctx.lineTo(player.x, player.y + player.height);
        ctx.lineTo(player.x + player.width, player.y + player.height);
        ctx.closePath();
        ctx.fill();

        // Process Lasers
        for (let i = bullets.length - 1; i >= 0; i--) {
            bullets[i].y -= bullets[i].speed;
            if (bullets[i].y < 0) {
                bullets.splice(i, 1);
                continue;
            }
            ctx.fillStyle = bullets[i].color;
            ctx.fillRect(bullets[i].x, bullets[i].y, bullets[i].width, bullets[i].height);
        }

        // Process Invader Asteroids
        for (let i = enemies.length - 1; i >= 0; i--) {
            enemies[i].y += enemies[i].speed;
            
            if (enemies[i].y > canvas.height) {
                gameOver = true;
            }

            ctx.fillStyle = enemies[i].color;
            ctx.fillRect(enemies[i].x, enemies[i].y, enemies[i].width, enemies[i].height);

            // Crash Collision Boundary Checks
            if (enemies[i].x < player.x + player.width &&
                enemies[i].x + enemies[i].width > player.x &&
                enemies[i].y < player.y + player.height &&
                enemies[i].y + enemies[i].height > player.y) {
                gameOver = true;
            }

            // Target Elimination Check
            for (let j = bullets.length - 1; j >= 0; j--) {
                if (bullets[j].x < enemies[i].x + enemies[i].width &&
                    bullets[j].x + bullets[j].width > enemies[i].x &&
                    bullets[j].y < enemies[i].y + enemies[i].height &&
                    bullets[j].y + bullets[j].height > enemies[i].y) {
                    
                    enemies.splice(i, 1);
                    bullets.splice(j, 1);
                    score += 10;
                    break;
                }
            }
        }

        // UI Score Panel Rendering
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 18px sans-serif";
        ctx.textAlign = "left";
        ctx.fillText(`Score: ${score}`, 15, 30);

        requestAnimationFrame(update);
    }

    resetGame();
</script>
</body>
</html>
"""

# Render Game via Streamlit Component Engine
components.html(game_html, height=720, scrolling=False)
