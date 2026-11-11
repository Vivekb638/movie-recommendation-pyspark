
import os
import uuid
import base64
import textwrap
from pathlib import Path

import pandas as pd
import requests
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CineMatch | Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = BASE_DIR / "assets" / "background.jpg"

GENRES = [
    "Action", "Adventure", "Animation", "Children's",
    "Comedy", "Crime", "Documentary", "Drama",
    "Fantasy", "Film-Noir", "Horror", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Thriller",
    "War", "Western"
]


# ============================================================
# 2. BACKEND CONFIGURATION
# ============================================================

def get_api_url():

    value = os.getenv("API_URL", "").strip()

    if not value:
        try:
            value = st.secrets.get("API_URL", "")
        except Exception:
            value = ""

    return str(value).strip().rstrip("/")


API_URL = get_api_url()


# ============================================================
# 3. ANONYMOUS VISITOR ID
# ============================================================

def get_anonymous_id():

    visitor_id = st.query_params.get("cinematch_id", "")

    if not visitor_id or len(visitor_id) < 8:

        visitor_id = uuid.uuid4().hex

        st.query_params["cinematch_id"] = visitor_id

    return visitor_id


ANONYMOUS_ID = get_anonymous_id()


# ============================================================
# 4. HTML RENDERING
# ============================================================

def render_html(content):
    st.html(textwrap.dedent(content))


# ============================================================
# 5. BACKGROUND IMAGE
# ============================================================

def load_background():

    if not BACKGROUND_PATH.is_file():
        return None

    try:

        image_data = base64.b64encode(
            BACKGROUND_PATH.read_bytes()
        ).decode("utf-8")

        return f"data:image/jpeg;base64,{image_data}"

    except OSError:

        return None


background_image = load_background()

if background_image:

    background_css = f"""
    background-image:
        linear-gradient(
            rgba(5, 15, 27, 0.68),
            rgba(8, 19, 33, 0.91)
        ),
        url("{background_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """

else:

    background_css = """
    background:
        radial-gradient(
            circle at top right,
            #183b58,
            transparent 45%
        ),
        linear-gradient(
            135deg,
            #081321,
            #142b40
        );
    """


# ============================================================
# 6. CINEMATIC NAVY AND GOLD CSS
# ============================================================

