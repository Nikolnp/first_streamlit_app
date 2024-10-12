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
    # Brands I Support Section
    st.title("Brands I Support")
    
    # Colibri Garden
    col1, col2 = st.columns([1, 4])
    with col1:
        # Update this URL with a direct link to the Colibri Garden logo if needed
        st.image("https://www.colibrigarden.com/wp-content/uploads/2020/06/logo-footer.png", width=100, caption="Colibri Garden")  
    with col2:
        st.markdown("[**Colibri Garden**](https://www.colibrigarden.com)")
        st.caption("Colibri Garden provides organic, eco-friendly gardening solutions and tools, promoting sustainable and natural living.")
    
    # Bokyna
    col3, col4 = st.columns([1, 4])
    with col3:
        # Update this URL with a direct link to the Bokyna logo
        st.image("https://bokyna.com/assets/images/bokyna-logo.png", width=100, caption="Bokyna")  
    with col4:
        st.markdown("[**Bokyna**](https://www.bokyna.com)")
        st.caption("Bokyna creates unique and handcrafted sandals, combining style, sustainability, and comfort for every occasion.")
    
    # Luvsko
    col5, col6 = st.columns([1, 4])
    with col5:
        # Update this URL with a direct link to the Luvsko logo
        st.image("https://www.luvsko.com/wp-content/uploads/2021/05/Luvsko-Logo-Header.png", width=100, caption="Luvsko")  
    with col6:
        st.markdown("[**Luvsko**](https://www.luvsko.com)")
        st.caption("Luvsko specializes in vegan and sustainable footwear, offering stylish and cruelty-free shoes that are comfortable and ethically made.")
    

# Run the app
if __name__ == "__main__":
    main()
