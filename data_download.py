
import pandas as pd
import requests
import json
import pprint
from datetime import datetime
import datetime


# this import data from csv is commented because of the Power BI Python script connection
# cities_df = pd.read_csv('european_cities_geo.csv')
cities_data = {
    'City': ['Warsaw', 'Berlin', 'Paris', 'Madrid', 'Rome', 'Amsterdam', 'Vienna', 'Lisbon'],
    'Latitude': [52.2297, 52.52, 48.8566, 40.4168, 41.9028, 52.3676, 48.2082, 38.7169],
    'Longitude': [21.0122, 13.405, 2.3522, -3.7038, 12.4964, 4.9041, 16.3738, -9.1393]
}
cities_df = pd.DataFrame(cities_data)
cities_df.set_index(keys='City', inplace=True)

cities_dict = cities_df.to_dict('index')
current_data = []
forecast_data = []
forecast_data_df = pd.DataFrame()
forecast_temp_df = pd.DataFrame()

for city, geo in cities_dict.items():
    latitude = geo['Latitude']
    longitude = geo['Longitude']
    # get weather data from API
    link = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&"
                                                                                                f"hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
            )
    json_file = requests.get(link).json()

    # manipulate current data
    current_weather = json_file.get('current_weather', {})
    current_weather_dict: dict = json_file['current']
    # add data to dictionary
    current_weather_dict['City'] = city
    current_weather_dict['Latitude'] = latitude
    current_weather_dict['Longitude'] = longitude
    current_weather_dict.pop('interval')
    # process data
    current_weather_dict['date'] = current_weather_dict['time'].split('T')[0]
    current_weather_dict['hour'] = current_weather_dict['time'].split('T')[1]

    # delete time key
    current_weather_dict.pop('time')
    current_data.append(current_weather_dict)

    # manipulate forecast
    forecast_dict = json_file['hourly']
    # add data to dictionary
    forecast_dict['City'] = [city] * len(forecast_dict['time'])
    forecast_dict['Latitude'] = [latitude] * len(forecast_dict['time'])
    forecast_dict['Longitude'] = [longitude] * len(forecast_dict['time'])
    forecast_temp_df = pd.DataFrame(forecast_dict)
    forecast_data_df = pd.concat([forecast_data_df, forecast_temp_df])

# add current weather data to dataframe
current_data_df = pd.DataFrame(current_data)
current_data_df.rename(columns={'wind_speed_10m':'wind_speed',
                                   'relative_humidity_2m':'relative_humidity',
                                    'temperature_2m':'temperature'},
                                    inplace=True
                       )

current_time_str = current_data_df.at[0, 'hour']
current_time = datetime.datetime.strptime(current_time_str, '%H:%M').time()

forecast_data_df.rename(columns={'wind_speed_10m':'wind_speed',
                                  'relative_humidity_2m':'relative_humidity',
                                  'temperature_2m':'temperature'},
                                    inplace=True
                        )

# split time column into date and hour
forecast_data_df[['date', 'hour']] = forecast_data_df['time'].str.split('T', expand=True)
forecast_data_df['date'] = pd.to_datetime(forecast_data_df['date']).dt.date
forecast_data_df['hour'] = pd.to_datetime(forecast_data_df['hour']).dt.hour

# filter final dataframe
forecast_time_df = forecast_data_df.loc[forecast_data_df['hour'] == current_time.hour]
forecast_time_df.drop(columns='time', inplace=True)













