import requests

# The URL where the form submits data
url = 'https://marcushurt.dev/db.php'

# The data you wish to submit
data = {
    'name': 'test',
    'email': 'test@test.com'
}

# Perform the HTTP POST request
response = requests.post(url, data=data)

# Check if the request was successful
if response.status_code == 200:
    print("Data submitted successfully.")
else:
    print(f"Failed to submit data. Status code: {response.status_code}")
