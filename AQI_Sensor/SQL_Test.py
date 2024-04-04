import requests

# The URL where the form submits data
url = 'https://marcushurt.dev/submit_AQI_data.php'

# The data you wish to submit
data = {
    'time': "2024-10-10",
    'pm25': 1,
    'pm10': 1,
    'pm100': 1
}

# Perform the HTTP POST request
response = requests.post(url, data=data)

# Check if the request was successful
if response.status_code == 200:
    print("Data submitted successfully.")
else:
    print(f"Failed to submit data. Status code: {response.status_code}")
