
import json
import logging
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cinematch")

# Model data
user_lookup = {}
item_lookup = {}
movie_features = pd.DataFrame()
user_ratings_lookup = {}

artifacts_ready = False
rating_history_available = False
artifact_error = None


# ============================================================
# 2. DATABASE IMPORTS
# ============================================================

from storage import (
    initialize_database,
    get_watchlist,
    add_to_watchlist,
    remove_from_watchlist,
    get_feedback,
    save_feedback,
    delete_feedback,
)


# ============================================================
# 3. MODEL ARTIFACT LOADING
# ============================================================

def load_json(filename: str, required: bool = True):
    """Load a JSON model artifact."""

    path = ARTIFACTS_DIR / filename

    if not path.exists():
        if required:
            raise FileNotFoundError(
                f"Missing model artifact: {path}"
            )

        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_artifacts():
    """Load ALS factors, movie metadata and rating history."""

    global user_lookup
    global item_lookup
    global movie_features
    global user_ratings_lookup
    global artifacts_ready
    global rating_history_available
    global artifact_error

    try:
        logger.info("Loading CineMatch model artifacts...")

        # Load required files.
        user_factors = load_json("user_factors.json")
        item_factors = load_json("item_factors.json")
        movie_data = load_json("movie_features.json")

        if not isinstance(movie_data, list) or not movie_data:
            raise ValueError(
                "movie_features.json must contain a non-empty list."
            )

        features = pd.DataFrame(movie_data)

        required_columns = {
            "movieId",
            "title",
            "genres",
            "hybrid_score",
        }

        missing_columns = required_columns - set(features.columns)

        if missing_columns:
            raise ValueError(
                f"Missing movie feature columns: {sorted(missing_columns)}"
            )

        # Convert ALS factors into lookup dictionaries.
        new_user_lookup = {
            int(row["id"]): np.asarray(
                row["features"], dtype=np.float64
            )
            for row in user_factors
        }

        new_item_lookup = {
            int(row["id"]): np.asarray(
                row["features"], dtype=np.float64
            )
            for row in item_factors
        }

        if not new_user_lookup:
            raise ValueError("No user factors were loaded.")

        if not new_item_lookup:
            raise ValueError("No item factors were loaded.")

        # Validate factor dimensions.
        user_dimensions = {
            len(vector)
            for vector in new_user_lookup.values()
        }

        item_dimensions = {
            len(vector)
            for vector in new_item_lookup.values()
        }

        if (
            len(user_dimensions) != 1
            or len(item_dimensions) != 1
            or user_dimensions != item_dimensions
        ):
            raise ValueError(
                "User and item ALS factor dimensions do not match."
            )

        # Validate numerical values.
        if not all(
            np.all(np.isfinite(vector))
            for vector in new_user_lookup.values()
        ):
            raise ValueError("Invalid values found in user factors.")

        if not all(
            np.all(np.isfinite(vector))
            for vector in new_item_lookup.values()
        ):
            raise ValueError("Invalid values found in item factors.")

        # Normalize movie metadata.
        features["movieId"] = pd.to_numeric(
            features["movieId"],
            errors="coerce"
        )

        features["hybrid_score"] = pd.to_numeric(
            features["hybrid_score"],
            errors="coerce"
        )

        features = features.dropna(
            subset=["movieId", "hybrid_score"]
        ).copy()

        features["movieId"] = features["movieId"].astype(int)
        features["genres"] = (
            features["genres"].fillna("").astype(str)
        )

        features = features.drop_duplicates(
            subset=["movieId"]
        )

        # Load optional user rating history.
        ratings_data = load_json(
            "user_ratings.json",
            required=False
        )

        new_ratings_lookup = {}

        if ratings_data is not None:

            if not isinstance(ratings_data, dict):
                raise ValueError(
                    "user_ratings.json must be a dictionary."
                )

            for user_id, movie_ids in ratings_data.items():

                new_ratings_lookup[int(user_id)] = {
                    int(movie_id)
                    for movie_id in movie_ids
                }

            rating_history_available = True

        else:

            rating_history_available = False

            logger.warning(
                "user_ratings.json not found. "
                "Previously rated movies cannot be excluded."
            )

        # Update global model state only after successful loading.
        user_lookup = new_user_lookup
        item_lookup = new_item_lookup
        movie_features = features
        user_ratings_lookup = new_ratings_lookup

        artifacts_ready = True
        artifact_error = None

        logger.info(
            "Model loaded successfully: %s users, %s item factors, %s movies.",
            len(user_lookup),
            len(item_lookup),
            len(movie_features),
        )

    except Exception as exc:

        artifacts_ready = False
        artifact_error = str(exc)

        logger.exception("Failed to load model artifacts.")

        raise


