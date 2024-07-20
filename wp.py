import streamlit as st
import requests
from config import API_KEY

st.title("Weather Station🌤️")

city = st.text_input("Enter City Name:", "ITANAGAR")
url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

response = requests.get(url)
weather_data = response.json()

if "error" not in weather_data:
    st.write(f"Weather in {city}: {weather_data['current']['condition']['text']}")
    st.write(f"Temperature: {weather_data['current']['temp_c']} Celsius")
    st.write(f"Humidity: {weather_data['current']['humidity']}%")
    st.write(f"Wind Speed: {weather_data['current']['wind_kph']} KPH")
    st.write(f"UV Index: {weather_data['current']['uv']}")
else:
    st.write("Error fetching weather data")