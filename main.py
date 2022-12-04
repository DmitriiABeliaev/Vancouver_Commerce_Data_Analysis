import sys
from pyspark.sql.functions import when, lit
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


# customers.join(
#     customer_referred_customer,
#     customers.customer_id ==customer_referred_customer.to,
#     "left")
#     .withColumn("is_referral",
#     f.when(customer_referred_customer["to"].isNull(),f.lit("false"))
#     .otherwise(f.lit("true"))
#     .select(customers["customer_id"],customers["name"], "is_referral")

def main():
    restaurants_osm = spark.read.json("restaurants_from_osm.json.gz", schema=restaurants_osm_scheme)
    franchise_data = spark.read.json("franchise_restaurants.json.gz", schema=franchise_data_scheme)

    data = restaurants_osm.join(
        franchise_data,
        restaurants_osm.name == franchise_data.name, "left"
    ).withColumn('is_franchise',
        when(franchise_data['name'].isNull(), lit("False"))
        .otherwise(lit("True"))
    )
    data.show()
    print(data)
    # data.write.json(output, mode='overwrite', compression='gzip')


if __name__ == '__main__':
    main()