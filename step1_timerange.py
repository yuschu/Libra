with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update initTimeRange to call updateTimelineSliderMax
old_initTimeRange = """    async function initTimeRange() {
      // Set defaults to data range (covers full sample data)
      const start = new Date("2026-09-01T00:00:00");
      const end = new Date("2026-09-07T23:00:00");
      document.getElementById("timeStart").value = start.toISOString().slice(0, 16);
      document.getElementById("timeEnd").value = end.toISOString().slice(0, 16);
      // Apply default range on load
      timeRange.start = start.toISOString().slice(0, 16);
      timeRange.end = end.toISOString().slice(0, 16);
      await Promise.all([fetchAccidents(), fetchVehicleTypes()]);
      
      document.getElementById("btnApplyRange").addEventListener("click", () => {
        timeRange.start = document.getElementById("timeStart").value || null;
        timeRange.end = document.getElementById("timeEnd").value || null;
        fetchAccidents();
        fetchVehicleTypes();
        renderHeatmap();
        showToast("时间范围已更新");
      });
      
      document.getElementById("btnResetView").addEventListener("click", () => {
        if (globeChart) {
          globeChart.dispatchAction({ type: "globeViewControl", action: "reset" });
          autoRotate = true;
        }
      });
      
      // Initialize granularity selector
      document.getElementById("granularitySelect").addEventListener("change", (e) => {
        const oldGran = timeGranularity;
        timeGranularity = e.target.value;
        // Convert current frame to new granularity
        const oldConfig = GRANULARITY_CONFIG[oldGran];
        const newConfig = GRANULARITY_CONFIG[timeGranularity];
        const progress = currentFrame / (oldConfig.framesPerHour * 24 * 7);
        const maxFrames = newConfig.framesPerHour * 24 * 7;
        currentFrame = Math.round(progress * maxFrames);
        updateTimelineSliderMax();
        updateFrame(currentFrame);
        showToast("时间粒度已切换: " + timeGranularity);
      });
      
      // Initialize slider max
      updateTimelineSliderMax();
    }"""

new_initTimeRange = """    async function initTimeRange() {
      // Set defaults to data range (covers full sample data)
      const start = new Date("2026-09-01T00:00:00");
      const end = new Date("2026-09-07T23:00:00");
      document.getElementById("timeStart").value = start.toISOString().slice(0, 16);
      document.getElementById("timeEnd").value = end.toISOString().slice(0, 16);
      // Apply default range on load
      timeRange.start = start.toISOString().slice(0, 16);
      timeRange.end = end.toISOString().slice(0, 16);
      await Promise.all([fetchAccidents(), fetchVehicleTypes()]);
      
      document.getElementById("btnApplyRange").addEventListener("click", () => {
        timeRange.start = document.getElementById("timeStart").value || null;
        timeRange.end = document.getElementById("timeEnd").value || null;
        fetchAccidents();
        fetchVehicleTypes();
        renderHeatmap();
        showToast("时间范围已更新");
      });
      
      document.getElementById("btnResetView").addEventListener("click", () => {
        if (threeCamera) {
          threeCamera.position.set(0, 0, 6000000);
          orbitControls.target.set(0, 0, 0);
          orbitControls.update();
          autoRotateGlobe = true;
        }
      });
      
      // Initialize granularity selector
      document.getElementById("granularitySelect").addEventListener("change", (e) => {
        const oldGran = timeGranularity;
        timeGranularity = e.target.value;
        // Convert current frame to new granularity
        const oldConfig = GRANULARITY_CONFIG[oldGran];
        const newConfig = GRANULARITY_CONFIG[timeGranularity];
        const progress = currentFrame / (oldConfig.framesPerHour * 24 * 7);
        const maxFrames = newConfig.framesPerHour * 24 * 7;
        currentFrame = Math.round(progress * maxFrames);
        updateTimelineSliderMax();
        updateFrame(currentFrame);
        showToast("时间粒度已切换: " + timeGranularity);
      });
      
      // Initialize slider max
      updateTimelineSliderMax();
    }"""

content = content.replace(old_initTimeRange, new_initTimeRange)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated initTimeRange for Three.js camera reset")
