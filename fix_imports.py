with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the script imports to use ES modules
old_imports = """  <script src="lib/three.min.js"></script>
  <script src="lib/controls/OrbitControls.js"></script>
  <script src="lib/postprocessing/EffectComposer.js"></script>
  <script src="lib/postprocessing/RenderPass.js"></script>
  <script src="lib/postprocessing/UnrealBloomPass.js"></script>
  <!-- echarts for heatmap only -->
  <script src="lib/echarts.min.js"></script>"""

new_imports = """  <script type="importmap">
    {
      "imports": {
        "three": "./lib/three.module.js",
        "three/addons/controls/OrbitControls.js": "./lib/controls/OrbitControls.js",
        "three/addons/postprocessing/EffectComposer.js": "./lib/postprocessing/EffectComposer.js",
        "three/addons/postprocessing/RenderPass.js": "./lib/postprocessing/RenderPass.js",
        "three/addons/postprocessing/UnrealBloomPass.js": "./lib/postprocessing/UnrealBloomPass.js"
      }
    }
  </script>
  <script type="module">
    import * as THREE from "three";
    import { OrbitControls } from "three/addons/controls/OrbitControls.js";
    import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
    import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
    import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
    import * as echarts from "./lib/echarts.min.js";
    // ECharts is global, we just ensure it loads
  </script>"""

content = content.replace(old_imports, new_imports)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated imports to use ES modules with importmap")
