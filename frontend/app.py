
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


# ============================================================
# 2. HTML RENDERING HELPER
# ============================================================

def render_html(content):
    """Render HTML without accidental Markdown code formatting."""
    st.html(textwrap.dedent(content))


# ============================================================
# 3. BACKGROUND IMAGE
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
            rgba(5, 15, 27, 0.65),
            rgba(8, 19, 33, 0.88)
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
# 4. PREMIUM NAVY AND GOLD CSS
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
        rgba(8, 19, 33, 0.91),
        rgba(20, 43, 64, 0.82)
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
    background: rgba(13, 29, 47, 0.93);
    border: 1px solid rgba(217, 164, 65, 0.32);
    border-radius: 18px;
    padding: 24px;
    min-height: 150px;
    backdrop-filter: blur(12px);
    transition: 0.2s ease;
}

.feature:hover {
    border-color: #D9A441;
    transform: translateY(-3px);
}

.feature h3 {
    color: #E9BC62;
    font-size: 18px;
    margin-bottom: 10px;
}

.feature p {
    color: #C4D0DB;
    font-size: 14px;
}

/* SECTION HEADINGS */

.section-heading {
    color: #F4E8D0;
    font-size: 27px;
    font-weight: 750;
    margin: 28px 0 16px 0;
}

/* CONTENT PANELS */

