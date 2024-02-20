# Hurt-Land-Monitor
This is a project to monitor my family land.

# Overview
This project is a sensor array to monitor enviornmental conditions.

Current Monitoring Capabilities:
- AQI PM 1, 2.5, 10

Current Hardware:
- Raspberry PI 4b
- Adafruit PMSA003I Air Quality Breakout

Development Requirements:
- Python3
- Raspberry PI OS
- SQLite3
- Adafruit-Blinka
- adafruit-circuitpython-pm25

# new development platform setup
1) Install vs code

2) Clone the repository

3) In a terminal in the repository folder run the following:
```bash
python3 -m venv .env
source .env/bin/activate
pip3 install Adafruit-Blinka
pip3 install adafruit-circuitpython-
deactivate
```

# new deployment steps
1) follow the new development platform steps starting at step 2

```bash
sudo apt-get update
sudo apt-get install sqlite3
source .env/bin/activate
pip install pyinstaller
pyinstaller --onefile 24_Hour_Rolling_Average.py
pyinstaller --onefile AQI_Logger.py
deactivate
nohup ./dist/AQI_Logger &
nohup ./dist/24_Hour_Rolling_Average &
```