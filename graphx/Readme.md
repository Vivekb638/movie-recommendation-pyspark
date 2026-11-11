# GraphX Movie Relationship Analysis

This module builds a user-movie graph using Apache Spark GraphX and the MovieLens 1M dataset.

## Requirements

- Java 17
- Scala 2.12.18
- Apache Spark 3.5.5
- SBT 1.10.7

## Input

Place the MovieLens ratings file at:

`graphx/data/ml-1m/ratings.dat`

Each line contains:

`UserID::MovieID::Rating::Timestamp`

## Run

From the `graphx` directory:

```bash
./sbt clean compile
./sbt "run"
```

## GraphX Analysis

1. Builds user and movie vertices.
2. Creates bidirectional rating edges.
3. Calculates vertex in-degrees.
4. Runs PageRank for 10 iterations.
5. Detects communities using Label Propagation.

## Outputs

- `results/vertex_degrees`
- `results/movie_pagerank`
- `results/communities`

Each output is a Spark directory containing part files and a `_SUCCESS` marker.

## Execution Environment

The application runs in Spark local mode inside GitHub Codespaces. This demonstrates Spark GraphX processing but is not a multi-node distributed cluster.