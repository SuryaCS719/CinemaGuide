import streamlit as st
import pickle
import pandas as pd
import requests
from imdb import IMDb


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
            movie_id))
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


def get_imdb_info(movie_name):
    ia = IMDb()
    try:
        # Search for the movie by name
        results = ia.search_movie(movie_name)
        if results:
            movie = results[0]  # Get the first search result
            imdb_id = movie.movieID
            imdb_link = ia.get_imdbURL(movie)
            return imdb_id, imdb_link
        else:
            print("No results found for the movie:", movie_name)
            return None, None
    except Exception as e:
        print(f"Error fetching IMDb info: {str(e)}")
        return None, None



movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_ = pd.DataFrame(movie_dict)

# similarity= pickle.load(open('similarity.pkl', 'rb'))
import bz2
import _pickle as cPickle

similarity = cPickle.load(bz2.BZ2File('similarity.pbz2', 'rb'))


# st.title('CinemaGuide')


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://github.com/SuryaCS719/CinemaGuide/blob/master/cinemaguide%20bg.png?raw=true");
             background-size: cover;
             color: white;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


add_bg_from_url()

# from streamlit_option_menu import option_menu

# col1, col2, col3 = st.columns(3)
# selected = col1.radio("Menu", ["Home", "About", "Contact"])

