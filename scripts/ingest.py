import csv
import sqlite3
from datetime import datetime
import pandas as pd
import re

EXCEL_PATH = 'assets/TrafficTwoMonth.xlsx'

df = pd.read_excel(EXCEL_PATH)
df = df.dropna()


def to_snake_case(name):
    # insert underscore b4 capital letters
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)

    # replace spaces with underscore
    name = name.replace(" ", "_")

    # replace multiple underscores with a single underscore
    # For example, "Traffic Situation" -> "Traffic _Situation" -> "Traffic__Situation"
    name = re.sub(r'__+', '_', name)

    return name.lower()


df.columns = [to_snake_case(col) for col in df.columns]

# remove the "zero date" from time col, which gets added by pandas when reading an excel 
# because it converts it into a full datetime 
df["time"] = df["time"].dt.strftime('%H:%M:%S')



DB_PATH = "traffic.db"
TRAFFIC_TABLE_NAME = "traffic_data"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {TRAFFIC_TABLE_NAME}")

    cursor.execute(f"""
       CREATE TABLE IF NOT EXISTS {TRAFFIC_TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            date INT,
            day_of_the_week TEXT,
            car_count INT,
            bike_count INT,
            bus_count INT,
            truck_count INT,
            total INT,
            traffic_situation TEXT
       )            
    """)

    try:
        cursor.executemany(f"""
        INSERT INTO {TRAFFIC_TABLE_NAME} (
                time, date, day_of_the_week, car_count, bike_count,
                bus_count, truck_count, total, traffic_situation
        ) VALUES (
                :time, :date, :day_of_the_week, :car_count, :bike_count,
                :bus_count, :truck_count, :total, :traffic_situation
        )               
        """, df.to_dict(orient="records"))
    except sqlite3.Error as e:
        print("Error inserting data:", e)