import requests
from datetime import datetime
import pytz
import pymysql

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='bballpass',
    database='bball_project',
    port=32769
)

def insert_team(cursor, team_name, city):
    sql = "INSERT INTO bballcompetition_team (team_name, city) VALUES (%s, %s)"
    cursor.execute(sql, (team_name, city))
    return cursor.lastrowid

def insert_game(cursor, home_team_id, away_team_id, start_time, start_time_zone, end_time, end_time_zone, current_period, home_team_score, away_team_score):
    sql = """
    INSERT INTO bballcompetition_game (home_team_id, away_team_id, start_time, start_time_zone, end_time, end_time_zone, current_period, home_team_score, away_team_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (home_team_id, away_team_id, start_time, start_time_zone, end_time, end_time_zone, current_period, home_team_score, away_team_score))

def get_team_id(cursor, team_name):
    sql = "SELECT id FROM bballcompetition_team WHERE team_name = %s"
    cursor.execute(sql, (team_name,))
    result = cursor.fetchone()
    return result['id'] if result else None

def fetch_and_insert_teams(cursor):
    team_mapping_url = "https://api.sportsdata.io/v3/cbb/scores/json/TeamsBasic?key=42a665cbaaae4593bfd8b5794d9f17fd"
    headers = {"Ocp-Apim-Subscription-Key": "42a665cbaaae4593bfd8b5794d9f17fd"}
    response = requests.get(team_mapping_url, headers=headers)
    team_mapping = {}
    if response.status_code == 200:
        teams_data = response.json()
        for team in teams_data:
            team_name = f"{team['School']} {team['Name']}"
            city = team['City']
            team_id = insert_team(cursor, team_name, city)
            team_mapping[team['Key']] = team_id
    return team_mapping

def fetch_and_insert_games(cursor, team_mapping):
    today_date = datetime.now().strftime("%Y-%m-%d")
    games_url = f"https://api.sportsdata.io/v3/cbb/scores/json/GamesByDate/{today_date}?key=42a665cbaaae4593bfd8b5794d9f17fd"
    headers = {"Ocp-Apim-Subscription-Key": "42a665cbaaae4593bfd8b5794d9f17fd"}
    response = requests.get(games_url, headers=headers)
    if response.status_code == 200:
        games_data = response.json()
        for game in games_data:
            home_team_id = get_team_id(cursor, game['HomeTeam'])
            away_team_id = get_team_id(cursor, game['AwayTeam'])
            # Handle datetime and timezone conversion properly here
            # For simplicity, assuming game['DateTimeUTC'] is already in the correct format
            insert_game(cursor, home_team_id, away_team_id, game['DateTimeUTC'], 'US/Eastern', None, None, game.get('Period', 'Upcoming'), game.get('HomeTeamScore', 0), game.get('AwayTeamScore', 0))

try:
    with connection.cursor() as cursor:
        team_mapping = fetch_and_insert_teams(cursor)
        fetch_and_insert_games(cursor, team_mapping)
        connection.commit()
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()

'''# First part: Fetch and create the team mapping
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
    print("Failed to retrieve games data:", games_response.status_code)'''
