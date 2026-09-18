# -*- coding: utf-8 -*-
import csv, random
from datetime import datetime, timedelta

random.seed(42)
out = r'D:\InformationTechnologyStudy\traffic-system\data\traffic_sample.csv'
roads = ['R001', 'R002', 'R003']
weathers = ['晴', '晴', '晴', '阴', '阴', '小雨']
start = datetime(2026, 9, 1, 0, 0)

rows = []
for day in range(7):
    for hour in range(24):
        t = start + timedelta(days=day, hours=hour)
        peak = (7 <= hour <= 9) or (17 <= hour <= 19)
        for r in roads:
            base = 420 if peak else 150
            flow = max(20, int(base + random.gauss(0, 35)))
            speed = round(55 - flow/12 + random.gauss(0, 2), 1)
            speed = max(8.0, speed)
            density = round(min(1.0, flow/520.0), 2)
            rows.append([t.strftime('%Y-%m-%d %H:%M'), r, flow, speed, density, random.choice(weathers)])

with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['dt', 'road_id', 'flow', 'avg_speed', 'density', 'weather'])
    w.writerows(rows)
print('ROWS', len(rows), out)
