with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Globe config - brighter baseColor, better lighting, closer distance, outline
old_globe = """        globe: {
          baseColor: "#0a1628",
          displacementScale: 0.05,
          shading: "realistic",
          realisticMaterial: {
            roughness: 0.8,
            metalness: 0.1
          },
          postEffect: { enable: true, bloom: { enable: true, intensity: 0.3 } },
          light: {
            main: { intensity: 1.2, shadow: true, alpha: 30, beta: 40 },
            ambient: { intensity: 0.3 }
          },
          viewControl: {
            autoRotate: true,
            autoRotateAfterStill: 3,
            distance: 20000000,
            minDistance: 1000000,
            maxDistance: 50000000,
            panMouseButton: "left",
            rotateMouseButton: "right",
            zoomMouseButton: "middle"
          }
        },"""

new_globe = """        globe: {
          baseColor: "#1a3a5c",
          displacementScale: 0.05,
          shading: "realistic",
          realisticMaterial: {
            roughness: 0.7,
            metalness: 0.15
          },
          postEffect: { enable: true, bloom: { enable: true, intensity: 0.5 } },
          light: {
            main: { intensity: 1.5, shadow: true, alpha: 25, beta: 35, color: "#ffffff" },
            ambient: { intensity: 0.4, color: "#446688" },
            ambientCubemap: { intensity: 0.5 }
          },
          outline: { enable: true, color: "#4a90d9", width: 2 },
          viewControl: {
            autoRotate: true,
            autoRotateAfterStill: 3,
            distance: 8000000,
            minDistance: 2000000,
            maxDistance: 30000000,
            panMouseButton: "left",
            rotateMouseButton: "right",
            zoomMouseButton: "middle"
          }
        },"""

content = content.replace(old_globe, new_globe)

# Fix 2: Add try/catch to initGlobe with error display
old_init = """    async function initGlobe() {
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

content = content.replace(old_init, new_init)

# Add try/catch wrapper end
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
    }"""

