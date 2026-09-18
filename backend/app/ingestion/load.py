# -*- coding: utf-8 -*-
"""把 data/traffic_sample.csv 导入 SQLite（幂等：先清空再插入）。"""
import sqlite3, csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, '..', '..', 'traffic.db'))
CSV = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'data', 'traffic_sample.csv'))

conn = sqlite3.connect(DB)
conn.execute('''CREATE TABLE IF NOT EXISTS traffic_flow(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dt TEXT, road_id TEXT, flow INTEGER,
    avg_speed REAL, density REAL, weather TEXT)''')
conn.execute('CREATE INDEX IF NOT EXISTS idx_road_dt ON traffic_flow(road_id, dt)')
conn.execute('DELETE FROM traffic_flow')

with open(CSV, encoding='utf-8-sig') as f:
    rows = [(r['dt'], r['road_id'], int(r['flow']),
             float(r['avg_speed']), float(r['density']), r['weather'])
            for r in csv.DictReader(f)]

conn.executemany(
    'INSERT INTO traffic_flow(dt,road_id,flow,avg_speed,density,weather) VALUES(?,?,?,?,?,?)',
    rows)
conn.commit()
n = conn.execute('SELECT COUNT(*) FROM traffic_flow').fetchone()[0]
roads = conn.execute('SELECT COUNT(DISTINCT road_id) FROM traffic_flow').fetchone()[0]
print('DB', DB)
print('ROWS', n, 'ROADS', roads)
conn.close()
