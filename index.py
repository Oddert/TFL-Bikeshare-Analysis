import kagglehub
import pandas as pd
import lux
from lux.vis.Vis import Vis

# KAGGLEHUB_CACHE 

# Download latest version
path = kagglehub.dataset_download("kalacheva/london-bike-share-usage-dataset")

print("Path to dataset files:", path)

df = pd.read_csv('./datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv')
df

print(len(df['Start station'].unique()))
print(df.groupby(['Start station','End station']).size().reset_index().rename(columns={0:'count'}))

# Number,Start date,Start station number,Start station,End date,End station number,End station,Bike number,Bike model,Total duration,Total duration (ms)

Vis(["Start station=Kennington Lane Rail Bridge, Vauxhall","Bike number"],df)

# https://nominatim.openstreetmap.org/search?q=Glasgow&format=json&countrycodes=gb
# https://nominatim.openstreetmap.org/search?q=Kennington%20Lane%20Rail%20Bridge,%20Vauxhall&format=json&countrycodes=gb
# Kennington Lane Rail Bridge, Vauxhall
# https://api.digital.tfl.gov.uk/BikePoint/Search?query=Kennington%20Lane%20Rail%20Bridge%2C%20Vauxhall
