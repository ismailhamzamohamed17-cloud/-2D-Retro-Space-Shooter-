import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtua Tactical: 3D Special Ops", layout="centered")
st.title("⚡ Virtua Tactical: WebGL 3D Operations")

game_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; user-select: none; -webkit-user-select: none; background: #010409; overflow: hidden; }
        
        #gameArea { 
            position: relative; width: 380px; height: 480px; 
            background: #05070a; border: 4px solid #1a1f26; overflow: hidden; margin: auto; border-radius: 16px; touch-action: none;
            box-shadow: 0 24px 60px rgba(0,0,0,0.9);
        }

        /* 🎬 3D CINEMATIC GRAPHICS SHADER FILTERS */
        #gameArea::after {
            content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 28;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://w3.org id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.045'/%3E%3C/svg%3E");
            background-size: auto;
            box-shadow: inset 0 0 70px rgba(0, 0, 0, 0.9), inset 0 0 130px rgba(0, 0, 0, 0.8);
            background-color: rgba(220, 20, 20, 0);
            transition: box-shadow 0.1s ease-out, background-color 0.1s ease-out;
        }

        #gameArea.taking-damage::after {
            background-color: rgba(220, 20, 20, 0.25);
            box-shadow: inset 0 0 110px rgba(220, 20, 20, 0.95), inset 0 0 180px rgba(180, 0, 0, 0.95);
        }
        #gameArea.critical-pulse::after { animation: wholeScreenLowHpPulse 0.55s ease-in-out infinite alternate; }
        @keyframes wholeScreenLowHpPulse {
            0% { background-color: rgba(220, 20, 20, 0.05); box-shadow: inset 0 0 85px rgba(160, 0, 0, 0.7); }
            100% { background-color: rgba(220, 20, 20, 0.25); box-shadow: inset 0 0 115px rgba(240, 0, 0, 0.95), inset 0 0 170px rgba(200, 0, 0, 0.85); }
        }

        /* 🎮 HARDWARE ACCELERATED WEBGL THREE.JS CANVAS TARGET */
        #webglCanvas { position: absolute; width: 100%; height: 100%; top: 0; left: 0; z-index: 1; }
        #weapon { position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%) scale(1.1); width: 100px; height: 160px; pointer-events: none; z-index: 25; will-change: transform; }
        .w-slide { position: absolute; top: 40px; left: 24px; width: 52px; height: 50px; background: linear-gradient(to right, #111 0%, #2a2a2a 30%, #0d0d0d 50%, #2a2a2a 70%, #111 100%); border-radius: 6px 6px 2px 2px; border-top: 1px solid #444; box-shadow: 0 12px 25px rgba(0,0,0,0.8), inset 0 2px 3px rgba(255,255,255,0.1); }
        .w-holo-sight { position: absolute; top: 2px; left: 29px; width: 42px; height: 38px; border: 3.5px solid #1c1c1c; border-bottom: none; border-radius: 6px 6px 0 0; background: linear-gradient(to bottom, rgba(0,240,255,0.1), rgba(0,240,255,0.02)); box-shadow: inset 0 0 8px rgba(0,240,255,0.15); }
        .w-holo-sight::after { content: ''; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: #ff003c; border-radius: 50%; box-shadow: 0 0 10px 2px #ff003c; }
        .w-grip-back { position: absolute; top: 90px; left: 32px; width: 36px; height: 70px; background: linear-gradient(to right, #0a0a0a, #1a1a1a, #050505); border-radius: 3px; }
        #flash { position: absolute; top: 15px; left: 30px; width: 40px; height: 40px; background: radial-gradient(circle, #ffffff 15%, #ff3c00 60%, transparent 80%); border-radius: 50%; display: none; z-index: 26; filter: drop-shadow(0 0 10px #ff3c00); }

        /* 🎯 RETICLE INTERFACES & THREAT DANGER RING OVERLAYS */
        .target-ring { position: absolute; border: 3px dashed #ff2222; border-radius: 50%; pointer-events: none; z-index: 10; transform: translate(-50%, -50%); display: block; box-shadow: 0 0 10px #ff2222; transition: width 0.03s, height 0.03s; }
        #sight { position: absolute; width: 32px; height: 32px; border: 2px solid #00ffff; border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); z-index: 20; box-shadow: 0 0 8px #00ffff; display: none; }

        #scoreCounter { position: absolute; top: 12px; left: 12px; color: #ffea00; font-weight: bold; font-family: 'Courier New', monospace; font-size: 22px; z-index: 30; background: rgba(0,0,0,0.85); padding: 4px 14px; border-radius: 6px; border: 2px solid #444; text-shadow: 0 0 5px #ffea00; }
        #chapterTxt { position: absolute; top: 12px; right: 12px; color: white; font-weight: bold; font-size: 11px; z-index: 30; background: rgba(0,0,0,0.85); padding: 6px 12px; border-radius: 6px; border: 1px solid #444; letter-spacing: 1px; }
        #targetTracker { position: absolute; top: 52px; right: 12px; color: #ff3333; font-weight: bold; font-family: monospace; font-size: 12px; z-index: 30; background: rgba(0,0,0,0.85); padding: 3px 8px; border-radius: 4px; }
        #healthCounter { position: absolute; bottom: 12px; left: 12px; color: #ff3333; font-weight: bold; font-family: 'Courier New', monospace; font-size: 16px; z-index: 30; background: rgba(0,0,0,0.9); padding: 5px 12px; border-radius: 4px; border: 2px solid #ff2222; text-shadow: 0 0 4px #ff0000; }

        #overScreen, #winScreen, #intermissionScreen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 40; }
        #overScreen { background: rgba(0,0,0,0.95); } #intermissionScreen { background: rgba(0,0,0,0.85); } #winScreen { background: linear-gradient(135deg, rgba(10,20,35,0.95), rgba(25,40,65,0.95)); }
        .retry-btn { padding: 12px 28px; background: #b01a25; color: white; font-size: 15px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(176,26,37,0.5); }
        .win-btn { padding: 12px 28px; background: #ffea00; color: #000; font-size: 15px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-top: 20px; box-shadow: 0 4px 12px rgba(255,234,0,0.5); }
        .intermission-title { color: #ffea00; font-size: 26px; font-weight: bold; text-shadow: 0 0 12px #ffea00; text-align: center; }
    </style>
    <!-- 🌐 LOAD CORE HARDWARE-ACCELERATED THREE.JS WEBGL LIBRARIES -->
    <script src="https://cloudflare.com"></script>
</head>
<body>
    <div id="gameArea">
        <div id="scoreCounter">00200</div>
        <div id="chapterTxt">CH 1: 3D CONTAINER PORT</div>
        <div id="targetTracker">SECTOR A: 0/3</div>
        <div id="healthCounter">HP: 100</div>
        
        <!-- Three.js renders inside this hardware wrapper window -->
        <div id="webglCanvas"></div>
        
        <div id="sight"></div>
        <div id="weapon">
            <div id="flash"></div> <div class="w-slide"></div> <div class="w-holo-sight"></div> <div class="w-grip-back"></div>
        </div>

        <div id="overScreen">
            <div style="color:#b01a25; font-size:32px; font-weight:bold; text-shadow:0 0 10px #000; font-family:monospace; letter-spacing:1px;">MISSION FAILURE</div>
            <div id="finalScore" style="color:white; font-size:16px; margin-top:10px;">Final Operation Score: 200</div>
            <button class="retry-btn" onclick="resetArcadeEngine(true)">RETRY MISSION 🔄</button>
        </div>

        <div id="intermissionScreen">
            <div class="intermission-title">CAMPAIGN ACCOMPLISHED! 🎉</div>
            <button class="win-btn" onclick="resetArcadeEngine(true)">PLAY AGAIN 🎮</button>
        </div>
    </div>

<script>
    let currentX = 190, currentY = 240, score = 200, isOver = false;
    let threatsList = []; let playerHp = 100;
    let audioCtx = null, spawnTimerId = null, heartbeatIntervalId = null;

    let currentSector = "A"; let sectorKills = 0;
    const sectorRequirements = { "A": 3, "B": 3, "C": 4 };

    // --- 🌐 THREE.JS ENGINE CORE GRAPHICS HOOKS ---
    let scene, camera, renderer;
    let warehouseTunnel, cameraTargetZ = 5, cameraTargetX = 0;

    const gameArea = document.getElementById("gameArea"), sight = document.getElementById("sight"), weapon = document.getElementById("weapon"), flash = document.getElementById("flash"), scoreCounter = document.getElementById("scoreCounter"), chapterTxt = document.getElementById("chapterTxt"), targetTracker = document.getElementById("targetTracker"), healthCounter = document.getElementById("healthCounter"), overScreen = document.getElementById("overScreen"), intermissionScreen = document.getElementById("intermissionScreen"), finalScore = document.getElementById("finalScore");

    function setupAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
    
    function sound(type) {
        setupAudio(); if (!audioCtx) return; let osc = audioCtx.createOscillator(), gain = audioCtx.createGain(); osc.connect(gain); gain.connect(audioCtx.destination);
        if (type === "zap") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(540, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(45, audioCtx.currentTime + 0.15); gain.gain.setValueAtTime(0.4, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.15); }
        else if (type === "ding") { osc.type = "sine"; osc.frequency.setValueAtTime(950, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(1350, audioCtx.currentTime + 0.08); gain.gain.setValueAtTime(0.2, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.08); }
        else if (type === "boom") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(110, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.38); gain.gain.setValueAtTime(0.5, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.38); }
        else if (type === "level") { osc.type = "sine"; osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2); gain.gain.setValueAtTime(0.25, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.4); }
        else if (type === "bullet_crack") { osc.type = "sawtooth"; osc.frequency.setValueAtTime(190, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(30, audioCtx.currentTime + 0.12); gain.gain.setValueAtTime(0.3, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.12); }
        else if (type === "heartbeat") { osc.type = "sine"; osc.frequency.setValueAtTime(60, audioCtx.currentTime); osc.frequency.exponentialRampToValueAtTime(25, audioCtx.currentTime + 0.18); gain.gain.setValueAtTime(0.45, audioCtx.currentTime); osc.start(); osc.stop(audioCtx.currentTime + 0.18); }
    }
    function aim(e) {
        if (isOver || intermissionScreen.style.display === "flex") return;
        let evt = e; if (e.touches && e.touches.length > 0) { evt = e.touches[0]; } else if (e.changedTouches && e.changedTouches.length > 0) { evt = e.changedTouches[0]; }
        let bounds = gameArea.getBoundingClientRect();
        currentX = evt.clientX - bounds.left; currentY = evt.clientY - bounds.top;
        
        sight.style.display = "block"; sight.style.left = currentX + "px"; sight.style.top = currentY + "px";
        let swayX = (currentX - 190) / 10; let swayY = (currentY - 240) / 12;
        weapon.style.transform = "translateX(-50%) scale(1.1) rotate(" + swayX + "deg) translateY(" + swayY + "px)";
    }
    gameArea.addEventListener("mousemove", aim); gameArea.addEventListener("touchmove", (e) => { e.preventDefault(); aim(e); }, { passive: false });
    gameArea.addEventListener("mousedown", (e) => { if(e.target.tagName !== "BUTTON") triggerFire(); });
    gameArea.addEventListener("touchstart", (e) => { if(e.target.tagName !== "BUTTON") { e.preventDefault(); aim(e); triggerFire(); } }, { passive: false });

    // --- 📦 BUILD REALSITIC POLYGONAL 3D ENVIRONMENT ---
    function init3DWorld() {
        const container = document.getElementById("webglCanvas");
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x0a0f1d, 0.04); // Adds realistic atmospheric distance fog

        camera = new THREE.PerspectiveCamera(65, 380 / 480, 0.1, 1000);
        camera.position.set(0, 1.6, 5); // Aligns camera to true human eye height (1.6m)

        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
        renderer.setSize(380, 480); renderer.setClearColor(0x0a0f1d);
        container.appendChild(renderer.domElement);

        // Add 3D Lighting Lamps
        const ambientLight = new THREE.AmbientLight(0x1e293b, 1.2); scene.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0x38bdf8, 1.5); directionalLight.position.set(5, 10, 7); scene.add(directionalLight);

        // Build Volumetric Corridor Tunnel (Floor, Ceiling, Walls)
        warehouseTunnel = new THREE.Group();
        
        // Floor Plane
        const floorGeo = new THREE.PlaneGeometry(16, 120);
        const floorMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.6 });
        const floor = new THREE.Mesh(floorGeo, floorMat); floor.rotation.x = -Math.PI / 2; floor.position.z = -50;
        warehouseTunnel.add(floor);

        // Left Cargo Wall Structure
        const wallGeo = new THREE.PlaneGeometry(120, 8);
        const leftWallMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 });
        const leftWall = new THREE.Mesh(wallGeo, leftWallMat); leftWall.rotation.y = Math.PI / 2; leftWall.position.set(-4, 4, -50);
        warehouseTunnel.add(leftWall);

        // Right Cargo Wall Structure
        const rightWall = new THREE.Mesh(wallGeo, leftWallMat); rightWall.rotation.y = -Math.PI / 2; rightWall.position.set(4, 4, -50);
        warehouseTunnel.add(rightWall);

        // Add 3D Shipping Cargo Boxes down the hall acting as ambush cover barriers
        const boxGeo = new THREE.BoxGeometry(2, 2, 3);
        const boxMat = new THREE.MeshStandardMaterial({ color: 0x7c2d12, roughness: 0.5 }); // Industrial rust brown
        
        let barricadePositions = [ {x:-2.2, z:-4}, {x:2.2, z:-14}, {x:-2.0, z:-24} ];
        barricadePositions.forEach(pos => {
            let box = new THREE.Mesh(boxGeo, boxMat); box.position.set(pos.x, 1, pos.z);
            warehouseTunnel.add(box);
        });

        scene.add(warehouseTunnel);
        animate3DRenderLoop();
    }
    function animate3DRenderLoop() {
        if (isOver) return;
        requestAnimationFrame(animate3DRenderLoop);

        // --- 🎬 SMOOTH 3D RAIL-CAM RUNNING ANIMATION LOOP ---
        // Lerps camera smoothly through 3D polygon space toward next sector targets
        camera.position.z += (cameraTargetZ - camera.position.z) * 0.06;
        camera.position.x += (cameraTargetX - camera.position.x) * 0.06;

        // Process active 3D infantry behavioral tracking adjustments
        threatsList.forEach(t => {
            if (t.isDying) {
                t.mesh.rotation.z += 0.1; t.mesh.position.y -= 0.08; // 3D Fall animation
                return;
            }
            
            // Auto fire routines with muzzle flash indicators
            t.age++;
            if (t.age % 40 === 0) {
                triggerEnemyDamageStrike();
                t.flashMesh.visible = true;
                setTimeout(() => { t.flashMesh.visible = false; }, 70);
            }

            // Project 3D vector screen markers onto flat 2D display HTML layout for ring tracking
            let vector = t.mesh.position.clone().project(camera);
            let screenX = (vector.x * 190) + 190;
            let screenY = -(vector.y * 240) + 240;
            
            t.ring.style.left = screenX + "px"; t.ring.style.top = screenY + "px";
            let scaleRadius = Math.max(0, 95 * (1.2 - (t.age / 45)));
            t.ring.style.width = scaleRadius + "px"; t.ring.style.height = scaleRadius + "px";
        });

        renderer.render(scene, camera);
    }

    function spawn3DThreatUnit() {
        let maxSimultaneous = 2;
        if (isOver || threatsList.length >= maxSimultaneous) return;

        // Create 3D Volumetric Soldier Group Mesh (Polygonal blocks instead of flat sprites)
        const soldierGroup = new THREE.Group();
        
        // Torso Cube
        const torsoGeo = new THREE.BoxGeometry(0.6, 0.9, 0.4);
        const camoMat = new THREE.MeshStandardMaterial({ color: 0x14532d }); // Military Forest Green
        const torso = new THREE.Mesh(torsoGeo, camoMat); torso.position.y = 0.45; soldierGroup.add(torso);
        
        // Head Sphere
        const headGeo = new THREE.SphereGeometry(0.22, 16, 16);
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xcdba96 });
        const head = new THREE.Mesh(headGeo, skinMat); head.position.y = 1.05; soldierGroup.add(head);

        // SMG Barrel Cylinder
        const gunGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.6);
        const gunMat = new THREE.MeshStandardMaterial({ color: 0x111111 });
        const gun = new THREE.Mesh(gunGeo, gunMat); gun.rotation.x = Math.PI / 2; gun.position.set(0.2, 0.4, 0.4);
        soldierGroup.add(gun);

        // 3D Muzzle Flash Ring Spark
        const flashGeo = new THREE.SphereGeometry(0.15, 8, 8);
        const flashMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 });
        const flashMesh = new THREE.Mesh(flashGeo, flashMat); flashMesh.position.set(0.2, 0.4, 0.7);
        flashMesh.visible = false; soldierGroup.add(flashMesh);

        // Calculate 3D spawn coordinates based on active rail camera zone sector
        let spawnZ = -5; let spawnX = 0;
        if (currentSector === "A") { spawnZ = -3.5; spawnX = -1.2; }
        else if (currentSector === "B") { spawnZ = -13.5; spawnX = 1.4; }
        else if (currentSector === "C") { spawnZ = -23.5; spawnX = -1.0; }

        soldierGroup.position.set(spawnX, 0.1, spawnZ);
        scene.add(soldierGroup);

        // Build flat screen 2D fallback ring node tracker
        let ring = document.createElement("div"); ring.className = "target-ring";
        gameArea.appendChild(ring);

        let threatObj = { mesh: soldierGroup, flashMesh: flashMesh, ring: ring, age: 0, isDying: false };
        threatsList.push(threatObj);
        sound("ding");
    }
    // --- 🎬 FIXED: ADVANCED 3D VIRTUA COP SECTOR FLY-FORWARD CONTROLLER ---
    function triggerSectorPathMovement() {
        if (currentSector === "A") {
            currentSector = "B"; sectorKills = 0;
            // Camera physically flies forward 10 meters and slides right behind cover!
            cameraTargetZ = -5; cameraTargetX = 1.2;
        } else if (currentSector === "B") {
            currentSector = "C"; sectorKills = 0;
            // Camera flies deeper down the volumetric warehouse corridor!
            cameraTargetZ = -15; cameraTargetX = -1.0;
        } else if (currentSector === "C") {
            // All 3D sectors clear -> Mission Complete!
            clearInterval(spawnTimerId); isOver = true;
            intermissionScreen.style.display = "flex"; return;
        }
        let needed = sectorRequirements[currentSector];
        targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
        sound("level");
    }

    function triggerEnemyDamageStrike() {
        if (isOver) return; playerHp -= 20; if (playerHp < 0) playerHp = 0;
        healthCounter.innerText = `HP: ${playerHp}`; sound("bullet_crack");
        gameArea.classList.add("taking-damage"); setTimeout(() => gameArea.classList.remove("taking-damage"), 130);

        if (playerHp <= 20 && !heartbeatIntervalId) {
            gameArea.classList.add("critical-pulse"); heartbeatIntervalId = setInterval(() => { sound("heartbeat"); }, 550);
        }
        if (playerHp <= 0) {
            isOver = true; sound("boom"); clearInterval(spawnTimerId);
            if(heartbeatIntervalId) { clearInterval(heartbeatIntervalId); gameArea.classList.remove("critical-pulse"); heartbeatIntervalId = null; }
            finalScore.innerText = "Final Operation Score: " + score; overScreen.style.display = "flex";
        }
    }

    function triggerFire() {
        if (isOver || intermissionScreen.style.display === "flex") return;
        sound("zap"); flash.style.display = "block"; setTimeout(() => { flash.style.display = "none"; }, 60);

        // Project raycaster traces from 2D screen mouse pixels directly into the Three.js 3D grid area
        let hitTarget = null;
        let lowestDistance = Infinity;

        threatsList.forEach((t) => {
            if (t.isDying) return;
            let ringRect = t.ring.getBoundingClientRect();
            let areaRect = gameArea.getBoundingClientRect();
            let rX = ringRect.left - areaRect.left + (ringRect.width/2);
            let rY = ringRect.top - areaRect.top + (ringRect.height/2);

            let clickDist = Math.hypot(currentX - rX, currentY - rY);
            if (clickDist < 35 && clickDist < lowestDistance) { lowestDistance = clickDist; hitTarget = t; }
        });

        if (hitTarget) {
            hitTarget.isDying = true; sound("shout_aaa");
            score += 100; scoreCounter.innerText = String(score).padStart(5, '0');
            sectorKills += 1;
            
            let needed = sectorRequirements[currentSector];
            targetTracker.innerText = `SECTOR ${currentSector}: ${sectorKills}/${needed}`;
            
            setTimeout(() => { scene.remove(hitTarget.mesh); hitTarget.ring.remove(); }, 600);

            if (sectorKills >= needed) {
                document.querySelectorAll(".target-ring").forEach(el => el.remove());
                threatsList.forEach(t => scene.remove(t.mesh)); threatsList = [];
                setTimeout(triggerSectorPathMovement, 500);
            }
        }
    }

    window.resetArcadeEngine = function(fullReset) {
        location.reload(); // Instantly clears WebGL textures and state hooks
    };

    // Initialize the Three.js viewport pipeline
    init3DWorld();
    spawnTimerId = setInterval(spawn3DThreatUnit, 1200);
</script>
</body>
</html>
'''

st.markdown('<div class="cab">', unsafe_allow_html=True)
components.html(game_html, height=560, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)
