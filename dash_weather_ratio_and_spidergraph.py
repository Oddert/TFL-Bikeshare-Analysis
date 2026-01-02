""" """

from datetime import datetime
from typing import List

from dash import callback, Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from constants.dataset_paths import COMBINED_STATIONS

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

df_stations = pd.read_json(COMBINED_STATIONS)

print('>>> df_weather')
print(df_weather)
print(df_weather.columns)
df_bike_data_read = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)

df_bike_data = pd.merge(
    df_bike_data_read,
    df_stations,
    left_on=['Start station'],
    right_on=['bikeDataStationName'],
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

test = df_merged['date_day'].unique()
print('>> test', test)

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
        dcc.Checklist(
            [{'value': 'use_ratio', 'label': 'Show weather metric as ratio'}],
            value=['use_ratio'],
            id='checkbox-use_ratio',
        ),
        html.Hr(),
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
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        dcc.RangeSlider(1, 31, 1, value=[1, 31], id='range-date'),
        dcc.Graph(id='graph-line'),
        dcc.Graph(id='graph-scatter'),
    ],
    style=CONTENT_STYLE,
)

app.layout = [
    html.H1(
        children='Weather events vs Trips whole month', style={'textAlign': 'center'}
    ),
    sidebar,
    content,
]

print('>>> df_merged')
print(df_merged)
print(df_merged.columns)


@callback(
    Output('graph-line', 'figure'),
    Output('graph-scatter', 'figure'),
    Input('radio-compare', 'value'),
    Input('radio-weather', 'value'),
    Input('radio-mode', 'value'),
    Input('dropdown-start_station', 'value'),
    Input('checkbox-use_ratio', 'value'),
    Input('range-date', 'value'),
)
def graph(
    compare_mode: str,
    weather: str,
    mode: str,
    start_station: str,
    use_ratio: List[str],
    range_date: List[int],
):
    print('--------------------------------------------------------------')
    start_date = datetime(2023, 8, range_date[0])
    end_date = datetime(2023, 8, range_date[1], 23, 59, 59)

    print('start date: ', start_date)
    print('end date: ', end_date)

    date_mask = (df_merged['date_day'] >= start_date) & (
        df_merged['date_day'] <= end_date
    )

    if mode == 'station':
        mask = (df_merged['Start station'] == start_station) & date_mask
        dff = df_merged[mask]
    else:
        dff = df_merged[date_mask]

    y1_label = (
        'Average Trip Duration (ms)' if compare_mode == 'duration' else 'Trips Started'
    )
    trip_key = 'avg_duration_ms' if compare_mode == 'duration' else 'trip_count'

    print('>>> dff')
    print(dff)
    print(dff.columns)

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

    hourly_agg['ratio'] = hourly_agg[trip_key] / hourly_agg['weather_agg']

    fig_line = go.Figure()

    fig_line.add_trace(
        go.Scatter(
            x=hourly_agg['date_hour'],
            y=hourly_agg[trip_key],
            mode='lines',
            name=y1_label,
            yaxis='y1',
        )
    )

    fig_line.add_trace(
        go.Scatter(
            x=hourly_agg['date_hour'],
            y=hourly_agg['ratio' if 'use_ratio' in use_ratio else 'weather_agg'],
            mode='lines',
            name=weather_keys[weather],
            yaxis='y2',
        )
    )

    fig_line.update_layout(
        title='Average Trip Duration and Trip Volume per Hour (August 2023)',
        xaxis=dict(title='hour'),
        yaxis=dict(title=y1_label, side='left'),
        yaxis2=dict(title=weather_keys[weather], overlaying='y', side='right'),
        legend=dict(x=0.01, y=0.99),
    )

    fig_scatter = px.scatter_map(
        df_stations,
        lat='lat',
        lon='lon',
        hover_data=['name', 'lat', 'lon'],
    )

    if mode == 'station':
        df_scatter_filter = dff[dff['Start station'] == start_station]
        df_scatter_grouped = (
            df_scatter_filter.groupby(['Start station', 'End station'])
            .size()
            .reset_index()
            .rename(columns={0: 'count'})
        )
        df_scatter = pd.merge(
            df_scatter_grouped,
            df_stations,
            left_on=['End station'],
            right_on=['bikeDataStationName'],
        )

        print('>>> df_scatter')
        print(df_scatter)
        print(df_scatter.size)
        print(df_scatter.columns)

        # Enable if only stations within mask are required, otherwise all stations will be rendered.
        # fig_scatter = px.scatter_map(
        #     df_scatter,
        #     lat='lat',
        #     lon='lon',
        #     hover_data=['name', 'lat', 'lon'],
        # )

        start_station_data = df_stations[
            df_stations['bikeDataStationName'] == start_station
        ].reset_index()
        if len(start_station_data):
            start_station_data = start_station_data.iloc[0]

            for i in range(len(df_scatter)):
                fig_scatter.add_trace(
                    go.Scattermap(
                        # locationmode = 'USA-states',
                        lon=[start_station_data['lon'], df_scatter['lon'][i]],
                        lat=[start_station_data['lat'], df_scatter['lat'][i]],
                        mode='lines',
                        # line=dict(width=1, color='red'),
                        opacity=1,
                        # opacity=float(df_combined['cnt'][i])
                        # / float(df_combined['cnt'].max()),
                    )
                )

        pass

    # df_unique_od = (
    #     df_bike_data.groupby(['Start station'])
    #     .size()
    #     .reset_index()
    #     .rename(columns={0: 'count'})
    #     .sort_values('count', ascending=False)
    # )
    # print(df_unique_od)
    # fig.update_xaxes(rangeslider_visible=True)

    return fig_line, fig_scatter


if __name__ == '__main__':
    app.run(debug=True)
