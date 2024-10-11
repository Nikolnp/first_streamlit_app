import streamlit as st
import pandas
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
    my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
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
            fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
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

    # Brands I Support Section
    st.title("Brands I Support")
    
    # Colibri Garden
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://www.colibrigarden.com/wp-content/uploads/2020/06/logo-footer.png", width=100)  # Add the brand logo
    with col2:
        st.markdown("[**Colibri Garden**](https://www.colibrigarden.com)")
        st.caption("Colibri Garden provides organic, eco-friendly gardening solutions and tools, promoting sustainable and natural living.")
    
    # Bokyna
    col3, col4 = st.columns([1, 4])
    with col3:
        st.image("https://www.bokyna.com/wp-content/uploads/2021/07/bokyna-logo-300x75.png", width=100)  # Add the brand logo
    with col4:
        st.markdown("[**Bokyna**](https://www.bokyna.com)")
        st.caption("Bokyna creates unique and handcrafted sandals, combining style, sustainability, and comfort for every occasion.")
    
    # Luvsko
    col5, col6 = st.columns([1, 4])
    with col5:
        st.image("https://www.luvsko.com/wp-content/uploads/2021/05/Luvsko-Logo-Header.png", width=100)  # Add the brand logo
    with col6:
        st.markdown("[**Luvsko**](https://www.luvsko.com)")
        st.caption("Luvsko specializes in vegan and sustainable footwear, offering stylish and cruelty-free shoes that are comfortable and ethically made.")


# Run the app
if __name__ == "__main__":
    main()