css = """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    BACKGROUND_PLACEHOLDER
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stHeader"] {
    background: rgba(8, 19, 33, 0.45);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* BRAND */

.brand {
    font-size: 35px;
    font-weight: 800;
    color: #F4E8D0;
    letter-spacing: -1px;
    margin-bottom: 0;
}

.brand span {
    color: #D9A441;
}

.brand-caption {
    color: #B8C6D5;
    font-size: 12px;
    margin-top: -5px;
}

/* HERO */

.hero {
    padding: 72px 25px;
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(8, 19, 33, 0.94),
        rgba(20, 43, 64, 0.86)
    );
    border: 1px solid rgba(217, 164, 65, 0.55);
    border-radius: 24px;
    margin: 25px 0;
    backdrop-filter: blur(12px);
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.25);
}

.hero h1 {
    font-size: clamp(34px, 5vw, 58px);
    font-weight: 800;
    color: #F4E8D0;
    line-height: 1.2;
    margin-bottom: 12px;
}

.gradient {
    background: linear-gradient(
        90deg,
        #F0C66A,
        #62B8E8
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 17px;
    color: #D2DCE5;
    margin-top: 15px;
}

/* FEATURE CARDS */

.feature {
    background: rgba(13, 29, 47, 0.94);
    border: 1px solid rgba(217, 164, 65, 0.32);
    border-radius: 18px;
    padding: 24px;
    min-height: 150px;
    backdrop-filter: blur(12px);
}

.feature h3 {
    color: #E9BC62;
    font-size: 18px;
}

.feature p {
    color: #C4D0DB;
    font-size: 14px;
}

/* SECTIONS */

.section-heading {
    color: #F4E8D0;
    font-size: 27px;
    font-weight: 750;
    margin: 28px 0 16px;
}

.glass {
    background: rgba(10, 25, 42, 0.94);
    border: 1px solid rgba(217, 164, 65, 0.4);
    border-radius: 20px;
    padding: 25px;
}

.info {
    color: #C4D0DB;
    font-size: 14px;
}

/* INPUTS */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #142B40;
    border-color: #4B7797;
}

label {
    color: #E7EAF0 !important;
}

.stTextInput input,
.stNumberInput input {
    color: #F4E8D0;
}

/* BUTTONS */

.stButton > button {
    width: 100%;
    border: 1px solid #E5BD69;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 700;
    color: #081321;
    background: linear-gradient(
        90deg,
        #E8BC60,
        #F5D995
    );
    transition: 0.2s ease;
}

.stButton > button:hover {
    color: #081321;
    border-color: #FFFFFF;
    box-shadow: none !important;
}

/* NAVIGATION - CLEAN HOVER, NO STATIC SHADOW */

.st-key-top_navigation {
    position: relative !important;
    z-index: 2 !important;
    overflow: visible !important;
    pointer-events: auto !important;
}

.st-key-top_navigation .stButton,
.st-key-top_navigation .stButton > button {
    position: relative !important;
    z-index: 3 !important;
    pointer-events: auto !important;
}

.st-key-top_navigation .stButton > button {
    width: 100%;
    min-height: 44px;
    white-space: nowrap;
    background: rgba(20, 43, 64, 0.95) !important;
    color: #F4E8D0 !important;
    border: 1px solid rgba(217, 164, 65, 0.55) !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    text-shadow: none !important;
    transform: none !important;
    transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease !important;
    cursor: pointer !important;
}

.st-key-top_navigation .stButton > button:hover {
    background: #D9A441 !important;
    color: #081321 !important;
    border-color: #F5D995 !important;
    box-shadow: none !important;
    transform: none !important;
}

.st-key-top_navigation .stButton > button:focus,
.st-key-top_navigation .stButton > button:focus-visible {
    outline: 2px solid #E9BC62 !important;
    outline-offset: 2px !important;
    box-shadow: none !important;
}

.st-key-top_navigation .stButton > button:active {
    background: #C99535 !important;
    color: #081321 !important;
    box-shadow: none !important;
}

/* METRICS */

[data-testid="stMetric"] {
    background: rgba(17, 39, 59, 0.95);
    border: 1px solid rgba(217, 164, 65, 0.4);
    padding: 17px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #C4D0DB;
}

[data-testid="stMetricValue"] {
    color: #F2C76B;
}

/* TABLE */

[data-testid="stTable"] {
    border: 1px solid rgba(217, 164, 65, 0.35);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(10, 25, 42, 0.95);
}

/* FOOTER */

.footer {
    text-align: center;
    color: #AAB9C8;
    font-size: 12px;
    padding: 40px 0 15px;
    border-top: 1px solid rgba(217, 164, 65, 0.2);
    margin-top: 45px;
}

.footer h2 {
    color: #E9BC62;
}

hr {
    border-color: rgba(217, 164, 65, 0.3);
}

</style>
"""

st.html(
    css.replace(
        "BACKGROUND_PLACEHOLDER",
        background_css
    )
)


# ============================================================
# 7. SESSION STATE
# ============================================================

defaults = {
    "page": "Home",
    "recommendations": None,
    "recommendation_type": "New User",
    "last_request": None,
    "watchlist": [],
    "feedback": {}
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# 8. SAFE FASTAPI REQUEST HELPER
# ============================================================

def api_request(method, endpoint, **kwargs):
    """Send a request to FastAPI and safely parse its response."""

    if not API_URL:

        raise RuntimeError(
            "Backend URL is not configured. "
            "Please configure API_URL."
        )

    url = f"{API_URL}{endpoint}"

    try:

        response = requests.request(
            method,
            url,
            timeout=30,
            headers={
                "Accept": "application/json"
            },
            **kwargs
        )

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if not response.ok:

            try:

                detail = response.json().get(
                    "detail",
                    response.text[:500]
                )

            except ValueError:

                detail = response.text[:500]

            raise RuntimeError(
                f"Backend HTTP {response.status_code}: {detail}"
            )

        if "application/json" not in content_type:

            raise RuntimeError(
                "FastAPI returned a non-JSON response. "
                f"Content-Type: {content_type or 'unknown'}. "
                "Check port 8000 and the API_URL configuration."
            )

        try:

            result = response.json()

        except ValueError:

            raise RuntimeError(
                "FastAPI returned invalid JSON: "
                + response.text[:500]
            )

        if not isinstance(result, dict):

            raise RuntimeError(
                "Unexpected response format from FastAPI."
            )

        return result

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "Backend request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Cannot connect to FastAPI. "
            "Check that the backend server is running."
        )


