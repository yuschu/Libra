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
    
    # Check for missing dependencies
    checks = {
        "Pass.js": "Pass.js" in r.text,
        "MaskPass.js": "MaskPass.js" in r.text,
        "ShaderPass.js": "ShaderPass.js" in r.text,
        "LuminosityHighPassShader.js": "LuminosityHighPassShader.js" in r.text,
    }
    
    for name, result in checks.items():
        print(f"  {name}: {result}")
    
    # Check for duplicate function
    if r.text.count("getCongestionThreeColor") > 1:
        print("  DUPLICATE getCongestionThreeColor FOUND!")
    else:
        print("  getCongestionThreeColor: single declaration OK")
    
    # Check for any 404s in the served JS files
    for js_file in ["Pass.js", "MaskPass.js", "ShaderPass.js", "LuminosityHighPassShader.js"]:
        r2 = requests.get(f"http://127.0.0.1:8000/web-screen/lib/postprocessing/{js_file}")
        if r2.status_code == 404:
            print(f"  404: {js_file}")
        else:
            print(f"  {js_file}: OK ({len(r2.content)} bytes)")
        
    r2 = requests.get("http://127.0.0.1:8000/web-screen/lib/shaders/LuminosityHighPassShader.js")
    if r2.status_code == 404:
        print("  404: shaders/LuminosityHighPassShader.js")
    else:
        print(f"  shaders/LuminosityHighPassShader.js: OK ({len(r2.content)} bytes)")
    
except Exception as e:
    print("Error:", e)
