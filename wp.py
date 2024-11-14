import streamlit as st
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

st.title("Weather Station🌤️")

# Input fields for city name, latitude, and longitude
city = st.text_input("Enter City Name:", "ITANAGAR")
latitude = st.number_input("Enter Latitude:", value=52.52)
longitude = st.number_input("Enter Longitude:", value=13.41)

# HTML & CSS for custom styling
st.markdown("""
    <style>
        .title {
            font-size: 2em;
            color: #1f77b4;
            text-align: center;
            font-weight: bold;
        }
        .section-title {
            color: #ff7f0e;
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 20px;
        }
        .data-table {
            border: 2px solid #4c72b0;
            border-radius: 5px;
            background-color: #f9f9f9;
            color: #333;
            padding: 10px;
            font-family: Arial, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Cache and retry settings for API requests
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Weather API URL and parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "cloud_cover"]
}
responses = openmeteo.weather_api(url, params=params)

# Extract data from API response
response = responses[0]
st.markdown("<div class='section-title'>Location Details</div>", unsafe_allow_html=True)
st.write(f"**Coordinates**: {response.Latitude()}°N, {response.Longitude()}°E")
st.write(f"**Elevation**: {response.Elevation()} m asl")
st.write(f"**Timezone**: {response.Timezone()} ({response.TimezoneAbbreviation()})")
st.write(f"**Timezone difference to GMT+0**: {response.UtcOffsetSeconds()} s")

# Process hourly weather data
hourly = response.Hourly()
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
    "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
    "dew_point_2m": hourly.Variables(2).ValuesAsNumpy(),
    "rain": hourly.Variables(3).ValuesAsNumpy(),
    "cloud_cover": hourly.Variables(4).ValuesAsNumpy()
}

hourly_dataframe = pd.DataFrame(data=hourly_data)

# Display hourly weather data with custom table styling
st.markdown("<div class='section-title'>Hourly Weather Data</div>", unsafe_allow_html=True)
st.markdown("<div class='data-table'>", unsafe_allow_html=True)
st.dataframe(hourly_dataframe.style.set_properties(**{'text-align': 'center'}))
st.markdown("</div>", unsafe_allow_html=True)
