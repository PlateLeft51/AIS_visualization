import numpy as np
import pandas
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_squared_error
import main
import pymysql

# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
# dataset = pandas.read_csv('a1-iris.csv', names=names)


conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
sql = "select mmsi,lon,lat,course,heading,speed from aislog where time>= '20210201010350' and time<='20210201052030' and lat<=5 and lat>=-5 and lon>='100' and lon<='110'"
# sql = "select ais.mmsi, ais.lon,ais.lat,ais.course,ais.heading,ais.speed,ship.type from ship_log ship join aislog ais on ship.mmsi=ais.mmsi " \
#       "where ais.time>= '20210201010350' and ais.time<='20210201052030' and ais.lat<=5 and ais.lat>=-5 and ais.lon>='100' and ais.lon<='110'"
dt = pandas.read_sql(sql, conn)

# preprocess
# dataset = dataset.drop('course')
# dataset = dataset.apply(pandas.to_numeric, errors='ignore')

dt = dt.drop(dt[(dt['course'] == 'None') |
                (dt['heading'] == 'None') |
                (dt['speed'] == 'None')].index)
# dt['type'].replace('Container ship', '1', inplace=True)
# dt['type'].replace('Tanker', '2', inplace=True)
# dt['type'].replace('None', '3', inplace=True)
# dt['type'].replace('Tug', '4', inplace=True)
# dt['type'].replace('Special Purpose Ship', '5', inplace=True)
# dt['type'].replace('Cargo', '6', inplace=True)
# dt['type'].replace('Passenger', '7', inplace=True)
# dt['type'].replace('Bulk Carrier', '8', inplace=True)
dt = dt.apply(pandas.to_numeric, errors='ignore')

dt['course'] = dt['course'].apply(lambda x: (round(x) // 45) * 45 + 45)
dt['heading'] = dt['heading'].apply(lambda x: (round(x) // 45))
dt['speed'] = dt['speed'].apply(lambda x: (round(x) // 2) * 2 + 2)

# dt.replace({'Container ship': 0})

dataset = pd.DataFrame(dt, columns=['lon', 'lat',  'heading'])
# print(dataset)

# keyMap = {}
#
# for mmsi, lon, lat, course, heading, speed in zip(dt['mmsi'], dt['lon'], dt['lat'], dt['course'],
#                                                   dt['heading'], dt['speed']):
#     data = [lon, lat, course, heading, speed]
#     if mmsi in keyMap:
#         keyMap[mmsi].append(data)
#     else:
#         keyMap[mmsi] = [data]
#
# keyMap = {k: v for k, v in keyMap.items() if len(v) > 1}

# print(keyMap)
# plotting data
# dataset.plot(kind='box', subplots=True, layout=(2, 3), sharex=False, sharey=False)
# plt.show()
# scatter_matrix(dataset)
# plt.show()

# Split-out validation dataset
array = dataset.values
X = array[:, 0:2]
Y = array[:, 2]
validation_size = 0.20

seed = 7

X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                random_state=seed)

# Test options and evaluation metric  neg_mean_squared_error/accuracy
mse = make_scorer(mean_squared_error, greater_is_better=False)
seed = 7
scoring = 'accuracy'

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

# evaluate each model in turn
results = []
names = []

for name, model in models:
    kfold = model_selection.KFold(n_splits=10)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring,
                                                 error_score='raise')

    results.append(cv_results * (1))
    names.append(name)

    msg = "%s: %f (%f)" % (name, cv_results.mean()*(1), cv_results.std())

    print(msg)

# print(names)
# print(results)
# plt.bar(names, results, width=0.7)''
2
# plt.show()

# Compare Algorithms
fig = plt.figure()
fig.suptitle('Algorithm Comparison (accuracy)')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

# print(X_train)
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
predictions = knn.predict(X_validation)
# print(predictions)
# print()
print(accuracy_score(Y_validation, predictions))
# print(confusion_matrix(Y_validation, predictions))
# print(classification_report(Y_validation, predictions))

#
num=0
res = 0
# for key, values in keyMap.items():
#     value = np.array(values)
#     X_pre = value[:, 0:4]
#     Y_pre = value[:, 4:5]
#
#     predict = knn.predict(X_pre)
#     res = Y_pre - np.reshape(predict,(-1,1))
#     outlier = res[np.where(res > 2)]
#
#     if key == 563036620:
#         print()
#         pass
#     if len(outlier) / len(res) > 0.4:
#         num = num+1
#         print(key, len(outlier) / len(res), len(outlier), len(res))
# print(num, len(keyMap))
# print('X_validation')
# print(X_validation)
