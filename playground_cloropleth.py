import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

# Documentation link for choropleth
# https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html

# Sample structure from the queried stations list.
# {
#     "place_id": 259591180,
#     "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
#     "osm_type": "way",
#     "osm_id": 849651127,
#     "lat": "51.4974682",
#     "lon": "-0.1119261",
#     "class": "highway",
#     "type": "primary",
#     "place_rank": 26,
#     "importance": 0.24404996673231694,
#     "addresstype": "road",
#     "name": "Kennington Road",
#     "display_name": "Kennington Road, Waterloo, London Borough of Lambeth, London, Greater London, England, SE1 7BX, United Kingdom",
#     "boundingbox": [
#         "51.4972422",
#         "51.4977018",
#         "-0.1120125",
#         "-0.1118229"
#     ]
# },

# Sample dataset
data = {
    "licence": [
        # "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright"
        # Name shortened for df preview
        "test"
    ],
    "osm_type": ["way"],
    "osm_id": [849651127],
    "lat": [51.4974682],
    "lon": [-0.1119261],
    "class": ["highway"],
    "type": ["primary"],
    "place_rank": [26],
    "importance": [0.24404996673231694],
    "addresstype": ["road"],
    "name": ["Kennington Road"],
    "display_name": [
        # "Kennington Road, Waterloo, London Borough of Lambeth, London, Greater London, England, SE1 7BX, United Kingdom"
        # Name shortened for df preview
        "test"
    ],
    # "boundingbox": [["51.4972422", "51.4977018", "-0.1120125", "-0.1118229"]],
}

# df = pd.DataFrame(data)
# print(df)

# Testing with choropleth, multiple methods of rendering from inbuilt datasets.
# fig = px.choropleth(
#     df,
#     # locations='State_Code',
#     # locations='gb',
#     # locations='gb',
#     locationmode='country names',  # One of ‘ISO-3’, ‘USA-states’, or ‘country names’
#     # color='Population',
#     # hover_name='State',
#     # color_continuous_scale='Viridis',
#     scope='GB',
#     title='U.S. State Population Estimates'
# )

# Attempting to use geojson files with choropleth_map, scatter_geo, scatter_map
# All had varying degrees of success but lacked the resolution at city level. Doubtfull that it was actually paying attention to my geojson.

# # # with open('./geojson/london.json') as f:
# with open(
#     "./geojson/European_Electoral_Regions_Dec_2018_FCB_UK_2022_9019130026153749519.geojson"
# ) as f:
#     data = json.load(f)

#     # fig = px.choropleth_map(
#     #     df, geojson={"type": "FeatureCollection", "features": [data]}
#     # )

#     # fig.show()

#     fig = px.scatter_map(
#         df,
#         # geojson={"type": "FeatureCollection", "features": [data]},
#         lat='lat',
#         lon='lon',
#         hover_data=['name', 'lat', 'lon'],
#         # mapbox_style='open-street-map',
#     )
#     fig.show()

# Loading an OSM map with plotted points from my queried stations
# stations_path = './computed_data/osm-supplied-stations-selected-list.json'
stations_path = './computed_data/tfl-supplied-stations-list.json'
df = pd.read_json(stations_path)
print(df)
print(df.columns)

fig = px.scatter_map(
    df,
    lat='lat',
    lon='lon',
    hover_data=['commonName', 'lat', 'lon'],
)

fig.show()
