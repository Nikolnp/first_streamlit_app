import streamlit as st
import pandas as pd
import requests
import numpy as np
import csv
import os
import uuid
from database import init_db, save_user_and_emissions, load_emissions
init_db()

# def get_weather_data(city, api_key):
#     """Fetch weather data from OpenWeatherMap API."""
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         try:
#             data = response.json()
#             return data
#         except ValueError:
#             st.error("Failed to parse the weather data.")
#             return None
#     else:
#         st.error(f"Error fetching data from OpenWeatherMap API. Status code: {response.status_code}")
#         return None

def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "weather": data["weather"][0]["main"]
        }
        except ValueError:
        st.error('Failed to parse the weather data.')
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

def main():
    with st.sidebar:
        st.markdown("<h3 style='text-align: center; color: grey;'>Blog Content</h3>", unsafe_allow_html=True)
        st.image("https://irelandtravelguides.com/wp-content/uploads/2020/06/gold-foil-tree-of-life-5262414_640.png")
        st.caption('_"One rarely falls in love without being as much attracted to what is interestingly wrong with someone as what is objectively healthy."― Alain de Botton_')
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "°C", "°F")
        col2.metric("Wind", "mph", "+/-")
        col3.metric("Humidity", "%", "%")
       
        # Title
        st.title("Weather Forecast")  
        city = st.text_input("Enter a city name", "London")
        
        api_key = "1a4fb3f2dc6ead2387e5fed61756ddb3"
    
        if st.button("Get Weather"):
            weather_data = get_weather_data(city, api_key)
            if weather_data and weather_data.get("cod") != 404:
                display_weather(weather_data)
            else:
                st.error("City not found!")

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
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://cdn.pixabay.com/photo/2014/04/03/10/38/yoga-310940_960_720.png")
    with col2:
        st.header('Lunch Menu')
        st.text('🥗 Grilled Chicken Salad with Quinoa')
        st.text(' 🥑 Avocado and Tomato Whole Grain Wrap')
        st.text('🍲 Lentil Soup with Vegetables')
        st.text('🥦 Steamed Broccoli with Lemon')
    with col3:
        st.image("https://cdn.pixabay.com/photo/2014/04/02/10/48/woman-304646_640.png")
        
    col7, col8, col9 = st.columns(3)
    with col7:
        st.header('Snack Menu')
        st.text('🥕 Carrot Sticks with Greek Yogurt Dip')
        st.text('🍇 Frozen Grapes')
        st.text('🍵 Green Tea')
    with col8:
        st.image("https://cdn3.iconfinder.com/data/icons/wrestler/755/muscle_bodybuilding_bodybuilder_bicep_tricep_healthy_fitness-512.png")
    with col9:
        st.header('Dinner Menu')
        st.text('🍛 Baked Salmon with Quinoa and Asparagus')
        st.text(' 🥦 Stir-Fried Tofu with Vegetables')
        st.text('🍲 Lentil Curry with Brown Rice')
        st.text('🍆 Grilled Eggplant with Tomato Sauce')
        
    col1, col2, col3 = st.columns(3) 
    #Header of Smoothie Maker
    st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
    #initialise the dataframe
    my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
    my_fruit_list = my_fruit_list.set_index('Fruit')
    
    #Add multiselect
    fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
    
    if fruits_selected:
        fruits_to_show = my_fruit_list.loc[fruits_selected]
        st.dataframe(fruits_to_show)
    else:
        st.warning("Please select at least one fruit.")
    
    # Fruityvice API call
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
    
    if fruityvice_response.status_code == 200:
        try:
            fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
            st.dataframe(fruityvice_normalized)
        except ValueError:
            st.error("The response from the Fruityvice API is not in JSON format.")
    else:
        st.error(f"Failed to fetch data from Fruityvice API. Status code: {fruityvice_response.status_code}")

    # Display specified videos
    st.title("Yoga Videos")
    
    # First video from YouTube
    st.subheader("1. 10 min Yoga for Beginners")
    st.video("https://www.youtube.com/watch?v=g_tea8ZNk5A")
    
    # Second video link (EkhartYoga)
    st.subheader("2. Brahmari Pranayama (Bumble Bee Breath)")
    st.markdown("[Watch Brahmari Pranayama on EkhartYoga](https://www.ekhartyoga.com/classes/3863/brahmari-pranayama-bumble-bee-breath)")


    
    # =========================================================
    # 🌍 HOUSEHOLD SUSTAINABILITY CALCULATOR (SQL + IQR READY)
    # =========================================================
    
    st.title("🌍 Household Sustainability Calculator")
    
    # ---------------- CONSTANTS ----------------
    FACTORS = {
        "electricity": 0.4,
        "water": 0.34,
        "car": 0.2,
        "diet": {
            "Plant-based": 120,
            "Mixed": 200,
            "Meat-heavy": 350
        }
    }
    
    # ---------------- CORE CALC ----------------
    def calculate_emissions(electricity, water, car_km, diet):
        electricity_em = electricity * FACTORS["electricity"]
        water_em = water * FACTORS["water"]
        car_em = car_km * FACTORS["car"]
        food_em = FACTORS["diet"][diet]
    
        total = electricity_em + water_em + car_em + food_em
    
        return {
            "electricity": electricity_em,
            "water": water_em,
            "car": car_em,
            "food": food_em,
            "total": total,
            "yearly": total * 12
        }
    
    # ---------------- FORM ----------------
    with st.form("sustainability_form"):
    
        name = st.text_input("Name (required)")
        email = st.text_input("Email (required)")
    
        electricity = st.number_input("Electricity (kWh)", value=200)
        water = st.number_input("Water usage (m³)", value=3)
        car_km = st.number_input("Car travel (km)", value=0)
    
        diet = st.selectbox("Diet type", ["Plant-based", "Mixed", "Meat-heavy"])
    
        submitted = st.form_submit_button("Calculate & Save")
    
    # =========================================================
    # 🚨 EVERYTHING BELOW ONLY RUNS AFTER SUBMIT
    # =========================================================
    
    if submitted:
    
        # ---------------- VALIDATION ----------------
        if not name or not email:
            st.error("Name and Email are required!")
            st.stop()
    
        # ---------------- CALCULATE ----------------
        results = calculate_emissions(electricity, water, car_km, diet)
    
        # ---------------- OUTPUT ----------------
        st.header("📊 Results")
        st.write(f"Monthly CO₂: **{results['total']:.2f} kg**")
        st.write(f"Yearly CO₂: **{results['yearly']:.2f} kg**")
    
        df = pd.DataFrame({
            "Category": ["Electricity", "Water", "Transport", "Food"],
            "Emissions": [
                results["electricity"],
                results["water"],
                results["car"],
                results["food"]
            ]
        })
    
        st.bar_chart(df.set_index("Category"))
    
        # =========================================================
        # 💾 DATABASE SAVE (SAFE INSIDE SUBMIT BLOCK)
        # =========================================================
        try:
            from database import save_user, email_exists
        except Exception:
            st.error("Database module not properly configured.")
            st.stop()
    
        user_payload = {
            "name": name,
            "email": email,
            "electricity": electricity,
            "water": water,
            "car_km": car_km,
            "diet": diet,
            "monthly_total": results["total"],
            "yearly_total": results["yearly"]
        }
    
        if email_exists(email):
            st.warning("Email exists → updating record")
        else:
            st.info("New user → inserting record")
    
        save_user(user_payload)
        st.success("Saved successfully!")
    
        # =========================================================
        # 📈 IQR OUTLIER ANALYSIS
        # =========================================================
        st.subheader("📈 Outlier Detection (IQR)")
    
        try:
            from database import get_all_users
    
            data = get_all_users()
            df_all = pd.DataFrame(data)
    
            if len(df_all) >= 4 and "monthly_total" in df_all.columns:
    
                q1 = df_all["monthly_total"].quantile(0.25)
                q3 = df_all["monthly_total"].quantile(0.75)
                iqr = q3 - q1
    
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
    
                df_all["outlier"] = (
                    (df_all["monthly_total"] < lower) |
                    (df_all["monthly_total"] > upper)
                )
    
                st.write(f"IQR range: {lower:.2f} → {upper:.2f}")
                st.dataframe(df_all)
    
                st.bar_chart(df_all.set_index("email")["monthly_total"])
    
            else:
                st.info("Not enough data yet for IQR analysis.")
    
        except Exception as e:
            st.warning("Could not load analytics data yet.")
# Run the app
if __name__ == "__main__":
    main()
