import pyspark
from pyspark.sql import SparkSession
#SparkSession is now the entry point of Spark
#SparkSession can also be construed as gateway to spark libraries

#create instance of spark class
spark=SparkSession.builder.appName('kaggling_games').getOrCreate()

#create spark dataframe of input csv file
df=spark.read.csv('Score_ML_Model/games.csv'
                  ,inferSchema=True,header=True)

from pyspark.ml.feature import StringIndexer
indexer=StringIndexer(inputCol='first',outputCol='kaggle_cat')
indexed=indexer.fit(df).transform(df)

for item in indexed.head():
    print(item)
    print('\n')


from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
#creating vectors from features
#Apache MLlib takes input if vector form
assembler=VectorAssembler(inputCols=['initial_time_seconds',
 'increment_seconds',
 'max_overtime_minutes'],outputCol='features')
output=assembler.transform(indexed)
output.select('features','game_duration_seconds').show(5)
#output as below


#final data consist of features and label which is crew.
final_data=output.select('features','game_duration_seconds')
#splitting data into train and test
train_data,test_data=final_data.randomSplit([0.8,0.2])
train_data.describe().show()


#import LinearRegression library
from pyspark.ml.regression import LinearRegression
#creating an object of class LinearRegression
#object takes features and label as input arguments
ship_lr = LinearRegression(featuresCol='features',labelCol='game_duration_seconds')
#pass train_data to train model
trained_ship_model=ship_lr.fit(train_data)
#evaluating model trained for Rsquared error
ship_results=trained_ship_model.evaluate(train_data)
  
print('Rsquared Error :',ship_results.r2)
#R2 value shows accuracy of model is 92%
#model accuracy is very good and can be use for predictive analysis