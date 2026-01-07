from datetime import datetime

import pandas as pd

# df_bike_data = pd.read_csv(
#     './datasets/kalacheva/london-bike-share-usage-dataset/versions/1/LondonBikeJourneyAug2023.csv'
# )

df_weather = pd.read_csv(
    './datasets/zongaobian/london-weather-data-from-1979-to-2023/versions/1/london_weather_data_1979_to_2023.csv'
)

print(df_weather)

df_weather['DATE'] = pd.to_datetime(df_weather['DATE'], format='%Y%m%d')
df_weather = df_weather[(df_weather['DATE'] >= datetime(2023, 8, 1)) & (df_weather['DATE'] <= datetime(2023, 8, 31, 23, 59, 59))]

print(df_weather.size)

print('>>> Quality 0')
print('Q_TX', 'Daily maximum temperature in 0.1°C.', df_weather[df_weather['Q_TX'] == 0].size)
print('Q_TN', 'Daily minimum temperature in 0.1°C.', df_weather[df_weather['Q_TN'] == 0].size)
print('Q_TG', 'Daily mean temperature in 0.1°C.', df_weather[df_weather['Q_TG'] == 0].size)
print('Q_SS', 'Daily sunshine duration in 0.1 hours.', df_weather[df_weather['Q_SS'] == 0].size)
print('Q_SD', 'Daily snow depth in 1 cm.', df_weather[df_weather['Q_SD'] == 0].size)
print('Q_RR', 'Daily precipitation amount in 0.1 mm.', df_weather[df_weather['Q_RR'] == 0].size)
print('Q_QQ', 'Daily global radiation in W/m².', df_weather[df_weather['Q_QQ'] == 0].size)
print('Q_PP', 'Daily sea level pressure in 0.1 hPa.', df_weather[df_weather['Q_PP'] == 0].size)
print('Q_HU', 'Daily relative humidity in %.', df_weather[df_weather['Q_HU'] == 0].size)
print('Q_CC', 'Daily cloud cover in oktas.', df_weather[df_weather['Q_CC'] == 0].size)


print('>>> Quality 1')
print('Q_TX', 'Daily maximum temperature in 0.1°C.', df_weather[df_weather['Q_TX'] == 1].size)
print('Q_TN', 'Daily minimum temperature in 0.1°C.', df_weather[df_weather['Q_TN'] == 1].size)
print('Q_TG', 'Daily mean temperature in 0.1°C.', df_weather[df_weather['Q_TG'] == 1].size)
print('Q_SS', 'Daily sunshine duration in 0.1 hours.', df_weather[df_weather['Q_SS'] == 1].size)
print('Q_SD', 'Daily snow depth in 1 cm.', df_weather[df_weather['Q_SD'] == 1].size)
print('Q_RR', 'Daily precipitation amount in 0.1 mm.', df_weather[df_weather['Q_RR'] == 1].size)
print('Q_QQ', 'Daily global radiation in W/m².', df_weather[df_weather['Q_QQ'] == 1].size)
print('Q_PP', 'Daily sea level pressure in 0.1 hPa.', df_weather[df_weather['Q_PP'] == 1].size)
print('Q_HU', 'Daily relative humidity in %.', df_weather[df_weather['Q_HU'] == 1].size)
print('Q_CC', 'Daily cloud cover in oktas.', df_weather[df_weather['Q_CC'] == 1].size)



print('>>> Quality 9')
print('Q_TX', 'Daily maximum temperature in 0.1°C.', df_weather[df_weather['Q_TX'] == -9999].size)
print('Q_TN', 'Daily minimum temperature in 0.1°C.', df_weather[df_weather['Q_TN'] == 9].size)
print('Q_TG', 'Daily mean temperature in 0.1°C.', df_weather[df_weather['Q_TG'] == 9].size)
print('Q_SS', 'Daily sunshine duration in 0.1 hours.', df_weather[df_weather['Q_SS'] == 9].size)
print('Q_SD', 'Daily snow depth in 1 cm.', df_weather[df_weather['Q_SD'] == 9].size)
print('Q_RR', 'Daily precipitation amount in 0.1 mm.', df_weather[df_weather['Q_RR'] == 9].size)
print('Q_QQ', 'Daily global radiation in W/m².', df_weather[df_weather['Q_QQ'] == 9].size)
print('Q_PP', 'Daily sea level pressure in 0.1 hPa.', df_weather[df_weather['Q_PP'] == 9].size)
print('Q_HU', 'Daily relative humidity in %.', df_weather[df_weather['Q_HU'] == 9].size)
print('Q_CC', 'Daily cloud cover in oktas.', df_weather[df_weather['Q_CC'] == 9].size)


print('>>> Quality -9999')
print('Q_TX', 'Daily maximum temperature in 0.1°C.', df_weather[df_weather['Q_TX'] == -9999].size)
print('Q_TN', 'Daily minimum temperature in 0.1°C.', df_weather[df_weather['Q_TN'] == -9999].size)
print('Q_TG', 'Daily mean temperature in 0.1°C.', df_weather[df_weather['Q_TG'] == -9999].size)
print('Q_SS', 'Daily sunshine duration in 0.1 hours.', df_weather[df_weather['Q_SS'] == -9999].size)
print('Q_SD', 'Daily snow depth in 1 cm.', df_weather[df_weather['Q_SD'] == -9999].size)
print('Q_RR', 'Daily precipitation amount in 0.1 mm.', df_weather[df_weather['Q_RR'] == -9999].size)
print('Q_QQ', 'Daily global radiation in W/m².', df_weather[df_weather['Q_QQ'] == -9999].size)
print('Q_PP', 'Daily sea level pressure in 0.1 hPa.', df_weather[df_weather['Q_PP'] == -9999].size)
print('Q_HU', 'Daily relative humidity in %.', df_weather[df_weather['Q_HU'] == -9999].size)
print('Q_CC', 'Daily cloud cover in oktas.', df_weather[df_weather['Q_CC'] == -9999].size)

print('>>> Value -9999')
print('TX', 'Daily maximum temperature in 0.1°C.', df_weather[df_weather['TX'] == -9999].size)
print('TN', 'Daily minimum temperature in 0.1°C.', df_weather[df_weather['TN'] == -9999].size)
print('TG', 'Daily mean temperature in 0.1°C.', df_weather[df_weather['TG'] == -9999].size)
print('SS', 'Daily sunshine duration in 0.1 hours.', df_weather[df_weather['SS'] == -9999].size)
print('SD', 'Daily snow depth in 1 cm.', df_weather[df_weather['SD'] == -9999].size)
print('RR', 'Daily precipitation amount in 0.1 mm.', df_weather[df_weather['RR'] == -9999].size)
print('QQ', 'Daily global radiation in W/m².', df_weather[df_weather['QQ'] == -9999].size)
print('PP', 'Daily sea level pressure in 0.1 hPa.', df_weather[df_weather['PP'] == -9999].size)
print('HU', 'Daily relative humidity in %.', df_weather[df_weather['HU'] == -9999].size)
print('CC', 'Daily cloud cover in oktas.', df_weather[df_weather['CC'] == -9999].size)
