import sqlite3
from server_config import DB_FILE

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
        temp1 = float(last_digits[0][1])  
        temp2 = float(last_digits[1][1])  
    except:
        return False

    print(f"Check: {temp1} -> {temp2}")
    if temp2 > temp1:
        return True
    else:
        return False


if rise_check():
    print("rise flag")
else:
    print("nope")
