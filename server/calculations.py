import sqlite3
from server_config import DB_FILE
from datetime import datetime, timedelta

def rise_check():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    #row fetch
    cursor.execute("SELECT time, value FROM temperature ORDER BY time ASC")
    rows = cursor.fetchall()
    connection.close()

    print(len(rows))

    #Checking if we have values, if not return false
    if len(rows) < 2:
        return False

    last_digits = rows[-2:]
    print(f"Vikat rivit: {last_digits}")

    try:
        time1 = datetime.strptime(last_digits[0][0], "%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(last_digits[1][0], "%Y-%m-%d %H:%M:%S")
        temp1 = float(last_digits[0][1])  
        temp2 = float(last_digits[1][1])  
    except:
        return False

    time_diff = time2 - time1
    if time_diff > timedelta(hours=1):
        return False

    print(f"Check: {temp1} -> {temp2}")
    if temp2 > temp1:
        return True
    else:
        return False
    
def is_brewing():
    return None


if rise_check():
    print("rise flag")
else:
    print("nope")
