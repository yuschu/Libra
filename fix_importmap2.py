with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the importmap to include all needed modules
old_importmap = """  <script type="importmap">
    {
      "imports": {
        "three": "./lib/three.module.js",
        "three/addons/controls/OrbitControls.js": "./lib/controls/OrbitControls.js",
        "three/addons/postprocessing/EffectComposer.js": "./lib/postprocessing/EffectComposer.js",
        "three/addons/postprocessing/RenderPass.js": "./lib/postprocessing/RenderPass.js",
        "three/addons/postprocessing/UnrealBloomPass.js": "./lib/postprocessing/UnrealBloomPass.js"
      }
    }
  </script>"""

new_importmap = """  <script type="importmap">
    {
      "imports": {
        "three": "./lib/three.module.js",
        "three/addons/controls/OrbitControls.js": "./lib/controls/OrbitControls.js",
        "three/addons/postprocessing/EffectComposer.js": "./lib/postprocessing/EffectComposer.js",
        "three/addons/postprocessing/RenderPass.js": "./lib/postprocessing/RenderPass.js",
        "three/addons/postprocessing/Pass.js": "./lib/postprocessing/Pass.js",
        "three/addons/postprocessing/MaskPass.js": "./lib/postprocessing/MaskPass.js",
        "three/addons/postprocessing/ShaderPass.js": "./lib/postprocessing/ShaderPass.js",
        "three/addons/postprocessing/UnrealBloomPass.js": "./lib/postprocessing/UnrealBloomPass.js",
        "three/addons/shaders/LuminosityHighPassShader.js": "./lib/shaders/LuminosityHighPassShader.js"
      }
    }
  </script>"""

content = content.replace(old_importmap, new_importmap)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated importmap with all postprocessing and shader dependencies")
