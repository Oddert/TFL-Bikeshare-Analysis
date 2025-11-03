"""
Intakes the result of the TFL API searches, finds entries which are missing from the TFL API, and attempts to requery them using the Open Street Map API.

Depends on the output from `query_unique_stations.py`.
"""

import json
from time import sleep

import requests

from constants.dataset_paths import OSM_STATIONS, TFL_STATIONS

stations_no_result = {}

with open(TFL_STATIONS, "r", encoding="utf8") as f:
    print(f)
    queried_stations = json.load(f)
    print(queried_stations)

    for i, item in enumerate(queried_stations):
        # print('-------')
        # print(item)
        if len(queried_stations[item]) == 0:
            stations_no_result[item] = queried_stations[item]
            # print('no items')

print("---------")
print("Number of stations with no response from the TFL API: ", len(stations_no_result))
print(stations_no_result)

requeried_stations = {}

for station in stations_no_result:
    print(f'Attempting OpenStreetMap query for "{station}"')
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={station}&format=json&countrycodes=gb"
        response = requests.get(
            url, timeout=3000, headers={"User-Agent": "robyn veitch"}
        )
        print(response)
        sleep(5)
        requeried_stations[station] = response.json()
    except Exception as ex:
        print(ex)

print(requeried_stations)

full_response_json_str = json.dumps(requeried_stations)

with open(OSM_STATIONS, "w", encoding="utf8") as f:
    f.write(full_response_json_str)
