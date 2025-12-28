"""
Produces a line graph showing the average trip duration, grouped per day, across the entire time series.

Standard Plotly output.
"""

import pandas as pd

import plotly.express as px


df_bike_data = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)
# Ensure Start date is parsed as datetime
df_bike_data['Start date'] = pd.to_datetime(df_bike_data['Start date'])

# Extract date (day-level)
df_bike_data['date'] = df_bike_data['Start date'].dt.date  # type: ignore

start_station = 'Abbey Orchard Street, Westminster'
end_station = 'Albert Gate, Hyde Park'

mask = (df_bike_data['Start station'] == start_station) & (
    df_bike_data['End station'] == end_station
)

# Group by day and compute average duration in ms
daily_avg_duration = df_bike_data.groupby('date', as_index=False)[
    'Total duration (ms)'
].mean()

# Create line chart
fig = px.line(
    daily_avg_duration,
    x='date',
    y='Total duration (ms)',
    title='Average Bike Trip Duration per Day (August 2023)',
    labels={'date': 'Date', 'Total duration (ms)': 'Average Trip Duration (ms)'},
)

fig.show()
