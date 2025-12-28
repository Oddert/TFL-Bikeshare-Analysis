"""
Downloads and joins the weather dataset to the main bike-share dataset.

Depending on comments, plots either the trip count or duration versus Precipitation.

Standard Plotly output.
"""

import kagglehub

import pandas as pd
import plotly.graph_objects as go

path = kagglehub.dataset_download('zongaobian/london-weather-data-from-1979-to-2023')
print(path)

df_weather = pd.read_csv(
    './datasets/zongaobian/london-weather-data-from-1979-to-2023/versions/1/london_weather_data_1979_to_2023.csv'
)

# DATE: Date in YYYYMMDD format.
# TX: Daily maximum temperature in 0.1°C.
# TN: Daily minimum temperature in 0.1°C.
# TG: Daily mean temperature in 0.1°C.
# SS: Daily sunshine duration in 0.1 hours.
# SD: Daily snow depth in 1 cm.
# RR: Daily precipitation amount in 0.1 mm.
# QQ: Daily global radiation in W/m².
# PP: Daily sea level pressure in 0.1 hPa.
# HU: Daily relative humidity in %.
# CC: Daily cloud cover in oktas.

df_weather['date_formatted'] = pd.to_datetime(df_weather['DATE'], format='%Y%m%d')

print('>>> df_weather')
print(df_weather)
print(df_weather.columns)
df_bike_data = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)
# Ensure Start date is parsed as datetime
df_bike_data['Start date'] = pd.to_datetime(df_bike_data['Start date'])

print('>>> df_bike_data')
print(df_bike_data)
print(df_bike_data.columns)

# Extract date (day-level)
df_bike_data['date_hour'] = df_bike_data['Start date'].dt.floor('h')  # type: ignore
df_bike_data['date_day'] = df_bike_data['Start date'].dt.floor('d')  # type: ignore

df_merged = pd.merge(
    left=df_bike_data,
    right=df_weather,
    left_on=['date_day'],
    right_on=['date_formatted'],
)

print('>>> df_merged')
print(df_merged)
print(df_merged.columns)

# dff = df_bike_data[df_bike_data['Start station'] == 'Euston Road, Euston'].reset_index()

# print(dff)

hourly_agg = (
    df_merged.groupby('date_hour')
    # df_bike_data.groupby(['date_hour', 'Start station', 'End station'])
    .agg(
        avg_duration_ms=('Total duration (ms)', 'mean'),
        trip_count=('Number', 'count'),
        rain=('RR', 'mean'),
    )
    .reset_index()
)


fig = go.Figure()

# fig.add_trace(
#     go.Scatter(
#         x=hourly_agg['date_hour'],
#         y=hourly_agg['avg_duration_ms'],
#         mode='lines',
#         name='Average Trip Duration (ms)',
#         yaxis='y1',
#     )
# )

fig.add_trace(
    go.Scatter(
        x=hourly_agg['date_hour'],
        y=hourly_agg['trip_count'],
        mode='lines',
        name='Trips Started',
        yaxis='y1',
    )
)

fig.add_trace(
    go.Scatter(
        x=hourly_agg['date_hour'],
        y=hourly_agg['rain'],
        mode='lines',
        name='Precipitation',
        yaxis='y2',
    )
)

fig.update_layout(
    title='Average Trip Duration and Trip Volume per Hour (August 2023)',
    xaxis=dict(title='hour'),
    yaxis=dict(title='Average Trip Duration (ms)', side='left'),
    yaxis2=dict(title='Number of Trips Started', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99),
)

fig.show()
