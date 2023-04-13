#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

from movie_reco_streamlit_V01 import recommendations
from movie_reco_streamlit_popular import popular_movies

#st.title("Welcome To WBSFLIX Movie Recommender")
st.markdown('<h1 style="font-size: 34px; color: #87CEEB;">Welcome To WBSFLIX Movie Recommender</h1>', unsafe_allow_html=True)

st.markdown('<h1 style="font-size: 24px; color: #FFD700;">Blockbusters</h1>', unsafe_allow_html=True)
#st.subheader('Blockbusters')


num_popular_movies = st.slider("How many blockbusters or popular movies would you like to display?", min_value=1, max_value=20, value=5, step=1)

def dataframe_to_markdown(df):
    markdown = '| ' + 'No. | ' + ' | '.join(df.columns) + ' |\n'
    markdown += '| ' + ' | '.join(['---'] * (len(df.columns) + 1)) + ' |\n'

    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        row_str = [str(idx)] + [str(e) for e in row]
        row_str[2] = row_str[2].replace("|", ", ")
        markdown += '| ' + ' | '.join(row_str) + ' |\n'
    return markdown

popular_movies_df = popular_movies(num_popular_movies)
st.write("Most popular movies:")
st.markdown(dataframe_to_markdown(popular_movies_df), unsafe_allow_html=True)

st.divider()

st.markdown('<h1 style="font-size: 24px; color: #FFD700;">Our Carefully Selected Movie Suggestions For You...</h1>', unsafe_allow_html=True)
#st.subheader('Our Carefully Selected Movie Suggestions For You')
user_id = st.number_input("Please enter your user id:", min_value=1, max_value=610, value=610, step=1)
num_recommendations = st.slider("How many personalized movie recommendations would you like to receive?", min_value=1, max_value=20, value=5, step=1)

if st.button("Get Recommendations"):
    try:
        result = recommendations(num_recommendations, user_id)
        st.write(f"You will probably like the following movies:")
        st.markdown(dataframe_to_markdown(result), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.divider()


# In[ ]:




