#!/usr/bin/env python3
import sqlite3
import time
from datetime import datetime, timedelta

# Function to initialize the database and create the averages table if it doesn't exist
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS averages
                 (timestamp TEXT, avg_pm1_0 REAL, avg_pm2_5 REAL, avg_pm10 REAL)''')
    conn.commit()
    conn.close()

# Function to get the 24-hour rolling averages of PM1.0, PM2.5, and PM10 readings
def get_24hr_rolling_avgs(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    twenty_four_hours_ago_str = twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')
    c.execute("SELECT pm1_0, pm2_5, pm10 FROM readings WHERE timestamp > ?", (twenty_four_hours_ago_str,))
    readings = c.fetchall()
    conn.close()
    if readings:
        avg_pm1_0 = sum([reading[0] for reading in readings]) / len(readings)
        avg_pm2_5 = sum([reading[1] for reading in readings]) / len(readings)
        avg_pm10 = sum([reading[2] for reading in readings]) / len(readings)
        return avg_pm1_0, avg_pm2_5, avg_pm10
    else:
        return None, None, None

# Function to log the averages to the database
def log_averages(db_name, avg_pm1_0, avg_pm2_5, avg_pm10):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO averages VALUES (?, ?, ?, ?)", (current_time, avg_pm1_0, avg_pm2_5, avg_pm10))
    conn.commit()
    conn.close()

print("Start 24 hour rolling average logging")
if __name__ == "__main__":
    db_name = "air_quality.db"  # Name of your SQLite database
    init_db(db_name)  # Initialize the database and create the averages table if it doesn't exist

    while True:
        avg_pm1_0, avg_pm2_5, avg_pm10 = get_24hr_rolling_avgs(db_name)
        if avg_pm1_0 is not None and avg_pm2_5 is not None and avg_pm10 is not None:
            log_averages(db_name, avg_pm1_0, avg_pm2_5, avg_pm10)
        else:
            print("No data available for the last 24 hours to log.")
        
        # Wait for an hour before the next calculation
        time.sleep(3600)
