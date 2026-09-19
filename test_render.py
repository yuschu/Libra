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
    print("Dashboard:", r.status_code, "chars:", len(r.text))
    
    has_webgl = "renderer: \"webgl\"" in r.text
    print("renderer=webgl:", has_webgl)
    
    r = requests.get("http://127.0.0.1:8000/api/v1/meta/roads")
    print("Roads:", len(r.json()["data"]))
    
    r = requests.get("http://127.0.0.1:8000/api/v1/traffic/flows?road_id=R001")
    data = r.json()["data"]
    print("Flows R001:", len(data["values"]), "values")
    
except Exception as e:
    print("Error:", e)
