import requests
from datetime import datetime
import pymysql

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='bballpass',
    database='bball_project',
    port=32769
)


def insert_team(cursor, team_name):
    sql = "INSERT INTO bballcompapp_team (team_name) VALUES (%s)"
    cursor.execute(sql, (team_name))
    return cursor.lastrowid

def insert_game(cursor, home_team_id, away_team_id, start_time, start_time_zone, end_time, end_time_zone, current_period, home_team_score, away_team_score):
    sql = """
    INSERT INTO bballcompapp_game (home_team_id, away_team_id, start_time, start_time_zone, end_time, end_time_zone, current_period, home_team_score, away_team_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (home_team_id, away_team_id, start_time, start_time_zone, end_time, end_time_zone, current_period, home_team_score, away_team_score))

def fetch_and_insert_teams(cursor):
    team_mapping_url = "https://api.sportsdata.io/v3/cbb/scores/json/TeamsBasic?key=42a665cbaaae4593bfd8b5794d9f17fd"
    headers = {"Ocp-Apim-Subscription-Key": "42a665cbaaae4593bfd8b5794d9f17fd"}
    response = requests.get(team_mapping_url, headers=headers)
    team_mapping = {}
    if response.status_code == 200:
        teams_data = response.json()
        for team in teams_data:
            team_name = f"{team['School']} {team['Name']}"
            team_id = insert_team(cursor, team_name)
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
            adjusted_period = "Upcoming" if game['Period'] is None else game['Period']
            home_team_id = team_mapping.get(game['HomeTeam'], "Unknown Team")
            away_team_id = team_mapping.get(game['AwayTeam'], "Unknown Team")
            insert_game(cursor, home_team_id, away_team_id, game['DateTimeUTC'], 'US/Eastern', None, None, adjusted_period, game.get('HomeTeamScore', 0), game.get('AwayTeamScore', 0))

try:
    with connection.cursor() as cursor:
        team_mapping = fetch_and_insert_teams(cursor)
        fetch_and_insert_games(cursor, team_mapping)
        connection.commit()
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
