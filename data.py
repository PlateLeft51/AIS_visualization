import pymysql
import json
import re

# with open('static/ais-processed-log-2021-02.json', 'r') as f:
#     lines = json.loads(f.readline())
#     # file_json = json.loads(f.readline())
#     # line = lines.split(':')
# # tp = jsonpath(file_json, "$..type")
# # line = json.loads(lines)
# print(type(lines))

with open('static/ais-processed-log-2021-02.json') as f:
    lines = json.load(f)

conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="root", charset='utf8', database='db')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

n = len(lines)
for i in range(n):
    line = lines[i]
    if line.get('status') is not None:
        typ = str(line.get('type'))
        mmsi = str(line.get('mmsi'))
        status = str(line.get('status'))
        turn = str(line.get('turn'))
        speed = str(line.get('speed'))
        accuracy = str(line.get('accuracy'))
        lon = str(line.get('lon'))
        lat = str(line.get('lat'))
        course = str(line.get('course'))
        heading = str(line.get('heading'))
        time = str(line.get('time'))
        time = ''.join(re.split('-|T|:|Z', time))

        cursor.execute("insert into aislog values('"+typ+"','"+mmsi+"','"+status+"','"
                      +turn+"','"+speed+"','"+accuracy+"','"+lon+"','"+lat+"','"+course+"','"+heading+"','"+time+"')")
        conn.commit()

cursor.close()
conn.close()
f.close()
