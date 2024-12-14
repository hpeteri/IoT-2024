import os
import sqlite3
import time
from flask import Flask, request # type: ignore
import json

app = Flask(__name__)

#sql db setup
connection = sqlite3.connect("bmp280data.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE if not exists temperature(time, value)")

#simple post data base adder
@app.route("/post", methods=["POST"])
def posting():
    temp = json.loads(request.data)
    print(temp)

    try:
        connection = sqlite3.connect("bmp280data.db")
        cursor = connection.cursor()

        t_value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(t_value)
        tmp_value = temp["temp"]
        sql = "INSERT INTO temperature (time, value) VALUES (?, ?)"
        cursor.execute(sql, (t_value, tmp_value))

        connection.commit()
        connection.close()
    except Exception as e:
        print(e)


    return f"Query Param Name: {temp}", 200

@app.route("/")
def test():
    return "<h1>Hello World!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
