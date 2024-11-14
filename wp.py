import streamlit as st
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

st.title("Weather Station🌤️")

def get_weather_data(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "cloud_cover"]
    }
    
    try:
        responses = openmeteo.weather_api(url, params=params)
        return responses[0]
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def display_weather_info(response):
    if response:
        st.write(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        st.write(f"Elevation: {response.Elevation()} m asl")
        st.write(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
        st.write(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()} s")

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
        hourly_rain = hourly.Variables(3).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["dew_point_2m"] = hourly_dew_point_2m
        hourly_data["rain"] = hourly_rain
        hourly_data["cloud_cover"] = hourly_cloud_cover

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        st.dataframe(hourly_dataframe)

city = st.text_input("Enter City Name:", "ITANAGAR")
latitude = st.number_input("Enter Latitude:", value=52.52, format="%.6f", min_value=-90.0, max_value=90.0)
longitude = st.number_input("Enter Longitude:", value=13.41, format="%.6f", min_value=-180.0, max_value=180.0)

if st.button("Get Weather Data"):
    response = get_weather_data(latitude, longitude)
    display_weather_info(response)