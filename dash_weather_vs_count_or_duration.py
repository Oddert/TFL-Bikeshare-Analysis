""" """

from dash import callback, Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objects as go

weather_keys = {
    'TX': 'Daily maximum temperature in 0.1°C.',
    'TN': 'Daily minimum temperature in 0.1°C.',
    'TG': 'Daily mean temperature in 0.1°C.',
    'SS': 'Daily sunshine duration in 0.1 hours.',
    'SD': 'Daily snow depth in 1 cm.',
    'RR': 'Daily precipitation amount in 0.1 mm.',
    'QQ': 'Daily global radiation in W/m².',
    'PP': 'Daily sea level pressure in 0.1 hPa.',
    'HU': 'Daily relative humidity in %.',
    'CC': 'Daily cloud cover in oktas.',
}

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

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
    'font-size': '13px',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

sidebar = html.Div(
    [
        html.H2('Trip Data'),
        dcc.RadioItems(
            options=[
                {'label': 'Trip count', 'value': 'count'},
                {'label': 'Avg. Duration', 'value': 'duration'},
            ],
            value='count',
            id='radio-compare',
        ),
        html.Hr(),
        html.H2('Weather Data'),
        dcc.RadioItems(
            options=[
                {'value': value, 'label': label}
                for value, label in weather_keys.items()
            ],
            value='RR',
            id='radio-weather',
        ),
        html.Hr(),
        html.H2('Mode'),
        dcc.RadioItems(
            options=[
                {'value': 'all', 'label': 'All data'},
                {'value': 'station', 'label': 'By start station'},
            ],
            value='all',
            id='radio-mode',
        ),
        dcc.Dropdown(
            df_bike_data['Start station'].unique(),  # type: ignore
            id='dropdown-start_station',
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = [
    html.H1(
        children='Weather events vs Trips whole month', style={'textAlign': 'center'}
    ),
    sidebar,
    html.Div(
        dcc.Graph(id='graph-content'),
        style=CONTENT_STYLE,
    ),
]

print('>>> df_merged')
print(df_merged)
print(df_merged.columns)

# dff = df_bike_data[df_bike_data['Start station'] == 'Euston Road, Euston'].reset_index()

# print(dff)


@callback(
    Output('graph-content', 'figure'),
    Input('radio-compare', 'value'),
    Input('radio-weather', 'value'),
    Input('radio-mode', 'value'),
    Input('dropdown-start_station', 'value'),
)
def graph(compare_mode: str, weather: str, mode: str, start_station: str):
    if mode == 'station':
        mask = df_bike_data['Start station'] == start_station
        dff = df_merged[mask]
    else:
        dff = df_merged

    hourly_agg = (
        dff.groupby('date_hour')
        # df_bike_data.groupby(['date_hour', 'Start station', 'End station'])
        .agg(
            avg_duration_ms=('Total duration (ms)', 'mean'),
            trip_count=('Number', 'count'),
            weather_agg=(weather, 'mean'),
        )
        .reset_index()
    )

    fig = go.Figure()

    y1_label = ''

    if compare_mode == 'duration':
        y1_label = 'Average Trip Duration (ms)'
        fig.add_trace(
            go.Scatter(
                x=hourly_agg['date_hour'],
                y=hourly_agg['avg_duration_ms'],
                mode='lines',
                name=y1_label,
                yaxis='y1',
            )
        )
    else:
        y1_label = 'Trips Started'
        fig.add_trace(
            go.Scatter(
                x=hourly_agg['date_hour'],
                y=hourly_agg['trip_count'],
                mode='lines',
                name=y1_label,
                yaxis='y1',
            )
        )

    fig.add_trace(
        go.Scatter(
            x=hourly_agg['date_hour'],
            y=hourly_agg['weather_agg'],
            mode='lines',
            name=weather_keys[weather],
            yaxis='y2',
        )
    )

    fig.update_layout(
        title='Average Trip Duration and Trip Volume per Hour (August 2023)',
        xaxis=dict(title='hour'),
        yaxis=dict(title=y1_label, side='left'),
        yaxis2=dict(title=weather_keys[weather], overlaying='y', side='right'),
        legend=dict(x=0.01, y=0.99),
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
