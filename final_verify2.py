import uvicorn
from backend.app.main import app
import threading
import time
import requests

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(3)

try:
    r = requests.get("http://127.0.0.1:8000/web-screen/dashboard.html")
    print("Dashboard:", r.status_code, "chars:", len(r.text))
    
    # Check for all key features
    checks = {
        "three.module.js": "lib/three.module.js" in r.text,
        "OrbitControls": "OrbitControls.js" in r.text,
        "EffectComposer": "EffectComposer.js" in r.text,
        "UnrealBloomPass": "UnrealBloomPass.js" in r.text,
        "Pass.js": "Pass.js" in r.text,
        "MaskPass.js": "MaskPass.js" in r.text,
        "ShaderPass.js": "ShaderPass.js" in r.text,
        "LuminosityHighPassShader": "LuminosityHighPassShader.js" in r.text,
        "importmap": "importmap" in r.text,
        "type=module": 'type="module"' in r.text,
        "threeScene": "threeScene" in r.text,
        "threeCamera": "threeCamera" in r.text,
        "threeRenderer": "threeRenderer" in r.text,
        "threeComposer": "threeComposer" in r.text,
        "bloomPass": "bloomPass" in r.text,
        "orbitControls": "orbitControls" in r.text,
        "globeMesh": "globeMesh" in r.text,
        "wireframeMesh": "wireframeMesh" in r.text,
        "animate": "animate()" in r.text,
        "onWindowResize": "onWindowResize" in r.text,
        "onGlobeClick": "onGlobeClick" in r.text,
        "updateRouteLines": "updateRouteLines" in r.text,
        "createRouteLine": "createRouteLine" in r.text,
        "formatTimeForGranularity": "formatTimeForGranularity" in r.text,
        "getCongestionThreeColor": "getCongestionThreeColor" in r.text,
        "echarts-gl removed": "echarts-gl" not in r.text,
        "type=module": 'type="module"' in r.text,
        "getCongestionThreeColor single": r.text.count("function getCongestionThreeColor(avgSpeed)") == 1,
        "formatTimeForGranularity single": r.text.count("function formatTimeForGranularity(dtStr)") == 1,
    }
    
    for name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    # Test all JS files load
    print("\n--- JS File Checks ---")
    for js_file in ["three.module.js", "OrbitControls.js", "EffectComposer.js", "RenderPass.js", 
                     "Pass.js", "MaskPass.js", "ShaderPass.js", "UnrealBloomPass.js", 
                     "LuminosityHighPassShader.js"]:
        r2 = requests.get(f"http://127.0.0.1:8000/web-screen/lib/postprocessing/{js_file}" if js_file != "three.module.js" and js_file != "OrbitControls.js" else 
                          f"http://127.0.0.1:8000/web-screen/lib/{js_file}" if js_file != "OrbitControls.js" else
                          f"http://127.0.0.1:8000/web-screen/lib/controls/OrbitControls.js")
        status = "OK" if r2.status_code == 200 else f"404 ({r2.status_code})"
        print(f"  {js_file}: {status}")
    
    # Check shaders
    r2 = requests.get("http://127.0.0.1:8000/web-screen/lib/shaders/LuminosityHighPassShader.js")
    print(f"  LuminosityHighPassShader.js (shaders/): {'OK' if r2.status_code == 200 else '404'}")
    
    # Test API
    r2 = requests.get("http://127.0.0.1:8000/api/v1/meta/roads")
    print(f"\nRoads API: {len(r2.json()['data'])} roads")
    
except Exception as e:
    print("Error:", e)
