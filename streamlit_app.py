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

#section imports
from weather import weather_section
#from sustainability import sustainability_section
#from analytics import analytics_section

#database
from database import init_db, save_user_and_emissions, load_emissions


#path to database
#st.write(os.getcwd())

# def get_weather(city, api_key):
#     """Fetch weather data safely from OpenWeather API"""
#     if not city:
#         st.warning("Please enter a city name.")
#         return None
#     try:
#         url = (
#             f"https://api.openweathermap.org/data/2.5/weather"
#             f"?q={city}&appid={api_key}&units=metric"
#         )
#         response = requests.get(url, timeout=10)
#         if response.status_code != 200:
#             try:
#                 error_data = response.json()
#                 message = error_data.get("message", "Unknown API error")
#             except Exception:
#                 message = "Weather service unavailable"
#             st.error(f"API error: {message}")
#             return None

#         data = response.json()

#         # Validate expected fields exist
#         try:
#             return {
#                 "name": data["name"],
#                 "country": data["sys"]["country"],
#                 "temp": data["main"]["temp"],
#                 "humidity": data["main"]["humidity"],
#                 "pressure": data["main"]["pressure"],
#                 "wind": data["wind"]["speed"],
#                 "weather": data["weather"][0]["description"],
#             }

#         except KeyError as e:
#             st.error(f"Unexpected API response format: missing {e}")
#             return None

#     except requests.exceptions.Timeout:
#         st.error("Request timed out. Try again.")
#         return None

#     except requests.exceptions.ConnectionError:
#         st.error("Connection error. Check internet access.")
#         return None

#     except Exception as e:
#         st.error(f"Unexpected error: {e}")
#         return None


# def display_weather(data):
#     """Display weather data safely"""
        
#     if not data:
#         st.warning("No weather data available.")
#         return
#     try:
#         st.write(f"#### Weather in {data['name']}, {data['country']}")
#         st.write(f"**Temperature:** {data['temp']} °C")
#         st.write(f"**Weather:** {data['weather']}")
#         st.write(f"**Wind Speed:** {data['wind']} m/s")
#         st.write(f"**Pressure:** {data['pressure']} hPa")
#         st.write(f"**Humidity:** {data['humidity']}%")

#     except KeyError as e:
#         st.error(f"Display error: missing field {e}")

#     except Exception as e:
#         st.error(f"Unexpected display error: {e}")

# def estimate_rain_probability(weather_data):
    
#     # Estimate rain probability from current weather conditions.
#     # Returns probability between 0 and 1.
    
#     try:
#         humidity = weather_data["humidity"]
#         pressure = weather_data["pressure"]
#         wind = weather_data["wind"]
#         description = weather_data["weather"].lower()

#         probability = 0.0

#         # Humidity contribution
#         if humidity > 85:
#             probability += 0.35
#         elif humidity > 70:
#             probability += 0.25
#         elif humidity > 55:
#             probability += 0.10

#         # Pressure contribution (low pressure = rain likely)
#         if pressure < 1005:
#             probability += 0.35
#         elif pressure < 1015:
#             probability += 0.20

#         # Wind contribution
#         if wind > 8:
#             probability += 0.10

#         # Weather description keywords
#         rain_keywords = [
#             "rain",
#             "drizzle",
#             "shower",
#             "storm",
#             "thunder",
#             "cloud"
#         ]

#         if any(word in description for word in rain_keywords):
#             probability += 0.25

#         # Clamp result between 0 and 1

#         probability = min(probability, 1.0)
#         return probability
#     except Exception as e:
#         return None


