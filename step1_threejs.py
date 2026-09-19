with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the entire initGlobe function with Three.js version
old_initGlobe = """    // ============ GLOBE INITIALIZATION ============
    async function initGlobe() {
      console.log("[Globe] Starting initialization...");
      
      // Check WebGL support
      const canvas = document.createElement("canvas");
      const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
      if (!gl) {
        throw new Error("WebGL not supported in this browser");
      }
      console.log("[Globe] WebGL supported:", gl.getParameter(gl.VERSION));
      console.log("[Globe] Renderer:", gl.getParameter(gl.RENDERER));
      
      // Check echarts availability
      if (typeof echarts === "undefined") {
        throw new Error("ECharts not loaded");
      }
      console.log("[Globe] ECharts version:", echarts.version);
      
      try {
        // Prepare series data for ECharts GL
        const seriesData = roadMeta.map(road => ({
          name: road.road_id,
          coordinates: road.bounds_geojson.coordinates.map(([lon, lat]) => [lon, lat, 10000]),
          lineStyle: { width: 6, opacity: 0.9 },
          itemStyle: { color: "#1890ff" }
        }));
        
        // Globe option
        const option = {
          backgroundColor: "transparent",
          globe: {
          baseColor: "#ff2020",
          displacementScale: 0.05,
          shading: "realistic",
          realisticMaterial: {
            roughness: 0.6,
            metalness: 0.2
          },
          postEffect: { enable: true, bloom: { enable: true, intensity: 0.6 } },
          light: {
            main: { intensity: 1.8, shadow: true, alpha: 20, beta: 30, color: "#ffffff" },
            ambient: { intensity: 0.5, color: "#5588aa" },
            ambientCubemap: { intensity: 0.6 }
          },
          outline: { enable: true, color: "#00d4ff", width: 3 },
          viewControl: {
            autoRotate: true,
            autoRotateAfterStill: 3,
            distance: 2000000,
            minDistance: 1500000,
            maxDistance: 25000000,
            panMouseButton: "left",
            rotateMouseButton: "right",
            zoomMouseButton: "middle"
          }
        },
        series: [{
          type: "lines3D",
          coordinateSystem: "globe",
          blendMode: "lighter",
          effect: {
            show: false
          },
          lineStyle: { width: 8, opacity: 1.0 },
          data: seriesData.map((s, i) => ({
            coords: s.coordinates,
            name: roadMeta[i].road_id,
            roadName: roadMeta[i].name,
            lineStyle: { color: "#00d4ff", width: 8 },
            itemStyle: { color: "#00d4ff" }
          }))
        }]
      };
      
      console.log("[Globe] Initializing echarts with webgl renderer...");
      globeChart = echarts.init(document.getElementById("globe"), null, { renderer: "webgl" });
      console.log("[Globe] ECharts initialized, setting option...");
      globeChart.setOption(option);
      console.log("[Globe] Option set successfully");
      
      // Click handler for camera flight
      globeChart.on("click", "series.lines3D", handleSegmentClick);
      
      // Hide loading
      hideLoading();
      console.log("[Globe] Loading hidden, loading initial frame...");
      
      // Load initial frame
      await updateFrame(0);
      console.log("[Globe] Initial frame loaded");
      
      // Fetch metadata for layers
      await Promise.all([fetchAccidents(), fetchVehicleTypes()]);
      renderHeatmap();
      console.log("[Globe] Initialization complete!");
      
    } catch (err) {
      console.error("[Globe] INIT FAILED:", err);
      console.error("[Globe] Stack trace:", err.stack);
      const container = document.getElementById("globe");
      if (container) {
        container.innerHTML = \`
          <div style="display:flex;align-items:center;justify-content:center;height:100%;flex-direction:column;color:#ff6b6b;padding:20px;text-align:center;">
            <h3>🌐 地球仪初始化失败</h3>
            <p style="margin:10px 0;max-width:400px;"><strong>错误:</strong> ${err.message}</p>
            <p style="font-size:12px;color:#888;">请检查：浏览器是否支持 WebGL2、显卡驱动是否最新、是否禁用了硬件加速</p>
            <details style="margin:10px 0;text-align:left;max-width:500px;">
              <summary style="cursor:pointer;color:#ff6b6b;">查看详细错误堆栈</summary>
              <pre style="margin-top:8px;padding:8px;background:#1a1a2e;color:#ff6b6b;font-size:11px;overflow:auto;max-height:200px;">${err.stack || "No stack trace"}</pre>
            </details>
            <button onclick="location.reload()" style="margin-top:16px;padding:8px 16px;background:#1890ff;color:white;border:none;border-radius:4px;cursor:pointer;">重试</button>
          </div>
        \`;
      }
      throw err;
    }
    }"""

new_initGlobe = """    // ============ THREE.JS GLOBE INITIALIZATION ============
    let threeScene, threeCamera, threeRenderer, threeComposer, bloomPass, orbitControls;
    let globeMesh, wireframeMesh, routeLines = {}, routeLineObjects = {};
    let autoRotateGlobe = true;
    let lastAutoRotateTime = 0;

    async function initGlobe() {
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
        window.addEventListener("resize", onWindowResize);
        
        // Click handler for route segments
        canvas.addEventListener("click", onGlobeClick);
        
        // Hide loading
        hideLoading();
        console.log("[ThreeJS] Initialization complete!");
        
        // Load initial frame
        await updateFrame(0);
        
        // Fetch metadata for layers
        await Promise.all([fetchAccidents(), fetchVehicleTypes()]);
        renderHeatmap();
        console.log("[ThreeJS] Initialization complete!");
        
      } catch (err) {
        console.error("[ThreeJS] INIT FAILED:", err);
        console.error("[ThreeJS] Stack trace:", err.stack);
        const container = document.getElementById("globe");
        if (container) {
          container.innerHTML = \`
            <div style="display:flex;align-items:center;justify-content:center;height:100%;flex-direction:column;color:#ff6b6b;padding:20px;text-align:center;">
              <h3>🌐 地球仪初始化失败</h3>
              <p style="margin:10px 0;max-width:400px;"><strong>错误:</strong> ${err.message}</p>
              <p style="font-size:12px;color:#888;">请检查：浏览器是否支持 WebGL2、显卡驱动是否最新、是否禁用了硬件加速</p>
              <details style="margin:10px 0;text-align:left;max-width:500px;">
                <summary style="cursor:pointer;color:#ff6b6b;">查看详细错误堆栈</summary>
                <pre style="margin-top:8px;padding:8px;background:#1a1a2e;color:#ff6b6b;font-size:11px;overflow:auto;max-height:200px;">${err.stack || "No stack trace"}</pre>
              </details>
              <button onclick="location.reload()" style="margin-top:16px;padding:8px 16px;background:#1890ff;color:white;border:none;border-radius:4px;cursor:pointer;">重试</button>
            </div>
          \`;
        }
        throw err;
      }
    }"""

content = content.replace(old_initGlobe, new_initGlobe)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced initGlobe with Three.js version")
