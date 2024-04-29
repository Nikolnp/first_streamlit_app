import streamlit 
import pandas
import requests
import numpy as np
# Necessary libraries weather
import os
import json




#Page Title
#streamlit.title('Blog')
# Object notation
import streamlit as st
import requests

def get_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def display_weather(data):
    """Display weather data in a user-friendly format."""
    st.write(f"#### Weather in {data['name']}, {data['sys']['country']}")
    st.write(f"**Temperature:** {data['main']['temp']} °C")
    st.write(f"**Weather:** {data['weather'][0]['description']}")
    st.write(f"**Wind Speed:** {data['wind']['speed']} m/s")
    st.write(f"**Pressure:** {data['main']['pressure']} hPa")
    st.write(f"**Humidity:** {data['main']['humidity']}%")

def main():
    st.title("Weather Forecast App")
    city = st.text_input("Enter a city name", "London")

    api_key = "1a4fb3f2dc6ead2387e5fed61756ddb3"

    if st.button("Get Weather"):
        weather_data = get_weather_data(city, api_key)
        if weather_data.get("cod") != 404:
            display_weather(weather_data)
        else:
            st.error("City not found!")

if __name__ == "__main__":
    main()

# "with" notation
with streamlit.sidebar:
   streamlit.markdown("<h3 style='text-align: center; color: grey;'>Blog Content</h3>", unsafe_allow_html=True)
   streamlit.image("https://irelandtravelguides.com/wp-content/uploads/2020/06/gold-foil-tree-of-life-5262414_640.png")
   streamlit.caption('_"One rarely falls in love without being as much attracted to what is interestingly wrong with someone as what is objectively healthy."― Alain de Botton_')
   col1, col2, col3 = streamlit.columns(3)
   col1.metric("Temperature", "70 °F", "1.2 °F")
   col2.metric("Wind", "9 mph", "-8%")
   col3.metric("Humidity", "86%", "4%")
   #if streamlit.button('HEALTH'):
    #  streamlit.write('Redirect to Healthy page')
   #else:
    #  streamlit.write('Home Page')

streamlit.markdown("<h1 style='text-align: center; color: grey;'>HEALTHY CAN BE TAISTY</h1>", unsafe_allow_html=True)

streamlit.image("http://www.pngall.com/wp-content/uploads/2016/07/Meditation-Transparent.png" )
col4, col5, col6 = streamlit.columns(3)
with col4:
   streamlit.header('Breakfast Menu')
   streamlit.text('🥣 Omega 3 and Bluberry Oatmeal')
   streamlit.text(' 🥗 Kale spinah and rocket smoothie')
   streamlit.text('🐔 Hard-boiled free range egg')
   streamlit.text( '🥑🍞 Avocado Toast')
with col5:
   streamlit.image("http://www.pngall.com/wp-content/uploads/5/Diet-PNG-Clipart.png")
with col6:
   streamlit.header('Snack Menu')
   streamlit.text('Apple')
   streamlit.text('Kiwi')
   streamlit.text('or another favorite fruit')
#def columns list
col1, col2, col3, = streamlit.columns(3)

with col1:
   streamlit.image("https://cdn.pixabay.com/photo/2014/04/03/10/38/yoga-310940_960_720.png")
with col2:
   streamlit.header('Lunch Menu')
   streamlit.text('🥣 Omega 3 and Bluberry Oatmeal')
   streamlit.text(' 🥗 Kale spinah and rocket smoothie')
   streamlit.text('🐔 Hard-boiled free range egg')
   streamlit.text( '🥑🍞 Avocado Toast')
with col3:
    streamlit.image("https://cdn.pixabay.com/photo/2014/04/02/10/48/woman-304646_640.png")
col7, col8, col9, = streamlit.columns(3)
with col7:
   streamlit.header('Snack Menu')
   streamlit.text('Carrots')
   streamlit.text('Humous')
with col8:
   streamlit.image("https://cdn3.iconfinder.com/data/icons/wrestler/755/muscle_bodybuilding_bodybuilder_bicep_tricep_healthy_fitness-512.png")
with col9:
   streamlit.header('Dinner Menu')
   streamlit.text('🥣 Omega 3 and Bluberry Oatmeal')
   streamlit.text(' 🥗 Kale spinah and rocket smoothie')
   streamlit.text('🐔 Hard-boiled free range egg')
   streamlit.text( '🥑🍞 Avocado Toast')
col1, col2, col3, = streamlit.columns(3) 


#Header of Smootie Maker
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#initialise the dataframe
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =  my_fruit_list.set_index('Fruit')

#Add multiselect
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the dataframe
streamlit.dataframe(fruits_to_show)
 
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#--------------------------------------------------------------------------------------------


