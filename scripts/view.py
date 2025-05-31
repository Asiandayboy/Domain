import sqlite3
from ingest import TRAFFIC_TABLE_NAME, DB_PATH


with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {TRAFFIC_TABLE_NAME} limit 10")
    rows = cursor.fetchall()

    for row in rows:
        print(row)