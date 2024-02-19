import requests

url = 'https://v1.basketball.api-sports.io/games'

payload = {}
headers = {
    'x-rapidapi-host': 'v1.basketball.api-sports.io',
    'x-rapidapi-key': '3e79c53118cf2ddc23f3c12fd2f7ace1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)