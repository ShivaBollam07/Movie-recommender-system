import streamlit as st
import pickle
import pandas as pd
import requests

def fetchposter(movieid):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movieid))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:11]  # Change the number of recommendations to 11

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetchposter(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select your option?',
     movies['title'].values
)

if st.button('Recommend'):
    recommended_movies, recommended_movies_posters = recommend(selected_movie_name)

    # Create 10 columns
    cols = st.columns(6)

    for i in range(6):
        with cols[i]:
            st.text(recommended_movies[i])
            st.image(recommended_movies_posters[i])
