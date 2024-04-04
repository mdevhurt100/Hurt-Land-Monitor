#!/usr/bin/env python3
import sqlite3
import time
from adafruit_pm25.i2c import PM25_I2C
import board
import busio
import requests

# Initialize the I2C connection to the sensor
i2c = busio.I2C(board.SCL, board.SDA)
pm25 = PM25_I2C(i2c, reset_pin=None)

# Function to create/connect to an SQLite database and create a table if it doesn't exist
def init_db(db_name="air_quality.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS readings
                 (timestamp TEXT, pm1_0 INTEGER, pm2_5 INTEGER, pm10 INTEGER)''')
    conn.commit()
    conn.close()

def log_reading(aq_data):    
    # URL to the PHP script that processes the form submission
    url = 'https://marcushurt.dev/submit_AQI_data.php'
    
    # Data to be submitted
    form_data = {
        'time': aq_data['time'],
        'pm25': aq_data['pm25'],
        'pm10': aq_data['pm10'],
        'pm100': aq_data['pm100']
    }
    
    # Perform the HTTP POST request
    response = requests.post(url, data=form_data)
    
    # Check if the submission was successful
    if response.status_code == 200:
        print("Reading logged successfully via form.")
    else:
        print(f"Failed to log reading via form. Status code: {response.status_code}")

# Initialize the database
init_db()

print("Start data logging")
while True:
    try:
        # Read from the sensor
        aq_data = pm25.read()
        # Prepare the data for logging
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        reading = {'time' : current_time, 
                   'pm25' : aq_data["pm25 standard"], 
                   'pm10' : aq_data["pm10 standard"],
                   'pm100' : aq_data["pm100 standard"]}
        # Log the reading
        log_reading(reading)
        # Sleep for a minute
        time.sleep(60)
    except KeyboardInterrupt:
        print("Stopping data logging.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
