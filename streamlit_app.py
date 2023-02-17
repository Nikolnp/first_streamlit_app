import streamlit 
import pandas
import requests



#Page Title
streamlit.title('HEALTHY CAN BE TAISTY')
#Columns
col1, col2, col3, = streamlit.columns(3)
with col1:
   #empty col
with col2:
   streamlit.image("http://www.pngall.com/wp-content/uploads/2016/07/Meditation-Transparent.png")

col4, col5, col6 = streamlit.columns(3)
with col3:
   #empty col

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


