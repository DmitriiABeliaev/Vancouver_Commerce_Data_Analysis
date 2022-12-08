import sys
import matplotlib.pyplot as plt
from pyspark.sql.functions import lit
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point

import numpy as np
from numpy import hstack
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier





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
     
def to_float(x):
    if x == "false":
        return 1 #1 for blue, 0 for red
    elif x == "true":
        return 0
    else:
        print("bad")
    
def classify(data):
    X = data[['lat','lon']]#.values
    y = data['is_franchise']#.values
    
#models
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.25, random_state=11)
    
    #rf
    rf_model = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=100, max_depth=3, min_samples_leaf=6, class_weight='balanced')
    )
    rf_model.fit(X_train, y_train)
    print(rf_model.score(X_valid, y_valid))
    
    #gaussian nb
    bayes_model = GaussianNB()
    bayes_model.fit(X_train, y_train)
    print(bayes_model.score(X_valid, y_valid))
    
    #knn
    knn_model = KNeighborsClassifier(n_neighbors=4)
    knn_model.fit(X_train, y_train)
    print(knn_model.score(X_valid, y_valid))
    
    
#plotting
    BBox = (-123.3000, -122.0000, 49.00, 49.3800)
    
    x2 = np.linspace(49.00, 49.3800, 130)
    y2 = np.linspace(-123.3000, -122.0000, 130)

    xx, yy = np.meshgrid(x2, y2)
    
    xa, xb = xx.flatten(), yy.flatten()
    xa, xb = xa.reshape((len(xa), 1)), xb.reshape((len(xb), 1))
    grid = hstack((xa,xb))
    
    predictions = knn_model.predict(grid)#can change model
    
    zz = predictions.reshape(xx.shape)
    func = np.vectorize(to_float)
    zz = func(zz)
    xx = xx.astype(float)
    yy = yy.astype(float)
    zz = zz.astype(float)
    
    plt.figure(2)
    img = plt.imread('../data/map.png')
    plt.imshow(img, zorder=0, extent= BBox)
    plt.contourf(yy, xx, zz, alpha=0.5, cmap='RdBu')
    #plt.title('RF (balanced)')
    #plt.title('Gaussian NB')
    plt.title('KNN (k=4)')
    #plt.show()
    plt.savefig('../data/knn.png')#should change name to match model
    

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
    
    classify(all_data)

if __name__ == '__main__':
    main()