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
from sustainability import sustainability_section
from sustainability import bernoulli_section
#from analytics import analytics_section

#database
from database import init_db


#path to database ; code used for debugging
#st.write(os.getcwd())

def main():
    
    #App title
    st.set_page_config(
        page_title="The Every Day App",
        page_icon="🌤️"
    )
        
    st.markdown("""
    <style>
    /* Primary Content Area */
    .main-center-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

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

    col1, col2, col3 = st.columns(5)
    tab1, tab2, tab3,tab4,tab5 = st.tabs([
        "Sustainability Calculator",
        'Food Ideas',
        "Smoothie Maker",
        'Wellness Excercises',
        'Blog'
    ])

    with tab1:
        sustainability_section()

    with tab2:
        food_ideas()

    with tab3:
        smoothie_maker_section()

    with tab4:
        wellness_excercises()

def wellness_excercises():        
    # Display specified videos
    st.title("Yoga Videos")

    with st.expander("🧘 Yoga Resources"):
        st.link_button(
            "10 Min Yoga for Beginners",
            "https://www.youtube.com/watch?v=g_tea8ZNk5A"
        )

        st.link_button(
            "Breathing Exercise",
            "https://www.ekhartyoga.com/classes/3863/brahmari-pranayama-bumble-bee-breath"
        )
 
    # First video from YouTube
    st.subheader("1. 10 min Yoga for Beginners")
    st.video("https://www.youtube.com/watch?v=g_tea8ZNk5A")
    
    # Second video link (EkhartYoga)
    st.subheader("2. Brahmari Pranayama (Bumble Bee Breath)")
    st.markdown("[Watch Brahmari Pranayama on EkhartYoga](https://www.ekhartyoga.com/classes/3863/brahmari-pranayama-bumble-bee-breath)")
    return None
    
    
def food_ideas():
    st.header('🍽️ Healthy Food Ideas')
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
    return None

   

def smoothie_maker_section():
    # Header of Smoothie Maker
    st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

    # initialise the dataframe
    my_fruit_list = pd.read_csv(
        "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
    )

    my_fruit_list = my_fruit_list.set_index('Fruit')
    if st.session_state.get('fruit_list') is None:
        st.session_state.fruit_list = my_fruit_list

    # Add multiselect
    fruits_selected = st.multiselect(
        "Pick some fruits:",
        list(st.session_state.fruit_list.index),
        ['Avocado', 'Strawberries']
    )

    if fruits_selected:

        fruits_to_show = st.session_state.fruit_list.loc[fruits_selected]

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
    return None  

#LEFT HAND SIDEBAR
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
    weather_section()
    
    st.title('Bernoulli Trial Simulation ⚖️')
    bernoulli_section()
    
# Run the app
if __name__ == "__main__":
    init_db()
    main()
