import json
import csv
from datetime import datetime



#-------- assign correct player_id to each player in the player_regular_season_stats.json file
# get the player csv file from player table in the supabase 
# get the player_season_stats json file from the player_season_stats.json file
# get the name from these two files. and assign the correct player_id from player scv file to player_season_stats.json file


def check_for_duplicate_player_id():
    from collections import defaultdict
    updated_json_file_path = 'player_regular_season_stats.json'
    with open(updated_json_file_path, mode='r') as jsonfile:
        player_stats = json.load(jsonfile)

    # Step 2: Check for duplicate player_id
    player_id_map = defaultdict(list)

    for player in player_stats:
        player_id = int(player['player_id'])
        player_id_map[player_id].append(player)

    # Step 3: Print entries with duplicate player_id
    unique_player_stats = []
    for player_id, entries in player_id_map.items():
        if len(entries) == 1:
            unique_player_stats.extend(entries)
        else:
            print(f"Removing duplicate player_id {player_id}:")
            for entry in entries:
                print(json.dumps(entry, indent=4))

    # Step 4: Save the updated JSON file without duplicates
    cleaned_json_file_path = 'player_regular_season_stats.json'
    with open(cleaned_json_file_path, mode='w') as jsonfile:
        json.dump(unique_player_stats, jsonfile, indent=4)

    print("Duplicate player IDs removed and cleaned JSON saved successfully.")

def assign_player_id_to_player_regualr_season_stats():
    # Step 1: Read the CSV file
    csv_file_path = 'players_rows.csv'
    players = {}

    with open(csv_file_path, mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            player_id = row['player_id']
            name = row['name']
            players[name] = player_id
            # print(player_id, " ", name)

    # Step 2: Read the JSON file
    json_file_path = 'player_regular_season_stats.json'
    with open(json_file_path, mode='r') as jsonfile:
        player_stats = json.load(jsonfile)
        # print(player_stats)

    # Step 3: Replace player_id in JSON using the mapping
    for player in player_stats:
        name = player['name']
        if name in players:
            player['player_id'] = int(players[name])

    # Step 4: Save the updated JSON file
    updated_json_file_path = 'player_regular_season_stats.json'
    with open(updated_json_file_path, mode='w') as jsonfile:
        json.dump(player_stats, jsonfile, indent=4)

    print("Player IDs updated successfully.")
    check_for_duplicate_player_id()

#-------- assign correct player_id to each player in the player_boxscore_regular_season_stats.json file

# get the regular_season_game csv file from the regular_season_games table in the supabase
# get the player_boxscore_regular_season_stats json file from the player_boxscore_regular_season_stats.json file
# assign player_id and game_id to player_boxscore_regular_season_stats.json file

   # Step 1: Read the CSV file


# csv_file_path = 'players_rows.csv'
# players = {}

# with open(csv_file_path, mode='r') as csvfile:
#     csvreader = csv.DictReader(csvfile)
#     for row in csvreader:
#         player_id = row['player_id']
#         name = row['name']
#         players[name] = player_id
#         # print(player_id, " ", name)

# # Step 2: Read the JSON file
# json_file_path = 'player_boxscore_regular_season.json'
# with open(json_file_path, mode='r') as jsonfile:
#     player_stats = json.load(jsonfile)
#     # print(player_stats)

# # Step 3: Replace player_id in JSON using the mapping
# for player in player_stats:
#     name = player['name']
#     if name in players:
#         player['player_id'] = int(players[name])

# # Step 4: Save the updated JSON file
# updated_json_file_path = 'updated_player_boxscore_regular_season.json'
# with open(updated_json_file_path, mode='w') as jsonfile:
#     json.dump(player_stats, jsonfile, indent=4)

# print("Player IDs updated successfully.")

# file_path = 'updated_player_boxscore_regular_season.json'

# # Read the JSON data
# with open(file_path, 'r') as file:
#     data = json.load(file)

# # Filter out entries without "player_id"
# filtered_data = [entry for entry in data if 'player_id' in entry]

# # Write the filtered data back to the JSON file
# with open(file_path, 'w') as file:
#     json.dump(filtered_data, file, indent=4)

# print(f"Filtered JSON saved to {file_path}")

#  "team": "PHX",
#         "opponent_team": "MIN",
#         "date": "04/14/2024",

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

csv_file_path = 'regular_season_game_rows.csv'
json_file_path = 'updated_player_boxscore_regular_season.json'

# Function to parse date strings into datetime.date objects
def parse_date(date_str, format):
    return datetime.strptime(date_str, format).date()

# Read the CSV data and store it in a dictionary for easy lookup
game_info = {}
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        game_id = row['game_id']
        date = parse_date(row['date'], "%Y-%m-%d")
        home_team = row['home_team']
        away_team = row['away_team']
        game_info[(date, home_team, away_team)] = game_id
        game_info[(date, away_team, home_team)] = game_id  # Include reverse for away games

# Read the JSON data
with open(json_file_path, 'r') as jsonfile:
    player_data = json.load(jsonfile)

# Update the JSON data with the corresponding game_id
for player in player_data:
    date = parse_date(player['date'], "%m/%d/%Y")
    team = player['team']
    opponent_team = player['opponent_team']
    game_id = game_info.get((date, team, opponent_team))
    if game_id:
        player['game_id'] = int(game_id)

filtered_data = [entry for entry in player_data if 'game_id' in entry and 'player_id' in entry]

# Write the filtered data back to the JSON file
with open(json_file_path, 'w') as jsonfile:
    json.dump(filtered_data, jsonfile, indent=4)

print(f"Filtered JSON saved to {json_file_path}")
