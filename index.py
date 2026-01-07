import kagglehub
import pandas as pd

import plotly.express as px

from lux.vis.Vis import Vis

# Set this variable to determine the location of the dataset download: KAGGLEHUB_CACHE

# Download latest version of the main dataset.
path = kagglehub.dataset_download('kalacheva/london-bike-share-usage-dataset')

print('Path to dataset files:', path)

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

# Take a precursory glance at all trips which only appear once, twice, etc up to 10, assuming a quick drop-off.
# The results are noted in commas following for quick reference, do not assume these are unchanged.
print('Dataframe unique Origin-Destination pairs:')
print(df_unique_od)
print('1 trip occurrences: ', df_unique_od['count'].value_counts().get(1))  # 76943
print('2 trip occurrences: ', df_unique_od['count'].value_counts().get(2))  # 36612
print('3 trip occurrences: ', df_unique_od['count'].value_counts().get(3))  # 20516
print('4 trip occurrences: ', df_unique_od['count'].value_counts().get(4))  # 13231
print('5 trip occurrences: ', df_unique_od['count'].value_counts().get(5))  # 9195
print('6 trip occurrences: ', df_unique_od['count'].value_counts().get(6))  # 6403
print('7 trip occurrences: ', df_unique_od['count'].value_counts().get(7))  # 4907
print('8 trip occurrences: ', df_unique_od['count'].value_counts().get(8))  # 3871
print('9 trip occurrences: ', df_unique_od['count'].value_counts().get(9))  # 2988
print('10 trip occurrences: ', df_unique_od['count'].value_counts().get(10))  # 2439
# Total <= 10 trips: 177105
# Total > 10 trips: 191630 - 177105 = 14525

# Column headers reference:
# Number,Start date,Start station number,Start station,End date,End station number,End station,Bike number,Bike model,Total duration,Total duration (ms)

# Take the largest number of repeat trips for reference (York Way, KX).
print('Max repeat values: ', df_unique_od.max())

kx = 'Serpentine Car Park, Hyde Park'

# Find a subset of data matching YW, Kings Cross as a start station.
# This will for the basis of later queries examining the validity of this subset.
print('All from KX: ')
print(df.loc[df['Start station'] == kx])

# We assume that trips under 60 seconds are potential "false starts".
# Select how many fall into this category.
print('All from KX under 1 minute: ')
print(
    df.loc[df['Start station'] == kx]['Total duration (ms)']
    .apply(lambda x: x < 60000)
    .sum()
)

# Given very few are potential "false starts", we must assume these are circular trips.
# How many unique OD trips are circular?
print('Unique Start station and End station are the same: ')
print(
    df_unique_od.loc[
        df_unique_od['Start station'] == df_unique_od['End station']
    ].reset_index()
)

# How many trips are circular in the entire dataset?
print('Full DF Start station and End station are the same: ')
print(df.loc[df['Start station'] == df['End station']].reset_index())

# Of this, how many are potential "false starts"?
print('Full DF Start station and End station are the same and less than 60 seconds: ')
print(
    df.loc[df['Start station'] == df['End station']]['Total duration (ms)']
    .apply(lambda x: x < 60000)
    .sum()
)

# Create a simple scatter plot of the unique OR trip df.
x = []
y = []

# Given the maximum value from `df_unique_od.max()` set the max x-axis of the chart to 3000. Ignore 0 as there cannot be 0 trips.
for i in range(1, 3000):
    # Loop over the trip quantity, query how many counts there are in the unique OD set.
    x.append(i)
    y_val = int(df_unique_od['count'].value_counts().get(i, 0))
    y.append(y_val)

# Given the steep x-axis drop off, we'll cut the graph at 145 to focus on the lower end.
cut_off = 145

x_left = x[:cut_off]
x_right = x[cut_off:]
y_left = y[:cut_off]
y_right = y[cut_off:]

# Create a table of the outliers for interest.
outliers = []

for idx, x_val in enumerate(x_right):
    if y_right[idx] != 0:
        outliers.append((x_val, y_right[idx]))

print(f'outliers ({len(outliers)}): ', outliers)

df_outliers = pd.DataFrame(
    outliers, columns=['Number of repetitions', 'Quantity of trips']
)

print('Outliers df:')
print(df_outliers)

# Show the graph
# fig = px.scatter(
#     x=x_left,
#     y=y_left,
#     title="Frequency of Repeat Trips",
#     labels={"x": "Number of repeat trips", "y": "Quantity of trips"},
# )
# fig.show()

Vis(['Start station=Kennington Lane Rail Bridge, Vauxhall', 'Bike number'], df)

# https://nominatim.openstreetmap.org/search?q=Glasgow&format=json&countrycodes=gb
# https://nominatim.openstreetmap.org/search?q=Kennington%20Lane%20Rail%20Bridge,%20Vauxhall&format=json&countrycodes=gb
# Kennington Lane Rail Bridge, Vauxhall
# https://api.digital.tfl.gov.uk/BikePoint/Search?query=Kennington%20Lane%20Rail%20Bridge%2C%20Vauxhall

plot2 = px.scatter(df, x='Start date', y='Total duration (ms)')
plot2.show()
