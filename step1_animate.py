with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the animate function and replace the end part
old_animate = """        animate();
        
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

new_animate = """        animate();
        
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

content = content.replace(old_animate, new_animate)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added road select handler to animate section")
