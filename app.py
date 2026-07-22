import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Cop Arcade", layout="centered")
st.title("🚓 Virtua Arcade Shooter")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
        /* 1. Large Arcade Layout Viewport Container */
        #gameArea { 
            position: relative; 
            width: 380px; 
            height: 480px; 
            background: linear-gradient(to bottom, #4a777a 0%, #a1c4fd 40%, #727d8c 41%, #3a4454 100%); 
            border: 4px solid #444; 
            overflow: hidden; 
            margin: auto; 
            border-radius: 16px; 
            touch-action: none;
            box-shadow: 0 12px 32px rgba(0,0,0,0.6);
            transition: background 1s ease; /* Fluid chapter lighting shift */
        }
        
        /* 3D Pseudo Arcade Horizon Buildings & Lanes */
        .building-l { position: absolute; top: 50px; left: 0; width: 130px; height: 150px; background: repeating-linear-gradient(to bottom, #1b263b 0px, #1b263b 14px, transparent 14px, transparent 20px), #0d1b2a; z-index: 1; transition: filter 1s; }
        .building-r { position: absolute; top: 40px; right: 0; width: 110px; height: 160px; background: repeating-linear-gradient(to bottom, #14213d 0px, #14213d 10px, transparent 10px, transparent 16px), #000814; z-index: 1; transition: filter 1s; }
        .roadway { position: absolute; bottom: 0; left: 0; width: 100%; height: 280px; background: linear-gradient(to bottom, #434952, #2c3036); clip-path: polygon(42% 0%, 58% 0%, 100% 100%, 0% 100%); z-index: 2; transition: filter 1s; }
        .roadway::before { content: ''; position: absolute; top: 0; left: 50%; width: 8px; height: 100%; background: repeating-linear-gradient(to bottom, #e5e5e5 0px, #e5e5e5 25px, transparent 25px, transparent 50px); transform: translateX(-50%); opacity: 0.4; }

        /* 🚗 HIGHLY REALISTIC 3D SHADED GETAWAY SUV */
        #car {
            position: absolute; top: 175px; left: 110px; width: 160px; height: 100px;
            background: linear-gradient(to bottom, #333, #1a1a1a, #0d0d0d); border-radius: 14px 14px 4px 4px;
            box-shadow: 0 15px 25px rgba(0,0,0,0.6), inset 0 2px 4px rgba(255,255,255,0.15); z-index: 4;
            border: 1px solid #222;
            will-change: transform, left, top;
            transform-origin: center bottom;
        }
        /* Slanted rear windshield window */
        .window { 
            position: absolute; top: 10px; left: 15px; width: 130px; height: 35px; 
            background: linear-gradient(180deg, rgba(142, 202, 230, 0.6) 0%, rgba(33, 158, 188, 0.3) 70%, rgba(2, 48, 71, 0.5) 100%); 
            border-radius: 8px 8px 2px 2px; border: 2px solid #000;
            box-shadow: inset 0 5px 5px rgba(255,255,255,0.2);
        }
        /* Deep tire rendering */
        #car::before { content: ''; position: absolute; bottom: -12px; left: 15px; width: 30px; height: 15px; background: #080808; border-radius: 4px; }
        #car::after { content: ''; position: absolute; bottom: -12px; right: 15px; width: 30px; height: 15px; background: #080808; border-radius: 4px; }
        
        .light-l { position: absolute; bottom: 20px; left: 12px; width: 22px; height: 12px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; border: 1px solid #800f2f; }
        .light-r { position: absolute; bottom: 20px; right: 12px; width: 22px; height: 12px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; border: 1px solid #800f2f; }

        /* 🔫 DETAILED AUTOMATIC PISTOL DISPLAY (MATCHES PIC) */
        #weapon {
            position: absolute; bottom: -35px; right: 45px; width: 90px; height: 180px; transform: rotate(0deg); transform-origin: bottom center; pointer-events: none; z-index: 25; will-change: transform;
        }
        .w-slide { 
            position: absolute; top: 10px; left: -30px; width: 110px; height: 26px; 
            background: linear-gradient(to bottom, #2b2b2b, #151515, #222); border-radius: 4px 2px 2px 2px; border-bottom: 2px solid #0d0d0d;
            box-shadow: -4px 4px 10px rgba(0,0,0,0.5);
        }
        .w-slide::before { content: ''; position: absolute; left: -4px; top: 6px; width: 4px; height: 10px; background: #000; }
        .w-grip { 
            position: absolute; top: 34px; left: 25px; width: 34px; height: 110px; 
            background: repeating-linear-gradient(45deg, #3d2b1f, #3d2b1f 2px, #241911 2px, #241911 4px);
            border: 3px solid #0a0a0a; border-radius: 4px 6px 12px 6px; transform: rotate(-10deg); box-shadow: -6px 6px 12px rgba(0,0,0,0.6);
        }
        .w-frame { position: absolute; top: 32px; left: -15px; width: 50px; height: 25px; background: #1a1a1a; border-radius: 0 0 10px 4px; }
        .w-guard { position: absolute; top: 30px; left: -5px; width: 22px; height: 22px; border: 3px solid #1a1a1a; border-radius: 50%; }
        #flash { position: absolute; top: -10px; left: -35px; width: 35px; height: 35px; background: radial-gradient(circle, #fff 10%, #ffea00 40%, transparent 70%); border-radius: 50%; display: none; z-index: 26; }

        /* Blue Aim Crosshair Circle */
        #sight { position: absolute; top: 218px; left: 168px; width: 32px; height: 32px; border: 2px solid #00f0ff; border-radius: 50%; pointer-events: none; z-index: 20; box-shadow: 0 0 6px rgba(0,240,255,0.5); }
        #sight::before { content: ''; position: absolute; top: 15px; left: 0; width: 32px; height: 1px; background: #00f0ff; }
        #sight::after { content: ''; position: absolute; top: 0; left: 15px; width: 1px; height: 32px; background: #00f0ff; }

        /* Virtua Cop Retro Yellow Locking Target Ring */
        .target-ring { position: absolute; width: 90px; height: 90px; border: 3px dashed #ffea00; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-30px, -30px); }

        /* --- 🏃 UPGRADED REALISTIC HUMAN TARGETS --- */
        .threat { position: absolute; width: 45px; height: 75px; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; transform-origin: center bottom; }
        /* Skin tone and round head */
        .t-head { background: linear-gradient(135deg, #e0a96d, #c48b53); border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #111; position: relative; box-shadow: inset -2px -2px 3px rgba(0,0,0,0.2); }
        /* Dark hair cap overlay */
        .t-head::before { content: ''; position: absolute; top: -2px; left: -1px; width: 26px; height: 10px; background: #3d2511; border-radius: 12px 12px 0 0; }
        /* Tiny furious glowing red combat eyes */
        .t-eyes { position: absolute; top: 11px; left: 4px; width: 14px; height: 4px; display: flex; justify-content: space-between; }
        .t-eyes::before, .t-eyes::after { content: ''; width: 3.5px; height: 3.5px; background: #000; border-radius: 50%; border-top: 1px solid red; }
        /* Fabric shading jacket */
        .t-torso { background: linear-gradient(to right, #1d3557, #457b9d, #1d3557); width: 32px; height: 36px; border-radius: 4px; border: 1.5px solid #111; position: relative; }
        /* Aiming arms holding weapons */
        .t-arm { position: absolute; top: 6px; width: 26px; height: 11px; background: #1d3557; border: 1.5px solid #111; border-radius: 3px; transform-origin: right center; }
        .arm-l { left: -16px; transform: rotate(-15deg); }
        .arm-r { right: -16px; transform: rotate(15deg); transform-origin: left center; }
        .t-weapon { position: absolute; top: -2px; width: 14px; height: 11px; background: #222; border-radius: 2px; }
        .arm-l .t-weapon { left: -12px; } .arm-r .t-weapon { right: -12px; }
        /* Walking animated leg frames */
        .t-legs { display: flex; justify-content: space-around; width: 28px; height: 16px; margin-top: auto; }
        .t-leg { background: #212529; width: 9px; height: 100%; border-radius: 2px; border: 1px solid #000; animation: walkCycle 0.25s ease-in-out infinite alternate; }
        .t-leg:nth-child(2) { animation-delay: 0.12s; }
        @keyframes walkCycle { 0% { transform: translateY(0); } 100% { transform: translateY(-5px); } }

        /* Scoring and Level Panels */
        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-family: monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.7); padding: 5px 12px; border-radius: 6px; border: 1px solid #444; }
        #overScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
        .retry-btn { padding: 12px 28px; background: #e63946; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(230,57,70,0.5); }
    </style>
</head>
<body>

    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CHAPTER 1: MORNING</div>
        <div class="building-l"></div>
        <div class="building-r"></div>
        <div class="roadway"></div>
        
        <div id="car">
            <div class="window"></div>
            <div class="light-l"></div>
            <div class="light-r"></div>
        </div>

        <div id="sight"></div>
            let currentX = 168, currentY = 218, score = 200, isOver = false, activeChapter = 1;
    let carPos = 110, carDir = 1.5, distanceScale = 0.2;
    let threatsList = [];
    let audioCtx = null, spawnTimerId = null, physicsTimerId = null;

    const gameArea = document.getElementById("gameArea");
    const sight = document.getElementById("sight");
    const weapon = document.getElementById("weapon");
    const flash = document.getElementById("flash");
    const car = document.getElementById("car");
    const scoreCounter = document.getElementById("scoreCounter");
    const chapterTxt = document.getElementById("chapterTxt");
    const overScreen = document.getElementById("overScreen");
    const finalScore = document.getElementById("finalScore");

    function setupAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function sound(type) {
        setupAudio(); if (!audioCtx) return;
        let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.connect(gain); gain.connect(audioCtx.destination);
        
        if (type === "zap") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.14);
            gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.14);
        } else if (type === "ding") {
            osc.type = "sine"; osc.frequency.setValueAtTime(950, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1300, audioCtx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.08);
        } else if (type === "boom") {
            osc.type = "sawtooth"; osc.frequency.setValueAtTime(120, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(25, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.45, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.35);
        }
    }

    function aim(e) {
        if (isOver) return;
        let evt = e.touches ? e.touches[0] : e;
        let bounds = gameArea.getBoundingClientRect();
        
        currentX = Math.max(-10, Math.min(350, evt.clientX - bounds.left - 16));
        currentY = Math.max(-10, Math.min(450, evt.clientY - bounds.top - 16));
        
        sight.style.left = currentX + "px";
        sight.style.top = currentY + "px";
        
        let rotationAngle = (currentX - 168) / 15;
        let horizontalShift = (currentX - 168) / 8;
        let verticalShift = (currentY - 218) / 12;
        weapon.style.transform = `rotate(${rotationAngle}deg) translateX(${horizontalShift}px) translateY(${verticalShift}px)`;
    }

    gameArea.addEventListener("mousemove", aim);
    gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });
    gameArea.addEventListener("mousedown", (e) => { if(e.target.className !== "retry-btn") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.className !== "retry-btn") { e.preventDefault(); triggerFire(); } });

    function triggerFire() {
        if (isOver) return;
        sound("zap");
        flash.style.display = "block";
        setTimeout(() => { flash.style.display = "none"; }, 60);
        
        let hitCenterX = currentX + 16;
        let hitCenterY = currentY + 16;

        threatsList.forEach((t, index) => {
            let tRect = t.el.getBoundingClientRect();
            let areaRect = gameArea.getBoundingClientRect();
            let tX = tRect.left - areaRect.left;
            let tY = tRect.top - areaRect.top;
            let tW = tRect.width;
            let tH = tRect.height;

            if (hitCenterX >= tX && hitCenterX <= tX + tW && hitCenterY >= tY && hitCenterY <= tY + tH) {
                sound("ding");
                score += 100;
                scoreCounter.innerText = String(score).padStart(5, '0');

                if (score >= 1200 && activeChapter === 2) {
                    activeChapter = 3;
                    chapterTxt.innerText = "CHAPTER 3: NIGHTTIME";
                    gameArea.style.background = "linear-gradient(to bottom, #023047 0%, #03071e 40%, #141519 41%, #0b0c10 100%)";
                    document.querySelectorAll(".building-l, .building-r, .roadway").forEach(el => el.style.filter = "brightness(0.3) contrast(1.2)");
                } else if (score >= 600 && activeChapter === 1) {
                    activeChapter = 2;
                    chapterTxt.innerText = "CHAPTER 2: DUSK TIME";
                    gameArea.style.background = "linear-gradient(to bottom, #f77f00 0%, #fcbf49 40%, #4a4e69 41%, #22223b 100%)";
                    document.querySelectorAll(".building-l, .building-r, .roadway").forEach(el => el.style.filter = "brightness(0.6) sepia(0.3)");
                }
                
                t.el.remove();
                t.ring.remove();
                threatsList.splice(index, 1);
            }
        });
    }

    function runEngineLoops() {
        // 1. Core Vehicle & Threat Pin Synchronization 3D Loop
        physicsTimerId = setInterval(() => {
            if (isOver) return;
            
            distanceScale += 0.005;
            if (distanceScale > 1.7) {
                distanceScale = 0.2;
                carPos = Math.random() * 100 + 60;
            }
            
            let currentTopY = 165 + (distanceScale * 45);
            car.style.transform = `scale(${distanceScale})`;
            car.style.left = carPos + "px";
            car.style.top = currentTopY + "px";

            threatsList.forEach((t) => {
                let updatedX = carPos + (t.sideOffset * distanceScale);
                let threatY = currentTopY + (t.baseTopY - 195) * distanceScale;
                
                t.el.style.transform = `scale(${distanceScale})`;
                t.el.style.left = updatedX + "px";
                t.el.style.top = threatY + "px";
                
                t.ring.style.width = (90 * (1.3 - (t.age / 45))) + "px";
                t.ring.style.height = (90 * (1.3 - (t.age / 45))) + "px";
                let rSize = 90 * (1.3 - (t.age / 45));
                t.ring.style.left = (updatedX + (20 * distanceScale) - (rSize / 2) + 15) + "px";
                t.ring.style.top = (threatY + (15 * distanceScale) - (rSize / 2) + 30) + "px";
                t.age += 1;
            });
        }, 30);

        // 2. High-Speed Threat Generator Clock Loop
        spawnTimerId = setInterval(() => {
            if (isOver || threatsList.length >= 2) return;

            let el = document.createElement("div");
            el.className = "threat";
            
            let roll = Math.random();
            let sideOffset, topY, armClass;
            
            if (roll < 0.25) { sideOffset = -25; topY = 185; armClass = "arm-l"; }
            else if (roll < 0.5) { sideOffset = 145; topY = 185; armClass = "arm-r"; }
            else if (roll < 0.75) { sideOffset = -15; topY = 210; armClass = "arm-l"; }
            else { sideOffset = 135; topY = 210; armClass = "arm-r"; }

            el.innerHTML = `
                <div class="t-head"><div class="t-eyes"></div></div> 
                <div class="t-torso"><div class="t-arm ${armClass}"><div class="t-weapon"></div></div></div> 
                <div class="t-legs"><div class="t-leg"></div><div class="t-leg"></div></div>`;
                
            let updatedX = carPos + (sideOffset * distanceScale);
            let threatY = (165 + (distanceScale * 45)) + (topY - 195) * distanceScale;
            
            el.style.left = updatedX + "px";
            el.style.top = threatY + "px";
            el.style.transform = `scale(${distanceScale})`;
            gameArea.appendChild(el);

            let ring = document.createElement("div");
            ring.className = "target-ring";
            gameArea.appendChild(ring);

            let threatObj = { el: el, ring: ring, sideOffset: sideOffset, baseTopY: topY, age: 0 };
            threatsList.push(threatObj);

            setTimeout(() => {
                if (!isOver && el.parentNode) {
                    isOver = true;
                    sound("boom");
                    clearInterval(spawnTimerId);
                    clearInterval(physicsTimerId);
                    finalScore.innerText = "Final Arcade Score: " + score;
                    overScreen.style.display = "flex";
                }
            }, 1400);
        }, 1200);
    }

    window.resetArcadeEngine = function() {
        clearInterval(spawnTimerId);
        clearInterval(physicsTimerId);
        
        threatsList.forEach(t => { t.el.remove(); t.ring.remove(); });
        threatsList = [];
        
        score = 200; isOver = false; carPos = 110; distanceScale = 0.2; activeChapter = 1;
        scoreCounter.innerText = "00200";
        chapterTxt.innerText = "CHAPTER 1: MORNING";
        gameArea.style.background = "linear-gradient(to bottom, #4a777a 0%, #a1c4fd 40%, #727d8c 41%, #3a4454 100%)";
        document.querySelectorAll(".building-l, .building-r, .roadway").forEach(el => el.style.filter = "none");
        
        sight.style.left = "168px"; sight.style.top = "218px";
        weapon.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
        overScreen.style.display = "none";
        
        runEngineLoops();
    };

    runEngineLoops();
</script>
</body>
</html>
"""

components.html(game_html, height=560)
