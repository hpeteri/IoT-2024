import os
import sqlite3
import time
from flask import Flask, request # type: ignore
import json
import threading
from cleanup import threadproc_cleanup_old_records
from server_config import DB_FILE
import traceback

app = Flask(__name__)

#sql db setup
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()
cursor.execute("CREATE TABLE if not exists temperature(time, value)")

#simple post data base adder
@app.route("/temperature", methods=["POST"])
def route_post_temperature():
    try:
        temp = json.loads(request.data)
        print(temp)

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        t_value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        tmp_value = temp["temp"]

        try:
            float(tmp_value)
        except ValueError:
            print(f"Temperature value is not a valid value {tmp_value}")
            raise

        sql = "INSERT INTO temperature (time, value) VALUES (?, ?)"
        cursor.execute(sql, (t_value, tmp_value))

        connection.commit()
        connection.close()

        return f"Query Param Name: {temp}", 200

    except Exception as e:
        print(f"Error during POST temperature. {e}")
        print(traceback.format_exc())
        return f"Bad Request", 400


@app.route("/")
def route_default():
    return "<h1>Server is running!</h1>"

if __name__ == "__main__":
    cleanup_thread = threading.Thread(target=threadproc_cleanup_old_records, daemon=True)
    cleanup_thread.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
