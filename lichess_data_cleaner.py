# This file takes in a large pgn file, and scrapes the player names from the file

import tqdm
import time
import re
import csv

FILE_PATH = "F:\Chess\lichess_db_standard_rated_2021-06.pgn"

#check lines in file for tqdm progress bar
num_lines = sum(1 for line in open(FILE_PATH))
print("There are {} lines in this file.".format(num_lines))


with open(FILE_PATH) as f:
    players = []

    # searches for lines that begin with White " or Black " as this is where the player
    # name is always located
    for line in tqdm.tqdm(f, total=num_lines):
        white_player = re.search(r'White "(.*?)"', line)
        black_player = re.search(r'Black "(.*?)"', line)

        # Making sure the group actually contains something
        if (white_player is not None):
            players.append(white_player.group(1))

        if (black_player is not None):
            players.append(black_player.group(1))

# removing duplicates
unique_players = list(set(players))

num_players = len(players)
num_unique_players = len(unique_players)


# saving it to a csv list
print("Found {} player names, of which {} were unique ({}%). Saving to player_list.csv".format(num_players, num_unique_players, round(100*(num_unique_players/num_players), 3)))
print("New file contains {}% of original amount of lines.".format(round(100*(num_players/num_lines), 3)))
with open("player_list.csv", 'w', newline='') as f:
    player_csv = csv.writer(f, quoting=csv.QUOTE_ALL)
    player_csv.writerow(unique_players)
print("Data saved to player_list.csv")

# fun stats stuff, seeing how many players are on the list multiple times
# duplicates = {player: players.count(player) for player in unique_players}


