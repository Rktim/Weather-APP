import streamlit as st
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

st.title("Weather Station🌤️")

def get_weather_data(city):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Geocoding to get latitude and longitude based on city name
    geocode_url = "https://api.open-meteo.com/v1/geocode"
    geocode_params = {
        "city": city
    }
    
    try:
        geocode_response = openmeteo.weather_api(geocode_url, params=geocode_params)
        latitude = geocode_response[0].Latitude()
        longitude = geocode_response[0].Longitude()
    except Exception as e:
        st.error(f"Error fetching geocode data: {e}")
        return None

    # Fetch weather data using latitude and longitude
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "uv_index", "aqi"]
    }
    
    try:
        weather_response = openmeteo.weather_api(weather_url, params=weather_params)
        return weather_response[0]
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def display_weather_info(response):
    if response:
        st.subheader("Weather Information:")
        st.write(f"Country: {response.get('country', 'N/A')}")
        st.write(f"City: {response.get('city', 'N/A')}")
        st.write(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
        
        hourly = response.Hourly()
        st.write(f"Temperature: {hourly.Variables(0).ValuesAsNumpy()[0]}°C")
        st.write(f"Humidity: {hourly.Variables(1).ValuesAsNumpy()[0]}%")
        st.write(f"Pressure: {response.get('pressure', 'N/A')} hPa")
        st.write(f"Wind Speed: {response.get('wind_speed', 'N/A')} km/h")
        st.write(f"UV Index: {hourly.Variables(2).ValuesAsNumpy()[0]}")
        st.write(f"AQI: {response.get('aqi', 'N/A')}")

city = st.text_input("Enter City Name:", "ITANAGAR")

if st.button("Get Weather Data"):
    response = get_weather_data(city)
    display_weather_info(response)
