import requests
import os
import time
import pymysql
import pandas as pd
import re
import random


def sql_select():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select mmsi from ship_info"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return data_list

def sql_select_ship():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select mmsi from ship_log"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return data_list

def sql_update(data_list):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
    cursor = conn.cursor()

    sql = "insert into ship_log (mmsi,name,type,length,width,draught) values (%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data_list)
    conn.commit()

    cursor.close()
    conn.close()


num = 0
data_list = sql_select()
res_list = []
queried_ship = sql_select_ship()
# print(queried_ship)
# k = {'mmsi': '248846000'}
# print(k in queried_ship)
for payload in data_list:
    num = num + 1
    print(num, '/', len(data_list))
    if len(res_list) > 300:
        print("update database")
        sql_update(res_list)
        res_list = []

    try:
        if payload not in queried_ship:
            r = requests.get("https://www.shipfinder.com/Monitor/GetIHSData", params=payload)
            result_json = r.json()
            if not result_json['Data']:
                result_type = None
            else:
                result_type = result_json['Data'][0]['ShipType']

            r = requests.get("https://www.shipfinder.com/ship/getship", params=payload)
            result_json = r.json()
            if not result_json['data']:
                result_length = result_width = result_draught = None
            else:
                result_name = result_json['data'][0]['name']
                result_length = result_json['data'][0]['length'] / 10
                result_width = result_json['data'][0]['width'] / 10
                result_draught = result_json['data'][0]['draught'] / 1000
            # print(payload['mmsi'], result_type, result_length, result_width, result_draught)
            res_list.append((payload['mmsi'], result_name, result_type, result_length, result_width, result_draught))
            time.sleep(0.5)

    except Exception as e:
        print(e)
if len(res_list)>0:
    sql_update(res_list)
# print(res_list)
# select mmsi from ship_info -> list
# for i in list:
#     requests() -> result_type result_length ...
# insert result into ship_info
