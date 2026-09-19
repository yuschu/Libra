with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove duplicate declarations inside initGlobe
# Find the initGlobe function and remove the local declarations
old_init_vars = """    async function initGlobe() {
      console.log("[ThreeJS] Starting initialization...");
      
      // Check WebGL support
      const canvas = document.getElementById("globe");
      if (!canvas) {
        throw new Error("Globe canvas not found");
      }
      
      const gl = canvas.getContext("webgl2", { antialias: true, alpha: true });
      if (!gl) {
        throw new Error("WebGL2 not supported");
      }
      console.log("[ThreeJS] WebGL2 supported:", gl.getParameter(gl.VERSION));
      console.log("[ThreeJS] Renderer:", gl.getParameter(gl.RENDERER));
      
      try {
        // ---- Scene ----
        threeScene = new THREE.Scene();
        
        // ---- Camera ----
        threeCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 50000000);
        threeCamera.position.set(0, 0, 6000000);
        
        // ---- Renderer ----
        threeRenderer = new THREE.WebGLRenderer({ 
          canvas: canvas, 
          antialias: true, 
          alpha: true,
          preserveDrawingBuffer: true
        });
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
        threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        threeRenderer.toneMapping = THREE.ACESFilmicToneMapping;
        threeRenderer.toneMappingExposure = 1.0;
        threeRenderer.setClearColor(0x000000, 1);
        
        // ---- Post-processing (Bloom) ----
        const renderPass = new THREE.RenderPass(threeScene, threeCamera);
        
        bloomPass = new THREE.UnrealBloomPass(
          new THREE.Vector2(window.innerWidth, window.innerHeight),
          1.2,   // strength
          0.3,   // radius
          0.85   // threshold
        );
        
        threeComposer = new THREE.EffectComposer(threeRenderer);
        threeComposer.addPass(renderPass);
        threeComposer.addPass(bloomPass);
        
        // ---- OrbitControls ----
        orbitControls = new THREE.OrbitControls(threeCamera, canvas);
        orbitControls.enableDamping = true;
        orbitControls.dampingFactor = 0.05;
        orbitControls.enablePan = true;
        orbitControls.enableZoom = true;
        orbitControls.enableRotate = true;
        orbitControls.autoRotate = true;
        orbitControls.autoRotateSpeed = 0.2;
        orbitControls.minDistance = 1500000;
        orbitControls.maxDistance = 30000000;
        orbitControls.target.set(0, 0, 0);
        orbitControls.update();
        
        // ---- Globe: Dark sphere + glowing wireframe ----
        // Base sphere (dark, slightly emissive)
        const globeGeometry = new THREE.SphereGeometry(1, 64, 64);
        const globeMaterial = new THREE.MeshBasicMaterial({
          color: 0x0a1628,
          transparent: true,
          opacity: 0.6,
          side: THREE.DoubleSide
        });
        globeMesh = new THREE.Mesh(globeGeometry, globeMaterial);
        threeScene.add(globeMesh);
        
        // Glowing wireframe (emissive grid lines)
        const wireGeometry = new THREE.SphereGeometry(1.005, 32, 32);
        const wireMaterial = new THREE.MeshBasicMaterial({
          color: 0x00d4ff,
          wireframe: true,
          transparent: true,
          opacity: 0.4,
          depthWrite: false
        });
        wireframeMesh = new THREE.Mesh(wireGeometry, wireMaterial);
        threeScene.add(wireframeMesh);
        
        // Outer glow sphere (for bloom effect)
        const glowGeometry = new THREE.SphereGeometry(1.02, 32, 32);
        const glowMaterial = new THREE.MeshBasicMaterial({
          color: 0x00d4ff,
          transparent: true,
          opacity: 0.15,
          side: THREE.BackSide,
          depthWrite: false
        });
        const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
        threeScene.add(glowMesh);
        
        // Point light for subtle illumination
        const pointLight = new THREE.PointLight(0x00d4ff, 0.5, 10);
        pointLight.position.set(0, 0, 5);
        threeScene.add(pointLight);
        
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x446688, 0.3);
        threeScene.add(ambientLight);
        
        // Directional light (sun-like)
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight.position.set(5, 3, 5);
        threeScene.add(dirLight);
        
        // ---- Route lines container ----
        routeLines = {};
        routeLineObjects = {};
        
        // ---- Animation loop ----
        function animate() {
          requestAnimationFrame(animate);
          
          // Auto-rotate
          if (autoRotateGlobe && !cameraFlying) {
            const now = performance.now();
            if (now - lastAutoRotateTime > 50) {
              globeMesh.rotation.y += 0.0001;
              wireframeMesh.rotation.y += 0.0001;
              Object.values(routeLineObjects).forEach(obj => obj.rotation.y += 0.0001);
              lastAutoRotateTime = now;
            }
          }
          
          orbitControls.update();
          
          // Render with bloom
          threeComposer.render();
        }
        
        animate();
        
        // Handle resize
        window.addEventListener(\"resize\", onWindowResize);
        
        // Click handler for route segments
        canvas.addEventListener(\"click\", onGlobeClick);
        
        // Road select handler
        document.getElementById(\"roadSelect\").addEventListener(\"change\", (e) => {
          selectedRoadId = e.target.value;
          updateFrame(currentFrame);
          fetchAccidents();
          fetchVehicleTypes();
          renderHeatmap();
        });"""
        
