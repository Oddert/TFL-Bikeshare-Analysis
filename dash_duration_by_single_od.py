"""
Presents a line graph for trip duration by time for two selected stations.

Creates a Dash app.
"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
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

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(
        children='Trip duration for Start and End Station',
        style={'textAlign': 'center'},
    ),
    dcc.Dropdown(df_bike_data['Start station'].unique(), id='dropdown-start_station'),  # type: ignore
    dcc.Dropdown(df_bike_data['End station'].unique(), id='dropdown-end_station'),  # type: ignore
    dcc.Graph(id='graph-content'),
]


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-start_station', 'value'),
    Input('dropdown-end_station', 'value'),
)
def update_start_station(start_station, end_station):
    mask = (df_bike_data['Start station'] == start_station) & (
        df_bike_data['End station'] == end_station
    )
    dff = df_bike_data[mask]
    dff.sort_values(by='Start date', inplace=True, ascending=False)
    # dff.groupby(pd.Grouper(key='Start date', axis=0, freq='2D', sort=True)).sum()
    # print(dff.groupby(dff['Start date'].dt.day)['Total duration'].mean())
    print(dff)
    return px.line(dff, x='Start date', y='Total duration')


if __name__ == '__main__':
    app.run(debug=True)
