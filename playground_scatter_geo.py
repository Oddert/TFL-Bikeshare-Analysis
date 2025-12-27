from datetime import datetime

import plotly.graph_objects as go
import pandas as pd

df_bike_data = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)
df_bike_data['Start date'] = pd.to_datetime(df_bike_data['Start date'], format='%m/%d/%Y %H:%M')
df_bike_data['End date'] = pd.to_datetime(df_bike_data['End date'], format='%m/%d/%Y %H:%M')

target_start_date = datetime.strptime('8/5/2023 0:00', '%m/%d/%Y %H:%M')
target_end_date = datetime.strptime('8/5/2023 23:59', '%m/%d/%Y %H:%M')

# # Filter on a specific day
# mask = (df_bike_data['Start date'] > target_start_date) & (df_bike_data['End date'] < target_end_date)
# df_bike_data = df_bike_data.loc[mask]

# Filter by start station
mask = df_bike_data['Start station'] == 'Kennington Lane Rail Bridge, Vauxhall'
df_bike_data = df_bike_data.loc[mask]

print('>>> [df_bike_data]')
print(df_bike_data)
print(df_bike_data.columns)

stations_path = './computed_data/tfl-supplied-stations-list.json'
df_stations_start = pd.read_json(stations_path)
df_stations_start.rename(columns={'lat': 'start_lat', 'lon': 'start_lon'}, inplace=True)
df_stations_end = pd.read_json(stations_path)
df_stations_end.rename(columns={'lat': 'end_lat', 'lon': 'end_lon'}, inplace=True)

print('>>> [df_stations_start]')
print(df_stations_start)
print(df_stations_start.columns)
print('>>> [df_stations_end]')
print(df_stations_end)
print(df_stations_end.columns)

df_combined1 = pd.merge(
    df_bike_data,
    df_stations_start,
    how='inner',
    left_on=['Start station'],
    right_on=['commonName'],
)

print('>>> [df_combined1]')
print(df_combined1)
print(df_combined1.columns)

df_combined2 = pd.merge(
    df_bike_data,
    df_stations_end,
    how='inner',
    left_on=['End station'],
    right_on=['commonName'],
)

print('>>> [df_combined2]')
print(df_combined2)
print(df_combined2.columns)

df_combined = pd.merge(
    df_combined1,
    df_combined2,
    how='inner',
    # left_on=['Number'],
    # right_on=['Number'],
    left_on=[
        'Number',
        'Start date',
        'Start station number',
        'Start station',
        'End date',
        'End station number',
        'End station',
        'Bike number',
        'Bike model',
        'Total duration',
        'Total duration (ms)',
    ],
    right_on=[
        'Number',
        'Start date',
        'Start station number',
        'Start station',
        'End date',
        'End station number',
        'End station',
        'Bike number',
        'Bike model',
        'Total duration',
        'Total duration (ms)',
    ],
)

print('>>> [df_combined]')
print(df_combined)
print(df_combined.columns)

fig = go.Figure()

fig.add_trace(
    go.Scattermap(
        # locationmode = 'USA-states',
        lon=df_stations_start['start_lon'],
        lat=df_stations_start['start_lat'],
        hoverinfo='text',
        text=df_stations_start['commonName'],
        mode='markers',
        marker=dict(
            size=2,
            color='rgb(255, 0, 0)',
            # line=dict(width=3, color='rgba(68, 68, 68, 0)'),
        ),
    )
)

# flight_paths = []
# for i in range(10):
for i in range(len(df_combined)):
    print('\nadding', df_combined['Number'][i])
    # print('from', df_combined['Start station'][i], df_combined['start_lat'][i], df_combined['start_lon'][i])
    # print('to', df_combined['End station'][i], df_combined['end_lat'][i], df_combined['end_lon'][i])
    print(df_combined['start_lon'][i], df_combined['end_lon'][i])
    print(df_combined['start_lat'][i], df_combined['end_lat'][i])
    fig.add_trace(
        go.Scattermap(
            # locationmode = 'USA-states',
            lon=[df_combined['start_lon'][i], df_combined['end_lon'][i]],
            lat=[df_combined['start_lat'][i], df_combined['end_lat'][i]],
            mode='lines',
            # line=dict(width=1, color='red'),
            opacity=1,
            # opacity=float(df_combined['cnt'][i])
            # / float(df_combined['cnt'].max()),
        )
    )

fig.update_layout(
    title_text='Aug. 2023 London Bike-Share Usage<br>(Hover for airport names)',
    showlegend=False,
    geo=dict(
        scope='europe',
        projection_type='azimuthal equal area',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(148, 148, 148)',
    ),
)

fig.show()
