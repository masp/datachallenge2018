import pandas as pd
import numpy as np
import os.path


movies_df = pd.read_excel('data/movies.xlsx')
links_df = pd.read_excel('data/links.xlsx')
ratings_df = pd.read_excel('data/ratings.xlsx')

# Separate genres into its own dataframe
if not os.path.isfile('data/genres.csv'):
    genres = movies_df['genres'].str.split('|', expand=True)
    flatten_genres = np.unique([x for x in genres.values.flatten() if x is not None])
    genres_df = pd.DataFrame(data={'genreName': flatten_genres})

    movie_genre_link_df = pd.DataFrame(columns=['movieId', 'genreId'])
    movie_genre_link_idx = 0
    for midx, movie_row in movies_df.iterrows():
        movieId = movie_row['movieId']
        for gidx, genre_row in genres_df.iterrows():
            if genre_row['genreName'] in movie_row['genres']:
                movie_genre_link_df.loc[movie_genre_link_idx] = {'genreId': gidx, 'movieId': movieId}
                movie_genre_link_idx += 1

    genres_df.to_csv('data/genres.csv')
    movie_genre_link_df.to_csv('data/moviegenre.csv')

genres_df = pd.read_csv('data/genres.csv')
movie_genre_df = pd.read_csv('data/moviegenre.csv')


ratings_movie_df = pd.merge(ratings_df, movies_df, on='movieId')
ratings_genre_df = pd.merge(movie_genre_df, ratings_movie_df, on='movieId')[['movieId', 'title', 'userId', 'genreId', 'rating', 'timestamp']]
ratings_genre_name_df = pd.merge(ratings_genre_df, genres_df, left_on='genreId', right_index=True)

# Ratings of movies


def get_genre_stats(ratings_genre_df):
    genre_groupby = ratings_genre_name_df.groupby(['genreId', 'genreName'])['rating']

    average_rating_per_genre = genre_groupby.mean()
    count_rating_per_genre = genre_groupby.count()
    return average_rating_per_genre, count_rating_per_genre


# Ratings of genres
avg_rating_gen, count_gen = get_genre_stats(ratings_genre_name_df)

ratings_genre_name_df['rating'] = ratings_genre_name_df.groupby(['userId'])['rating'].transform(lambda x: (x - x.mean()) / x.std())
avg_norm_rating_gen, _ = get_genre_stats(ratings_genre_name_df)