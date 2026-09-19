with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update the legend to use the new congestion colors (already correct)
# Update the timeline time display to use formatTimeForGranularity
old_timeline_display = """      // Update timeline display
      document.getElementById("timelineTime").textContent = dt;
      document.getElementById("timelineSlider").value = frameIndex;"""

new_timeline_display = """      // Update timeline display
      document.getElementById("timelineTime").textContent = formatTimeForGranularity(dt);
      document.getElementById("timelineSlider").value = frameIndex;"""

content = content.replace(old_timeline_display, new_timeline_display)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated timeline display to use formatTimeForGranularity")