# ============================================================
# 9. WATCHLIST API HELPERS
# ============================================================

def refresh_watchlist():

    result = api_request(
        "GET",
        f"/watchlist/{ANONYMOUS_ID}"
    )

    st.session_state.watchlist = result.get(
        "watchlist",
        []
    )

    return st.session_state.watchlist


def add_movie(movie):

    result = api_request(
        "POST",
        "/watchlist",
        json={
            "anonymous_id": ANONYMOUS_ID,
            "movie": movie
        }
    )

    st.session_state.watchlist = result.get(
        "watchlist",
        []
    )


def remove_movie(movie_id):

    result = api_request(
        "DELETE",
        f"/watchlist/{ANONYMOUS_ID}/{int(movie_id)}"
    )

    st.session_state.watchlist = result.get(
        "watchlist",
        []
    )


# ============================================================
# 10. FEEDBACK API HELPERS
# ============================================================

def refresh_feedback():

    result = api_request(
        "GET",
        f"/feedback/{ANONYMOUS_ID}"
    )

    st.session_state.feedback = {
        str(item["movieId"]): item["feedback"]
        for item in result.get("feedback", [])
    }


def send_feedback(movie_id, feedback):

    result = api_request(
        "PUT",
        f"/feedback/{ANONYMOUS_ID}/{int(movie_id)}",
        json={
            "anonymous_id": ANONYMOUS_ID,
            "feedback": feedback
        }
    )

    st.session_state.feedback = {
        str(item["movieId"]): item["feedback"]
        for item in result.get("feedback", [])
    }


def remove_feedback(movie_id):

    result = api_request(
        "DELETE",
        f"/feedback/{ANONYMOUS_ID}/{int(movie_id)}"
    )

    st.session_state.feedback = {
        str(item["movieId"]): item["feedback"]
        for item in result.get("feedback", [])
    }


# ============================================================
# 11. RECOMMENDATION HELPER
# ============================================================

def generate_recommendations(payload):

    result = api_request(
        "POST",
        "/recommend",
        json=payload
    )

    st.session_state.recommendations = result.get(
        "recommendations",
        []
    )

    st.session_state.last_request = payload

    st.session_state.page = "My Recommendations"


# ============================================================
# 12. TOP NAVIGATION
# ============================================================

with st.container(key="top_navigation"):

    logo, navigation = st.columns([1.25, 4])

    with logo:

        render_html(
            """
            <div class="brand">
                🎬 Cine<span>Match</span>
            </div>
            <div class="brand-caption">
                PERSONALIZED MOVIE DISCOVERY
            </div>
            """
        )

    with navigation:

        nav_columns = st.columns(5)

        pages = [
            ("Home", nav_columns[0]),
            ("Discover", nav_columns[1]),
            ("Recommendations", nav_columns[2]),
            ("Watchlist", nav_columns[3]),
            ("About", nav_columns[4])
        ]

        page_mapping = {
            "Home": "Home",
            "Discover": "Discover Movies",
            "Recommendations": "My Recommendations",
            "Watchlist": "My Watchlist",
            "About": "About Project"
        }

        for page_name, column in pages:

            with column:

                if st.button(
                    page_name,
                    key=f"nav_{page_name}",
                    use_container_width=True
                ):

                    st.session_state.page = page_mapping[page_name]
                    st.rerun()


