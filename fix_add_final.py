with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add the function back - find the first formatTimeForGranularity and add before it
old_format = """    function formatTimeForGranularity(dtStr) {"""

new_format = """    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    function formatTimeForGranularity(dtStr) {"""

content = content.replace(old_format, new_format)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added getCongestionThreeColor function back (once)")