# ============================================================
# 4. APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize SQLite and load model artifacts on startup."""

    initialize_database()
    load_artifacts()

    yield

    logger.info("CineMatch API shutting down.")


# ============================================================
# 5. FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CineMatch Recommendation API",
    description=(
        "Personalized movie recommendations using Apache Spark MLlib ALS, "
        "movie preferences, persistent watchlists and movie feedback."
    ),
    version="3.0.0",
    lifespan=lifespan,
)


# ============================================================
# 6. REQUEST MODELS
# ============================================================

class RecommendationRequest(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": None,
                "preferred_genres": [
                    "Action",
                    "Comedy",
                    "Adventure"
                ],
                "top_n": 10
            }
        }
    )

    user_id: Optional[int] = Field(
        default=None,
        ge=1
    )

    preferred_genres: list[str] = Field(
        default_factory=list,
        max_length=18
    )

    top_n: int = Field(
        default=10,
        ge=1,
        le=50
    )


class WatchlistRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    anonymous_id: str = Field(
        min_length=8,
        max_length=128
    )

    movie: dict[str, Any]


class FeedbackRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    anonymous_id: str = Field(
        min_length=8,
        max_length=128
    )

    feedback: str = Field(
        pattern="^(like|dislike)$"
    )


# ============================================================
# 7. COMMON HELPERS
# ============================================================

def ensure_ready():
    """Ensure model artifacts are available."""

    if not artifacts_ready:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model is not ready."
        )


def validate_anonymous_id(anonymous_id: str):
    """Validate anonymous browser identifier format."""

    if not re.fullmatch(
        r"[A-Za-z0-9_-]{8,128}",
        anonymous_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid anonymous identifier."
        )


def clean_records(dataframe: pd.DataFrame):
    """Convert Pandas and NumPy values into JSON-safe records."""

    records = dataframe.to_dict(orient="records")
    cleaned = []

    for record in records:

        clean_record = {}

        for key, value in record.items():

            if isinstance(value, np.generic):
                value = value.item()

            if isinstance(value, float) and not np.isfinite(value):
                value = None

            clean_record[key] = value

        cleaned.append(clean_record)

    return cleaned


def filter_by_genres(
    dataframe: pd.DataFrame,
    preferred_genres: list[str]
):
    """Filter movies matching at least one preferred genre."""

    if not preferred_genres:
        return dataframe

    selected_genres = {
        genre.casefold()
        for genre in preferred_genres
    }

    mask = dataframe["genres"].apply(
        lambda value: bool(
            selected_genres.intersection(
                genre.strip().casefold()
                for genre in str(value).split("|")
                if genre.strip()
            )
        )
    )

    return dataframe.loc[mask].copy()


# ============================================================
# 8. GENERAL API ROUTES
# ============================================================

@app.get("/")
def home():

    return {
        "application": "CineMatch",
        "message": "Movie Recommendation API is running.",
        "version": app.version,
        "documentation": "/docs"
    }


@app.get("/health")
def health():

    return {
        "status": (
            "healthy"
            if artifacts_ready
            else "unavailable"
        ),
        "artifacts_ready": artifacts_ready,
        "movies_loaded": len(movie_features),
        "users_loaded": len(user_lookup),
        "items_loaded": len(item_lookup),
        "rating_history_available": rating_history_available,
        "database": "SQLite"
    }


# ============================================================
# 9. MOVIE RECOMMENDATION ROUTE
# ============================================================

