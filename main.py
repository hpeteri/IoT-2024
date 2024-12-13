import os
import sqlite3
import time
from flask import Flask, request # type: ignore

app = Flask(__name__)

#sql db setup
connection = sqlite3.connect("bmp280data.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE if not exists temperature(time, value)")

#simple post data base adder
@app.route("/post", methods=["POST"])
def posting():
    temp = request.args.get("temp")
    print(temp)
    return f"Query Param Name: {temp}", 200

@app.route("/")
def test():
    return "<h1>Hello World!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)