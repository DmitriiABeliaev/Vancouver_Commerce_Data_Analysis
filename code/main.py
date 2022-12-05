import sys
import matplotlib.pyplot as plt
from pyspark.sql.functions import lit
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point



from pyspark.sql import SparkSession, functions, types, Row
spark = SparkSession.builder.appName('OSM point of interest extracter').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

data_scheme = types.StructType([
    types.StructField('lat', types.DoubleType(), nullable=False),
    types.StructField('lon', types.DoubleType(), nullable=False),
    types.StructField('timestamp', types.TimestampType(), nullable=False),
    types.StructField('amenity', types.StringType(), nullable=False),
    types.StructField('name', types.StringType(), nullable=True),
    types.StructField('tags', types.MapType(types.StringType(), types.StringType()), nullable=False),
    types.StructField('is_franchise', types.BooleanType(), nullable=False),
])
    
def main():
    coordinate_data = spark.read.csv("../data/save_coordinate.csv").toDF('name','lat', 'lon', 'is_franchise')
    
    non_franchise_data = coordinate_data.filter(coordinate_data['is_franchise'] == False)
    franchise_data = coordinate_data.filter(coordinate_data['is_franchise'] == True)

    non_franchise_data = non_franchise_data.toPandas()
    franchise_data = franchise_data.toPandas()
    all_data = coordinate_data.toPandas()

    
    non_franchise_data['lon'] = non_franchise_data['lon'].astype('float')
    non_franchise_data['lat'] = non_franchise_data['lat'].astype('float')
    franchise_data['lon'] = franchise_data['lon'].astype('float')
    franchise_data['lat'] = franchise_data['lat'].astype('float')
  
    all_data['lon'] = all_data['lon'].astype('float')
    all_data['lat'] = all_data['lat'].astype('float')
    
    BBox = (-123.3000, -122.0000, 49.00, 49.3800)
    
    
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig, ( ax2, ax3) = plt.subplots(2)
    # non_fran = ax1.scatter(non_franchise_data['lon'], non_franchise_data['lat'], zorder=1, alpha= 0.2, c='b', s=10)
    # fran = ax1.scatter(franchise_data['lon'], franchise_data['lat'], zorder=1, alpha= 0.2, c='b', s=10)
    # ax1.set_title('Vancouver Restaurants Locations')
    # ax1.set_xlim(BBox[0],BBox[1])
    # ax1.set_ylim(BBox[2],BBox[3])
    # ax1.legend('All restaurants')

    ax2.scatter(non_franchise_data['lon'], non_franchise_data['lat'], zorder=1, alpha= 0.5, c='b', s=10)
    ax2.set_title('Vancouver Non-Chained Restaurants Locations')
    ax2.set_xlim(BBox[0],BBox[1])
    ax2.set_ylim(BBox[2],BBox[3])
    ax2.set_label('non_chained_restaurants')

    ax3.scatter(franchise_data['lon'], franchise_data['lat'], zorder=1, alpha= 0.5, c='r', s=10)
    ax3.set_title('Vancouver Chained Restaurants Locations')
    ax3.set_xlim(BBox[0],BBox[1])
    ax3.set_ylim(BBox[2],BBox[3])
    ax3.set_label('chained_restaurants')

    img = plt.imread('../data/map.png')

    # imgplot = ax1.imshow(img, zorder=0, extent= BBox)
    imgplot = ax2.imshow(img, zorder=0, extent= BBox)
    imgplot = ax3.imshow(img, zorder=0, extent= BBox)

    # plt.show()
    plt.savefig('../data/data_mapped.png')

if __name__ == '__main__':
    main()