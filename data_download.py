from tarfile import data_filter
import pandas as pd
import requests
import json
import pprint

latitude = '52.237049'
longitude: str = '21.017532'

# link = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
# data = requests.get(link).json()
# with open('weather_data.json', 'w') as f:
#     json.dump(data, f)


# read file and convert to json format
with open('weather_data.json', 'r') as str_file:
    str_file = str_file.read()
    json_file = json.loads(str_file)

# manupulate current weather
current_weather_dict = json_file['current']
current_weather_df = pd.DataFrame([current_weather_dict])

# manupulate forecast
forecast_dict = json_file['hourly']
forecast_df = pd.DataFrame(forecast_dict).rename(columns={'wind_speed_10m':'wind_speed',
                                                          'relative_humidity_2m':'relative_humidity',
                                                          'temperature_2m':'temperature'})
# split time column into date and hour
forecast_df
print(forecast_df)