@app.post("/recommend")
def recommend(request: RecommendationRequest):

    ensure_ready()

    preferred_genres = [
        genre.strip()
        for genre in request.preferred_genres
        if genre and genre.strip()
    ]

    # --------------------------------------------------------
    # EXISTING USER: ALS RECOMMENDATIONS
    # --------------------------------------------------------

    if request.user_id is not None:

        user_id = request.user_id

        if user_id not in user_lookup:

            raise HTTPException(
                status_code=404,
                detail=(
                    "User ID not found. "
                    "Try a new-user recommendation without user_id."
                )
            )

        user_vector = user_lookup[user_id]

        # Get movies already rated by this user.
        already_rated = user_ratings_lookup.get(
            user_id,
            set()
        )

        scores = []

        for movie_id, movie_vector in item_lookup.items():

            # Exclude previously rated movies.
            if movie_id in already_rated:
                continue

            predicted_rating = float(
                np.dot(user_vector, movie_vector)
            )

            if not np.isfinite(predicted_rating):
                continue

            scores.append({
                "movieId": movie_id,
                "predicted_rating": predicted_rating
            })

        if not scores:

            return {
                "recommendations": [],
                "recommendation_type": "existing_user_als",
                "rating_history_available": rating_history_available,
                "message": "No eligible recommendations are available."
            }

        results = pd.DataFrame(scores)

        results = results.merge(
            movie_features,
            on="movieId",
            how="inner"
        )

        results = filter_by_genres(
            results,
            preferred_genres
        )

        results = results.sort_values(
            by=["predicted_rating", "movieId"],
            ascending=[False, True]
        )

        return {
            "recommendations": clean_records(
                results.head(request.top_n)
            ),
            "recommendation_type": "existing_user_als",
            "rating_history_available": rating_history_available
        }

    # --------------------------------------------------------
    # NEW USER: GENRE AND HYBRID SCORE RECOMMENDATIONS
    # --------------------------------------------------------

    results = filter_by_genres(
        movie_features.copy(),
        preferred_genres
    )

    results = results.sort_values(
        by=["hybrid_score", "movieId"],
        ascending=[False, True]
    )

    return {
        "recommendations": clean_records(
            results.head(request.top_n)
        ),
        "recommendation_type": "new_user_preferences",
        "rating_history_available": rating_history_available
    }


# ============================================================
# 10. PERSISTENT WATCHLIST ROUTES
# ============================================================

@app.get("/watchlist/{anonymous_id}")
def api_get_watchlist(anonymous_id: str):

    validate_anonymous_id(anonymous_id)

    return {
        "watchlist": get_watchlist(anonymous_id)
    }


@app.post("/watchlist")
def api_add_watchlist(request: WatchlistRequest):

    validate_anonymous_id(request.anonymous_id)

    movie = request.movie

    try:

        movie_id = int(movie.get("movieId", 0))

        if movie_id <= 0:
            raise ValueError("A valid movieId is required.")

        if not isinstance(movie.get("title"), str):
            raise ValueError("Movie title is required.")

        # Store only the fields needed by the application.
        safe_movie = {
            "movieId": movie_id,
            "title": movie["title"][:300],
            "genres": str(movie.get("genres", ""))[:500],
        }

        for field in [
            "avg_rating",
            "hybrid_score",
            "predicted_rating",
            "als_predicted_rating"
        ]:

            value = movie.get(field)

            if value is not None:

                numeric_value = float(value)

                if np.isfinite(numeric_value):
                    safe_movie[field] = numeric_value

        saved_watchlist = add_to_watchlist(
            request.anonymous_id,
            safe_movie
        )

        return {
            "message": "Movie added to watchlist.",
            "watchlist": saved_watchlist
        }

    except (ValueError, TypeError) as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@app.delete("/watchlist/{anonymous_id}/{movie_id}")
def api_remove_watchlist(
    anonymous_id: str,
    movie_id: int
):

    validate_anonymous_id(anonymous_id)

    if movie_id <= 0:

        raise HTTPException(
            status_code=400,
            detail="Invalid movie ID."
        )

    updated_watchlist = remove_from_watchlist(
        anonymous_id,
        movie_id
    )

    return {
        "message": "Movie removed from watchlist.",
        "watchlist": updated_watchlist
    }


# ============================================================
# 11. MOVIE FEEDBACK ROUTES
# ============================================================

@app.get("/feedback/{anonymous_id}")
def api_get_feedback(anonymous_id: str):

    validate_anonymous_id(anonymous_id)

    return {
        "feedback": get_feedback(anonymous_id)
    }


@app.put("/feedback/{anonymous_id}/{movie_id}")
def api_save_feedback(
    anonymous_id: str,
    movie_id: int,
    request: FeedbackRequest
):

    validate_anonymous_id(anonymous_id)

    if movie_id <= 0:

        raise HTTPException(
            status_code=400,
            detail="Invalid movie ID."
        )

    if request.anonymous_id != anonymous_id:

        raise HTTPException(
            status_code=400,
            detail="Anonymous IDs in path and body must match."
        )

    updated_feedback = save_feedback(
        anonymous_id,
        movie_id,
        request.feedback
    )

    return {
        "message": "Movie feedback saved.",
        "feedback": updated_feedback
    }


@app.delete("/feedback/{anonymous_id}/{movie_id}")
def api_delete_feedback(
    anonymous_id: str,
    movie_id: int
):

    validate_anonymous_id(anonymous_id)

    if movie_id <= 0:

        raise HTTPException(
            status_code=400,
            detail="Invalid movie ID."
        )

    updated_feedback = delete_feedback(
        anonymous_id,
        movie_id
    )

    return {
        "message": "Movie feedback removed.",
        "feedback": updated_feedback
    }
