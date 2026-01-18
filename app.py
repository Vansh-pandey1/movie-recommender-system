import streamlit as st
import pandas as pd
import numpy as np
import faiss
import requests

TMDB_API_KEY = st.secrets['TMDB_API_KEY']

# ---- LOAD DATA ----
@st.cache_resource
def load_data():
    df = pd.read_pickle("movies.pkl")
    embeddings_np = np.load("embeddings.npy")
    index = faiss.read_index("movies.index")
    return df, embeddings_np, index

df, embeddings_np, index = load_data()

# ---- RECOMMEND FUNCTION ----
def recommend_by_index(movie_idx, k=5):
    query_emb = embeddings_np[movie_idx].reshape(1, -1)
    distances, indices = index.search(query_emb, k+1)   # +1 = skip itself
    return indices[0][1:]  # skip the first one (same movie)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url).json()
    
    if "poster_path" in response and response['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w500" + response['poster_path']
    else:
        return None
    
# ---- STREAMLIT UI ----
st.title("🎬 Movie Recommender System")
st.write(":red[.. vansh pandey]")

selected_movie = st.selectbox(
    "Select a movie:",
    df['title'].values
)

if st.button("Recommend :sunglases"):
    movie_idx = df[df['title'] == selected_movie].index[0]
    similar_indices = recommend_by_index(movie_idx, k=5)
    
    st.write(f"### Movies similar to **{selected_movie}**:")
    
    for idx in similar_indices:
        title = df.loc[idx, 'title']
        movie_id = df.loc[idx, 'movie_id']
        poster = fetch_poster(movie_id)
    
        col1, col2 = st.columns([1,3])
        if poster:
            col1.image(poster, use_column_width=True)
        else:
            col1.write("No poster")
        
        col2.write(f"**{title}**")



