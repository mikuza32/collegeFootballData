import requests
import json
import os

#API key and base url I am querying from CFB data
API_KEY = '************************'
BASE_URL = 'https://api.collegefootballdata.com'

#Directory to save the data
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

#Makes sure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def fetchGameData(week, year=2024, team='Colorado'):
    # Fetches the API to pull exact team data needed for this project
    endpoint = f'{BASE_URL}/games/teams'
    params = {
        'year': year,
        'week': week,
        'team': team
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Try catch to make request to query
    try:
        response = requests.get(endpoint, headers=headers, params=params)

        # Make sure request is successful via status code
        if response.status_code == 200:
            try:
                data = response.json()  # Attempt to parse the JSON response
                print(f"Successfully fetched data for week {week}")
                return data
            except json.JSONDecodeError:
                print("Error decoding the JSON response.")
                print(f"Response content: {response.text}")
                return None
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
            print(f"Response content: {response.text}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None

def extractMetrics(data, team='Colorado'):
    # Extracts the data needed in the exact JSON format to be further manipulated and displayed
    metrics = {
        'team': team,
        'offense': {
            'Total Yards': 0,
            'Passing Yards': 0,
            'Rushing Yards': 0,
            'Points Scored': 0,
            'Turnovers': 0,
        },
        'defense': {
            'Total Yards Allowed': 0,
            'Passing Yards Allowed': 0,
            'Rushing Yards Allowed': 0,
            'Sacks': 0,
            'Interceptions': 0
        }
    }

    # Loops through all various metrics to display once we need, in order to continue
    for game in data:
        for team_data in game.get('teams', []):
            if team_data['school'] == team:
                # Extract relevant offensive metrics
                metrics['offense']['Points Scored'] = team_data.get('points', 0)
                for stat in team_data.get('stats', []):
                    category = stat.get('category')
                    value = stat.get('stat')
                    if category == 'totalYards':
                        metrics['offense']['Total Yards'] = value
                    elif category == 'netPassingYards':
                        metrics['offense']['Passing Yards'] = value
                    elif category == 'rushingYards':
                        metrics['offense']['Rushing Yards'] = value
                    elif category == 'turnovers':
                        metrics['offense']['Turnovers'] = value
                    elif category == 'sacks':
                        metrics['defense']['Sacks'] = value
                    elif category == 'interceptions':
                        metrics['defense']['Interceptions'] = value

            # Handle opponent's data to get defensive stats
            else:
                for stat in team_data.get('stats', []):
                    category = stat.get('category')
                    value = stat.get('stat')
                    if category == 'totalYards':
                        metrics['defense']['Total Yards Allowed'] = value
                    elif category == 'netPassingYards':
                        metrics['defense']['Passing Yards Allowed'] = value
                    elif category == 'rushingYards':
                        metrics['defense']['Rushing Yards Allowed'] = value

    return metrics


def saveDataToFile(metrics, week):
    # After the successfull query, we format and save the data into a JSON format
    filePath = os.path.join(DATA_DIR, f'week{week}.json')
    with open(filePath, 'w') as jsonFile:
        json.dump(metrics, jsonFile, indent=4)
    print(f"Data has been saved to {filePath}")

def main():
    # Runs the logic about from weeks 1-8
    for week in range(1, 9):
        gameData = fetchGameData(week)
        if gameData:
            metrics = extractMetrics(gameData)
            saveDataToFile(metrics, week)

if __name__ == '__main__':
    main()
