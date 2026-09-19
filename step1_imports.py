with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Step 1: Add Three.js imports after the existing script tags
old_scripts = """  <script src="lib/echarts.min.js"></script>
  <script src="lib/echarts-gl.min.js"></script>"""

new_scripts = """  <script src="lib/three.min.js"></script>
  <script src="lib/controls/OrbitControls.js"></script>
  <script src="lib/postprocessing/EffectComposer.js"></script>
  <script src="lib/postprocessing/RenderPass.js"></script>
  <script src="lib/postprocessing/UnrealBloomPass.js"></script>
  <!-- echarts for heatmap only -->
  <script src="lib/echarts.min.js"></script>"""

content = content.replace(old_scripts, new_scripts)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added Three.js imports")
