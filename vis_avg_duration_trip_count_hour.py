import pandas as pd
import plotly.graph_objects as go

df_bike_data = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)
# Ensure Start date is parsed as datetime
df_bike_data['Start date'] = pd.to_datetime(df_bike_data['Start date'])

# Extract date (day-level)
df_bike_data['date'] = df_bike_data['Start date'].dt.floor('H')  # type: ignore
# df_bike_data['date'] = df_bike_data['Start date'].dt.floor('d')  # type: ignore

hourly_agg = (
    df_bike_data.groupby('date')
    # df_bike_data.groupby(['date', 'Start station', 'End station'])
    .agg(
        avg_duration_ms=('Total duration (ms)', 'mean'), trip_count=('Number', 'count')
    )
    .reset_index()
)

print(hourly_agg)
print(hourly_agg.columns)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=hourly_agg['date'],
        y=hourly_agg['avg_duration_ms'],
        mode='lines',
        name='Average Trip Duration (ms)',
        yaxis='y1',
    )
)

fig.add_trace(
    go.Scatter(
        x=hourly_agg['date'],
        y=hourly_agg['trip_count'],
        mode='lines',
        name='Trips Started',
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
