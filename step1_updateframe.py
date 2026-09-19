with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update the updateFrame function to work with Three.js
old_updateFrame = """    // ============ FRAME UPDATE ============
    async function updateFrame(frameIndex) {
      currentFrame = frameIndex;
      const dt = getCurrentDt();
      
      // Update timeline display
      document.getElementById("timelineTime").textContent = dt;
      document.getElementById("timelineSlider").value = frameIndex;
      
      // Fetch traffic data for this frame
      const roadIds = selectedRoadId ? [selectedRoadId] : roadMeta.map(r => r.road_id);
      
      try {
        for (const rid of roadIds) {
          const cacheKey = `${rid}-${dt}`;
          if (!trafficCache.has(cacheKey)) {
            // Fetch from API
            const res = await fetch(`${API_BASE}/traffic/flows?road_id=${rid}&dt=${encodeURIComponent(dt)}`);
            const data = await res.json();
            if (data.code === 0 && data.data.values.length > 0) {
              // Find the matching hour
              const labels = data.data.labels;
              const values = data.data.values;
              const idx = labels.findIndex(l => l === dt.slice(11, 16));
              if (idx >= 0) {
                trafficCache.set(cacheKey, { 
                  road_id: rid, 
                  flow: values[idx], 
                  avg_speed: values[idx] // placeholder, API only returns flow
                });
              }
            }
          }
        }
        
        // Update globe series colors
        updateGlobeColors();
        updateHeatmapForTime(dt);
        
      } catch (e) {
        console.error("Frame update error:", e);
      }
    }"""

new_updateFrame = """    // ============ FRAME UPDATE ============
    async function updateFrame(frameIndex) {
      currentFrame = frameIndex;
      const dt = getCurrentDt();
      
      // Update timeline display
      document.getElementById("timelineTime").textContent = formatTimeForGranularity(dt);
      document.getElementById("timelineSlider").value = frameIndex;
      
      // Fetch traffic data for this frame
      const roadIds = selectedRoadId ? [selectedRoadId] : roadMeta.map(r => r.road_id);
      
      try {
        for (const rid of roadIds) {
          const cacheKey = `${rid}-${dt}`;
          if (!trafficCache.has(cacheKey)) {
            // Fetch from API
            const res = await fetch(`${API_BASE}/traffic/flows?road_id=${rid}&dt=${encodeURIComponent(dt)}`);
            const data = await res.json();
            if (data.code === 0 && data.data.values.length > 0) {
              // Find the matching hour
              const labels = data.data.labels;
              const values = data.data.values;
              const idx = labels.findIndex(l => l === dt.slice(11, 16));
              if (idx >= 0) {
                trafficCache.set(cacheKey, { 
                  road_id: rid, 
                  flow: values[idx], 
                  avg_speed: values[idx] // placeholder, API only returns flow
                });
              }
            }
          }
        }
        
        // Update or create route lines for this frame
        updateRouteLines(dt);
        updateHeatmapForTime(dt);
        
      } catch (e) {
        console.error("Frame update error:", e);
      }
    }"""

content = content.replace(old_updateFrame, new_updateFrame)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated updateFrame for Three.js")
