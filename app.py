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

<div id="gameContainer" style="position:relative; width:95vw; max-width:400px; height:55vh; max-height:450px; background:#000000; border:2px solid #30363d; border-radius:8px; overflow:hidden;">
    <!-- Main Interactive Surface -->
    <div id="gameBoard" style="position:relative; width:100%; height:100%;">
        <!-- Rocket Ship Entity Layer -->
        <div id="playerShip" style="position:absolute; bottom:20px; left:180px; width:40px; height:40px; background:#238636; clip-path:polygon(50% 0%, 0% 100%, 100% 100%); display:none;"></div>
        
        <!-- Interactive Start Overlay Panel -->
        <div id="menuScreen" onclick="startGame()" style="position:absolute; top:0; left:0; width:100%; height:100%; background:#21262d; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#ffffff; font-weight:bold; cursor:pointer; font-size:20px; z-index:100;">
            <span style="color:#58a6ff; margin-bottom:15px;">SPACE SHOOTER</span>
            <span style="font-size:14px; background:#238636; padding:10px 15px; border-radius:4px;">CLICK HERE TO PLAY</span>
        </div>
    </div>
</div>



<div id="controls">
    <div class="nav-cluster">
        <div id="leftBtn" class="btn">◀</div>
        <div id="rightBtn" class="btn">▶</div>
    </div>
    <div id="fireBtn" class="btn">FIRE</div>
</div>

    let playerX = 180;
    const board = document.getElementById("gameBoard");
    const ship = document.getElementById("playerShip");
    const menu = document.getElementById("menuScreen");

    // Click handler embedded at root window scope level to bypass iframe blocking
    window.startGame = function() {
        menu.style.display = "none";
        ship.style.display = "block";
        spawnLoop();
    };

    // Responsive Action Handlers
    window.movePlayer = function(direction) {
        if (direction === 'left' && playerX > 10) playerX -= 25;
        if (direction === 'right' && playerX < (board.clientWidth - 50)) playerX += 25;
        ship.style.left = playerX + "px";
    };

    window.fireBullet = function() {
        const bullet = document.createElement("div");
        bullet.style.cssText = `position:absolute; bottom:60px; left:${playerX + 17}px; width:6px; height:15px; background:#58a6ff; border-radius:2px;`;
        board.appendChild(bullet);

        // Standard CSS transition manipulation bypasses game animation lag
        let currentBottom = 60;
        const bInterval = setInterval(() => {
            currentBottom += 8;
            bullet.style.bottom = currentBottom + "px";
            if (currentBottom > board.clientHeight) {
                clearInterval(bInterval);
                bullet.remove();
            }
        }, 1000 / 60);
    };

    function spawnLoop() {
        setInterval(() => {
            const enemy = document.createElement("div");
            const randomX = Math.random() * (board.clientWidth - 40);
            enemy.style.cssText = `position:absolute; top:0px; left:${randomX}px; width:30px; height:30px; background:#f85149; border-radius:4px;`;
            board.appendChild(enemy);

            let currentTop = 0;
            const eInterval = setInterval(() => {
                currentTop += 3;
                enemy.style.top = currentTop + "px";
                if (currentTop > board.clientHeight) {
                    clearInterval(eInterval);
                    enemy.remove();
                }
            }, 1000 / 60);
        }, 1200);
    }

    // Connect standard hardware buttons up dynamically
    document.getElementById("leftBtn").addEventListener("touchstart", (e) => { e.preventDefault(); movePlayer('left'); });
    document.getElementById("rightBtn").addEventListener("touchstart", (e) => { e.preventDefault(); movePlayer('right'); });
    document.getElementById("fireBtn").addEventListener("touchstart", (e) => { e.preventDefault(); fireBullet(); });



"""

_, center_column, _ = st.columns([1, 4, 1])

with center_column:
    components.html(game_html, height=900, scrolling=False)
