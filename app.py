import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Space Shooter", layout="centered")
st.title("🚀 Micro Space Shooter")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        #board { position: relative; width: 320px; height: 350px; background: black; border: 3px solid #333; overflow: hidden; margin: auto; }
        #ship { position: absolute; bottom: 10px; left: 140px; width: 40px; height: 40px; background: lime; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); }
        .btn { padding: 15px 25px; font-size: 18px; margin: 5px; background: #222; color: white; border-radius: 8px; border: 1px solid #555; }
        #fire { background: red; }
    </style>
</head>
<body>

    <div id="board">
        <div id="ship"></div>
    </div>

    <div style="text-align: center; margin-top: 15px;">
        <button class="btn" onclick="move(-20)">◀ Left</button>
        <button class="btn" onclick="move(20)">Right ▶</button>
        <button class="btn" id="fire" onclick="shoot()">FIRE</button>
    </div>

<script>
    let shipX = 140;
    const board = document.getElementById("board");
    const ship = document.getElementById("ship");

    function move(dir) {
        shipX = Math.max(0, Math.min(280, shipX + dir));
        ship.style.left = shipX + "px";
    }

    function shoot() {
        let b = document.createElement("div");
        b.style.cssText = "position:absolute; bottom:50px; left:"+(shipX+17)+"px; width:6px; height:15px; background:cyan;";
        board.appendChild(b);
        let bY = 50;
        let bInt = setInterval(() => {
            bY += 8; b.style.bottom = bY + "px";
            if(bY > 350) { clearInterval(bInt); b.remove(); }
        }, 20);
    }

    setInterval(() => {
        let e = document.createElement("div");
        e.style.cssText = "position:absolute; top:0px; left:"+Math.random()*290+"px; width:25px; height:25px; background:red; border-radius:4px;";
        board.appendChild(e);
        let eY = 0;
        let eInt = setInterval(() => {
            eY += 3; e.style.top = eY + "px";
            if(eY > 350) { clearInterval(eInt); e.remove(); }
        }, 20);
    }, 1500);
</script>
</body>
</html>
"""

components.html(game_html, height=500)
