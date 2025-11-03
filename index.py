import kagglehub
import pandas as pd
import numpy as np
import lux
from lux.vis.Vis import Vis
import plotly.express as px

# KAGGLEHUB_CACHE

# Download latest version
path = kagglehub.dataset_download("kalacheva/london-bike-share-usage-dataset")

print("Path to dataset files:", path)

df = pd.read_csv(
    "./datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv"
)
df

print(len(df["Start station"].unique()))
df2 = (
    df.groupby(["Start station", "End station"])
    .size()
    .reset_index()
    .rename(columns={0: "count"})
)
print(df2)
print('1 trip occurrences: ', df2["count"].value_counts().get(1))  # 76943
print('2 trip occurrences: ', df2["count"].value_counts().get(2))  # 36612
print('3 trip occurrences: ', df2["count"].value_counts().get(3))  # 20516
print('4 trip occurrences: ', df2["count"].value_counts().get(4))  # 13231
print('5 trip occurrences: ', df2["count"].value_counts().get(5))  # 9195
print('6 trip occurrences: ', df2["count"].value_counts().get(6))  # 6403
print('7 trip occurrences: ', df2["count"].value_counts().get(7))  # 4907
print('8 trip occurrences: ', df2["count"].value_counts().get(8))  # 3871
print('9 trip occurrences: ', df2["count"].value_counts().get(9))  # 2988
print('10 trip occurrences: ', df2["count"].value_counts().get(10))  # 2439
# Total: 177105
# More then 10: 191630 - 177105 = 14525

# Number,Start date,Start station number,Start station,End date,End station number,End station,Bike number,Bike model,Total duration,Total duration (ms)
kx = 'York Way, Kings Cross'
print('Max repeat values: ', df2.max())
print('All from KX: ')
print(df.loc[df['Start station'] == kx])
print('All from KX under 1 minute: ')
print(df.loc[df['Start station'] == kx]['Total duration (ms)'].apply(lambda x: x < 60000).sum())
print('Unique Start station and End station are the same: ')
print(df2.loc[df2['Start station'] == df2['End station']].reset_index())
print('Full DF Start station and End station are the same: ')
print(df.loc[df['Start station'] == df['End station']].reset_index())
print('Full DF Start station and End station are the same and less than 60 seconds: ')
print(df.loc[df['Start station'] == df['End station']]['Total duration (ms)'].apply(lambda x: x < 60000).sum())

x = []
y = []
test = 0

for i in range(1, 3000):
    x.append(i)
    y_val = int(df2["count"].value_counts().get(i, 0))
    y.append(y_val)
    test =  test + y_val

cut_off = 145

x_left = x[:cut_off]
x_right = x[cut_off:]
y_left = y[:cut_off]
y_right = y[cut_off:]

outliers = []

for idx, x_val in enumerate(x_right):
    if y_right[idx] != 0:
        outliers.append((x_val, y_right[idx]))

print(f'outliers ({len(outliers)}): ', outliers)

fig = px.scatter(x=x_left, y=y_left)
fig.show()

Vis(["Start station=Kennington Lane Rail Bridge, Vauxhall", "Bike number"], df)

# https://nominatim.openstreetmap.org/search?q=Glasgow&format=json&countrycodes=gb
# https://nominatim.openstreetmap.org/search?q=Kennington%20Lane%20Rail%20Bridge,%20Vauxhall&format=json&countrycodes=gb
# Kennington Lane Rail Bridge, Vauxhall
# https://api.digital.tfl.gov.uk/BikePoint/Search?query=Kennington%20Lane%20Rail%20Bridge%2C%20Vauxhall

76943 + 36612 + 20516 + 13231 + 9195 + 6403 + 4907 + 3871 + 2988 + 2439