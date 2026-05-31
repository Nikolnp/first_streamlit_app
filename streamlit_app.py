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
from random import random
import altair as alt

#section imports
from weather import weather_section
from sustainability import sustainability_section
#from sustainability import bernoulli_section #commented out for debuging
#from analytics import analytics_section
from database import load_published_articles
from analytics import educational_section
#database
from database import init_db, save_article


#path to database ; code used for debugging
#st.write(os.getcwd())

# =====================================================
# SESSION AUTH STATE
# =====================================================

if "is_admin" not in st.session_state:

    st.session_state.is_admin = False


# =====================================================
# ADMIN LOGIN
# =====================================================

st.sidebar.subheader("Admin Access")

admin_password = st.sidebar.text_input(
    "Admin Password",
    type="password"
)

if st.sidebar.button("Login"):
    #check admin secrets
    admin_secret = st.secrets.get(
        "ADMIN_KEY"
    ) 
    st.write(dict(st.secrets))
    if admin_secret is None:
        st.error(
            "Admin secret not configured."
        )  
    else:
        if admin_password == admin_secret:
            st.session_state.is_admin = True
        if admin_password == st.secrets["ADMIN_KEY"]:
            st.write(st.secrets)
            st.session_state.is_admin = True
            st.write('')
            st.sidebar.success(
                "Admin authenticated"
            )
    
        else:
    
            st.sidebar.error(
                "Invalid admin password"
            )

if st.session_state.is_admin:

    st.sidebar.success(
        "Admin session active"
    )

    if st.sidebar.button("Logout"):

        st.session_state.is_admin = False

        st.rerun()

#-----------------------------------------------------------------------------------------------#

def main():
    
    #App title
    st.set_page_config(
        page_title="The Every Day App",
        page_icon="🌤️"
    )

    initialize_session_state()

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

    render_navigation()
    route_to_page()  
#---------------------------------------------------------------------------------------------------------------------#
       
def render_navigation():

    st.sidebar.radio(

        "Navigation",

        options=list(PAGES.keys()),

        format_func=lambda x:
            PAGES[x]["title"],

        key="active_page"
    )

