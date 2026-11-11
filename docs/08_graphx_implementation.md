# GraphX Implementation

## 1. Introduction

The GraphX module analyzes relationships between users and movies using Apache Spark GraphX. The MovieLens 1M dataset is used to construct a user-movie interaction graph.

## 2. Graph Structure

The graph is a bipartite graph containing two types of vertices:

- User vertices represent MovieLens users.
- Movie vertices represent movies.

Each rating creates two directed edges between the user and movie vertices. The rating is stored as the edge attribute.

Movie vertex IDs are shifted by 1,000,000 to avoid collisions with user IDs.

## 3. Dataset Statistics

| Metric | Value |
|---|---:|
| Total ratings | 1,000,209 |
| Unique users in ratings | 6,040 |
| Unique rated movies | 3,706 |
| Total graph vertices | 9,746 |
| Total directed edges | 2,000,418 |

The graph includes movies that appear in the ratings dataset. Movies without ratings are not included in this graph.

## 4. GraphX Algorithms

### 4.1 Vertex Degree Analysis

The implementation uses `graph.inDegrees` to calculate the number of incoming edges for each vertex.

Since each rating creates edges in both directions, the incoming degree represents the number of neighboring vertices for each user or movie.

Output: `results/vertex_degrees`

### 4.2 PageRank

PageRank is executed for 10 iterations using:

`graph.pageRank(10)`

The results are filtered to include movie vertices only. The movie ID offset is removed before saving.

Output: `results/movie_pagerank`

### 4.3 Community Detection

Label Propagation is used to identify groups of connected vertices:

`LabelPropagation.run(graph, 10)`

The output contains vertex IDs and their assigned community labels.

Output: `results/communities`

## 5. Technology Stack

- Apache Spark 3.5.5
- Apache Spark GraphX
- Scala 2.12.18
- Java 17
- SBT 1.10.7
- MovieLens 1M dataset
- GitHub Codespaces

## 6. Execution

The GraphX application is compiled and executed using:

```bash
./sbt clean compile
./sbt "run"
```

The application uses Spark local mode (`local[*]`) inside GitHub Codespaces.

## 7. Conclusion

The GraphX module constructs a user-movie graph and applies degree analysis, PageRank, and Label Propagation. These graph-based results complement the collaborative filtering recommendation model developed using Spark MLlib.
