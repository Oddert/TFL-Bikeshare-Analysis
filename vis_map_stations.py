"""
Displays a point on an OSM map for all stations with tooltips showing name and coordinates.
"""

import plotly.express as px
import pandas as pd

# Loading an OSM map with plotted points from my queried stations
# stations_path = './computed_data/osm-supplied-stations-selected-list.json'
stations_path = './computed_data/tfl-supplied-stations-list.json'
df = pd.read_json(stations_path)

fig = px.scatter_map(
    df,
    lat='lat',
    lon='lon',
    hover_data=['commonName', 'lat', 'lon'],
)

fig.show()
