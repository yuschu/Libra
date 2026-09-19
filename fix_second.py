with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the SECOND occurrence (the one after formatTimeForGranularity definition ends)
# The pattern is: } \n    function getCongestionThreeColor... \n    function formatTimeForGranularity
# The second one appears after a closing brace }

old_second = """    }
    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    function formatTimeForGranularity(dtStr) {"""

new_second = """    }
    function formatTimeForGranularity(dtStr) {"""

content = content.replace(old_second, new_second)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed second duplicate getCongestionThreeColor")
