# Weather Station🌤️

Welcome to the Weather Station application! This simple and interactive app allows you to check the current weather conditions for any city around the world using the WeatherAPI service.

## Features

- **City Input**: Enter the name of any city to get its current weather information.
- **Weather Conditions**: Displays the current weather condition (e.g., Sunny, Rainy, etc.).
- **Temperature**: Shows the current temperature in Celsius.
- **Humidity**: Provides the current humidity level as a percentage.
- **Wind Speed**: Shows the current wind speed in kilometers per hour (KPH).
- **UV Index**: Displays the current UV index.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have installed the required Python packages using `pip`.
- You have a WeatherAPI key. If not, sign up [here](https://www.weatherapi.com/signup.aspx) to get one.


## Code Explanation

The main components of the code are as follows:

1. **Imports and Configuration**

   ```python
   import streamlit as st
   import requests
   from config import API_KEY
   ```

   These lines import the necessary libraries and the API key from the configuration file.

2. **App Title and City Input**

   ```python
   st.title("Weather Station🌤️")
   city = st.text_input("Enter City Name:", "ITANAGAR")
   ```

   Sets the title of the app and provides an input box for the user to enter the city name. By default, it displays "ITANAGAR".

3. **API Request and Data Handling**

   ```python
   url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
   response = requests.get(url)
   weather_data = response.json()
   ```

   Constructs the API request URL using the provided city name and API key, sends the request, and parses the JSON response.

4. **Display Weather Information**

   ```python
   if "error" not in weather_data:
       st.write(f"Weather in {city}: {weather_data['current']['condition']['text']}")
       st.write(f"Temperature: {weather_data['current']['temp_c']} Celsius")
       st.write(f"Humidity: {weather_data['current']['humidity']}%")
       st.write(f"Wind Speed: {weather_data['current']['wind_kph']} KPH")
       st.write(f"UV Index: {weather_data['current']['uv']}")
   else:
       st.write("Error fetching weather data")
   ```

   Checks if there is no error in the response data, and then displays the weather information. If an error occurs, it shows an error message.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

If you have any questions, please feel free to contact me at raktmxx@gmail.com.

Enjoy checking the weather with Weather Station! 🌤️

