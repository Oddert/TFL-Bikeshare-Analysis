from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv'
)

df_bike_data = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)
df_bike_data['Start date'] = pd.to_datetime(
    df_bike_data['Start date'], format='%m/%d/%Y %H:%M'
)
df_bike_data['End date'] = pd.to_datetime(
    df_bike_data['End date'], format='%m/%d/%Y %H:%M'
)

# Extract date (day-level)
df_bike_data['date'] = df_bike_data['Start date'].dt.floor('H')  # type: ignore


app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Dropdown(df_bike_data['Start station'].unique(), id='dropdown-start_station'),  # type: ignore
    dcc.Dropdown(df_bike_data['End station'].unique(), id='dropdown-end_station'),  # type: ignore
    dcc.RadioItems(
        options=[
            {'label': 'start', 'value': 'From start station'},
            {'label': 'start-end', 'value': 'From Start to End station'},
        ],
        value='start',
        id='radio-use_stations',
    ),
    dcc.Graph(id='graph-content'),
]


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-start_station', 'value'),
    Input('dropdown-end_station', 'value'),
    Input('radio-use_stations', 'value'),
)
def update_start_station(start_station, end_station, use_stations):
    if use_stations == 'start-end':
        mask = (df_bike_data['Start station'] == start_station) & (
            df_bike_data['End station'] == end_station
        )
    else:
        mask = df_bike_data['Start station'] == start_station

    dff = df_bike_data[mask]

    hourly_agg = (
        dff.groupby('date')
        .agg(
            avg_duration_ms=('Total duration (ms)', 'mean'),
            trip_count=('Number', 'count'),
        )
        .reset_index()
    )

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

    return fig


if __name__ == '__main__':
    app.run(debug=True)