def main():

    st.set_page_config(
        page_title="Weather App",
        page_icon="🌤️"
    )

    weather_section()

    with st.sidebar:

        st.markdown(
            "<h3 style='text-align:center;color:grey;'>Blog Content</h3>",
            unsafe_allow_html=True,
        )

        image = Image.open("assets/tree.webp")
        st.image(image)

        st.caption(
            '_"One rarely falls in love without being as much attracted to what is interestingly wrong with someone as what is objectively healthy." — Alain de Botton_'
        )

        st.title("Weather Forecast 🌍")

        city = st.text_input(
            "Enter a city name",
            "London"
        )

        try:
            api_key = "1a4fb3f2dc6ead2387e5fed61756ddb3"

        except Exception:
            st.error("API key missing.")

    if st.button("Get Weather"):

        weather_data = get_weather(
            city.strip(),
            api_key
        )

        if weather_data:
            st.session_state.weather_data = weather_data

    # IMPORTANT: display weather AFTER button logic using session_state
    if "weather_data" in st.session_state:

        weather_data = st.session_state.weather_data

        display_weather(weather_data)

        rain_prob = estimate_rain_probability(weather_data)

        if rain_prob is not None:

            st.metric(
                "Rain Probability",
                f"{round(rain_prob * 100)}%"
            )

            st.subheader(
                "🎲 Need help deciding? \n Roll the weather dice!"
            )

            dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

            try:

                if st.button(
                    "Roll Decision Dice",
                    key="umbrella_dice"
                ):

                    placeholder = st.empty()

                    for _ in range(10):

                        roll = random.randint(1, 6)

                        placeholder.markdown(
                            f"<h1 style='text-align:center'>{dice_faces[roll-1]}</h1>",
                            unsafe_allow_html=True
                        )

                        time.sleep(0.06)

                    # decision logic
                    if roll <= 3:
                        st.info(
                            "🚶 Would you walk without an umbrella?"
                        )

                    else:
                        st.success(
                            "☔ Though it might rain, to take an umbrella or not is your decision"
                        )

            except Exception as e:

                st.warning(
                    "Dice helper temporarily unavailable."
                )

                st.write(e)

        try:

            from scipy.stats import bernoulli

            p = st.slider(
                "Probability of sustainable day",
                0.0,
                1.0,
                0.5
            )

            result = bernoulli.rvs(p)

            if result == 1:
                st.success("Sustainable outcome")

            else:
                st.error("Unsustainable outcome")

        except Exception as e:

            st.warning(
                "Bernolli Trial Function at lines 465 - 475 has failed with exception "
            )

    st.markdown(
        "<h1 style='text-align: center; color: grey;'>HEALTHY - WEALTHY</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align: center; color: grey;'>Тhe true science behind good choices</h2>",
        unsafe_allow_html=True
    )

    st.image(
        "http://www.pngall.com/wp-content/uploads/2016/07/Meditation-Transparent.png"
    )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.header('Breakfast Menu')
        st.text('🥣 Quinoa Breakfast Bowl')
        st.text(' 🥤 Green Smoothie with Kale and Banana')
        st.text('🍳 Poached Eggs with Whole Grain Toast')
        st.text('🍓 Greek Yogurt with Mixed Berries')

    with col5:
        st.image(
            "http://www.pngall.com/wp-content/uploads/5/Diet-PNG-Clipart.png"
        )

    with col6:
        st.header('Snack Menu')
        st.text('🍎 Apple Slices with Almond Butter')
        st.text('🥒 Sliced Cucumber with Hummus')
        st.text('🥜 Handful of Mixed Nuts')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(
            "https://cdn.pixabay.com/photo/2014/04/03/10/38/yoga-310940_960_720.png"
        )

    with col2:
        st.header('Lunch Menu')
        st.text('🥗 Grilled Chicken Salad with Quinoa')
        st.text(' 🥑 Avocado and Tomato Whole Grain Wrap')
        st.text('🍲 Lentil Soup with Vegetables')
        st.text('🥦 Steamed Broccoli with Lemon')

    with col3:
        st.image(
            "https://cdn.pixabay.com/photo/2014/04/02/10/48/woman-304646_640.png"
        )

    col7, col8, col9 = st.columns(3)

    with col7:
        st.header('Snack Menu')
        st.text('🥕 Carrot Sticks with Greek Yogurt Dip')
        st.text('🍇 Frozen Grapes')
        st.text('🍵 Green Tea')

    with col8:
        st.image(
            "https://cdn3.iconfinder.com/data/icons/wrestler/755/muscle_bodybuilding_bodybuilder_bicep_tricep_healthy_fitness-512.png"
        )

    with col9:
        st.header('Dinner Menu')
        st.text('🍛 Baked Salmon with Quinoa and Asparagus')
        st.text(' 🥦 Stir-Fried Tofu with Vegetables')
        st.text('🍲 Lentil Curry with Brown Rice')
        st.text('🍆 Grilled Eggplant with Tomato Sauce')

    col1, col2, col3 = st.columns(3)

    # Header of Smoothie Maker
    st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

    # initialise the dataframe
    my_fruit_list = pd.read_csv(
        "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
    )

    my_fruit_list = my_fruit_list.set_index('Fruit')

    # Add multiselect
    fruits_selected = st.multiselect(
        "Pick some fruits:",
        list(my_fruit_list.index),
        ['Avocado', 'Strawberries']
    )

    if fruits_selected:

        fruits_to_show = my_fruit_list.loc[fruits_selected]

        st.dataframe(fruits_to_show)

    else:
        st.warning("Please select at least one fruit.")

# Run the app
if __name__ == "__main__":
    main()
