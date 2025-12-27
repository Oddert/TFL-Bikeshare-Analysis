import pandas as pd

import plotly.express as px

df = pd.read_csv(
    './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
)

# Create a new df which contains a list of all unique trips (origin-destination pairs) and the quantity counts for each.
df_sorted = (
    df.groupby(['Start station'])
    .size()
    .reset_index()
    .rename(columns={0: 'count'})
    .sort_values('count', ascending=False)
    .reset_index()
)
print(df_sorted)

px.bar(df_sorted, x='Start station', y='count')
