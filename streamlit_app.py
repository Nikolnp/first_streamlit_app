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
    
  # Bokyna Logo from Facebook (not guaranteed to work)
    col3, col4 = st.columns([1, 4])
    with col3:
        st.image("data:image/png;base64,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", width=100)  # Facebook-hosted image
    with col4:
        st.markdown("[**Bokyna**](https://www.bokyna.com)")
        st.caption("Bokyna creates unique and handcrafted sandals, combining style, sustainability, and comfort for every occasion.")

    
    # Luvsko
    col5, col6 = st.columns([1, 4])
    with col5:
        st.image("data:image/jpeg;base64,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", width=100)  # Direct link to favicon (assuming no other image available)
    with col6:
        st.markdown("[**Luvsko**](https://www.luvsko.com)")
        st.caption("Luvsko specializes in vegan and sustainable footwear, offering stylish and cruelty-free shoes that are comfortable and ethically made.")

# Run the app
if __name__ == "__main__":
    main()
