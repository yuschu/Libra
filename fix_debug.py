with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update initGlobe with better error handling and debugging
old_init = """    async function initGlobe() {
      try {
        // Prepare series data for ECharts GL
        const seriesData = roadMeta.map(road => ({
          name: road.road_id,
          coordinates: road.bounds_geojson.coordinates.map(([lon, lat]) => [lon, lat, 10000]), // 10km altitude
          lineStyle: { width: 6, opacity: 0.9 },
          // Initial color - will be updated per frame
          itemStyle: { color: "#1890ff" }
        }));
        
        // Globe option
        const option = {
          backgroundColor: "transparent",
          globe: {
"""

new_init = """    async function initGlobe() {
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
"""

content = content.replace(old_init, new_init)

# Update the try/catch block end
old_end = """      };
      
      globeChart = echarts.init(document.getElementById("globe"), null, { renderer: "webgl" });
      globeChart.setOption(option);
      
      // Click handler for camera flight
      globeChart.on("click", "series.lines3D", handleSegmentClick);
      
      // Hide loading
      hideLoading();
      
      // Load initial frame
      await updateFrame(0);
      
      // Fetch metadata for layers
      await Promise.all([fetchAccidents(), fetchVehicleTypes()]);
      renderHeatmap();
      
    } catch (err) {
      console.error("Globe init failed:", err);
      const container = document.getElementById("globe");
      if (container) {
        container.innerHTML = \`
          <div style="display:flex;align-items:center;justify-content:center;height:100%;flex-direction:column;color:#ff6b6b;padding:20px;text-align:center;">
            <h3>🌐 地球仪初始化失败</h3>
            <p style="margin:10px 0;max-width:400px;">\${err.message}</p>
            <p style="font-size:12px;color:#888;">请检查：浏览器是否支持 WebGL2、显卡驱动是否最新、是否禁用了硬件加速</p>
            <button onclick="location.reload()" style="margin-top:16px;padding:8px 16px;background:#1890ff;color:white;border:none;border-radius:4px;cursor:pointer;">重试</button>
          </div>
        \`;
      }
      throw err;
    }"""

new_end = """      };
      
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
            <p style="margin:10px 0;max-width:400px;"><strong>错误:</strong> \${err.message}</p>
            <p style="font-size:12px;color:#888;">请检查：浏览器是否支持 WebGL2、显卡驱动是否最新、是否禁用了硬件加速</p>
            <details style="margin:10px 0;text-align:left;max-width:500px;">
              <summary style="cursor:pointer;color:#ff6b6b;">查看详细错误堆栈</summary>
              <pre style="margin-top:8px;padding:8px;background:#1a1a2e;color:#ff6b6b;font-size:11px;overflow:auto;max-height:200px;">\${err.stack || "No stack trace"}</pre>
            </details>
            <button onclick="location.reload()" style="margin-top:16px;padding:8px 16px;background:#1890ff;color:white;border:none;border-radius:4px;cursor:pointer;">重试</button>
          </div>
        \`;
      }
      throw err;
    }"""

content = content.replace(old_end, new_end)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated initGlobe with detailed error logging")
