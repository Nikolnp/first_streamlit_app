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
        st.image("data:image/jpeg;base64,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R+ZrL6FznDy2HupUk9spxcdL+Tm8HYWQwVLWgWbVSAHuBYDXrYLQFAcD4B/w3SMgJzSaukd3e7V30Gg+in1cVSM5u5MIiKiQiIgCIiAIiIAiIgCIiAIiIAvCupW10b4ni7XtLT7EWK90QGR4LxHP4buNDWxPfTtceTM0X8pJPsRc7bg36WXXxT4l0mKQPpqWKSofMwstlIAzC225I3sFps8DKgZXta5vZwBH2K8qXD4KM3jijYf4WNb+QUcX0mac4t21swzgrAK3iKSSikq5adtM0Xjubi5OgAI27+oVxPhnVYd56TE52vHR+x+x/sVK8XcKVDp24hQPDKlos9h+WVvY+vvv6WUZJx9isH6t+DScza4e4tv3sIzp/Uo4pdluTluJ4M8QK3hbNBidOXPDSYpY7Wlt0PTtqPqF40GA4h4hgVFbO6CndrHDFpdvQ69+5B9gvei4Jq+LpTV4qcgylsdOw2yA6X30sdepJtfsmDtxvgsOpWUvxsAJMTxIGloJ2N+n8PTobJvz0Nf61Z2S+FtNhzS+mq6ime0Xz5wW6D94WGn1WfVnEdRi8jIa6d01HDL+skhYbPA2JIGt/VXep4exnjMgVsjaWmvcwxm7neh1/M212Kv+FYTBhMLYImBsbRa29+5N9ye5XeN9aOc672/+8kVhfFeFcpvKqYGRtbo3MG5R2ymxVT4u4rdxZ/6dhoMpk0lmAORjL669u5+gVyquDsNq3Zn0cJPfIB+Sk8Pw6HDW5IYmRt7NaB+W6ppvRCcVsjuHeGKbA4GQtjY4tHmeWi7ndSdO6l4qdkPysa32AH5L0RUlRLdhERdOBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQH//Z", width=100)  # Direct link to logo
    with col2:
        st.markdown("[**Colibri Garden**](https://www.colibrigarden.com)")
        st.caption("Colibri Garden provides organic, eco-friendly gardening solutions and tools, promoting sustainable and natural living.")
    
    # Bokyna
    col3, col4 = st.columns([1, 4])
    with col3:
        st.image("data:image/jpeg;base64,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", width=100)  # Direct link to favicon (assuming no other image available)
    with col4:
        st.markdown("[**Bokyna**](https://www.bokyna.com)")
        st.caption("Bokyna creates unique and handcrafted sandals, combining style, sustainability, and comfort for every occasion.")
    
    # Luvsko
    col5, col6 = st.columns([1, 4])
    with col5:
        st.image("https://www.luvsko.com/favicon.ico", width=100)  # Direct link to favicon (assuming no other image available)
    with col6:
        st.markdown("[**Luvsko**](https://www.luvsko.com)")
        st.caption("Luvsko specializes in vegan and sustainable footwear, offering stylish and cruelty-free shoes that are comfortable and ethically made.")
    

# Run the app
if __name__ == "__main__":
    main()
