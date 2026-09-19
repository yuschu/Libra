with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the OLD echarts-gl initGlobe with Three.js version
# The OLD one starts with "const canvas = document.createElement"
# The NEW one should use "const canvas = document.getElementById"

old_start = """    async function initGlobe() {
      console.log("[Globe] Starting initialization...");
      
      // Check WebGL support
      const canvas = document.createElement("canvas");"""

new_start = """    async function initGlobe() {
      console.log("[ThreeJS] Starting initialization...");
      
      // Check WebGL support
      const canvas = document.getElementById("globe");"""

content = content.replace(old_start, new_start)

# Also replace the echarts check
old_echarts_check = """      // Check echarts availability
      if (typeof echarts === "undefined") {
        throw new Error("ECharts not loaded");
      }
      console.log("[Globe] ECharts version:", echarts.version);"""

new_echarts_check = """      // Check Three.js availability
      if (typeof THREE === "undefined") {
        throw new Error("Three.js not loaded");
      }
      console.log("[ThreeJS] Three.js version:", THREE.REVISION);"""

content = content.replace(old_echarts_check, new_echarts_check)

# Replace the try block content - need to replace the entire echarts-gl option with Three.js setup
# This is complex, let me do a more targeted replacement

# First, let me just replace the echarts.init line
old_echarts_init = """      console.log("[Globe] Initializing echarts with webgl renderer...");
      globeChart = echarts.init(document.getElementById("globe"), null, { renderer: "webgl" });
      console.log("[Globe] ECharts initialized, setting option...");
      globeChart.setOption(option);
      console.log("[Globe] Option set successfully");
      
      // Click handler for camera flight
      globeChart.on("click", "series.lines3D", handleSegmentClick);"""

new_echarts_init = """      console.log("[ThreeJS] Initializing Three.js renderer...");
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
      orbitControls.update();"""

content = content.replace(old_echarts_init, new_echarts_init)

# Replace the click handler
old_click = """      // Click handler for camera flight
      globeChart.on("click", "series.lines3D", handleSegmentClick);"""

new_click = """      // Click handler for route segments
      canvas.addEventListener("click", onGlobeClick);"""

content = content.replace(old_click, new_click)

# Replace the hideLoading and frame loading
old_loading = """      // Hide loading
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
            <h3>地球仪初始化失败</h3>
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
    }"""

new_loading = """      // Hide loading
      hideLoading();
      console.log("[ThreeJS] Loading hidden, loading initial frame...");
      
      // Load initial frame
      await updateFrame(0);
      console.log("[ThreeJS] Initial frame loaded");
      
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
            <h3>地球仪初始化失败</h3>
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
    }"""

content = content.replace(old_loading, new_loading)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced initGlobe echarts-gl code with Three.js version")
