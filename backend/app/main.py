import os, sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Traffic System API", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'traffic.db'))

def query(sql, args=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, args).fetchall()
    conn.close()
    return rows

def _ok(data):
    return {"code": 0, "message": "ok", "data": data}

@app.get("/api/v1/stats/overview")
def overview():
    r = query("SELECT SUM(flow) s, AVG(avg_speed) v, COUNT(DISTINCT road_id) rd FROM traffic_flow")[0]
    return _ok({"total_flow": int(r["s"]),
                 "avg_speed": round(r["v"], 1),
                 "road_count": r["rd"], "alerts": 0})

@app.get("/api/v1/traffic/flows")
def flows(road_id: str = "R001"):
    rows = query("SELECT dt, flow FROM traffic_flow WHERE road_id=? ORDER BY dt DESC LIMIT 24", (road_id,))
    rows = list(reversed(rows))
    labels = [r["dt"][11:16] for r in rows]      # "HH:MM"
    values = [r["flow"] for r in rows]
    return _ok({"road_id": road_id, "labels": labels, "values": values})

@app.get("/")
def root():
    return {"msg": "ok, see /docs"}
