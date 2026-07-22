import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Cop: 20 Chapters", layout="centered")
st.title("🚓 Virtua Arcade: Campaign Mode")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; }
        
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
            transition: background 0.8s ease;
        }
        
        .building-l { position: absolute; top: 50px; left: 0; width: 130px; height: 150px; background: repeating-linear-gradient(to bottom, #1b263b 0px, #1b263b 14px, transparent 14px, transparent 20px), #0d1b2a; z-index: 1; transition: filter 0.8s; }
        .building-r { position: absolute; top: 40px; right: 0; width: 110px; height: 160px; background: repeating-linear-gradient(to bottom, #14213d 0px, #14213d 10px, transparent 10px, transparent 16px), #000814; z-index: 1; transition: filter 0.8s; }
        .roadway { position: absolute; bottom: 0; left: 0; width: 100%; height: 280px; background: linear-gradient(to bottom, #434952, #2c3036); clip-path: polygon(42% 0%, 58% 0%, 100% 100%, 0% 100%); z-index: 2; transition: filter 0.8s; }
        .roadway::before { content: ''; position: absolute; top: 0; left: 50%; width: 8px; height: 100%; background: repeating-linear-gradient(to bottom, #e5e5e5 0px, #e5e5e5 25px, transparent 25px, transparent 50px); transform: translateX(-50%); opacity: 0.4; }

        #car {
            position: absolute; top: 175px; left: 110px; width: 160px; height: 105px;
            background: linear-gradient(to bottom, #2c2c2c, #151515, #0a0a0a); border-radius: 14px 14px 6px 6px;
            box-shadow: 0 15px 25px rgba(0,0,0,0.6), inset 0 2px 4px rgba(255,255,255,0.15); z-index: 4;
            border: 1px solid #1c1c1c;
            will-change: transform, left, top;
            transform-origin: center bottom;
        }
        .window { 
            position: absolute; top: 12px; left: 15px; width: 130px; height: 35px; 
            background: linear-gradient(180deg, rgba(142, 202, 230, 0.6) 0%, rgba(33, 158, 188, 0.3) 70%, rgba(2, 48, 71, 0.5) 100%); 
            border-radius: 8px 8px 2px 2px; border: 2px solid #000;
        }
        .wheel { position: absolute; background: #080808; border-radius: 4px; box-shadow: inset 0 0 6px #000; border: 1px solid #1a1a1a; }
        .w-front-l { bottom: 12px; left: -8px; width: 10px; height: 26px; transform: rotate(-5deg); }
        .w-front-r { bottom: 12px; right: -8px; width: 10px; height: 26px; transform: rotate(5deg); }
        .w-rear-l { bottom: -12px; left: 16px; width: 32px; height: 16px; }
        .w-rear-r { bottom: -12px; right: 16px; width: 32px; height: 16px; }
        
        .light-l { position: absolute; bottom: 22px; left: 12px; width: 22px; height: 12px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; }
        .light-r { position: absolute; bottom: 22px; right: 12px; width: 22px; height: 12px; background: radial-gradient(circle, #ff4d6d, #c9184a); border-radius: 3px; box-shadow: 0 0 12px #ff4d6d; border: 1px solid #800f2f; }

        #weapon {
            position: absolute; bottom: -35px; right: 45px; width: 90px; height: 180px; transform: rotate(0deg); transform-origin: bottom center; pointer-events: none; z-index: 25; will-change: transform;
        }
        .w-slide { position: absolute; top: 10px; left: -30px; width: 110px; height: 26px; background: linear-gradient(to bottom, #2b2b2b, #151515, #222); border-radius: 4px 2px 2px 2px; border-bottom: 2px solid #0d0d0d; box-shadow: -4px 4px 10px rgba(0,0,0,0.5); }
        .w-grip { position: absolute; top: 34px; left: 25px; width: 34px; height: 110px; background: repeating-linear-gradient(45deg, #3d2b1f, #3d2b1f 2px, #241911 2px, #241911 4px); border: 3px solid #0a0a0a; border-radius: 4px 6px 12px 6px; transform: rotate(-10deg); }
        .w-frame { position: absolute; top: 32px; left: -15px; width: 50px; height: 25px; background: #1a1a1a; border-radius: 0 0 10px 4px; }
        .w-guard { position: absolute; top: 30px; left: -5px; width: 22px; height: 22px; border: 3px solid #1a1a1a; border-radius: 50%; }
        #flash { position: absolute; top: -10px; left: -35px; width: 35px; height: 35px; background: radial-gradient(circle, #fff 10%, #ffea00 40%, transparent 70%); border-radius: 50%; display: none; z-index: 26; }

        #sight { position: absolute; top: 218px; left: 168px; width: 32px; height: 32px; border: 2px solid #00f0ff; border-radius: 50%; pointer-events: none; z-index: 20; box-shadow: 0 0 6px rgba(0,240,255,0.5); }
        #sight::before { content: ''; position: absolute; top: 15px; left: 0; width: 32px; height: 1px; background: #00f0ff; }
        #sight::after { content: ''; position: absolute; top: 0; left: 15px; width: 1px; height: 32px; background: #00f0ff; }

        .target-ring { position: absolute; width: 90px; height: 90px; border: 3px dashed #ffea00; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-30px, -30px); }

        .threat { position: absolute; width: 45px; height: 75px; z-index: 5; pointer-events: none; display: flex; flex-direction: column; align-items: center; transform-origin: center bottom; transition: transform 0.4s ease-out, top 0.4s ease-out, opacity 0.4s ease-out; }
        .t-head { background: linear-gradient(135deg, #e0a96d, #c48b53); border-radius: 50%; width: 24px; height: 24px; border: 1.5px solid #111; position: relative; }
        .t-head::before { content: ''; position: absolute; top: -2px; left: -1px; width: 26px; height: 10px; background: #3d2511; border-radius: 12px 12px 0 0; }
        .t-eyes { position: absolute; top: 11px; left: 4px; width: 14px; height: 4px; display: flex; justify-content: space-between; }
        .t-eyes::before, .t-eyes::after { content: ''; width: 3.5px; height: 3.5px; background: #000; border-radius: 50%; border-top: 1px solid red; }
        .t-torso { background: linear-gradient(to right, #1d3557, #457b9d, #1d3557); width: 32px; height: 36px; border-radius: 4px; border: 1.5px solid #111; position: relative; }
        .t-arm { position: absolute; top: 6px; width: 26px; height: 11px; background: #1d3557; border: 1.5px solid #111; border-radius: 3px; transform-origin: right center; }
        .arm-l { left: -16px; transform: rotate(-15deg); }
        .arm-r { right: -16px; transform: rotate(15deg); transform-origin: left center; }
        .t-weapon { position: absolute; top: -2px; width: 14px; height: 11px; background: #222; border-radius: 2px; }
        .arm-l .t-weapon { left: -12px; } .arm-r .t-weapon { right: -12px; }
        .t-legs { display: flex; justify-content: space-around; width: 28px; height: 16px; margin-top: auto; }
        .t-leg { background: #212529; width: 9px; height: 100%; border-radius: 2px; border: 1px solid #000; animation: walkCycle 0.25s ease-in-out infinite alternate; }
        .t-leg:nth-child(2) { animation-delay: 0.12s; }
        @keyframes walkCycle { 0% { transform: translateY(0); } 100% { transform: translateY(-5px); } }

        .blood-drop {
            position: absolute; width: 4px; height: 4px; background: #ba000d; border-radius: 50%; z-index: 12; pointer-events: none;
            animation: explodeBlood 0.35s ease-out forwards;
        }
        @keyframes explodeBlood {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(var(--vx), var(--vy)) scale(0.3); opacity: 0; }
        }

        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-family: monospace; font-size: 13px; z-index: 30; background: rgba(0,0,0,0.7); padding: 5px 12px; border-radius: 6px; border: 1px solid #444; }
        #targetTracker { position: absolute; top: 50px; right: 12px; color: #ff3333; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.7); padding: 3px 8px; border-radius: 4px; }

        #overScreen, #winScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
        #overScreen { background: rgba(0,0,0,0.9); }
        #winScreen { background: linear-gradient(135deg, rgba(29,53,87,0.95), rgba(69,123,157,0.95)); }
        
        .retry-btn { padding: 12px 28px; background: #e63946; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(230,57,70,0.5); }
        .win-btn { padding: 12px 28px; background: #38b000; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(56,176,0,0.5); }
    </style>
</head>
<body>

    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CHAPTER 1/20</div>
        <div id="targetTracker">TARGETS CLEAR: 0/5</div>
        
        <div class="building-l"></div>
        <div class="building-r"></div>
        <div class="roadway"></div>
        let currentX = 168, currentY = 218, score = 200, isOver = false, activeChapter = 1;
    let carPos = 110, distanceScale = 0.2, carParked = false;
    let threatsList = [];
    let chapterKills = 0;
    let audioCtx = null, spawnTimerId = null, physicsTimerId = null;

    const gameArea = document.getElementById("gameArea");
    const sight = document.getElementById("sight");
    const weapon = document.getElementById("weapon");
    const flash = document.getElementById("flash");
    const car = document.getElementById("car");
    const scoreCounter = document.getElementById("scoreCounter");
    const chapterTxt = document.getElementById("chapterTxt");
    const targetTracker = document.getElementById("targetTracker");
    const overScreen = document.getElementById("overScreen");
    const winScreen = document.getElementById("winScreen");
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
        } else if (type === "level") {
            osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime);
            osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1);
            osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.4);
        } else if (type === "shout_aaa") {
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(290, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(220, audioCtx.currentTime + 0.25);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            osc.start(); osc.stop(audioCtx.currentTime + 0.25);
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
    gameArea.addEventListener("mousedown", (e) => { if (e.target.tagName !== "BUTTON") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if (e.target.tagName !== "BUTTON") { e.preventDefault(); triggerFire(); } });

    function updateLevelAtmosphere() {
        let maxNeeded = 5 + (activeChapter - 1) * 2;
        chapterTxt.innerText = `CHAPTER ${activeChapter}/20`;
        targetTracker.innerText = `TARGETS CLEAR: ${chapterKills}/${maxNeeded}`;
        let mod = activeChapter % 3;
        
        if (mod === 1) {
            gameArea.style.background = "linear-gradient(to bottom, #4a777a 0%, #a1c4fd 40%, #727d8c 41%, #3a4454 100%)";
            document.querySelectorAll(".building-l, .building-r, .roadway").forEach(el => el.style.filter = "none");
        } else if (mod === 2) {
            gameArea.style.background = "linear-gradient(to bottom, #f77f00 0%, #fcbf49 40%, #4a4e69 41%, #22223b 100%)";
            document.querySelectorAll(".building-l, .building-r, .roadway").forEach(el => el.style.filter = "brightness(0.6) sepia(0.3)");
        } else {
            gameArea.style.background = "linear-gradient(to bottom, #023047 0%, #03071e 40%, #141519 41%, #0b0c10 100%)";
            document.querySelectorAll(".building-l, .building-r, .roadway").forEach(el => el.style.filter = "brightness(0.35) contrast(1.2)");
        }
    }

    function spawnBloodSpit(x, y) {
        for (let i = 0; i < 8; i++) {
            let drop = document.createElement("div");
            drop.className = "blood-drop";
            drop.style.left = x + "px";
            drop.style.top = y + "px";
            
            let vx = (Math.random() * 40 - 20);
            let vy = (Math.random() * -35 - 5);
            drop.style.setProperty('--vx', vx + 'px');
            drop.style.setProperty('--vy', vy + 'px');
            gameArea.appendChild(drop);
            setTimeout(() => drop.remove(), 350);
        }
    }
     function triggerFire() {
        if (isOver) return;
        sound("zap");
        flash.style.display = "block";
        setTimeout(() => { flash.style.display = "none"; }, 60);
        
        let hitCenterX = currentX + 16;
        let hitCenterY = currentY + 16;

        threatsList.forEach((t, index) => {
            if (t.isDying) return;
            
            let tRect = t.el.getBoundingClientRect();
            let areaRect = gameArea.getBoundingClientRect();
            let tX = tRect.left - areaRect.left;
            let tY = tRect.top - areaRect.top;
            let tW = tRect.width;
            let tH = tRect.height;

            if (hitCenterX >= tX && hitCenterX <= tX + tW && hitCenterY >= tY && hitCenterY <= tY + tH) {
                t.isDying = true;
                sound("shout_aaa");
                spawnBloodSpit(hitCenterX, hitCenterY);
                
                score += 100;
                scoreCounter.innerText = String(score).padStart(5, '0');
                chapterKills += 1;
                
                let maxNeeded = 5 + (activeChapter - 1) * 2;
                targetTracker.innerText = `TARGETS CLEAR: ${chapterKills}/${maxNeeded}`;

                t.ring.remove();
                t.el.style.transform += " rotate(80deg)";
                t.el.style.top = (parseFloat(t.el.style.top) + 20) + "px";
                t.el.style.opacity = "0";

                setTimeout(() => {
                    t.el.remove();
                    threatsList = threatsList.filter(item => item !== t);
                }, 400);

                if (chapterKills >= maxNeeded) {
                    if (activeChapter >= 20) {
                        isOver = true;
                        clearInterval(spawnTimerId);
                        clearInterval(physicsTimerId);
                        winScreen.style.display = "flex";
                        return;
                    }
                    sound("level");
                    activeChapter += 1;
                    chapterKills = 0;
                    chapterTxt.innerText = "MISSION ACCOMPLISHED! 🎉";
                    setTimeout(() => {
                        updateLevelAtmosphere();
                        resetArcadeEngine(false);
                    }, 1200);
                }
            }
        });
    }

    function runEngineLoops() {
        physicsTimerId = setInterval(() => {
            if (isOver) return;
            
            if (!carParked) {
                distanceScale += 0.015;
                if (distanceScale >= 1.0) {
                    distanceScale = 1.0;
                    carParked = true;
                }
            }

            let currentTopY = 165 + (distanceScale * 45);
            car.style.transform = `scale(${distanceScale})`;
            car.style.left = carPos + "px";
            car.style.top = currentTopY + "px";

            threatsList.forEach((t) => {
                if (t.isDying) return;
                let updatedX = carPos + (t.sideOffset * distanceScale);
                let threatY = currentTopY + (t.baseTopY - 195) * distanceScale;
                
                t.el.style.transform = `scale(${distanceScale})`;
                t.el.style.left = updatedX + "px";
                t.el.style.top = threatY + "px";
                
                t.ring.style.width = (90 * (1.3 - (t.age / 40))) + "px";
                t.ring.style.height = (90 * (1.3 - (t.age / 40))) + "px";
                let rSize = 90 * (1.3 - (t.age / 40));
                t.ring.style.left = (updatedX + (20 * distanceScale) - (rSize / 2) + 15) + "px";
                t.ring.style.top = (threatY + (15 * distanceScale) - (rSize / 2) + 30) + "px";
                t.age += 1;
            });
        }, 30);

        spawnTimerId = setInterval(() => {
            if (isOver || threatsList.length >= 2 || !carParked) return;

            let el = document.createElement("div");
            el.className = "threat";
            
            let roll = Math.random();
            let sideOffset, topY, armClass;
            
            if (roll < 0.25) { sideOffset = -30; topY = 190; armClass = "arm-l"; }
            else if (roll < 0.5) { sideOffset = 150; topY = 185; armClass = "arm-r"; }
            else if (roll < 0.75) { sideOffset = -15; topY = 210; armClass = "arm-l"; }
            else { sideOffset = 130; topY = 210; armClass = "arm-r"; }

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

            let threatObj = { el: el, ring: ring, sideOffset: sideOffset, baseTopY: topY, age: 0, isDying: false };
            threatsList.push(threatObj);

            sound("ding");

            setTimeout(() => {
                if (!isOver && el.parentNode && !threatObj.isDying) {
                    isOver = true;
                    sound("boom");
                    clearInterval(spawnTimerId);
                    clearInterval(physicsTimerId);
                    finalScore.innerText = "Final Arcade Score: " + score;
                    overScreen.style.display = "flex";
                }
            }, 1400);
        }, 1100);
    }

    window.resetArcadeEngine = function(resetFullCampaign) {
        clearInterval(spawnTimerId);
        clearInterval(physicsTimerId);
        
        threatsList.forEach(t => { t.el.remove(); t.ring.remove(); });
        threatsList = [];
        
        if (resetFullCampaign) {
            score = 200;
            activeChapter = 1;
            chapterKills = 0;
            scoreCounter.innerText = "00200";
        }
        
        updateLevelAtmosphere();
        isOver = false;
        distanceScale = 0.2;
        carParked = false;
        carPos = Math.random() * 80 + 70;
        
        sight.style.left = "168px"; 
        sight.style.top = "218px";
        weapon.style.transform = "rotate(0deg) translateX(0px) translateY(0px)";
        overScreen.style.display = "none";
        winScreen.style.display = "none";
        
        runEngineLoops();
    };

    updateLevelAtmosphere();
    runEngineLoops();
</script>
</body>
</html>
"""

components.html(game_html, height=560)
