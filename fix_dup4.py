with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the second occurrence specifically
old_second = """    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    function formatTimeForGranularity(dtStr) {"""

new_text = """    function formatTimeForGranularity(dtStr) {"""

content = content.replace(old_second, new_text)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed second duplicate getCongestionThreeColor")
