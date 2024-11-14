import streamlit as st
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
st.title("Weather Station🌤️")

city = st.text_input("Enter City Name:", "ITANAGAR")


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Input fields for latitude and longitude
latitude = st.number_input("Enter Latitude:", value=52.52)
longitude = st.number_input("Enter Longitude:", value=13.41)

# Make sure all required weather variables are listed here
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "cloud_cover"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
st.write(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
st.write(f"Elevation: {response.Elevation()} m asl")
st.write(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
st.write(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()} s")


# Process hourly data. The order of variables needs to be the same as requested.
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
