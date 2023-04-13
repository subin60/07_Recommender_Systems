#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import imdb
import requests
from PIL import Image
from io import BytesIO
import streamlit as st


from imdb import IMDb
import requests
from PIL import Image
from io import BytesIO

ia = IMDb()

def get_movie_image_url(title, year):
    try:
        results = ia.search_movie(f"{title} ({year})")
        movie = results[0]
        ia.update(movie)
        url = movie['full-size cover url']
        return url
    except:
        return None

# Function to generate movie recommendations for a user
def recommendations(n, user_id):
    # Read input data files
    links = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/links.csv')
    movies = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/movies.csv')
    ratings = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/ratings.csv')
    tags = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/tags.csv')

    # Merge movie and rating data
    movieID_ratings = pd.merge(movies, ratings, on='movieId')
    Movies_ratings = movieID_ratings.copy()

    # Extract year and movie title information
    Movies_ratings['Year'] = Movies_ratings['title'].str.extract('\((\d{4})\)')
    Movies_ratings['Movie'] = Movies_ratings['title'].str.replace('\((\d{4})\)', '', regex=True)

    # Drop unnecessary columns and rename columns for readability
    Movies_ratings = Movies_ratings.drop(columns=['title', 'timestamp'])
    Movies_ratings = Movies_ratings.rename(columns={'movieId': 'Movie_Id', 'genres': 'Genres', 'userId': 'User_Id', 'rating': 'Movie Rating', 'Year': 'Release Year'})

    # Reorder columns
    Movies_ratings = Movies_ratings.reindex(columns=['Movie_Id', 'Movie', 'Release Year', 'Genres', 'User_Id', 'Movie Rating'])

    # Group by movie and compute the median rating
    Movies_ratings_1 = Movies_ratings.groupby(['Movie_Id', 'Movie', 'Genres', 'Release Year'])['Movie Rating'].median().reset_index()

    # Create a pivot table with User_Id as rows and Movie_Id as columns
    users_items = pd.pivot_table(data=Movies_ratings,
                                 values='Movie Rating',
                                 index='User_Id',
                                 columns='Movie_Id')
    users_items.fillna(0, inplace=True)

    # Compute cosine similarity between users
    user_similarities = pd.DataFrame(cosine_similarity(users_items),
                                     columns=users_items.index,
                                     index=users_items.index)

    # Calculate weights for user similarities
    weights = (
        user_similarities
        .query('User_Id!=@user_id')[user_id]
        / sum(user_similarities
        .query('User_Id!=@user_id')[user_id])
    )

    # Identify movies the target user has not seen
    not_seen_movies = (
        users_items
        .loc[users_items.index != user_id
             , users_items.loc[user_id, :] == 0]
    )

    # Calculate weighted averages for not seen movies
    weighted_averages = (
        pd.DataFrame(not_seen_movies.T.dot(weights),
                     columns=['Predicted_Rating'])
    )

    # Merge weighted averages with movie details
    recommendations_for_user = (
        weighted_averages
        .merge(Movies_ratings_1, left_index=True, right_on='Movie_Id')
    )

    # Return the top-n recommendations sorted by predicted rating
    #return (
        #recommendations_for_user
        #.sort_values('Predicted_Rating', ascending=False)
        #.head(n)
    #)
    
    recom = (
        recommendations_for_user
        .sort_values('Predicted_Rating', ascending=False)
    )
    
    recom = (
        recommendations_for_user
        .sort_values('Predicted_Rating', ascending=False)
    )
    
    recom_df = recom[['Movie', 'Genres', 'Release Year', 'Movie Rating']].head(n)
    
    
    recom_df['Image URL'] = recom_df.apply(lambda x: get_movie_image_url(x['Movie'], x['Release Year']), axis=1)
    
    return recom_df

recommendations(5,4)


# In[ ]:




