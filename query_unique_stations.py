"""
Uses the dataset kalacheva/london-bike-share-usage-dataset and generates a list of unique stations, querying their full entry from the TFL API.
"""

import json
import requests

from time import sleep

import pandas as pd

df = pd.read_csv(
    "./datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv"
)

unique_start = df["Start station"].unique()
unique_end = df["End station"].unique()

print(len(unique_start))
print(len(unique_end))

unique_total = {}

for start_station in unique_start:
    unique_total[start_station] = True

for end_station in unique_end:
    unique_total[end_station] = True

print(len(unique_total))

stations_queried = {}

app_id = "097cb67e122744e591dc5aeabfdf8883"

for i, station in enumerate(unique_total):
    url = f"https://api.tfl.gov.uk/BikePoint/Search?query={station}&app_id={app_id}"
    print(url)
    print("Count: ", i)
    response = requests.get(url, timeout=3000)
    r = response.json()
    stations_queried[station] = r
    sleep(0.3)
    print(r)

json_str = json.dumps(stations_queried)

with open("tfl-supplied-stations.json", "w", encoding="utf8") as f:
    f.write(json_str)