new_end = """      };
      
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

content = content.replace(old_end, new_end)

# Fix 3: Heatmap - ensure time range covers data by default, fix renderHeatmap
old_render = """    function renderHeatmap() {
      const container = document.getElementById("heatmapContainer");
      
      // Build 24x7 matrix of average speeds per hour+weekday
      const matrix = Array(7).fill(null).map(() => Array(24).fill(null).map(() => ({ speeds: [], count: 0 })));
      
      // Aggregate from traffic data (using cached sample data)
      trafficCache.forEach((traffic, key) => {
        const [roadId, dt] = key.split("-");
        const date = new Date(dt);
        const day = date.getDay(); // 0=Sun, 1=Mon...
        const hour = date.getHours();
        const dayIdx = day === 0 ? 6 : day - 1; // Convert to Mon=0
        
        if (traffic.avg_speed != null) {
          matrix[dayIdx][hour].speeds.push(traffic.avg_speed);
          matrix[dayIdx][hour].count++;
        }
      });
      
      // Compute averages
      const avgMatrix = matrix.map(row => row.map(cell => 
        cell.count > 0 ? cell.speeds.reduce((a,b)=>a+b,0)/cell.count : null
      ));
      
      // Render
      let html = '<div class="heatmap-grid">';
      // Header row
      html += '<div class="heatmap-cell heatmap-header"></div>';
      HOURS.forEach(h => html += `<div class="heatmap-cell heatmap-header">${h}</div>`);
      
      // Data rows
      WEEKDAYS.forEach((day, dayIdx) => {
        html += `<div class="heatmap-cell heatmap-row-label">${day}</div>`;
        HOURS.forEach((_, hourIdx) => {
          const avgSpeed = avgMatrix[dayIdx][hourIdx];
          let color = "#1a1a2e";
          let level = "无数据";
          if (avgSpeed != null) {
            color = getCongestionColor(avgSpeed);
            level = getCongestionLevel(avgSpeed);
          }
          html += `<div class="heatmap-cell" style="background:${color}" data-day="${dayIdx}" data-hour="${hourIdx}" data-speed="${avgSpeed || 0}" data-count="${matrix[dayIdx][hourIdx].count}" title="${day} ${HOURS[hourIdx]}: ${level} (${avgSpeed?.toFixed(1) || 'N/A'} km/h, ${matrix[dayIdx][hourIdx].count} samples)"></div>`;
        });
      });
      html += '</div>';
      container.innerHTML = html;
      
      // Tooltip
      const tooltip = document.getElementById("heatmapTooltip");
      container.querySelectorAll(".heatmap-cell[data-speed]").forEach(cell => {
        cell.addEventListener("mouseenter", (e) => {
          const speed = parseFloat(cell.dataset.speed);
          const count = parseInt(cell.dataset.count);
          const day = WEEKDAYS[parseInt(cell.dataset.day)];
          const hour = HOURS[parseInt(cell.dataset.hour)];
          const level = getCongestionLevel(speed);
          tooltip.innerHTML = `<strong>${day} ${hour}</strong><br>平均速度: ${speed.toFixed(1)} km/h (${level})<br>样本数: ${count}`;
          tooltip.style.left = e.clientX + 12 + "px";
          tooltip.style.top = e.clientY - 40 + "px";
          tooltip.classList.add("show");
        });
        cell.addEventListener("mouseleave", () => tooltip.classList.remove("show"));
        cell.addEventListener("mousemove", (e) => {
          tooltip.style.left = e.clientX + 12 + "px";
          tooltip.style.top = e.clientY - 40 + "px";
        });
      });
    }"""

new_render = """    function renderHeatmap() {
      const container = document.getElementById("heatmapContainer");
      
      // Build 24x7 matrix of average speeds per hour+weekday
      // Use all data (not filtered by timeRange) for heatmap
      const matrix = Array(7).fill(null).map(() => Array(24).fill(null).map(() => ({ speeds: [], count: 0 })));
      
      // Aggregate from ALL traffic data (trafficCache has all frames)
      trafficCache.forEach((traffic, key) => {
        const [roadId, dt] = key.split("-");
        const date = new Date(dt);
        const day = date.getDay(); // 0=Sun, 1=Mon...
        const hour = date.getHours();
        const dayIdx = day === 0 ? 6 : day - 1; // Convert to Mon=0
        
        if (traffic.avg_speed != null) {
          matrix[dayIdx][hour].speeds.push(traffic.avg_speed);
          matrix[dayIdx][hour].count++;
        }
      });
      
      // Compute averages
      const avgMatrix = matrix.map(row => row.map(cell => 
        cell.count > 0 ? cell.speeds.reduce((a,b)=>a+b,0)/cell.count : null
      ));
      
      // Render
      let html = '<div class="heatmap-grid">';
      // Header row
      html += '<div class="heatmap-cell heatmap-header"></div>';
      HOURS.forEach(h => html += `<div class="heatmap-cell heatmap-header">${h}</div>`);
      
      // Data rows
      WEEKDAYS.forEach((day, dayIdx) => {
        html += `<div class="heatmap-cell heatmap-row-label">${day}</div>`;
        HOURS.forEach((_, hourIdx) => {
          const avgSpeed = avgMatrix[dayIdx][hourIdx];
          let color = "#1a1a2e";
          let level = "无数据";
          if (avgSpeed != null) {
            color = getCongestionColor(avgSpeed);
            level = getCongestionLevel(avgSpeed);
          }
          html += `<div class="heatmap-cell" style="background:${color}" data-day="${dayIdx}" data-hour="${hourIdx}" data-speed="${avgSpeed || 0}" data-count="${matrix[dayIdx][hourIdx].count}" title="${day} ${HOURS[hourIdx]}: ${level} (${avgSpeed?.toFixed(1) || 'N/A'} km/h, ${matrix[dayIdx][hourIdx].count} samples)"></div>`;
        });
      });
      html += '</div>';
      container.innerHTML = html;
      
      // Tooltip
      const tooltip = document.getElementById("heatmapTooltip");
      container.querySelectorAll(".heatmap-cell[data-speed]").forEach(cell => {
        cell.addEventListener("mouseenter", (e) => {
          const speed = parseFloat(cell.dataset.speed);
          const count = parseInt(cell.dataset.count);
          const day = WEEKDAYS[parseInt(cell.dataset.day)];
          const hour = HOURS[parseInt(cell.dataset.hour)];
          const level = getCongestionLevel(speed);
          tooltip.innerHTML = `<strong>${day} ${hour}</strong><br>平均速度: ${speed.toFixed(1)} km/h (${level})<br>样本数: ${count}`;
          tooltip.style.left = e.clientX + 12 + "px";
          tooltip.style.top = e.clientY - 40 + "px";
          tooltip.classList.add("show");
        });
        cell.addEventListener("mouseleave", () => tooltip.classList.remove("show"));
        cell.addEventListener("mousemove", (e) => {
          tooltip.style.left = e.clientX + 12 + "px";
          tooltip.style.top = e.clientY - 40 + "px";
        });
      });
    }"""

content = content.replace(old_render, new_render)

# Fix 4: updateGlobeColors - ensure it updates line colors correctly
old_update_colors = """    function updateGlobeColors() {
      if (!globeChart) return;
      const option = globeChart.getOption();
      const series = option.series[0];
      
      series.data.forEach((item, i) => {
        const road = roadMeta[i];
        const dt = getCurrentDt();
        const cacheKey = `${road.road_id}-${dt}`;
        const traffic = trafficCache.get(cacheKey);
        
        let color = "#1890ff";
        let speed = 0;
        if (traffic && traffic.avg_speed) {
          speed = traffic.avg_speed;
          color = getCongestionColor(speed);
        } else if (traffic && traffic.flow) {
          // Estimate speed from flow if needed
          color = getCongestionColor(estimateSpeed(traffic.flow, road.road_id));
        }
        
        item.lineStyle = { color, width: 6, opacity: 0.9 };
        item.itemStyle = { color };
      });
      
      globeChart.setOption({ series: [{ data: series.data }] });
    }"""

new_update_colors = """    function updateGlobeColors() {
      if (!globeChart) return;
      const option = globeChart.getOption();
      const series = option.series[0];
      
      series.data.forEach((item, i) => {
        const road = roadMeta[i];
        const dt = getCurrentDt();
        const cacheKey = `${road.road_id}-${dt}`;
        const traffic = trafficCache.get(cacheKey);
        
        let color = "#1890ff";
        let speed = 0;
        if (traffic && traffic.avg_speed != null) {
          speed = traffic.avg_speed;
          color = getCongestionColor(speed);
        } else if (traffic && traffic.flow != null) {
          // Estimate speed from flow if needed
          color = getCongestionColor(estimateSpeed(traffic.flow, road.road_id));
        }
        
        // Update line style with congestion color
        item.lineStyle = { color, width: 6, opacity: 0.95 };
        item.itemStyle = { color };
      });
      
      globeChart.setOption({ series: [{ data: series.data }] });
    }"""

content = content.replace(old_update_colors, new_update_colors)

# Fix 5: Ensure time range defaults cover all data
old_timerange = """      // Set defaults to data range
      const start = new Date("2026-09-01T00:00:00");
      const end = new Date("2026-09-07T23:00:00");
      document.getElementById("timeStart").value = start.toISOString().slice(0, 16);
      document.getElementById("timeEnd").value = end.toISOString().slice(0, 16);"""

new_timerange = """      // Set defaults to data range (covers full sample data)
      const start = new Date("2026-09-01T00:00:00");
      const end = new Date("2026-09-07T23:00:00");
      document.getElementById("timeStart").value = start.toISOString().slice(0, 16);
      document.getElementById("timeEnd").value = end.toISOString().slice(0, 16);
      // Apply default range on load
      timeRange.start = start.toISOString().slice(0, 16);
      timeRange.end = end.toISOString().slice(0, 16);
      await Promise.all([fetchAccidents(), fetchVehicleTypes()]);"""

content = content.replace(old_timerange, new_timerange)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("All fixes applied")
