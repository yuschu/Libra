with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Change the main script to type="module" and ensure all Three.js code is inside
# Find the script tag and change it to type="module"
old_script_start = """  <script>
    // ============ CONFIGURATION ============"""

new_script_start = """  <script type="module">
    // ============ CONFIGURATION ============"""

content = content.replace(old_script_start, new_script_start)

# Also need to remove the old echarts-gl initGlobe completely
# The old initGlobe function should already be replaced, but let me check for any remaining echarts references in the init
# The main script should now be type=module

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Changed main script to type=module")
