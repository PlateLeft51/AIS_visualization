import numpy as np
import pandas as pd
from sklearn import model_selection

from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pymysql


# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
# dataset = pandas.read_csv('a1-iris.csv', names=names)

def get_outliers():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    sql = "select mmsi,lon,lat,course,heading,speed from aislog where time>= '20210201010350' and time<='20210201052030' and lat<=5 and lat>=-5 and lon>='100' and lon<='110'"
    dt = pd.read_sql(sql, conn)

    # preprocess
    # dataset = dataset.drop('course')
    # dataset = dataset.apply(pandas.to_numeric, errors='ignore')

    dt = dt.drop(dt[(dt['course'] == 'None') |
                    (dt['heading'] == 'None') |
                    (dt['speed'] == 'None')].index)
    dt = dt.apply(pd.to_numeric, errors='ignore')

    dt['course'] = dt['course'].apply(lambda x: (round(x) // 45) * 45 + 45)
    dt['heading'] = dt['heading'].apply(lambda x: (round(x) // 45) * 45 + 45)
    dt['speed'] = dt['speed'].apply(lambda x: (round(x) // 2) * 2 + 2)

    dataset = pd.DataFrame(dt, columns=['lon', 'lat', 'course', 'heading', 'speed'])
    # print(dataset)

    keyMap = {}

    for mmsi, lon, lat, course, heading, speed in zip(dt['mmsi'], dt['lon'], dt['lat'], dt['course'],
                                                      dt['heading'], dt['speed']):
        data = [lon, lat, course, heading, speed]
        if mmsi in keyMap:
            keyMap[mmsi].append(data)
        else:
            keyMap[mmsi] = [data]

    keyMap = {k: v for k, v in keyMap.items() if len(v) > 1}
    # print(keyMap)

    # Split-out validation dataset
    array = dataset.values
    X = array[:, 0:4]
    Y = array[:, 4]
    validation_size = 0.20

    seed = 7

    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                    random_state=seed)

    # Test options and evaluation metric
    seed = 7

    knn = KNeighborsClassifier()
    knn.fit(X_train, Y_train)
    predictions = knn.predict(X_validation)

    # print(accuracy_score(Y_validation, predictions))

    #
    num = 0
    outlier_list = []
    for key, values in keyMap.items():
        value = np.array(values)
        X_pre = value[:, 0:4]
        Y_pre = value[:, 4:5]

        predict = knn.predict(X_pre)
        res = Y_pre - np.reshape(predict, (-1, 1))
        outlier = res[np.where(res > 2)]

        if len(outlier) / len(res) > 0.4:
            outlier_list.append(key)
            num = num + 1
            # print(key, len(outlier) / len(res), len(outlier), len(res))
    # print(num, len(keyMap))
    # print(outlier_list)
    return outlier_list
