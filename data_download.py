
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
hourly_data_df = pd.DataFrame()
hourly_temp_df = pd.DataFrame()
daily_temp_df = pd.DataFrame()
daily_data_df = pd.DataFrame()


for city, geo in cities_dict.items():
    latitude = geo['Latitude']
    longitude = geo['Longitude']
    # get weather data from API
    link = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_gusts_10m,is_day,snowfall,rain,cloud_cover&"
                   f"hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,visibility,wind_gusts_10m,rain,snowfall,cloud_cover&"
                   f"daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,sunshine_duration,uv_index_max,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,wind_speed_10m_max"
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

    # manipulate hourly forecast
    hourly_dict = json_file['hourly']
    # add data to dictionary
    hourly_dict['City'] = [city] * len(hourly_dict['time'])
    hourly_dict['Latitude'] = [latitude] * len(hourly_dict['time'])
    hourly_dict['Longitude'] = [longitude] * len(hourly_dict['time'])
    hourly_temp_df = pd.DataFrame(hourly_dict)
    hourly_data_df = pd.concat([hourly_data_df, hourly_temp_df])

    daily_dict = json_file['daily']
    daily_dict['City'] = [city] * len(daily_dict['time'])
    daily_dict['Latitude'] = [latitude] * len(daily_dict['time'])
    daily_dict['Longitude'] = [longitude] * len(daily_dict['time'])
    daily_temp_df = pd.DataFrame(daily_dict)
    daily_data_df = pd.concat([daily_data_df, daily_temp_df])



# add current weather data to dataframe
current_data_df = pd.DataFrame(current_data)
current_data_df.rename(columns={'wind_speed_10m':'wind_speed',
                                   'relative_humidity_2m':'relative_humidity',
                                    'temperature_2m':'temperature'},
                                    inplace=True
                       )

current_time_str = current_data_df.at[0, 'hour']
current_time = datetime.datetime.strptime(current_time_str, '%H:%M').time()

hourly_data_df.rename(columns={'wind_speed_10m': 'wind_speed',
                                  'relative_humidity_2m':'relative_humidity',
                                  'temperature_2m':'temperature'},
                      inplace=True
                      )

# split time column into date and hour
hourly_data_df[['date', 'hour']] = hourly_data_df['time'].str.split('T', expand=True)
hourly_data_df['date'] = pd.to_datetime(hourly_data_df['date']).dt.date
hourly_data_df['hour'] = pd.to_datetime(hourly_data_df['hour']).dt.hour
hourly_data_df.drop(columns='time')

# filter final dataframe
# forecast_time_df = hourly_data_df.loc[hourly_data_df['hour'] == current_time.hour]
# forecast_time_df.drop(columns='time', inplace=True)


# = Table.AddColumn(#"Removed Columns", "Custom", each if Text.Length(Text.From([hour])) = 1 then "0" & Text.From([hour]) else Text.From([hour]))










