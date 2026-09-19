with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add helper functions and update route lines
old_congestion = """    function getCongestionColor(avgSpeed) {
      if (avgSpeed == null) return "#666";
      for (const t of CONGESTION_THRESHOLDS) {
        if (avgSpeed < t.max) return t.color;
      }
      return "#666";
    }"""

new_congestion = """    function getCongestionColor(avgSpeed) {
      if (avgSpeed == null) return "#666";
      for (const t of CONGESTION_THRESHOLDS) {
        if (avgSpeed < t.max) return t.color;
      }
      return "#666";
    }
    
    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    function formatTimeForGranularity(dtStr) {
      // dtStr format: "2026-09-01 08:00"
      const config = GRANULARITY_CONFIG[timeGranularity];
      const date = new Date(dtStr.replace(" ", "T"));
      switch (timeGranularity) {
        case "ms":
          return date.toISOString().slice(11, 23).replace("T", " ");
        case "s":
          return date.toISOString().slice(11, 19).replace("T", " ");
        case "min":
          return date.toISOString().slice(11, 16).replace("T", " ");
        case "h":
        default:
          return date.toISOString().slice(11, 16).replace("T", " ");
      }
    }"""

content = content.replace(old_congestion, new_congestion)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added formatTimeForGranularity and Three.js color helper")
