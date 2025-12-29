"""
Displays a point on an OSM map for all stations with tooltips showing name and coordinates.
"""

import plotly.express as px
import pandas as pd

from constants.dataset_paths import COMBINED_STATIONS

# Loading an OSM map with plotted points from my queried stations
df = pd.read_json(COMBINED_STATIONS)

fig = px.scatter_map(
    df,
    lat='lat',
    lon='lon',
    hover_data=['name', 'lat', 'lon'],
)

fig.show()
