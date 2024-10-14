import streamlit as st
import pandas as pd
import requests
import numpy as np

def get_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except ValueError:
            st.error("Failed to parse the weather data.")
            return None
    else:
        st.error(f"Error fetching data from OpenWeatherMap API. Status code: {response.status_code}")
        return None

def display_weather(data):
    """Display weather data in a user-friendly format."""
    if data:
        st.write(f"#### Weather in {data['name']}, {data['sys']['country']}")
        st.write(f"**Temperature:** {data['main']['temp']} °C")
        st.write(f"**Weather:** {data['weather'][0]['description']}")
        st.write(f"**Wind Speed:** {data['wind']['speed']} m/s")
        st.write(f"**Pressure:** {data['main']['pressure']} hPa")
        st.write(f"**Humidity:** {data['main']['humidity']}%")

def display_brands():
    """Display 'Brands I Love'."""
    st.title("Brands I Love")
    st.write("Here are some of my favorite brands:")
    st.markdown("""
    - **Apple** - Innovation and design
    - **Nike** - Quality sportswear
    - **Tesla** - Sustainable electric cars
    - **Sony** - Premium electronics
    - **Patagonia** - Ethical outdoor gear
    """)

def main():
    # Hamburger menu for page navigation
    st.sidebar.title("Menu")
    menu_selection = st.sidebar.selectbox("Choose a page:", ["Weather Forecast", "Healthy Menu", "Brands I Love"])
    
    # Page for weather forecast
    if menu_selection == "Weather Forecast":
        st.title("Weather Forecast")  
        city = st.text_input("Enter a city name", "London")
        
        api_key = "your_openweathermap_api_key"  # Replace with your own API key
    
        if st.button("Get Weather"):
            weather_data = get_weather_data(city, api_key)
            if weather_data and weather_data.get("cod") != 404:
                display_weather(weather_data)
            else:
                st.error("City not found!")
    
    # Page for healthy menu
    elif menu_selection == "Healthy Menu":
        st.markdown("<h1 style='text-align: center; color: grey;'>HEALTHY CAN BE TASTY</h1>", unsafe_allow_html=True)
        st.image("http://www.pngall.com/wp-content/uploads/2016/07/Meditation-Transparent.png")
        
        col4, col5, col6 = st.columns(3)
        with col4:
            st.header('Breakfast Menu')
            st.text('🥣 Quinoa Breakfast Bowl')
            st.text(' 🥤 Green Smoothie with Kale and Banana')
            st.text('🍳 Poached Eggs with Whole Grain Toast')
            st.text('🍓 Greek Yogurt with Mixed Berries')
        with col5:
            st.image("http://www.pngall.com/wp-content/uploads/5/Diet-PNG-Clipart.png")
        with col6:
            st.header('Snack Menu')
            st.text('🍎 Apple Slices with Almond Butter')
            st.text('🥒 Sliced Cucumber with Hummus')
            st.text('🥜 Handful of Mixed Nuts')

        col7, col8, col9 = st.columns(3)
        with col7:
            st.header('Dinner Menu')
            st.text('🍛 Baked Salmon with Quinoa and Asparagus')
            st.text('🥦 Stir-Fried Tofu with Vegetables')
            st.text('🍲 Lentil Curry with Brown Rice')
            st.text('🍆 Grilled Eggplant with Tomato Sauce')
    
    # Page for "Brands I Love"
    elif menu_selection == "Brands I Love":
        display_brands()

# Run the app
if __name__ == "__main__":
    main()
