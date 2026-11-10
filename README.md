# 🎬 Movie Recommendation and User Preference Analysis Using PySpark

## Project Overview

An AI-powered distributed movie recommendation system developed using Apache Spark, PySpark MLlib, GraphX, FastAPI, and Streamlit.

The system analyzes user preferences, movie ratings, movie relationships, and user communities to generate personalized movie recommendations.

## Objectives

- Build a distributed movie data processing pipeline using Apache Spark.
- Analyze user ratings and movie preferences.
- Construct user-movie relationship graphs using GraphX.
- Discover user communities and movie relationships.
- Implement collaborative filtering using Spark MLlib ALS.
- Build a hybrid recommendation engine.
- Evaluate model performance and scalability.
- Develop a web application using Streamlit and FastAPI.
- Deploy the complete application using free cloud services.

## Technology Stack

| Component | Technology |
|---|---|
| Data Processing | Apache Spark / PySpark |
| Graph Processing | Spark GraphX |
| Machine Learning | Spark MLlib, Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Dataset | MovieLens |
| Storage | Google Drive / Parquet |
| Version Control | GitHub |
| Cloud Development | Google Colab, GitHub Codespaces |

## Main Features

1. Personalized movie recommendations.
2. Genre-based movie discovery.
3. Collaborative filtering.
4. Content-based recommendations.
5. Hybrid recommendation engine.
6. User preference analysis.
7. Movie popularity analysis.
8. Graph-based community detection.
9. Model performance dashboard.
10. Recommendation evaluation.

## Dataset

Primary dataset: MovieLens 1M.

Download: https://files.grouplens.org/datasets/movielens/ml-1m.zip

Dataset source: https://grouplens.org/datasets/movielens/

## Project Architecture

The system consists of:

- Streamlit frontend
- FastAPI backend
- PySpark data processing pipeline
- Spark MLlib recommendation model
- Scala-based GraphX analytics
- Cloud-based model and data storage

## Project Structure

```text
movie-recommendation-pyspark/
├── README.md
├── docs/
├── notebooks/
├── graphx/
├── backend/
├── frontend/
├── ml/
├── tests/
├── artifacts/
└── reports/
```

## Cloud Development

All development and execution will take place using browser-based cloud platforms.

No local software installation is required.

## Evaluation Metrics

- RMSE
- MAE
- Precision@K
- Recall@K
- NDCG@K
- Catalog Coverage
- Training Time
- Processing Time
- Scalability

## Project Status

Currently in development.

Experimental results and deployment links will be added after implementation and testing.

## Documentation

Detailed technical documentation is maintained in the `docs/` directory.

## License

MIT License

## Acknowledgements

- GroupLens Research
- Apache Spark
- Python
- Streamlit
- FastAPI
