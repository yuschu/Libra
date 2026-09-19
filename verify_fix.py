import uvicorn
from backend.app.main import app
import threading
import time
import requests

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(2)

try:
    r = requests.get("http://127.0.0.1:8000/web-screen/dashboard.html")
    content = r.text
    
    # Check for the new debugging features
    checks = {
        "webgl check": "WebGL not supported" in content,
        "echarts version": "echarts.version" in content,
        "init logging": "console.log.*Globe.*Initialization" in content,
        "error stack": "err.stack" in content,
        "webgl renderer": "renderer: \"webgl\"" in content,
        "baseColor": "baseColor" in content,
        "outline": "outline:" in content,
    }
    
    for name, result in checks.items():
        print(f"  {name}: {result}")
    
    print()
    print("Dashboard loads successfully:", r.status_code == 200)
    
except Exception as e:
    print("Error:", e)
