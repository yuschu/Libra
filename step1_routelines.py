with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add updateRouteLines function after updateGlobeColors
old_updateColors = """    function updateGlobeColors() {
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

new_updateColors = """    // ---- Route Lines Update ----
    function updateRouteLines(dt) {
      const roadIds = selectedRoadId ? [selectedRoadId] : roadMeta.map(r => r.road_id);
      
      roadIds.forEach(rid => {
        const cacheKey = `${rid}-${dt}`;
        const traffic = trafficCache.get(cacheKey);
        const road = roadMeta.find(r => r.road_id === rid);
        if (!road) return;
        
        const avgSpeed = traffic?.avg_speed ?? null;
        const color = getCongestionThreeColor(avgSpeed);
        const congestionColor = getCongestionColor(avgSpeed);
        
        // Get or create route line
        let lineObj = routeLineObjects[rid];
        if (!lineObj) {
          lineObj = createRouteLine(rid, road.bounds_geojson.coordinates);
          routeLineObjects[rid] = lineObj;
          threeScene.add(lineObj);
        }
        
        // Update line color
        if (lineObj.material) {
          lineObj.material.color = color;
          lineObj.material.emissive = color.clone().multiplyScalar(0.5);
          lineObj.material.emissiveIntensity = 0.5;
          lineObj.material.needsUpdate = true;
        }
        
        // Store color for legend/heatmap sync
        routeLines[rid] = { color: congestionColor, avgSpeed };
      });
      
      // Remove lines for roads not in current view
      Object.keys(routeLineObjects).forEach(rid => {
        if (!roadIds.includes(rid)) {
          const obj = routeLineObjects[rid];
          threeScene.remove(obj);
          if (obj.geometry) obj.geometry.dispose();
          if (obj.material) obj.material.dispose();
          delete routeLineObjects[rid];
          delete routeLines[rid];
        }
      });
    }"""

content = content.replace(old_updateColors, new_updateColors)

# Also add createRouteLine function
old_estimateSpeed = """    function estimateSpeed(flow, roadId) {
      // Rough estimation based on typical capacity
      const capacities = { R001: 2000, R002: 2200, R003: 1800 };
      const cap = capacities[roadId] || 2000;
      const ratio = flow / cap;
      if (ratio > 0.9) return 15;
      if (ratio > 0.7) return 30;
      if (ratio > 0.5) return 50;
      return 70;
    }"""

new_estimateSpeed = """    function estimateSpeed(flow, roadId) {
      // Rough estimation based on typical capacity
      const capacities = { R001: 2000, R002: 2200, R003: 1800 };
      const cap = capacities[roadId] || 2000;
      const ratio = flow / cap;
      if (ratio > 0.9) return 15;
      if (ratio > 0.7) return 30;
      if (ratio > 0.5) return 50;
      return 70;
    }
    
    function createRouteLine(roadId, coordinates) {
      // Create a curved line along the route coordinates
      const points = coordinates.map(([lon, lat]) => {
        // Convert lat/lon to 3D position on sphere
        const phi = (90 - lat) * Math.PI / 180;
        const theta = (lon + 180) * Math.PI / 180;
        const radius = 1.01; // Slightly above globe surface
        return new THREE.Vector3(
          radius * Math.sin(phi) * Math.cos(theta),
          radius * Math.cos(phi),
          radius * Math.sin(phi) * Math.sin(theta)
        );
      });
      
      // Create smooth curve
      const curve = new THREE.CatmullRomCurve3(points);
      const tubeGeometry = new THREE.TubeGeometry(curve, 64, 0.003, 8, false);
      
      const material = new THREE.MeshBasicMaterial({
        color: 0x00d4ff,
        transparent: true,
        opacity: 0.9,
        depthWrite: false
      });
      
      const mesh = new THREE.Mesh(tubeGeometry, material);
      mesh.userData = { roadId };
      return mesh;
    }"""

content = content.replace(old_congestion, new_congestion)
content = content.replace(old_estimateSpeed, new_estimateSpeed)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added updateRouteLines and createRouteLine")
