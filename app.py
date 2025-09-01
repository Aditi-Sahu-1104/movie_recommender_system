import streamlit as st
import pickle
import pandas as pd
import requests
# import gdown

# Load Data
# similarity_id="1CuqrM4AVIYdsr2zvs-cFEUWN06QF2tgz"
# movies_id="1cfC7QeQcLBUL_PXTMwbUuvhjM7T_hMUq"

# def download_model(file_id,output):
#     url = f"https://drive.google.com/uc?id={file_id}"
#     gdown.download(url, output, quiet=True)

# download_model(movies_id, "movies.pkl")
# download_model(similarity_id, "similarity.pkl")


movies_dict = pickle.load(open("movies_list.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))
def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8ed75c147325ae8854c21b3fa3f85086&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
# Recommend function
def recommend(movie):
    if movie not in movies["title"].values:
        return ["Movie not found! Please select from the dropdown."], []

    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


# Streamlit UI
st.title("🎬 Movie Recommender System")

# Dropdown to select a movie
selected_movie = st.selectbox("Select a Movie:", movies["title"].values)

# if st.button("Recommend"):
#     names,posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"<p style='text-align:center; font-size:16px; font-weight:bold'>{name}</p>", unsafe_allow_html=True)
            st.image(poster, use_container_width=True)