# Keep the same but remove the duplicate variable declarations
# The variables are already declared at module level
new_init_vars = """    async function initGlobe() {
      console.log("[ThreeJS] Starting initialization...");
      
      // Check WebGL support
      const canvas = document.getElementById("globe");
      if (!canvas) {
        throw new Error("Globe canvas not found");
      }
      
      const gl = canvas.getContext("webgl2", { antialias: true, alpha: true });
      if (!gl) {
        throw new Error("WebGL2 not supported");
      }
      console.log("[ThreeJS] WebGL2 supported:", gl.getParameter(gl.VERSION));
      console.log("[ThreeJS] Renderer:", gl.getParameter(gl.RENDERER));
      
      try {
        // ---- Scene ----
        threeScene = new THREE.Scene();
        
        // ---- Camera ----
        threeCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 50000000);
        threeCamera.position.set(0, 0, 6000000);
        
        // ---- Renderer ----
        threeRenderer = new THREE.WebGLRenderer({ 
          canvas: canvas, 
          antialias: true, 
          alpha: true,
          preserveDrawingBuffer: true
        });
        threeRenderer.setSize(window.innerWidth, window.innerHeight);
        threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        threeRenderer.toneMapping = THREE.ACESFilmicToneMapping;
        threeRenderer.toneMappingExposure = 1.0;
        threeRenderer.setClearColor(0x000000, 1);
        
        // ---- Post-processing (Bloom) ----
        const renderPass = new THREE.RenderPass(threeScene, threeCamera);
        
        bloomPass = new THREE.UnrealBloomPass(
          new THREE.Vector2(window.innerWidth, window.innerHeight),
          1.2,   // strength
          0.3,   // radius
          0.85   // threshold
        );
        
        threeComposer = new THREE.EffectComposer(threeRenderer);
        threeComposer.addPass(renderPass);
        threeComposer.addPass(bloomPass);
        
        // ---- OrbitControls ----
        orbitControls = new THREE.OrbitControls(threeCamera, canvas);
        orbitControls.enableDamping = true;
        orbitControls.dampingFactor = 0.05;
        orbitControls.enablePan = true;
        orbitControls.enableZoom = true;
        orbitControls.enableRotate = true;
        orbitControls.autoRotate = true;
        orbitControls.autoRotateSpeed = 0.2;
        orbitControls.minDistance = 1500000;
        orbitControls.maxDistance = 30000000;
        orbitControls.target.set(0, 0, 0);
        orbitControls.update();
        
        // ---- Globe: Dark sphere + glowing wireframe ----
        // Base sphere (dark, slightly emissive)
        const globeGeometry = new THREE.SphereGeometry(1, 64, 64);
        const globeMaterial = new THREE.MeshBasicMaterial({
          color: 0x0a1628,
          transparent: true,
          opacity: 0.6,
          side: THREE.DoubleSide
        });
        globeMesh = new THREE.Mesh(globeGeometry, globeMaterial);
        threeScene.add(globeMesh);
        
        // Glowing wireframe (emissive grid lines)
        const wireGeometry = new THREE.SphereGeometry(1.005, 32, 32);
        const wireMaterial = new THREE.MeshBasicMaterial({
          color: 0x00d4ff,
          wireframe: true,
          transparent: true,
          opacity: 0.4,
          depthWrite: false
        });
        wireframeMesh = new THREE.Mesh(wireGeometry, wireMaterial);
        threeScene.add(wireframeMesh);
        
        // Outer glow sphere (for bloom effect)
        const glowGeometry = new THREE.SphereGeometry(1.02, 32, 32);
        const glowMaterial = new THREE.MeshBasicMaterial({
          color: 0x00d4ff,
          transparent: true,
          opacity: 0.15,
          side: THREE.BackSide,
          depthWrite: false
        });
        glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
        threeScene.add(glowMesh);
        
        // Point light for subtle illumination
        const pointLight = new THREE.PointLight(0x00d4ff, 0.5, 10);
        pointLight.position.set(0, 0, 5);
        threeScene.add(pointLight);
        
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x446688, 0.3);
        threeScene.add(ambientLight);
        
        // Directional light (sun-like)
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight.position.set(5, 3, 5);
        threeScene.add(dirLight);
        
        // ---- Route lines container ----
        routeLines = {};
        routeLineObjects = {};
        
        // ---- Animation loop ----
        function animate() {
          requestAnimationFrame(animate);
          
          // Auto-rotate
          if (autoRotateGlobe && !cameraFlying) {
            const now = performance.now();
            if (now - lastAutoRotateTime > 50) {
              globeMesh.rotation.y += 0.0001;
              wireframeMesh.rotation.y += 0.0001;
              Object.values(routeLineObjects).forEach(obj => obj.rotation.y += 0.0001);
              lastAutoRotateTime = now;
            }
          }
          
          orbitControls.update();
          
          // Render with bloom
          threeComposer.render();
        }
        
        animate();
        
        // Handle resize
        window.addEventListener("resize", onWindowResize);
        
        // Click handler for route segments
        canvas.addEventListener("click", onGlobeClick);
        
        // Road select handler
        document.getElementById("roadSelect").addEventListener("change", (e) => {
          selectedRoadId = e.target.value;
          updateFrame(currentFrame);
          fetchAccidents();
          fetchVehicleTypes();
          renderHeatmap();
        });"""

content = content.replace(old_init_vars, new_init_vars)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed duplicate variable declarations from initGlobe")
