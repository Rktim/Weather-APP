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
        st.write(f"City: {response.City()}")
        st.write(f"Country: {response.Country()}")
        st.write(f"Latitude: {response.Latitude()}°N")
        st.write(f"Longitude: {response.Longitude()}°E")

        st.subheader("Time Information:")
        st.write(f"Timestamp: {response.UtcOffsetSeconds()}")
        st.write(f"Time Zone: {response.Timezone()}")

        st.subheader("Temperature:")
        st.write(f"Temperature: {response.Hourly().Variables(0).ValuesAsNumpy()[0]}°C")
        st.write(f"Feels Like: {response.Hourly().Variables(2).ValuesAsNumpy()[0]}°C")
        st.write(f"Minimum Temperature: {response.Hourly().Variables(3).ValuesAsNumpy()[0]}°C")
        st.write(f"Maximum Temperature: {response.Hourly().Variables(4).ValuesAsNumpy()[0]}°C")

        st.subheader("Weather Condition:")
        st.write(f"Condition: {response.WeatherCondition()}")
        st.write(f"Condition Code or Icon: {response.ConditionCode()}")
        st.write(f"Description: {response.Description()}")

        st.subheader("Humidity and Pressure:")
        st.write(f"Humidity: {response.Hourly().Variables(1).ValuesAsNumpy()[0]}%")
        st.write(f"Pressure: {response.Pressure()} hPa")

        st.subheader("Wind:")
        st.write(f"Wind Speed: {response.WindSpeed()} km/h")
        st.write(f"Wind Direction: {response.WindDirection()}°")

        st.subheader("Precipitation:")
        st.write(f"Precipitation Volume: {response.PrecipitationVolume()} mm")
        st.write(f"Probability of Precipitation: {response.ProbabilityOfPrecipitation()}%")

        st.subheader("Visibility:")
        st.write(f"Visibility: {response.Visibility()} km")

        st.subheader("Cloudiness:")
        st.write(f"Cloudiness: {response.Cloudiness()}%")

        st.subheader("UV Index:")
        st.write(f"UV Index: {response.UVIndex()}")

        st.subheader("Air Quality (Optional):")
        st.write(f"Air Quality Index (AQI): {response.AQI()}")

        st.subheader("Sunrise and Sunset:")
        st.write(f"Sunrise Time: {response.SunriseTime()}")
        st.write(f"Sunset Time: {response.SunsetTime()}")

city = st.text_input("Enter City Name:", "ITANAGAR")

if st.button("Get Weather Data"):
    response = get_weather_data(city)
    display_weather_info(response)
