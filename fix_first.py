with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the FIRST occurrence (the one we just added back) and keep the second
# Find the first occurrence and remove it up to formatTimeForGranularity
old_first = """    
    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    function formatTimeForGranularity(dtStr) {"""

new_first = """    function formatTimeForGranularity(dtStr) {"""

content = content.replace(old_first, new_first)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed first occurrence, keeping second")
