import sqlite3
import time
from server_config import DB_FILE

def threadproc_cleanup_old_records():
    while True:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            delete_query = f"""
            DELETE FROM temperature
            WHERE time < DATETIME('now', '-24 hours');
            """
            cursor.execute(delete_query)
            conn.commit()
            print("Old records cleaned up successfully.")
        except sqlite3.Error as e:
            print(f"Error during cleanup: {e}")
        finally:
            conn.close()

        #sleep for 1 hour
        time.sleep(3600)
