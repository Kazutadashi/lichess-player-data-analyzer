# This file is responsible for making a single JSON file for all players so that it can easily
# be used later for analysis

import tqdm
import csv
import json
import urllib.request
import time

PLAYER_LIST_PATH = "player_list_june_2021.csv"
OUTPUT_FILENAME = "player_data_2021.json"

# opens csv file to load in players
with open(PLAYER_LIST_PATH, newline='') as f:
    reader = csv.reader(f)
    players = list(reader)

#print(players[0])

# first creates a file that starts with a JSON list structure
with open(OUTPUT_FILENAME, "w") as player_data_json:
    player_data_json.write("""{"players": [\n""")

# Gets json data for each player, in this specific [0][0:1000] we just want 1000 players to test
# uses tqdm for a progress bar
for player in tqdm.tqdm(players[0][0:1000]):
    try:
        #print("Fetching JSON data for " + player + "...")
        with urllib.request.urlopen("https://lichess.org/api/user/" + player) as url:
            player_data = json.loads(url.read().decode())

        # Adds a player to the JSON list
        with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=4)
            f.write(",\n")

    except Exception as exception:
        print(exception)

# Ends the file with the correct structure to make this JSON accessible in the future.
with open(OUTPUT_FILENAME, "a") as player_data_json:
    player_data_json.write("""]}""")