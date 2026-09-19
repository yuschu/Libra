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
    # Test dashboard loads
    r = requests.get("http://127.0.0.1:8000/web-screen/dashboard.html")
    print("Dashboard:", r.status_code, "chars:", len(r.text))
    
    # Check key fixes
    has_baseColor = "baseColor" in r.text
    has_outline = "outline:" in r.text
    has_distance_8M = "distance: 8000000" in r.text
    has_try_catch = "try {" in r.text and "catch (err)" in r.text
    has_timeRange_defaults = "timeRange.start" in r.text
    
    print("baseColor:", has_baseColor)
    print("outline:", has_outline)
    print("distance 8M:", has_distance_8M)
    print("try/catch:", has_try_catch)
    print("timeRange defaults:", has_timeRange_defaults)
    
    # Test API
    r = requests.get("http://127.0.0.1:8000/api/v1/meta/roads")
    print("Roads:", len(r.json()["data"]))
    
except Exception as e:
    print("Error:", e)
