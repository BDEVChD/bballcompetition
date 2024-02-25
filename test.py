import requests

# API Endpoint URL
url = "https://api.sportsdata.io/v3/cbb/scores/json/SchedulesBasic/2024?key=42a665cbaaae4593bfd8b5794d9f17fd"

# Headers with your API Key
headers = {
    "Ocp-Apim-Subscription-Key": "42a665cbaaae4593bfd8b5794d9f17fd"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Convert the response to JSON
    games_data = response.json()
    # Do something with the data
    print(games_data)
else:
    print("Failed to retrieve data:", response.status_code)