st.divider()


# ============================================================
# 15. MOVIE DISPLAY COMPONENT
# ============================================================

def display_movie(movie, index, location):

    movie_id = int(movie["movieId"])

    title = str(
        movie.get("title", "Untitled movie")
    )

    genres = str(
        movie.get("genres", "Not specified")
    )

    avg_rating = movie.get("avg_rating")
    predicted = movie.get("predicted_rating")
    hybrid = movie.get("hybrid_score")

    saved_ids = {
        int(item["movieId"])
        for item in st.session_state.watchlist
    }

    current_feedback = st.session_state.feedback.get(
        str(movie_id)
    )

    with st.container(border=True):

        st.markdown(f"### {index}. {title}")

        st.caption(f"Genres: {genres}")

        col1, col2, col3 = st.columns(3)

        if avg_rating is not None:

            col1.metric(
                "Average Rating",
                f"{float(avg_rating):.2f}/5"
            )

        if predicted is not None:

            col2.metric(
                "ALS Prediction",
                f"{float(predicted):.2f}"
            )

        if hybrid is not None:

            col3.metric(
                "Hybrid Score",
                f"{float(hybrid):.3f}"
            )

        button1, button2, button3 = st.columns(3)

        # WATCHLIST BUTTON
        with button1:

            if movie_id in saved_ids:

                if st.button(
                    "✓ Saved",
                    key=f"{location}_saved_{movie_id}"
                ):

                    try:

                        remove_movie(movie_id)

                        st.toast(
                            "Movie removed from watchlist."
                        )

                        st.rerun()

                    except RuntimeError as error:

                        st.error(str(error))

            else:

                if st.button(
                    "＋ Watchlist",
                    key=f"{location}_save_{movie_id}"
                ):

                    try:

                        add_movie(movie)

                        st.toast(
                            "Movie added to watchlist."
                        )

                        st.rerun()

                    except RuntimeError as error:

                        st.error(str(error))

        # LIKE BUTTON
        with button2:

            label = (
                "♥ Liked"
                if current_feedback == "like"
                else "♥ Like"
            )

            if st.button(
                label,
                key=f"{location}_like_{movie_id}"
            ):

                try:

                    if current_feedback == "like":

                        remove_feedback(movie_id)

                    else:

                        send_feedback(movie_id, "like")

                    st.rerun()

                except RuntimeError as error:

                    st.error(str(error))

        # DISLIKE BUTTON
        with button3:

            label = (
                "Disliked"
                if current_feedback == "dislike"
                else "Dislike"
            )

            if st.button(
                label,
                key=f"{location}_dislike_{movie_id}"
            ):

                try:

                    if current_feedback == "dislike":

                        remove_feedback(movie_id)

                    else:

                        send_feedback(movie_id, "dislike")

                    st.rerun()

                except RuntimeError as error:

                    st.error(str(error))



# ============================================================
# 13. HOME PAGE
# ============================================================

