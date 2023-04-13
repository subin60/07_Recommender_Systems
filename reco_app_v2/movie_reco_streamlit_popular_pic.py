#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
def popular_movies(n):
    # Read input data files
    links = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/links.csv')
    movies = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/movies.csv')
    ratings = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/ratings.csv')
    tags = pd.read_csv('/Users/subinjosethomas/Desktop/Bootcamp/MainCourse/07_Recommender_Systems/ml-latest-small/tags.csv')
    movieID_ratings = pd.merge(movies, ratings, on='movieId')
    Movies_ratings = movieID_ratings.copy()

    # Extract year and movie title information
    Movies_ratings['Year'] = Movies_ratings['title'].str.extract('\((\d{4})\)')
    Movies_ratings['Movie'] = Movies_ratings['title'].str.replace('\((\d{4})\)', '', regex=True)

    # Drop unnecessary columns and rename columns for readability
    Movies_ratings = Movies_ratings.drop(columns=['title', 'timestamp'])
    Movies_ratings = Movies_ratings.rename(columns={'movieId': 'Movie_Id', 'genres': 'Genres', 'userId': 'User_Id', 'rating': 'Movie Rating', 'Year': 'Release Year'})
    #Movies_ratings['Rating Count'] = Movies_ratings.groupby(['Movie_Id', 'Movie', 'Genres', 'Release Year'])['Movie Rating'].count().reset_index()
    Movies_ratings_count = pd.DataFrame(Movies_ratings.groupby(['Movie_Id'])['Movie Rating'].count()).reset_index().rename(columns={'Movie Rating':'Rating Count'})

    # Reorder columns
    Movies_ratings = Movies_ratings.reindex(columns=['Movie_Id', 'Movie', 'Release Year', 'Genres', 'User_Id', 'Movie Rating'])
    #Movies_ratings
    # Group by movie and compute the median rating
    Movies_ratings_1 = Movies_ratings.groupby(['Movie_Id', 'Movie', 'Genres', 'Release Year'])['Movie Rating'].median().reset_index()
    Movies_ratings_1 = Movies_ratings_1.merge(Movies_ratings_count, on='Movie_Id')
    #Movies_ratings_1.sort_values('Movie Rating', ascending=False)
    #Movies_ratings_1.loc[(Movies_ratings_1['rating']>Movies_ratings_1['Movie Rating'].mean())
    #Movies_ratings_1 = Movies_ratings_1.loc[(Movies_ratings_1['Movie Rating']>3) & (Movies_ratings_1['Rating Count']>20)]
    Movies_ratings_1 = Movies_ratings_1.loc[(Movies_ratings_1['Movie Rating']>4) & (Movies_ratings_1['Rating Count']>100)]
    #Movies_ratings_1 = Movies_ratings_1.sort_values('Movie Rating', ascending=False)
    Movies_ratings_1 = Movies_ratings_1.sort_values('Rating Count', ascending=False)

    popular_movies_df = Movies_ratings_1.head(int(n))[['Movie','Genres','Release Year','Movie Rating']]
    
    # Add a new column for movie image URLs
    popular_movies_df['Image URL'] = popular_movies_df.apply(lambda x: get_movie_image_url(x['Movie'], x['Release Year']), axis=1)
    
    return popular_movies_df
n=10
popular_movies(n)


# In[ ]:




