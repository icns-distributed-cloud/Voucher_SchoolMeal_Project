from flask import Flask, Response, render_template
from flask_apscheduler import APScheduler
import requests
import socket
import urllib3
import pymysql

app = Flask(__name__)
scheduler = APScheduler()

Time = Gas = Light = Humid = Temp = None

def scheduleTask():
    con = pymysql.connect(host="localhost", port=3306, user="root", password=PW, db ="sensor_data")
    cur = con.cursor()
    sql = "select * from sensor_data order by time desc limit 1"
    cur.execute(sql)

    rows = list(cur.fetchall())
    print(rows, type(rows))

    global Time, Gas, Light, Humid, Temp
    Time, Gas, Light, Humid, Temp = rows[0]

    Gas = int(Gas)
    Light = int(Light)
    Humid = int(Humid)
    Temp = int(Temp)
    

@app.route('/')
def home():
    return render_template("index.html",
        Gas = Gas, Light = Light, Humid = Humid, Temp = Temp)

if __name__ == '__main__':
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", seconds=4)
    scheduler.start()
    app.run(host="0.0.0.0", port=13220, debug=True)
