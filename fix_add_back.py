with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the first getCongestionThreeColor call and add the function definition before it
# Find where formatTimeForGranularity is defined - that's where we removed the function
old_format = """    function formatTimeForGranularity(dtStr) {"""

new_format = """    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    function formatTimeForGranularity(dtStr) {"""

content = content.replace(old_format, new_format)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added back getCongestionThreeColor function")