if st.session_state.page == "Home":

    render_html(
        """
        <div class="hero">
            <h1>
                Discover Your Next<br>
                <span class="gradient">
                    Favorite Movie.
                </span>
            </h1>
            <p>
                Intelligent recommendations.
                Your preferences. Endless entertainment.
            </p>
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    feature_data = [
        (
            "👤 Personalized Discovery",
            "Find movies using collaborative filtering powered by Spark MLlib ALS."
        ),
        (
            "🔗 Graph Intelligence",
            "Explore user-movie relationships using Apache Spark GraphX."
        ),
        (
            "✨ Smart Recommendations",
            "Discover films using ratings, genres and recommendation signals."
        )
    ]

    for column, item in zip([c1, c2, c3], feature_data):

        with column:

            render_html(
                f"""
                <div class="feature">
                    <h3>{item[0]}</h3>
                    <p>{item[1]}</p>
                </div>
                """
            )

    render_html(
        """
        <div class="section-heading">
            Your Movie Journey Starts Here
        </div>

        <div class="glass">
            <h3 style="color:#E9BC62;">
                🍿 Find Something Amazing to Watch
            </h3>
            <p class="info">
                Discover personalized movies, save your favorites
                and share your feedback.
            </p>
        </div>
        """
    )

    if st.button("Explore Movies →"):

        st.session_state.page = "Discover Movies"
        st.rerun()


# ============================================================
# 14. DISCOVER MOVIES PAGE
# ============================================================

elif st.session_state.page == "Discover Movies":

    render_html(
        """
        <div class="section-heading">
            🎯 Discover Movies
        </div>

        <p class="info">
            Tell CineMatch what you enjoy watching.
            We'll find movies that match your interests.
        </p>
        """
    )

    if not API_URL:

        st.error(
            "Backend URL is not configured. "
            "Configure API_URL before starting Streamlit."
        )

    else:

        with st.container(border=True):

            st.subheader("1. Recommendation Type")

            user_type = st.radio(
                "Choose your profile",
                ["New User", "Existing User"],
                horizontal=True,
                index=(
                    0
                    if st.session_state.recommendation_type == "New User"
                    else 1
                )
            )

            st.session_state.recommendation_type = user_type

            user_id = None

            if user_type == "Existing User":

                user_id = st.number_input(
                    "MovieLens User ID",
                    min_value=1,
                    max_value=6040,
                    value=1,
                    step=1
                )

            st.divider()

            st.subheader("2. Select Your Favorite Genres")

            preferred_genres = st.multiselect(
                "Choose one or more genres",
                GENRES,
                default=["Action", "Adventure", "Comedy"]
            )

            st.divider()

            st.subheader("3. Recommendation Quantity")

            top_n = st.slider(
                "Number of movies",
                min_value=5,
                max_value=20,
                value=10
            )

            if st.button(
                "✨ Generate My Recommendations",
                type="primary"
            ):

                if user_type == "New User" and not preferred_genres:

                    st.warning(
                        "Please select at least one genre."
                    )

                else:

                    payload = {
                        "user_id": (
                            int(user_id)
                            if user_type == "Existing User"
                            else None
                        ),
                        "preferred_genres": preferred_genres,
                        "top_n": int(top_n)
                    }

                    try:

                        with st.spinner(
                            "🎬 Finding movies you'll love..."
                        ):

                            generate_recommendations(payload)

                        st.success(
                            "Your recommendations are ready!"
                        )

                        st.rerun()

                    except RuntimeError as error:

                        st.error(str(error))


# ============================================================
# 16. MY RECOMMENDATIONS PAGE
# ============================================================

elif st.session_state.page == "My Recommendations":

    render_html(
        """
        <div class="section-heading">
            🎥 Your Movie Recommendations
        </div>
        """
    )

    recommendations = st.session_state.recommendations

    if recommendations is None:

        st.info(
            "You haven't generated recommendations yet. "
            "Visit Discover Movies to get started."
        )

        if st.button("Discover Movies →"):

            st.session_state.page = "Discover Movies"
            st.rerun()

    elif len(recommendations) == 0:

        st.warning(
            "No recommendations were returned. "
            "Try selecting different genres."
        )

    else:

        try:

            refresh_watchlist()
            refresh_feedback()

        except RuntimeError as error:

            st.warning(str(error))

        df = pd.DataFrame(recommendations)

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Movies Recommended",
            len(df)
        )

        if "avg_rating" in df.columns:

            average_rating = pd.to_numeric(
                df["avg_rating"],
                errors="coerce"
            ).mean()

            metric2.metric(
                "Average Movie Rating",
                (
                    f"{average_rating:.2f}/5"
                    if pd.notna(average_rating)
                    else "N/A"
                )
            )

        else:

            metric2.metric(
                "Average Movie Rating",
                "N/A"
            )

        metric3.metric(
            "Recommendation Engine",
            (
                "Spark ALS"
                if "predicted_rating" in df.columns
                else "Hybrid Ranking"
            )
        )

        st.divider()

        search = st.text_input(
            "Search recommended movies",
            placeholder="Enter a movie title..."
        )

        filtered = df.copy()

        if search:

            filtered = filtered[
                filtered["title"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if filtered.empty:

            st.info("No matching movies found.")

        else:

            st.subheader("🍿 Recommended Movies")

            for index, movie in enumerate(
                filtered.to_dict("records"),
                start=1
            ):

                display_movie(
                    movie,
                    index,
                    "recommendation"
                )

        st.divider()

        st.download_button(
            "⬇️ Download Movie Recommendations",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="CineMatch_recommendations.csv",
            mime="text/csv"
        )

        if st.button("Find More Movies"):

            st.session_state.page = "Discover Movies"
            st.rerun()


# ============================================================
# 17. MY WATCHLIST PAGE
# ============================================================

elif st.session_state.page == "My Watchlist":

    render_html(
        """
        <div class="section-heading">
            ⭐ My Watchlist
        </div>

        <p class="info">
            Your saved movies are stored in CineMatch.
            They remain available when you refresh this browser
            using the same anonymous visitor link.
        </p>
        """
    )

    try:

        watchlist = refresh_watchlist()
        refresh_feedback()

        st.metric(
            "Saved Movies",
            len(watchlist)
        )

        if not watchlist:

            st.info(
                "Your watchlist is empty. "
                "Discover movies and save your favorites."
            )

            if st.button("Discover Movies →"):

                st.session_state.page = "Discover Movies"
                st.rerun()

        else:

            for index, movie in enumerate(
                watchlist,
                start=1
            ):

                display_movie(
                    movie,
                    index,
                    "watchlist"
                )

    except RuntimeError as error:

        st.error(str(error))

        st.info(
            "Check that FastAPI is running on port 8000 "
            "and that API_URL is correct."
        )


# ============================================================
# 18. ABOUT PROJECT PAGE
# ============================================================

elif st.session_state.page == "About Project":

    render_html(
        """
        <div class="section-heading">
            ℹ️ About CineMatch
        </div>

        <div class="glass">

            <h2 style="color:#E9BC62;">
                Movie Recommendation and User Preference Analysis
            </h2>

            <p class="info">
                CineMatch is a Big Data movie recommendation project
                developed using Apache Spark, GraphX and machine learning.

                It processes movie ratings and user preferences to
                generate personalized movie recommendations.
            </p>

        </div>
        """
    )

    st.subheader("🛠️ Technologies Used")

    technologies = [
        ("Apache Spark", "Distributed data processing"),
        ("PySpark", "Data preprocessing and analysis"),
        ("Spark MLlib ALS", "Collaborative filtering"),
        ("Spark GraphX", "User-movie graph analysis"),
        ("FastAPI", "Recommendation backend"),
        ("Streamlit", "Interactive frontend"),
        ("SQLite", "Persistent anonymous watchlists and feedback"),
        ("MovieLens 1M", "Movie ratings dataset")
    ]

    for technology, purpose in technologies:

        st.markdown(
            f"**{technology}** — {purpose}"
        )

    st.divider()

    st.subheader("🏗️ Project Architecture")

    st.code(
        """
MovieLens 1M Dataset
        |
        v
Apache Spark / PySpark
        |
        +------> GraphX Analysis
        |
        +------> MLlib ALS Model
        |
        v
Recommendation Engine
        |
        v
FastAPI Backend
        |
        +------> SQLite Watchlist
        |
        +------> Movie Feedback
        |
        v
Streamlit Frontend
        |
        v
Personalized Movie Discovery
        """,
        language="text"
    )

    st.divider()

    st.subheader("📊 Dataset Information")

    st.write(
        "The MovieLens 1M dataset contains movie ratings, "
        "movie information and user information. "
        "It supports data preprocessing, exploratory analysis, "
        "model training and recommendation evaluation."
    )


# ============================================================
# 19. FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        <h2>🎬 CineMatch</h2>

        <p>
            Movie Recommendation and User Preference Analysis
        </p>

        <p>
            Apache Spark · PySpark · GraphX · MLlib · FastAPI · Streamlit
        </p>

        <p>
            Academic Big Data Project
        </p>

    </div>
    """
)
