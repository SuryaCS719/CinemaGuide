import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_[movies_['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies_.iloc[i[0]].movie_id

        recommended_movies.append(movies_.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_ = pd.DataFrame(movie_dict)

# similarity = pickle.load(open('similarity.pkl', 'rb'))
import bz2
import _pickle as cPickle
similarity = cPickle.load(bz2.BZ2File('similarity.pbz2', 'rb'))


st.title('CinemaGuide')


page_bg_img = """
<style>



[data-testid="stAppViewContainer"] {
background-image: url("https://img.freepik.com/free-photo/movie-background-collage_23-2149876028.jpg?w=996&t=st=1685013223~exp=1685013823~hmac=abf1b0c04934aad023a83a318fee63b6fc0d33f3c4183d5c8f532384b5c63074");
background-size: cover;
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


select_movie = st.selectbox('Find Your Perfect Film:',
movies_['title'].values)


if st.button('Find Recommendations'):
    names, posters =  recommend(select_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

