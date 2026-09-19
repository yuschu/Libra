with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# The second occurrence has TWO blank lines before getCongestionLevel
old_exact = """    }
    function getCongestionThreeColor(avgSpeed) {
      const hex = getCongestionColor(avgSpeed);
      return new THREE.Color(hex);
    }
    
    
    function getCongestionLevel(avgSpeed) {"""

new_exact = """    }
    function getCongestionLevel(avgSpeed) {"""

content = content.replace(old_exact, new_exact)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed second duplicate with exact whitespace match")
