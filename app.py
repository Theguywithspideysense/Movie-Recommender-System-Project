import requests
import streamlit as st
import pickle
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
)

# ── Netflix-style CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import fonts */
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');

  /* Global reset */
  html, body, [class*="css"] {
    background-color: #141414;
    color: #e5e5e5;
    font-family: 'Inter', sans-serif;
  }

  /* Hide Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

  /* ── NAVBAR ── */
  .navbar {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 1rem 0 2rem;
    border-bottom: 1px solid #222;
    margin-bottom: 2.5rem;
  }
  .navbar-logo {
    font-family: 'Bebas Neue', cursive;
    font-size: 2.4rem;
    color: #E50914;
    letter-spacing: 2px;
    line-height: 1;
  }
  .navbar-tagline {
    font-size: 0.8rem;
    color: #888;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  /* ── HERO SEARCH AREA ── */
  .hero-label {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.6rem;
    color: #fff;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
  }
  .hero-sub {
    font-size: 0.85rem;
    color: #aaa;
    margin-bottom: 1rem;
  }

  /* Streamlit selectbox styling */
  .stSelectbox > div > div {
    background-color: #1f1f1f !important;
    border: 1px solid #444 !important;
    color: #fff !important;
    border-radius: 4px;
    font-size: 1rem;
  }

  /* ── RECOMMEND BUTTON ── */
  .stButton > button {
    background-color: #E50914;
    color: #fff;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.6rem 2.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
  }
  .stButton > button:hover {
    background-color: #f40612;
    box-shadow: 0 0 12px rgba(229,9,20,0.5);
  }

  /* ── SECTION TITLE ── */
  .section-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.4rem;
    color: #e5e5e5;
    letter-spacing: 1px;
    margin: 2.5rem 0 1rem;
    border-left: 4px solid #E50914;
    padding-left: 0.6rem;
  }

  /* ── MOVIE CARD ── */
  .movie-card {
    background: #1a1a1a;
    border-radius: 6px;
    overflow: hidden;
    transition: transform 0.25s, box-shadow 0.25s;
    cursor: pointer;
  }
  .movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(0,0,0,0.7);
    z-index: 10;
  }
  .movie-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
  }
  .movie-card-body {
    padding: 0.6rem 0.7rem 0.8rem;
  }
  .movie-title {
    font-weight: 600;
    font-size: 0.85rem;
    color: #fff;
    line-height: 1.3;
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .movie-meta {
    font-size: 0.72rem;
    color: #aaa;
  }
  .movie-badge {
    display: inline-block;
    background: #E50914;
    color: #fff;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 3px;
    margin-top: 0.3rem;
    letter-spacing: 0.5px;
  }

  /* ── DIVIDER ── */
  .red-divider {
    height: 2px;
    background: linear-gradient(to right, #E50914, transparent);
    margin: 2rem 0;
    border: none;
  }

  /* ── FOOTER ── */
  .app-footer {
    text-align: center;
    color: #555;
    font-size: 0.75rem;
    padding-top: 3rem;
    letter-spacing: 0.5px;
  }
</style>
""", unsafe_allow_html=True)


# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    movies = pickle.load(open("movie_list.pkl", "rb"))
    print(movies.columns.tolist())
    print(movies.head())  
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

try:
    movies, similarity = load_data()
    movie_list = movies["title"].values
except FileNotFoundError:
    st.error("⚠️ Could not find **movie_list.pkl** or **similarity.pkl**. Make sure both files are in the same folder as app.py.")
    st.stop()


# ── TMDB Poster Fetch ─────────────────────────────────────────────────────────

API_KEY = "0ff4cc61a5005fcc2bd6e2254fd767e3"

session = requests.Session()

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    try:
        r = session.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        r.raise_for_status()

        poster_path = r.json().get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    except Exception as e:
        print(f"Movie ID {movie_id}: {e}")
        return None

# ── Recommendation Logic ──────────────────────────────────────────────────────
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recs = []
    for i in distances[1:11]:   # top 10
        movie_id = movies.iloc[i[0]].movie_id
        recs.append({
            "title": movies.iloc[i[0]].title,
            "poster": fetch_poster(movie_id),
            "score": round(i[1] * 100, 1),
        })
    return recs


# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div>
    <div class="navbar-logo">🎬 CineMatch</div>
    <div class="navbar-tagline">Powered by ML · Built for movie lovers</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Search / Select ───────────────────────────────────────────────────────────
st.markdown('<div class="hero-label">What are you in the mood for?</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Pick a movie you love — we\'ll find ten more like it.</div>', unsafe_allow_html=True)

selected_movie = st.selectbox(" ", movie_list, label_visibility="collapsed")

if st.button("Get Recommendations →"):
    with st.spinner("Finding your next obsession…"):
        results = recommend(selected_movie)

    st.markdown('<hr class="red-divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Because you liked · {selected_movie}</div>', unsafe_allow_html=True)

    # ── Movie Grid (5 per row, 2 rows) ────────────────────────────────────────
    for row_start in range(0, 10, 5):
        cols = st.columns(5, gap="medium")
        for col, movie in zip(cols, results[row_start:row_start + 5]):
            with col:
                st.markdown(f"""
                <div class="movie-card">
                  <img src="{movie['poster']}" alt="{movie['title']}">
                  <div class="movie-card-body">
                    <div class="movie-title">{movie['title']}</div>
                    <div class="movie-meta">Match Score</div>
                    <div class="movie-badge">{'⭐ ' + str(movie['score'])}%</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="app-footer">CineMatch · ML-powered recommendations · Made with Streamlit</div>', unsafe_allow_html=True)