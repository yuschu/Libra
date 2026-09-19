import re

with open("web-screen/dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# The old globe config block
old = r"""        globe: {
          baseTexture: "https://cdn.jsdelivr.net/gh/ecomfe/echarts-gl@latest/assets/earth/land_ocean_8192.jpg",
          heightTexture: "https://cdn.jsdelivr.net/gh/ecomfe/echarts-gl@latest/assets/earth/bump_8192.jpg",
          environment: "https://cdn.jsdelivr.net/gh/ecomfe/echarts-gl@latest/assets/earth/skybox_1024.jpg",
          displacementScale: 0.05,
          shading: "realistic",
          realisticMaterial: {
            roughness: 0.8,
            metalness: 0.1
          },
          postEffect: { enable: true, bloom: { enable: true, intensity: 0.3 } },
          light: {
            main: { intensity: 1.2, shadow: true, alpha: 30, beta: 40 },
            ambient: { intensity: 0.3 },
            ambientCubemap: { texture: "https://cdn.jsdelivr.net/gh/ecomfe/echarts-gl@latest/assets/earth/skybox_1024.jpg", intensity: 0.5 }
          },
          viewControl: {
            autoRotate: true,
            autoRotateAfterStill: 3,
            distance: 20000000,
            minDistance: 1000000,
            maxDistance: 50000000,
            panMouseButton: "left",
            rotateMouseButton: "right",
            zoomMouseButton: "middle"
          }
        },"""

new = r"""        globe: {
          baseColor: "#0a1628",
          displacementScale: 0.05,
          shading: "realistic",
          realisticMaterial: {
            roughness: 0.8,
            metalness: 0.1
          },
          postEffect: { enable: true, bloom: { enable: true, intensity: 0.3 } },
          light: {
            main: { intensity: 1.2, shadow: true, alpha: 30, beta: 40 },
            ambient: { intensity: 0.3 }
          },
          viewControl: {
            autoRotate: true,
            autoRotateAfterStill: 3,
            distance: 20000000,
            minDistance: 1000000,
            maxDistance: 50000000,
            panMouseButton: "left",
            rotateMouseButton: "right",
            zoomMouseButton: "middle"
          }
        },"""

content = content.replace(old, new)

with open("web-screen/dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced globe config")
