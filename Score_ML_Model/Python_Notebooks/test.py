from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MinMaxScalerExample").getOrCreate()

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "postgresql-42.5.0.jar") \
    .getOrCreate()


df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://vichogent.be:40033/depdatabase") \
    .option("dbtable", "KMO") \
    .option("user", "postgres") \
    .option("password", "DEPdatabase1") \
    .option("driver", "org.postgresql.Driver") \
    .load()