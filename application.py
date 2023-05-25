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


# st.title('CinemaGuide')


page_bg_img = """
<style>



[data-testid="stAppViewContainer"] {
background-image: url("https://drive.google.com/uc?id=1f0EfMNxWi7yoZEGsKEcWn4JZTdo131mc");
background-size: cover;
olor: white;

}

.title {
    color: #ADD8E6;
    font-size: 118px;
    text-align: center;
    margin-bottom: 50px;
    
}

.header {
    margin-bottom: 50em;
    color: #CCCCFF;
    # color: #6495ED;
    font-weight: bold;
    font-size: 25px;
    text-align: center;
    margin-bottom: -15em;
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown('<p class="title" style="font-weight: bold;">CinemaGuide</p>', unsafe_allow_html=True)

# st.markdown('<p class="title">CinemaGuide</p>', unsafe_allow_html=True)



# select_movie = st.selectbox('Find Your Perfect Film:', movies_['title'].values)

st.markdown('<p class="header">Find your perfect film! </p>', unsafe_allow_html=True)

select_movie = st.selectbox('',movies_['title'].values)


if st.markdown(
    """
    <style>
    .my-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 5vh;
        margin-bottom: 2em;
    }

    .my-button {
        padding: 10px 40px;
        background-color: #800000;
        color: #F5F5DC;
        font-weight: bold;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
    }

    .movie-container {
        display: flex;
        overflow-x: auto;
        gap: 2em;
        margin-top: 1em;
    }

    .movie-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .movie-title {
        margin-top: 0.3em;
        margin-bottom: 2.5em;
        font-weight: bold;
    }
    </style>
    <div class="my-button-container">
        <div class="my-button">Discover Movies</div>
    </div>
    """,
    unsafe_allow_html=True
):
    names, posters = recommend(select_movie)

    st.markdown('<div class="movie-container">', unsafe_allow_html=True)
    for name, poster in zip(names, posters):
        st.markdown(
            """
            <div class="movie-card">
                <img src="{}" width="150">
                <p class="movie-title">{}</p>
            </div>
            """.format(poster, name),
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
