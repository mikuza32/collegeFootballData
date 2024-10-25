import requests
import json
import os

# API Key and Base URL
API_KEY = 'sQdzmVcd+wHpsLKozkwLaTINmZpfUvnunRx/XyvtrhLlFyh/tkVGeNKeDEly9zjY'
BASE_URL = 'https://api.collegefootballdata.com'

# Directory to save the data
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def fetchGameData(week, year=2024, team='Colorado'):
    """Fetches game data for a specific week and team."""
    endpoint = f'{BASE_URL}/games/teams'
    params = {
        'year': year,
        'week': week,
        'team': team
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Make the request to the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)

        # Check if the request was successful
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
    """Extracts the required metrics from the raw API data."""
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

    # Iterate through the data to find relevant metrics
    for game in data:
        # 'teams' is a list of dictionaries, one for each team
        for team_data in game.get('teams', []):
            # Check if this is the team we are interested in
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
    """Saves the extracted metrics to a JSON file."""
    filePath = os.path.join(DATA_DIR, f'week{week}.json')
    with open(filePath, 'w') as jsonFile:
        json.dump(metrics, jsonFile, indent=4)
    print(f"Data has been saved to {filePath}")

def main():
    """Main function to collect data for weeks 1 through 8."""
    for week in range(1, 9):
        gameData = fetchGameData(week)
        if gameData:
            metrics = extractMetrics(gameData)
            saveDataToFile(metrics, week)

if __name__ == '__main__':
    main()
