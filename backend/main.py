
import json
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"


def load_json(filename):
    path = ARTIFACTS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing artifact: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


user_factors = load_json("user_factors.json")
item_factors = load_json("item_factors.json")
movie_features = pd.DataFrame(load_json("movie_features.json"))

user_lookup = {
    int(row["id"]): np.array(row["features"], dtype=float)
    for row in user_factors
}

item_lookup = {
    int(row["id"]): np.array(row["features"], dtype=float)
    for row in item_factors
}

app = FastAPI(
    title="Movie Recommendation API",
    description="Movie recommendations using ALS and movie preferences",
    version="1.0"
)


class RecommendationRequest(BaseModel):
    user_id: Optional[int] = None
    preferred_genres: List[str] = Field(default_factory=list)
    top_n: int = Field(default=10, ge=1, le=50)


@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "movies_loaded": len(movie_features),
        "users_loaded": len(user_lookup)
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest):

    if request.user_id is not None:
        user_id = request.user_id

        if user_id not in user_lookup:
            raise HTTPException(
                status_code=404,
                detail="User ID not found. Try without user_id for new-user recommendations."
            )

        user_vector = user_lookup[user_id]

        scores = []

        for movie_id, movie_vector in item_lookup.items():
            predicted_rating = float(np.dot(user_vector, movie_vector))

            scores.append({
                "movieId": movie_id,
                "predicted_rating": predicted_rating
            })

        results = pd.DataFrame(scores)

        results = results.merge(
            movie_features,
            on="movieId",
            how="left"
        )

        results = results.sort_values(
            "predicted_rating",
            ascending=False
        )

        return {
            "recommendations": results.head(request.top_n)
            .replace({np.nan: None})
            .to_dict("records")
        }

    results = movie_features.copy()

    if request.preferred_genres:
        results = results[
            results["genres"].fillna("").apply(
                lambda genres: any(
                    genre.strip() in request.preferred_genres
                    for genre in genres.split("|")
                )
            )
        ]

    results = results.sort_values(
        "hybrid_score",
        ascending=False
    )

    return {
        "recommendations": results.head(request.top_n)
        .replace({np.nan: None})
        .to_dict("records")
    }
