import sys
import matplotlib.pyplot as plt
from pyspark.sql.functions import lit, coalesce
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types, Row
spark = SparkSession.builder.appName('OSM point of interest extracter').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

restaurants_osm_scheme = types.StructType([
    types.StructField('lat', types.DoubleType(), nullable=False),
    types.StructField('lon', types.DoubleType(), nullable=False),
    types.StructField('timestamp', types.TimestampType(), nullable=False),
    types.StructField('amenity', types.StringType(), nullable=False),
    types.StructField('name', types.StringType(), nullable=True),
    types.StructField('tags', types.MapType(types.StringType(), types.StringType()), nullable=False),
])

franchise_data_scheme = types.StructType([
    types.StructField('name', types.StringType(), nullable=True),
])

def main():
    restaurants_osm = spark.read.json("../data/restaurants_from_osm.json.gz", schema=restaurants_osm_scheme)
    franchise_data = spark.read.option('multiline', 'true').json("../data/franchise_restaurants.json.gz", schema=franchise_data_scheme)

    data = restaurants_osm.join(franchise_data.withColumn('is_franchise', lit(True)), 'name', 'left').fillna(False)
    data.write.json("../data/restaurants_with_is_franchise", mode='overwrite', compression='gzip')

    
    save_coordinate = data.select(data['name'], data['lat'], data['lon'], data['is_franchise'])
    save_coordinate.show()
    save_coordinate.coalesce(1).write.format("com.databricks.spark.csv").option("header", "false").mode("overwrite").save("../data/save_coordinate.csv")
    # save_coordinate.write.csv("../data/save_coordinate.csv")
 
if __name__ == '__main__':
    main()