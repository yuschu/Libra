import requests
import time
time.sleep(2)
r = requests.get('http://127.0.0.1:8000/api/v1/meta/roads')
data = r.json()
for road in data['data']:
    rid = road['road_id']
    name = road['name']
    coords = road['bounds_geojson']['coordinates']
    print(rid + ': ' + name)
    print('  Coords: ' + str(len(coords)) + ' points')
    for i, c in enumerate(coords[:3]):
        print('    [' + str(c[0]) + ', ' + str(c[1]) + ']')
    if len(coords) > 3:
        print('    ...')