# Custom CSS to hide the sidebar by default
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        margin-left: -16rem;
        transition: margin-left 0.3s;
    }
    .sidebar.--collapsed .sidebar-content {
        margin-left: 0;
    }
    .reportview-container .main .block-container {
        max-width: 100%;
        padding-top: 0rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Hide the sidebar by default
st.markdown('<style>div.Widget.row-widget.stRadio > div{visibility:hidden}</style>', unsafe_allow_html=True)

# Menu options as separate tabs
selected = st.sidebar.radio("Menu", ["Home", "About", "Contact"])


if selected == "Home":
    # Code for Home page
    page_bg_img = """
        <style>



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

    # st.markdown('<p class="title" style="font-weight: bold;">CinemaGuidee</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: bold; font-size: 70px; text-align: center;">CinemaGuide</p>', unsafe_allow_html=True)


    # st.markdown('<p class="title">CinemaGuide</p>', unsafe_allow_html=True)

    # select_movie = st.selectbox('Find Your Perfect Film:', movies_['title'].values)

    st.markdown('<p class="header">Find your perfect film! </p>', unsafe_allow_html=True)

    select_movie = st.selectbox('', movies_['title'].values)

    button_style = '''
            <style>
            .stButton button {
                background-color: #800000;
                color: #F5F5DC;
                text-align: center;
                display: block;
                margin: 0 auto;
                padding: 10px 25px;
                border-radius: 5px;
                cursor: default;
                font-weight: bold;
                font-style: italic;
            }
            </style>
        '''

    st.markdown(button_style, unsafe_allow_html=True)

    if st.button('Discover Movies'):

        if st.markdown(
                """
                <style>

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

                """,
                unsafe_allow_html=True
        ):
            names, posters = recommend(select_movie)

            # st.markdown('<div class="movie-container">', unsafe_allow_html=True)
            # for name, poster in zip(names, posters):
            #     st.markdown(
            #         """
            #         <div class="movie-card">
            #             <img src="{}" width="150">
            #             <p class="movie-title">{}</p>
            #         </div>
            #         """.format(poster, name),
            #         unsafe_allow_html=True
            #     )
            # st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="movie-container">', unsafe_allow_html=True)
            for name, poster in zip(names, posters):
                imdb_id, imdb_link = get_imdb_info(name)
                st.markdown(
                    """
                    <div class="movie-card">
                        <a href="{}" target="_blank">
                            <img src="{}" width="150">
                            <p class="movie-title">{}</p>
                        </a>
                    </div>
                    """.format(imdb_link, poster, name),
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)


# elif selected == "About":
#     # Code for About page
#     st.title("Welcome to CinemaGuide!")
#     st.markdown("""
#             CinemaGuide is a powerful movie recommendation system designed to enhance your movie-watching experience. We understand that finding the perfect movie to watch can be overwhelming, with countless options available. That's where CinemaGuide comes in. Our intelligent recommendation algorithm analyzes your preferences and provides personalized movie suggestions tailored just for you.
#
#             Key Features:
#
#             1. Personalized Recommendations:
#                CinemaGuide takes into account your movie preferences, including genres, actors, directors, and past viewing history, to generate highly personalized recommendations. Say goodbye to endlessly scrolling through movie lists!
#
#             2. Rich Movie Information:
#                Discover detailed information about movies, including plot summaries, cast and crew details, ratings, and reviews. Make informed decisions and explore the world of cinema like never before.
#
#             3. Similar Movie Suggestions:
#                Found a movie you loved? CinemaGuide suggests similar movies that you might enjoy based on your preferences. Expand your movie repertoire and explore new genres.
#
#             4. User-Friendly Interface:
#                We've designed CinemaGuide to be user-friendly and intuitive. With a clean and easy-to-navigate interface, finding your next movie has never been easier.
#         """)

elif selected == "About":
    # Code for About page
    st.title("Welcome to CinemaGuide!")
    st.markdown("""
        <span style="color: #DDDDDD;"><b>CinemaGuide is a powerful movie recommendation system designed to enhance your film selection process. We understand that finding the perfect movie to watch can be overwhelming, with countless options available. That's where CinemaGuide comes in. Our intelligent recommendation algorithm analyzes your preferences and provides personalized movie suggestions tailored just for you.</b>
        </span>
        <br>
        <b><h6> With CinemaGuide, you can expect: </h6></b>
        <span style="color: #F5F5DC;"><b>1. <u>Personalized Recommendations</u>:</b></span> CinemaGuide takes into account your movie preferences, including genres, actors, directors, and past viewing history, to generate highly personalized recommendations. Say goodbye to endlessly scrolling through movie lists!
        <br><br>
        <span style="color: #F5F5DC;"><b>2. <u>Rich Movie Information</u>:</b></span> Discover detailed information about movies, including plot summaries, cast and crew details, ratings, and reviews. Make informed decisions and explore the world of cinema like never before.
        <br><br>
        <span style="color: #F5F5DC;"><b>3. <u>Similar Movie Suggestions</u>:</b></span> Found a movie you loved? CinemaGuide suggests similar movies that you might enjoy based on your preferences. Expand your movie repertoire and explore new genres.
        <br><br>
        <span style="color: #F5F5DC;"><b>4. <u>User-Friendly Interface</u>:</b></span> We've designed CinemaGuide to be user-friendly and intuitive. With a clean and easy-to-navigate interface, finding your next movie has never been easier.
        <br><br>
        <h10> Let us help you discover the perfect movies that match your tastes and preferences. </h10>
        """, unsafe_allow_html=True)


elif selected == "Contact":
    # Code for Contact page

    st.subheader("Contact Us")

    # import streamlit as st  # pip install streamlit

    # st.header(":mailbox: Get In Touch With Me!")

    st.write("For any inquiries or feedback, please don't hesitate to reach out to us using the contact information provided.")
    # st.subheader("Reach out to us:")
    # st.write("- Email: contact@cinemaguide.com")
    st.write(":mailbox: team.cinemaguide@gmail.com")
    st.write("Have questions, feedback, or suggestions? We'd love to hear from you!")


    contact_form = """
        <form action="https://formsubmit.co/team.cinemaguide@gmail.com" method="POST">
             <input type="hidden" name="_captcha" value="false">
             <input type="text" name="name" placeholder="Your name" required>
             <input type="email" name="email" placeholder="Your email" required>
             <textarea name="Suggestion" placeholder="Your suggestion here"></textarea>
             <button type="submit">Send</button>
        </form>
        """

    st.markdown(contact_form, unsafe_allow_html=True)


    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")





