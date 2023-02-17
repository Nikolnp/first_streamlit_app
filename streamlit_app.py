import streamlit 
import pandas
import requests



#Page Title
streamlit.title('Blog')
# Object notation

# "with" notation
with streamlit.sidebar:
   streamlit.image("http://clipart-library.com/new_gallery/52-522940_clipart-drops-prismatic-transparent-background-brain-png.png")
   if streamlit.button('Say hello'):
      streamlit.write('Why hello there')
   else:
      streamlit.write('Goodbye')

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
   streamlit.text('🥣 Omega 3 and Bluberry Oatmeal')
   streamlit.text(' 🥗 Kale spinah and rocket smoothie')
   streamlit.text('🐔 Hard-boiled free range egg')
   streamlit.text( '🥑🍞 Avocado Toast')
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
   streamlit.text('🥣 Omega 3 and Bluberry Oatmeal')
   streamlit.text(' 🥗 Kale spinah and rocket smoothie')
   streamlit.text('🐔 Hard-boiled free range egg')
   streamlit.text( '🥑🍞 Avocado Toast')
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

#New section to display the API call
#streamlit.header('Fruityvice Fruit Advice!')
#fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)


#output it the screen as a table
#streamlit.dataframe(fruityvice_normalized)