.glass {
    background: rgba(10, 25, 42, 0.94);
    border: 1px solid rgba(217, 164, 65, 0.4);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(12px);
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
    padding: 12px 18px;
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
    box-shadow: 0 0 20px rgba(217, 164, 65, 0.4);
    transform: translateY(-2px);
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

/* DIVIDERS */

hr {
    border-color: rgba(217, 164, 65, 0.3);
}

</style>
"""

css = css.replace(
    "BACKGROUND_PLACEHOLDER",
    background_css
)

st.html(css)


# ============================================================
# 5. SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

if "recommendation_type" not in st.session_state:
    st.session_state.recommendation_type = "New User"


# ============================================================
# 6. TOP NAVIGATION
# ============================================================

logo, navigation = st.columns([1.3, 3])

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

    nav1, nav2, nav3, nav4 = st.columns(4)

    navigation_items = [
        ("Home", nav1),
        ("Discover Movies", nav2),
        ("My Recommendations", nav3),
        ("About Project", nav4)
    ]

    for page_name, column in navigation_items:

        with column:

            if st.button(
                page_name,
                key=f"navigation_{page_name}"
            ):

                st.session_state.page = page_name
                st.rerun()


st.divider()


# ============================================================
# 7. HOME PAGE
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

    with c1:

        render_html(
            """
            <div class="feature">
                <h3>👤 Personalized Discovery</h3>
                <p>
                    Find movies using collaborative filtering
                    powered by Spark MLlib ALS.
                </p>
            </div>
            """
        )

    with c2:

        render_html(
            """
            <div class="feature">
                <h3>🔗 Graph Intelligence</h3>
                <p>
                    Explore user-movie relationships
                    using Apache Spark GraphX.
                </p>
            </div>
            """
        )

    with c3:

        render_html(
            """
            <div class="feature">
                <h3>✨ Smart Recommendations</h3>
                <p>
                    Discover films using movie ratings,
                    genres and recommendation signals.
                </p>
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
                Choose your favorite movie genres, select your
                recommendation type, and let CineMatch find
                movies that match your interests.
            </p>
        </div>
        """
    )

    st.write("")

    if st.button(
        "Explore Movies →",
        key="home_explore"
    ):

        st.session_state.page = "Discover Movies"
        st.rerun()


# ============================================================
# 8. DISCOVER MOVIES PAGE
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

    with st.container(border=True):

        st.subheader("1. Backend Connection")

        api_url = st.text_input(
            "FastAPI Backend URL",
            value=st.session_state.api_url,
            placeholder="https://your-api-url"
        )

        st.session_state.api_url = api_url.strip().rstrip("/")

        st.divider()

        st.subheader("2. Recommendation Type")

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

        st.subheader("3. Select Your Favorite Genres")

        available_genres = [
            "Action",
            "Adventure",
            "Animation",
            "Children's",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film-Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "War",
            "Western"
        ]

        preferred_genres = st.multiselect(
            "Choose one or more genres",
            available_genres,
            default=["Action", "Adventure", "Comedy"]
        )

        st.divider()

        st.subheader("4. Recommendation Quantity")

        top_n = st.slider(
            "Number of movies",
            min_value=5,
            max_value=20,
            value=10
        )

        st.write("")

        if st.button(
            "✨ Generate My Recommendations",
            type="primary",
            key="generate_recommendations"
        ):

            if user_type == "New User" and not preferred_genres:

                st.warning(
                    "Please select at least one genre."
                )

            elif not st.session_state.api_url:

                st.warning(
                    "Please enter your FastAPI URL."
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

                        response = requests.post(
                            f"{st.session_state.api_url}/recommend",
                            json=payload,
                            timeout=90
                        )

                    if response.status_code == 200:

                        st.session_state.recommendations = (
                            response.json().get(
                                "recommendations",
                                []
                            )
                        )

                        st.success(
                            "Your movie recommendations are ready!"
                        )

                        st.session_state.page = "My Recommendations"
                        st.rerun()

                    else:

                        st.error(
                            f"API Error: {response.status_code}"
                        )

                        st.code(response.text)

                except requests.exceptions.RequestException as error:

                    st.error(
                        "Could not connect to the FastAPI backend."
                    )

                    st.info(
                        "Check whether your backend server is running "
                        "and verify the forwarded port URL."
                    )

                    st.code(str(error))


# ============================================================
# 9. MY RECOMMENDATIONS PAGE
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

        df = pd.DataFrame(recommendations)

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "Movies Recommended",
                len(df)
            )

        with metric2:

            if "avg_rating" in df.columns:

                average_rating = pd.to_numeric(
                    df["avg_rating"],
                    errors="coerce"
                ).mean()

                st.metric(
                    "Average Movie Rating",
                    (
                        f"{average_rating:.2f}/5"
                        if pd.notna(average_rating)
                        else "N/A"
                    )
                )

            else:

                st.metric(
                    "Average Movie Rating",
                    "N/A"
                )

        with metric3:

            st.metric(
                "Recommendation Engine",
                "Spark ALS"
            )

        st.divider()

        st.subheader("🍿 Recommended Movies")

        preferred_columns = [
            "title",
            "genres",
            "avg_rating",
            "hybrid_score",
            "predicted_rating",
            "als_predicted_rating"
        ]

        display_columns = [
            column
            for column in preferred_columns
            if column in df.columns
        ]

        display_df = df[display_columns].copy()

        for column in [
            "avg_rating",
            "hybrid_score",
            "predicted_rating",
            "als_predicted_rating"
        ]:

            if column in display_df.columns:

                display_df[column] = pd.to_numeric(
                    display_df[column],
                    errors="coerce"
                ).round(3)

        # Static table: avoids the interactive DataFrame component.
        st.table(display_df)

        st.download_button(
            "⬇️ Download Movie Recommendations",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="CineMatch_recommendations.csv",
            mime="text/csv"
        )

        st.write("")

        if st.button("Find More Movies"):

            st.session_state.page = "Discover Movies"
            st.rerun()


# ============================================================
# 10. ABOUT PROJECT PAGE
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
        v
Streamlit Frontend
        |
        v
Movie Recommendations
        """,
        language="text"
    )

    st.divider()

    st.subheader("📊 Dataset Information")

    st.write(
        "The MovieLens 1M dataset contains movie ratings, "
        "movie information and user information. "
        "It is used for data processing, exploratory analysis, "
        "model training and recommendation evaluation."
    )


# ============================================================
# 11. FOOTER
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
