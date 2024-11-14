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
        st.write(f"Feels Like: {hourly.Variables(2).ValuesAsNumpy()[0]}°C")
        st.write(f"Minimum Temperature: {hourly.Variables(3).ValuesAsNumpy()[0]}°C")
        st.write(f"Maximum Temperature: {hourly.Variables(4).ValuesAsNumpy()[0]}°C")

        st.subheader("Weather Condition:")
        st.write(f"Condition: {response.get('weather_condition', 'N/A')}")
        st.write(f"Condition Code or Icon: {response.get('condition_code', 'N/A')}")
        st.write(f"Description: {response.get('description', 'N/A')}")

        st.subheader("Humidity and Pressure:")
        st.write(f"Humidity: {hourly.Variables(1).ValuesAsNumpy()[0]}%")
        st.write(f"Pressure: {response.get('pressure', 'N/A')} hPa")

        st.subheader("Wind:")
        st.write(f"Wind Speed: {response.get('wind_speed', 'N/A')} km/h")
        st.write(f"Wind Direction: {response.get('wind_direction', 'N/A')}°")

        st.subheader("Precipitation:")
        st.write(f"Precipitation Volume: {response.get('precipitation_volume', 'N/A')} mm")
        st.write(f"Probability of Precipitation: {response.get('probability_of_precipitation', 'N/A')}%")

        st.subheader("Visibility:")
        st.write(f"Visibility: {response.get('visibility', 'N/A')} km")

        st.subheader("Cloudiness:")
        st.write(f"Cloudiness: {response.get('cloudiness', 'N/A')}%")

        st.subheader("UV Index:")
        st.write(f"UV Index: {response.get('uv_index', 'N/A')}")

        st.subheader("Air Quality (Optional):")
        st.write(f"Air Quality Index (AQI): {response.get('aqi', 'N/A')}")

        st.subheader("Sunrise and Sunset:")
        st.write(f"Sunrise Time: {response.get('sunrise_time', 'N/A')}")
        st.write(f"Sunset Time: {response.get('sunset_time', 'N/A')}")

city = st.text_input("Enter City Name:", "ITANAGAR")
latitude = st.number_input("Enter Latitude:", value=52.52, format="%.6f", min_value=-90.0, max_value=90.0)
longitude = st.number_input("Enter Longitude:", value=13.41, format="%.6f", min_value=-180.0, max_value=180.0)

if st.button("Get Weather Data"):
    response = get_weather_data(latitude, longitude)
    display_weather_info(response)
