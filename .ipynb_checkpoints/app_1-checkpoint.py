#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from movie_reco_streamlit import recommendations  # Replace 'your_module' with the module name containing your 'recommendations' function

st.title("Movie Recommender")

user_id = st.number_input("Enter your User_Id:", min_value=1, value=610, step=1)
num_recommendations = st.number_input("How many movie recommendations do you want?", min_value=1, value=20, step=1)

if st.button("Get Recommendations"):
    try:
        result = recommendations(num_recommendations, user_id)
        st.write(f"You will probably like the following movies:")
        st.write(result)
    except Exception as e:
        st.error(f"An error occurred: {e}")

