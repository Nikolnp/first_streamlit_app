import streamlit
import pandas

streamlit.title('My Moms New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and Bluberry Oatmeal')
streamlit.text(' 🥗 Kale spinah and rocket smoothie')
streamlit.text('🐔 Hard-boiled free range egg')
streamlit.text( '🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#initialise the dataframe
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =  my_fruit_list.set_index('Fruit')

#Add multiselect
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#display the dataframe
streamlit.dataframe(my_fruit_list)
 

