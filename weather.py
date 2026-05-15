import streamlit as st
import pandas as pd
import requests
import numpy as np
import csv
import os
import uuid
from PIL import Image
import random
import time
from scipy.stats import bernoulli


# =========================================================
# WEATHER FETCH FUNCTION
# =========================================================
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
                message = error_data.get(
                    "message",
                    "Unknown API error"
                )

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

            st.error(
                f"Unexpected API response format: missing {e}"
            )

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


# =========================================================
# WEATHER DISPLAY SECTION
# =========================================================
def weather_section():
    """Display weather data safely"""
    if "weather_data" not in st.session_state:
        st.session_state.weather_data = None
    
    city = st.text_input(
        "Enter a city name",
        "London"
    )

    api_key = "1a4fb3f2dc6ead2387e5fed61756ddb3" 
    # IMPORTANT FIX
    data = None

    if st.button(
        "Get Weather", 
         key="weather_button"
    ):
       st.session_state.weather_data = get_weather(
        city,
        api_key
    )

    data = st.session_state.weather_data

    if data:

        st.write(data)

        if not data:
            st.warning("No weather data available.")
            return

        try:

            st.write(
                f"#### Weather in {data['name']}, {data['country']}"
            )

            st.write(
                f"**Temperature:** {data['temp']} °C"
            )

            st.write(
                f"**Weather:** {data['weather']}"
            )

            st.write(
                f"**Wind Speed:** {data['wind']} m/s"
            )

            st.write(
                f"**Pressure:** {data['pressure']} hPa"
            )

            st.write(
                f"**Humidity:** {data['humidity']}%"
            )

            # =========================================================
            # RAIN PROBABILITY
            # =========================================================
            rain_prob = estimate_rain_probability(data)

            if rain_prob is not None:

                st.metric(
                    "Rain Probability",
                    f"{round(rain_prob * 100)}%"
                )

            # =========================================================
            # WEATHER DECISION DICE
            # =========================================================
            st.subheader(
                "🎲 Need help deciding?\nRoll the weather dice!"
            )

            dice_faces = [
                "⚀",
                "⚁",
                "⚂",
                "⚃",
                "⚄",
                "⚅"
            ]

            if st.button(
                "Roll Decision Dice",
                key="umbrella_dice"
            ):
                 #session logic
                if 'dice_roll' not in st.session_state:
                    st.session_state.dice_roll = None
                placeholder = st.empty()
                for _ in range(10):
                    st.session_state.dice_roll = random.randint(1,6)
                    roll = st.session_state.dice_roll
                    placeholder.markdown(
                        f"<h1 style='text-align:center'>{dice_faces[roll - 1]}</h1>",
                        unsafe_allow_html=True
                    )
                    time.sleep(0.06)
                # loop finished
                final_roll = st.session_state.dice_roll
                # decision logic
                if roll <= 3:
                    st.info(
                        "🚶 Would you walk without an umbrella?"
                    )
                else:
                    st.success(
                        "☔ Though it might rain, to take an umbrella or not is your decision"
                    )
                
            # =========================================================
            # BERNOULLI TRIAL
            # =========================================================
            try:
                p = st.slider(
                    "Probability of sustainable day",
                    0.0,
                    1.0,
                    0.5
                )
                # 1. Initialize the only two variables you need
                if 'bernoulli_result' not in st.session_state.bernoulli_result:
                    st.session_state.bernoulli_result = 0
                if "sustainable" not in st.session_state:
                    st.session_state.sustainable = 0
                if "unsustainable" not in st.session_state:
                    st.session_state.unsustainable = 0

                # 2. Separate functions to strictly modify the counts
                def increment_sustainable():
                    st.session_state.sustainable += 1

                def increment_unsustainable():
                    st.session_state.unsustainable += 1
                
                if st.button(
                    "Run Bernoulli Trial",
                    key="bernoulli_button"
                ):
                    st.session_state.bernoulli_result = bernoulli.rvs(p)
                result = st.session_state.bernoulli_result
                st.write(f"DEBUG result: {result}")
                if result is not None:
                    if result == 1:
                        st.success("Sustainable outcome")
                        st.session_state.sustainable += 1
                    else:
                        st.error("Unsustainable outcome")
                        st.session_state.unsustainable += 1
                st.session_state.total += 1
                st.divider()

                # 3. Calculate the total instantly on the fly (Prevents +1 overhead errors)
                total_outcomes = st.session_state.sustainable + st.session_state.unsustainable

                # 4. Display the results in 3 columns
                col1, col2, col3 = st.columns(3)

                col1.metric("Sustainable outcomes", st.session_state.sustainable)
                col2.metric("Unsustainable outcomes", st.session_state.unsustainable)
                col3.metric("Total Outcomes", total_outcomes)

            except Exception as e:

                st.warning(
                    f"Bernoulli Trial Function unavailable: {e}"
                )

        except KeyError as e:

            st.error(
                f"Display error: missing field {e}"
            )

        except Exception as e:

            st.error(
                f"Unexpected display error: {e}"
            )


# =========================================================
# RAIN PROBABILITY ESTIMATION
# =========================================================
def estimate_rain_probability(weather_data):
    """
    Estimate rain probability from current weather conditions.
    Returns probability between 0 and 1.
    """

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

        # Pressure contribution
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

        if any(
            word in description
            for word in rain_keywords
        ):

            probability += 0.25

        # Clamp result between 0 and 1
        probability = min(probability, 1.0)

        return probability

    except Exception:
        return None
