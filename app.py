import streamlit as st
import pickle
import pandas as pd
import requests


st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>

/* Background */
html, body, [class*="css"] {
    background-color: #141414;
    color: white;
    font-family: Arial, sans-serif;
}

/* Title */
.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #E50914;
    margin-bottom: 30px;
}

/* Selectbox */
.stSelectbox label {
    font-size: 20px;
    color: white !important;
}

/* Button */
.stButton>button {
    background-color: #E50914;
    color: white;
    border: none;
    padding: 12px 20px;
    font-size: 18px;
    border-radius: 8px;
    width: 100%;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ff1f1f;
    transform: scale(1.03);
}

/* Movie Cards */
.movie-card {
    background-color: #222;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    transition: 0.3s;
    height: 430px;
}

.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(229,9,20,0.8);
}

.poster {
    width: 100%;
    height: 340px;
    object-fit: cover;
    border-radius: 10px;
}

.movie-name {
    margin-top: 10px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# OMDB API
API_KEY = "74bb5333"


def fetch_poster(movie_name):
    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]

        text = movie_name.replace(" ", "+")
        return f"https://dummyimage.com/300x450/000/fff&text={text}"

    except:
        text = movie_name.replace(" ", "+")
        return f"https://dummyimage.com/300x450/000/fff&text={text}"


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

#UI
st.markdown("<div class='title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)

movie_list = sorted(movies["title"].values)

selected_movie_name = st.selectbox(
    "Search or choose a movie",
    movie_list,
    index=None,
    placeholder="Type movie name here..."
)

if selected_movie_name and st.button("Recommend Movies"):
    with st.spinner("Finding Best Movies For You..."):
        names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{posters[i]}" class="poster">
                <div class="movie-name">{names[i]}</div>
            </div>
            """, unsafe_allow_html=True)
