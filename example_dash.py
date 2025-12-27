from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv'
)

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Dropdown(df['country'].unique(), id='dropdown-start_station'),  # type: ignore
    dcc.Graph(id='graph-content'),
]


@callback(Output('graph-content', 'figure'), Input('dropdown-start_station', 'value'))
def update_graph(value):
    dff = df[df['country'] == value]
    return px.line(dff, x='year', y='pop')


if __name__ == '__main__':
    app.run(debug=True)
