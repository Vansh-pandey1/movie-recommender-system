import streamlit as st
import pickle
import requests

tmdb_api_key = st.secrets["TMDB_API_KEY"]

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = df[df['title'] == movie].index[0]
    distance = sorted(list(enumerate(top_k[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distance[1:6]:
        # fetch the movie poster
        movie_id = df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters



df = pickle.load(open('data.pkl','rb'))
top_k = pickle.load(open("similar_k.pkl", "rb"))

st.title("MOVIE RECOMMENDATION SYSTEM")
st.write(":red[.. vansh pandey]")
selected_name = st.selectbox("Enter ur movie name"
                    ,df['title'])

if st.button(":blue[Recommend] :sunglasses:"):

    recommended_movie_names,recommended_movie_posters = recommend(selected_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])

            st.image(recommended_movie_posters[i])

