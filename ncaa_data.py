import requests
from datetime import datetime
import pytz

# API Endpoint URL
url = "https://api.sportsdata.io/v3/cbb/scores/json/SchedulesBasic/2024?key=42a665cbaaae4593bfd8b5794d9f17fd"

# Headers with your API Key
headers = {
    "Ocp-Apim-Subscription-Key": "42a665cbaaae4593bfd8b5794d9f17fd"
}

# Make the GET request
response = requests.get(url, headers=headers)

games_data = response.json()

print(type(games_data))

filtered_games = []

for game in games_data:
    if game['Status'] == 'Final':
        game_info = {
        'HomeTeam': game['HomeTeam'],
        'AwayTeam': game['AwayTeam'],
        'StartTimeUTC': game['DateTimeUTC'],
        'HomeTeamScore': game['HomeTeamScore'],
        'AwayTeamScore': game['AwayTeamScore']
    }
        filtered_games.append(game_info)

for game in filtered_games[:5]:
    start_time_utc = datetime.strptime(game['StartTimeUTC'], "%Y-%m-%dT%H:%M:%S")
    local_timezone = pytz.timezone('US/Eastern')
    start_time_local = start_time_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    start_time_str = start_time_local.strftime("%m/%d/%Y %I:%M %p")
    print(f" Game: {game['AwayTeam']} @ {game['HomeTeam']}: {game['AwayTeamScore']} - {game['HomeTeamScore']}")
    print(f" Game Time Start: {start_time_str}")