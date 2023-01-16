import json
import pymysql
from flask import Flask, render_template, request
from outlier_detection import get_outliers
from spline import get_spline_points
app = Flask(__name__)

outliers = []
# first edition
@app.route("/info", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("_index.html")

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        data_list = sql_connect_ais(start, end)

        return render_template("_index.html", data_list=data_list, time={"st": start, "ed": end})


# static page
@app.route("/home", methods=["GET", "POST"])
def index_static():
    if request.method == 'GET':
        return render_template("static.html")

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        data_list = sql_connect_ais(start, end)
        type_list = sql_connect_type()

        return render_template("static.html", data_list=data_list,
                               time={"st": start, "ed": end}, type="static", ship_type=type_list)


# dynamic page
@app.route("/dyn", methods=["GET", "POST"])
def index_dynamic():
    if request.method == 'GET':
        return render_template("dynamic.html")

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        data_list = sql_connect_ais(start, end)
        type_list = sql_connect_type()
        track = get_spline_points(start, end)

        return render_template("dynamic.html", data_list=data_list,
                               time={"st": start, "ed": end}, type="dynamic", ship_type=type_list, track=track)


# trajectory page
@app.route("/tra", methods=["GET", "POST"])
def index_trajectory():
    if request.method == 'GET':
        return render_template("trajectory.html")

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        data_list = sql_connect_ais(start, end)
        type_list = sql_connect_type()
        track = get_spline_points(start, end)

        return render_template("trajectory.html", data_list=data_list,
                               time={"st": start, "ed": end}, type="trajectory", ship_type=type_list, track=track)


# outliers page
@app.route("/out", methods=["GET", "POST"])
def index_outliers():
    if request.method == 'GET':
        return render_template("outliers.html")

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        data_list = sql_connect_ais(start, end)
        type_list = sql_connect_type()
        track = get_spline_points(start, end)

        return render_template("outliers.html", data_list=data_list, time={"st": start, "ed": end},
                               type="outliers", ship_type=type_list, outlier=outliers, track=track)


# @app.route('/infores', methods=['POST'])
# def res():
#     start = request.form.get("start")
#     end = request.form.get("end")
#
#     data_list = sql_connect(start, end)
#
#     return render_template("_index.html", data_list=data_list, time={"st": start, "ed": end})


def sql_connect_ais(start, end):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from aislog where time>= %(n1)s and time<= %(n2)s and lat<='10'"
    cursor.execute(sql, {"n1": start, "n2": end})
    data_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return data_list


def sql_connect_type():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from ship_log"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return data_list


if __name__ == '__main__':
    outliers = get_outliers()
    app.run()
