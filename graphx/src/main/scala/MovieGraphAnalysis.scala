import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.graphx._
import org.apache.spark.graphx.lib.LabelPropagation

object MovieGraphAnalysis {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf()
      .setAppName("MovieRecommendationGraphX")
      .setMaster("local[*]")

    val sc = new SparkContext(conf)
    sc.setLogLevel("WARN")

    val inputPath = "data/ml-1m/ratings.dat"
    val outputPath = "results"
    val movieOffset = 1000000L

    // Read MovieLens ratings
    val ratings = sc.textFile(inputPath)
      .map { line =>
        val fields = line.split("::")

        val userId = fields(0).toLong
        val movieId = fields(1).toLong
        val rating = fields(2).toDouble

        (userId, movieId, rating)
      }
      .cache()

    // Create user vertices
    val userVertices = ratings.map {
      case (userId, _, _) =>
        (userId, "USER")
    }

    // Create movie vertices
    val movieVertices = ratings.map {
      case (_, movieId, _) =>
        (movieId + movieOffset, "MOVIE")
    }

    val vertices = userVertices
      .union(movieVertices)
      .distinct()

    // Create edges
    val edges = ratings.flatMap {
      case (userId, movieId, rating) =>
        Seq(
          Edge(userId, movieId + movieOffset, rating),
          Edge(movieId + movieOffset, userId, rating)
        )
    }

    // Build graph
    val graph = Graph(vertices, edges, "UNKNOWN")

    println("Graph created successfully!")
    println("Total vertices: " + graph.vertices.count())
    println("Total directed edges: " + graph.edges.count())

    // Calculate vertex degrees
    graph.inDegrees
      .saveAsTextFile(outputPath + "/vertex_degrees")

    // Calculate PageRank
    val pageRankGraph = graph.pageRank(10)

    pageRankGraph.vertices
      .filter { case (id, _) => id >= movieOffset }
      .map { case (id, rank) => (id - movieOffset, rank) }
      .saveAsTextFile(outputPath + "/movie_pagerank")

    // Detect communities
    val communities = LabelPropagation.run(graph, 10)
    communities.vertices.saveAsTextFile(outputPath + "/communities")

    println("GraphX analysis completed successfully!")

    sc.stop()
  }
}
