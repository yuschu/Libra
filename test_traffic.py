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
    # Test traffic data for different time frames
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001")
    data = r.json()["data"]
    print("R001 24h labels:", data["labels"][:5], "...")
    print("R001 24h values:", data["values"][:5], "...")
    
    # Test specific time frame
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001&dt=2026-09-01%2008:00")
    print("R001 08:00:", r.json())
    
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001&dt=2026-09-01%2020:00")
    print("R001 20:00:", r.json())
    
    # Test other roads
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R002")
    data = r.json()["data"]
    print("R002 values:", data["values"][:5], "...")
    
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R003")
    data = r.json()["data"]
    print("R003 values:", data["values"][:5], "...")
    
except Exception as e:
    print("Error:", e)
