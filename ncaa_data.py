import requests
import datetime

url = 'https://v1.basketball.api-sports.io/games'

payload = {}
headers = {
    'x-rapidapi-host': 'v1.basketball.api-sports.io',
    'x-rapidapi-key': '3e79c53118cf2ddc23f3c12fd2f7ace1'
}

today = datetime.date.today()

params = {
    'league': '116',
    'season': '2023-2024',
    'date': today
}


response = requests.request("GET", url, headers=headers, data=payload, params=params)

data = response.json()

print(data)
# if 'response' in data:
#     print(data['response'][0])
# else:
#     print("No response found")
