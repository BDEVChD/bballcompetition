import requests
from datetime import datetime
import pytz

# First part: Fetch and create the team mapping
team_mapping_url = "https://api.sportsdata.io/v3/cbb/scores/json/TeamsBasic?key=42a665cbaaae4593bfd8b5794d9f17fd"
headers = {"Ocp-Apim-Subscription-Key": "42a665cbaaae4593bfd8b5794d9f17fd"}

team_mapping_response = requests.get(team_mapping_url, headers=headers)
team_mapping = {}

if team_mapping_response.status_code == 200:
    teams_data = team_mapping_response.json()
    for team in teams_data:
        key = team['Key']
        school_and_name = f"{team['School']} {team['Name']}"
        team_mapping[key] = school_and_name

# Second part: Fetch the games by today's date and use the team mapping
today_date = datetime.now().strftime("%Y-%m-%d")
games_url = f"https://api.sportsdata.io/v3/cbb/scores/json/GamesByDate/{today_date}?key=42a665cbaaae4593bfd8b5794d9f17fd"

games_response = requests.get(games_url, headers=headers)

if games_response.status_code == 200:
    games_data = games_response.json()
    filtered_games = []

    for game in games_data:
        home_team_full = team_mapping.get(game['HomeTeam'], "Unknown Team")
        away_team_full = team_mapping.get(game['AwayTeam'], "Unknown Team")
        
        home_team_score = 0 if game['HomeTeamScore'] is None else game['HomeTeamScore']
        away_team_score = 0 if game['AwayTeamScore'] is None else game['AwayTeamScore']
        adjusted_period = "Upcoming" if game['Period'] is None else game['Period']

        game_info = {
            'HomeTeam': home_team_full,
            'AwayTeam': away_team_full,
            'StartTimeUTC': game['DateTimeUTC'],
            'HomeTeamScore': home_team_score,
            'AwayTeamScore': away_team_score,
            'Period': adjusted_period
        }
        filtered_games.append(game_info)

    for game in filtered_games:
        start_time_utc = datetime.strptime(game['StartTimeUTC'], "%Y-%m-%dT%H:%M:%S")
        local_timezone = pytz.timezone('US/Eastern')
        start_time_local = start_time_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        start_time_str = start_time_local.strftime("%m/%d/%Y %I:%M %p")
        print(f" Game: {game['AwayTeam']} @ {game['HomeTeam']}: {game['AwayTeamScore']} - {game['HomeTeamScore']}")
        print(f" Game Time Start: {start_time_str}; Game Period: {game['Period']}")
else:
    print("Failed to retrieve games data:", games_response.status_code)
