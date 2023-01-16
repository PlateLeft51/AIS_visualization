import itertools
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql


def get_spline_points(start, end):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    sql = "select mmsi,lat,lon from aislog where time>='" + start + "' and time<= '" + end + "'"
    # print(sql)
    dt = pd.read_sql(sql, conn)

    spline = {}
    interpolations_methods = ['slinear', 'quadratic', 'cubic']
    for method in interpolations_methods:
        keyMap = {}

        for mmsi, lat, lon in zip(dt['mmsi'], dt['lat'], dt['lon']):
            data = [lat, lon]
            if mmsi in keyMap:
                keyMap[mmsi].append(data)
            else:
                keyMap[mmsi] = [data]

        keyMap = {k: v for k, v in keyMap.items() if len(v) > 1}
        kMap = keyMap
        # print(method)
        for key in kMap:
            points = kMap[key]
            points = [k for k, _ in itertools.groupby(points)]
            if len(points) > 3:
                # print(keyMap)

                # print(points)
                points = np.array(points)
                points = points.astype(float)
                # print(key, len(keyMap[key]))

                # Linear length along the line:
                distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
                distance = np.insert(distance, 0, 0) / distance[-1]

                # Interpolation for different methods:
                # interpolations_methods = ['cubic']
                alpha = np.linspace(0, 1, 75)

                interpolated_points = {}

                interpolator = interp1d(distance, points, kind=method, axis=0)
                interpolated_points[method] = np.around(interpolator(alpha), decimals=5)

                if check(interpolated_points[method]):
                    kMap[key] = interpolated_points[method].astype(str).tolist()

        spline[method] = kMap
        # print(spline)
        # print()

    return spline
    # print(interpolated_points['quadratic'])


def check(pt):
    if pt[0][0]-pt[len(pt)//2][0] < 0.1:
        return True
    return False
# keyMap = get_spline_points('20210201000350','20210201001550')
# print(keyMap)

# # Graph:
# plt.figure(figsize=(7, 7))
# for method_name, curve in interpolated_points.items():
#     plt.plot(*curve.T, '-', label=method_name)
#
# plt.plot(*points.T, 'ok', label='original points')
# plt.axis('equal')
# plt.legend()
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()


# spline-ref
# import numpy as np
# from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
#
# # Define some points:
# points = np.array([[0, 1, 8, 2, 2],
#                    [1, 0, 6, 7, 2]]).T  # a (nbre_points x nbre_dim) array
#
# # Linear length along the line:
# distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
# distance = np.insert(distance, 0, 0) / distance[-1]
#
# # Interpolation for different methods:
# interpolations_methods = ['slinear', 'quadratic', 'cubic']
# alpha = np.linspace(0, 1, 75)
#
# interpolated_points = {}
# for method in interpolations_methods:
#     interpolator = interp1d(distance, points, kind=method, axis=0)
#     interpolated_points[method] = interpolator(alpha)
#
# # Graph:
# plt.figure(figsize=(7, 7))
# for method_name, curve in interpolated_points.items():
#     plt.plot(*curve.T, '-', label=method_name)
#
# plt.plot(*points.T, 'ok', label='original points')
# plt.axis('equal')
# plt.legend()
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()
