import streamlit as st
import requests_cache
import pandas as pd
from retry_requests import retry
import openmeteo_requests

st.title("Weather Station🌤️")

def get_weather_data(city):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 0,  # Placeholder, will be replaced with actual latitude
        "longitude": 0,  # Placeholder, will be replaced with actual longitude
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
        st.subheader("Location Details:")
        st.write(f"Latitude: {response.Latitude()}°N")
        st.write(f"Longitude: {response.Longitude()}°E")
        st.write(f"Elevation: {response.Elevation()} m asl")
        st.write(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
        st.write(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()} s")

        st.subheader("Time Information:")
        st.write(f"Timestamp: {response.UtcOffsetSeconds()}")

        st.subheader("Temperature:")
        hourly = response.Hourly()
        st.write(f"Temperature: {hourly.Variables(0).ValuesAsNumpy()[0]}°C")
        st.write(f"Minimum Temperature: {hourly.Variables(3).ValuesAsNumpy()[0]}°C")
        st.write(f"Maximum Temperature: {hourly.Variables(4).ValuesAsNumpy()[0]}°C")

        st.subheader("Humidity and Pressure:")
        st.write(f"Humidity: {hourly.Variables(1).ValuesAsNumpy()[0]}%")
        
        # Displaying optional fields only if they are available
        try:
            uv_index = getattr(response, 'uv_index', 'N/A')
            st.subheader("UV Index:")
            st.write(f"UV Index: {uv_index}")

            aqi = getattr(response, 'aqi', 'N/A')
            st.subheader("Air Quality (Optional):")
            st.write(f"Air Quality Index (AQI): {aqi}")

            sunrise_time = getattr(response, 'sunrise_time', 'N/A')
            sunset_time = getattr(response, 'sunset_time', 'N/A')
            st.subheader("Sunrise and Sunset:")
            st.write(f"Sunrise Time: {sunrise_time}")
            st.write(f"Sunset Time: {sunset_time}")

        except AttributeError:
            st.write("Some optional data is not available.")

city = st.text_input("Enter City Name:", "ITANAGAR")

if st.button("Get Weather Data"):
    response = get_weather_data(city)
    display_weather_info(response)
