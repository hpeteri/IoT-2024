import os
import sqlite3
import time
from flask import Flask, request
import json
import threading
from cleanup import threadproc_cleanup_old_records
from server_config import DB_FILE
import traceback
from calculations import rise_check
import random

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

        t_value = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
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


@app.route("/temperature", methods=["GET"])
def route_get_temperature():

    """
    @brief data end point to query 50 latest temperature data points
    @return json [{"time": "%Y-%m-%d %H:%M:%S", "value": <float>}]
    """

    sql = """
    SELECT *
    FROM temperature
    ORDER BY time DESC
    LIMIT 50
    ;
    """

    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(sql)

        records = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        connection.close()

        for record in records:
            print(record)

        data = [dict(zip(columns, row)) for row in records]

        return json.dumps(data), 200

    except Exception as e:
        print(f"Error during GET temperature. {e}")
        print(traceback.format_exc())
        return "Bad Request", 400

@app.route("/brewing", methods=["GET"])
def route_get_brewing_status():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        delete_query = f"""
        SELECT value
        FROM temperature
        WHERE time < DATETIME('now', '-10 seconds');
        """
        cursor.execute(delete_query)
        conn.commit()

        records = cursor.fetchall()

        prev = 0
        if len(records):
            prev = float(records[0][0])

        count = 0

        conn.close()

        print(f"/brewing got {len(records)} records")

        for record in records:
            if float(record[0]) >= prev:
                count += 1

        if count > len(records) / 2 and count != 0:
            return json.dumps({"value": True}), 200
        else:
            return json.dumps({"value": False}), 200

    except Exception as e:
        print(f"Error during GET /ready: {e}")

    return json.dumps({"value": False}), 200

@app.route("/ready", methods=["GET"])
def route_get_ready_status():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        delete_query = f"""
        SELECT value
        FROM temperature
        WHERE time < DATETIME('now', '-6 minutes');
        """
        cursor.execute(delete_query)
        conn.commit()

        records = cursor.fetchall()

        conn.close()

        count = 0
        print(f"/ready got {len(records)} records")
        for record in records:
            if float(record[0]) > 35:
                count += 1

        if count > len(records) / 2 and count != 0:
            return json.dumps({"value": True}), 200

        else:
            return json.dumps({"value": False}), 200

    except Exception as e:
        print(f"Error during GET /ready: {e}")


    return json.dumps({"value": False}), 200

@app.route("/")
def route_default():
    return "<h1>Server is running!</h1>"

if __name__ == "__main__":
    cleanup_thread = threading.Thread(target=threadproc_cleanup_old_records, daemon=True)
    cleanup_thread.start()

    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(e)
