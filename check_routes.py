with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix routeLineObjects - it needs to be declared at module level, not inside initGlobe
# Find where routeLineObjects is declared and move it to module level
# First, let's check where routeLineObjects is used

old_route_lines = """    let routeLines = {}, routeLineObjects = {};
    let globeMesh, wireframeMesh, routeLines = {}, routeLineObjects = {};"""

# Actually, let me check the current state
idx = content.index("let routeLines = {}, routeLineObjects = {};")
print("Found at:", idx)
print(content[idx:idx+200])
