import streamlit as st
import pickle
import pandas as pd
import requests

moviedict = pickle.load(open('movies_dict.pkl', 'rb'))
movie_lists = pd.DataFrame(moviedict)

def fetch_poster(id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=4)  # Add a timeout
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = movie_lists[movie_lists['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_list = []
    recommended_poster = []
    for i in distance:
        # Fetch the movie id
        id = movie_lists.iloc[i[0]].id
        recommended_poster.append(fetch_poster(id))
        recommended_list.append(movie_lists.iloc[i[0]].title)  # Change movie_list to movie_lists

    return recommended_list, recommended_poster

similarity = pickle.load(open('movies_similarity.pkl', 'rb'))

st.title("Movie Recommender App")
movie_list = movie_lists['title'].values
selected_movie_name = st.selectbox(
    "Enter the movie name....",
    movie_list,
    index=None,
    placeholder="Search movie name for recommendation..."
)

if st.button('Show Recommendation'):
    recommended_list, recommended_poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)  # Update to st.columns

    with col1:
        st.text(recommended_list[0])
        st.image(recommended_poster[0])
    with col2:
        st.text(recommended_list[1])
        st.image(recommended_poster[1])
    with col3:
        st.text(recommended_list[2])
        st.image(recommended_poster[2])
    with col4:
        st.text(recommended_list[3])
        st.image(recommended_poster[3])
    with col5:
        st.text(recommended_list[4])
        st.image(recommended_poster[4])
