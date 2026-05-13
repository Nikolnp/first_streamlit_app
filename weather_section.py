import streamlit as st
import pandas as pd
import requests
import numpy as np
import csv
import os
#other imports
import uuid
from PIL import Image
import random
import time

def get_weather(city, api_key):
    """Fetch weather data safely from OpenWeather API"""
    if not city:
        st.warning("Please enter a city name.")
        return None
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            try:
                error_data = response.json()
                message = error_data.get("message", "Unknown API error")
            except Exception:
                message = "Weather service unavailable"
            st.error(f"API error: {message}")
            return None

        data = response.json()

        # Validate expected fields exist
        try:
            return {
                "name": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind": data["wind"]["speed"],
                "weather": data["weather"][0]["description"],
            }

        except KeyError as e:
            st.error(f"Unexpected API response format: missing {e}")
            return None

    except requests.exceptions.Timeout:
        st.error("Request timed out. Try again.")
        return None

    except requests.exceptions.ConnectionError:
        st.error("Connection error. Check internet access.")
        return None

    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


def display_weather(data):
    """Display weather data safely"""
        
    if not data:
        st.warning("No weather data available.")
        return
    try:
        st.write(f"#### Weather in {data['name']}, {data['country']}")
        st.write(f"**Temperature:** {data['temp']} °C")
        st.write(f"**Weather:** {data['weather']}")
        st.write(f"**Wind Speed:** {data['wind']} m/s")
        st.write(f"**Pressure:** {data['pressure']} hPa")
        st.write(f"**Humidity:** {data['humidity']}%")

    except KeyError as e:
        st.error(f"Display error: missing field {e}")

    except Exception as e:
        st.error(f"Unexpected display error: {e}")

def estimate_rain_probability(weather_data):
    
    # Estimate rain probability from current weather conditions.
    # Returns probability between 0 and 1.
    
    try:
        humidity = weather_data["humidity"]
        pressure = weather_data["pressure"]
        wind = weather_data["wind"]
        description = weather_data["weather"].lower()

        probability = 0.0

        # Humidity contribution
        if humidity > 85:
            probability += 0.35
        elif humidity > 70:
            probability += 0.25
        elif humidity > 55:
            probability += 0.10

        # Pressure contribution (low pressure = rain likely)
        if pressure < 1005:
            probability += 0.35
        elif pressure < 1015:
            probability += 0.20

        # Wind contribution
        if wind > 8:
            probability += 0.10

        # Weather description keywords
        rain_keywords = [
            "rain",
            "drizzle",
            "shower",
            "storm",
            "thunder",
            "cloud"
        ]

        if any(word in description for word in rain_keywords):
            probability += 0.25

        # Clamp result between 0 and 1
        probability = min(probability, 1.0)

        return probability

    except Exception as e:
        return None
