#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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
    Movies_ratings = Movies_ratings.rename(columns={'movieId': 'Movie_Id', 'genres': 'Genres', 'userId': 'User_Id', 'rating': 'Rating', 'Year': 'Release_Year'})

    # Reorder columns
    Movies_ratings = Movies_ratings.reindex(columns=['Movie_Id', 'Movie', 'Release_Year', 'Genres', 'User_Id', 'Rating'])

    # Group by movie and compute the median rating
    Movies_ratings_1 = Movies_ratings.groupby(['Movie_Id', 'Movie', 'Genres', 'Release_Year'])['Rating'].median().reset_index()

    # Create a pivot table with User_Id as rows and Movie_Id as columns
    users_items = pd.pivot_table(data=Movies_ratings,
                                 values='Rating',
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
    
    return recom[['Movie', 'Genres', 'Release_Year', 'Rating']].head(n)

# Function for chat bot interaction
#def chat_bot():
    #print("Hi! I'm your personal recommender. Tell me your User_Id.\n")
    #user_id = int(input())
    #print('\nHow many movie recommendations you want?\n')
    #n = int(input())
    #recom = recommendations(n, user_id)
    #print(f"\nYou will probably like the following movies:\n")
    #return recom[['Movie', 'Genres', 'Release_Year', 'Rating']]


#chat_bot()

#recommendations(5,4)


# In[ ]:




