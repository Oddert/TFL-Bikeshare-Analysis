import pandas as pd

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

dff = df.groupby('Start station')['Total duration (ms)'].apply(lambda x: x < 60000).sum()
print(dff)
