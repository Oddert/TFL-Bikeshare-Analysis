"""
Displays a bar chart of the top ten most common trips by number of trips counted.

Standard Plotly output.
"""

import pandas as pd

import plotly.express as px

x_axis_quant = 20

df = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)

# Verify the data read was successful.
print(df)
print('Number of unique start stations: ')
print(len(df['Start station'].unique()))
print('Number of unique end stations: ')
print(len(df['End station'].unique()))

# Create a new df which contains a list of all unique trips (origin-destination pairs) and the quantity counts for each.
df_unique_od = (
    df.groupby(['Start station', 'End station'])
    .size()
    .reset_index()
    .rename(columns={0: 'count'})
)

df_sorted = df_unique_od.sort_values('count', ascending=False).reset_index().head(x_axis_quant)
print(df_sorted)

fig = px.bar(df_sorted, x='Start station', y='count')

fig.show()
