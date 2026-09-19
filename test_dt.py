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
    # Test dt parameter behavior
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001")
    data = r.json()["data"]
    print("No dt - labels:", len(data["labels"]), data["labels"][:3], "...", data["labels"][-3:])
    print("No dt - values:", len(data["values"]))
    
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001&dt=2026-09-01%2000:00")
    data = r.json()["data"]
    print("dt=00:00 - labels:", len(data["labels"]), data["labels"][:3], "...", data["labels"][-3:])
    print("dt=00:00 - values:", len(data["values"]))
    
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001&dt=2026-09-01%2008:00")
    data = r.json()["data"]
    print("dt=08:00 - labels:", len(data["labels"]), data["labels"][:3], "...", data["labels"][-3:])
    
    # Test if 00:00 is in labels
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001&dt=2026-09-01%2000:00")
    data = r.json()["data"]
    has_00 = "00:00" in data["labels"]
    print("Has 00:00 in labels:", has_00)
    if has_00:
        idx = data["labels"].index("00:00")
        print("  00:00 value:", data["values"][idx])
    
except Exception as e:
    print("Error:", e)