def initialize_session_state():
    defaults = {

        "active_page": "sustainability",

        "is_admin": False,

        "bernoulli_result": None,

        "sustainable": 0,

        "unsustainable": 0,

        "total": 0,

        "trial_history": [],

        "sustainable_history": [],

        "unsustainable_history": []
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value
    

def route_to_page():

    page = PAGES[
        st.session_state.active_page
    ]

    if page["admin_only"]:

        if not st.session_state.is_admin:

            st.warning(
                "Admin access required."
            )

            return

    page["handler"]()

def add_article():
    st.title("Write Article")
    
    title = st.text_input("Title")
    
    excerpt = st.text_area("Excerpt")
    
    content = st.text_area(
        "Content",
        height=400
    )
    
    author = st.text_input("Author")
    status = st.selectbox(
    "Status",
    [
        "draft",
        "published"
    ]
)
    if st.button("Save Draft"):
    
        save_article(
            title,
            excerpt,
            content,
            author,
            status
        )
    
        st.success("Draft saved")

def display_published_articles():

    st.title("Research Journal")
    
    articles = load_published_articles()
    
    if not articles.empty:
    
        for _, article in articles.iterrows():
    
            with st.container():
    
                st.subheader(article["title"])
    
                st.caption(
                    f"By {article['author']}"
                )
    
                st.write(article["excerpt"])
    
                with st.expander("Read Article"):
    
                    st.markdown(
                        article["content"]
                    )
    
                st.divider()
    
    else:
    
        st.info("No published articles yet.")

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

def science_podcast():
    print('Coming soon')
    
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
    
    #st.title('Bernoulli Trial Simulation ⚖️')
    #bernoulli_section()

    # =========================================================
    # VISUALIZATION FUNCTION
    # =========================================================
    
    def visualize_outcomes(history):
    
        if len(history) == 0:
    
            st.info("No trials yet.")
    
            return
    
        df = pd.DataFrame({
    
            "Trial": list(range(len(history))),
    
            "Outcome": [
    
                "Sustainable"
                if x == 1
                else "Unsustainable"
    
                for x in history
            ]
        })
    
        chart = alt.Chart(df).mark_circle(
            size=120
        ).encode(
    
            x="Trial",
    
            y="Outcome",
    
            color="Outcome",
    
            tooltip=[
                "Trial",
                "Outcome"
            ]
        ).properties(
    
            title=
            "Bernoulli Trial Visualization",
    
            width=700,
    
            height=300
        )
    
        st.altair_chart(
            chart,
            use_container_width=True
        )


# =========================================================
# BERNOULLI SECTION
# =========================================================

def sidebar_radio_menu(): 
    try:
        st.title(
            "🧠 Bernoulli Trial Explorer"
        )
        # =================================================
        # RESET EXPERIMENT IF p CHANGES
        # =================================================

        def reset_bernoulli_experiment():
    
            st.session_state.sustainable = 0
        
            st.session_state.unsustainable = 0
        
            st.session_state.total = 0
        
            st.session_state.bernoulli_result = None
        
            st.session_state.trial_history = []
        
            st.session_state.sustainable_history = []
        
            st.session_state.unsustainable_history = []
        
            st.warning(
                "Probability changed. "
                "Experiment reset."
            )
        if "current_page" not in st.session_state:
        
            st.session_state.current_page = (
                "Bernoulli Trials"
            )
        
        page = st.sidebar.selectbox(
        
            "Choose Module",
        
            [
        
                "Bernoulli Trials",
        
                "Linear Regression",
        
                "Clustering"
            ],
        
            key="current_page"
        )
        # =================================================
        # PROBABILITY SLIDER
        # =================================================

        p = st.slider(

            "Probability of sustainable day",
        
            0.0,
        
            1.0,
        
            0.5,
        
            key="bernoulli_probability",
        
            on_change=reset_bernoulli_experiment
        )
      
       
        # =================================================
        # RUN BERNOULLI TRIAL
        # =================================================

        if st.button(

            "Run Bernoulli Trial",

            key="b_button"
        ):

            result = 1 if random() < p else 0

            st.session_state.bernoulli_result = result

            st.session_state.trial_history.append(
                result
            )

            if result == 1:

                st.success(
                    "Sustainable outcome"
                )

                st.session_state.sustainable += 1

                st.session_state.sustainable_history.append(
                    1
                )

                st.session_state.unsustainable_history.append(
                    0
                )

            else:

                st.error(
                    "Unsustainable outcome"
                )

                st.session_state.unsustainable += 1

                st.session_state.sustainable_history.append(
                    0
                )

                st.session_state.unsustainable_history.append(
                    1
                )

                st.session_state.total += 1
                st.write(
                    "Trial History:",
                    st.session_state.trial_history
                )
                
                st.write(
                    "Sustainable History:",
                    st.session_state.sustainable_history
                )
                
                st.write(
                    "Unsustainable History:",
                    st.session_state.unsustainable_history
                )
        # =================================================
        # METRICS
        # =================================================

        total_outcomes = (

            st.session_state.sustainable +

            st.session_state.unsustainable
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(

            "Sustainable Outcomes",

            st.session_state.sustainable
        )

        col2.metric(

            "Unsustainable Outcomes",

            st.session_state.unsustainable
        )

        col3.metric(

            "Total Outcomes",

            total_outcomes
        )

        # =================================================
        # LIVE FORMULA
        # =================================================

        st.subheader(
            "📘 Bernoulli Formula"
        )

        st.latex(r"P(X=1)=p")

        # =================================================
        # VISUALIZATION
        # =================================================

        st.subheader(
            "📈 Outcome Visualization"
        )

        visualize_outcomes(

            st.session_state.trial_history
        )

        # =================================================
        # ACTIVE LEARNING QUESTIONS
        # =================================================

        st.subheader(
            "🧪 Knowledge Check"
        )

        q1 = st.radio(

            "What happens when p approaches 1?",

            [

                "More failures",

                "More successes",

                "No change"
            ]
        )

        if q1 == "More successes":

            st.success(
                "Correct!"
            )

        q2 = st.radio(

            "Why must probability remain constant?",

            [

                "Because Bernoulli assumes identical trials",

                "Only for visualization",

                "It does not matter"
            ]
        )

        if q2 == "Because Bernoulli assumes identical trials":

            st.success(
                "Correct!"
            )

        q3 = st.radio(

            "What does a Bernoulli trial produce?",

            [

                "Continuous outcomes",

                "One binary outcome",

                "Infinite values"
            ]
        )

        if q3 == "One binary outcome":

            st.success(
                "Correct!"
            )

        # =================================================
        # MINI EXPERIMENT
        # =================================================

        st.subheader(
            "🔬 Mini Experiment"
        )

        st.info(

            "Set p = 0.8 and run 20 trials.\n\n"

            "Then compare against p = 0.2.\n\n"

            "Observe how the visualization changes."
        )

        # =================================================
        # RELATED CONCEPTS
        # =================================================

        st.subheader(
            "🔗 Related Concepts"
        )

        related_cols = st.columns(4)

        related_cols[0].button(
            "Probability"
        )

        related_cols[1].button(
            "Binomial Distribution"
        )

        related_cols[2].button(
            "Statistics"
        )

        related_cols[3].button(
            "Random Variables"
        )

    except Exception as e:

        st.error(

            f"Bernoulli Section Error: {e}"
        )
# Pages with keys
PAGES = {

    "sustainability": {

        "title":
        "🌍 Sustainability Calculator",

        "handler":
        sustainability_section,

        "admin_only":
        False
    },

    "food": {

        "title":
        "🍎 Food Ideas",

        "handler":
        food_ideas,

        "admin_only":
        False
    },

    "smoothie": {

        "title":
        "🥤 Smoothie Maker",

        "handler":
        smoothie_maker_section,

        "admin_only":
        False
    },

    "wellness": {

        "title":
        "🧘 Wellness Exercises",

        "handler": 
        wellness_excercises,

        "admin_only":
        False
    },

    "blog": {

        "title":
        "📝 Blog",

        "handler":
        add_article,

        "admin_only":
        True
    },

    "podcast": {

        "title":
        "🎙 Science Podcast",

        "handler":
        science_podcast,

        "admin_only":
        False
    },

    "learning": {

        "title":
        "🧠 Education & Learning",

        "handler":
        educational_section,

        "admin_only":
        False
    }
} 
# Run the app
if __name__ == "__main__":
    init_db()
    main()
