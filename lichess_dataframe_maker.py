# This file takes the JSON data and then performs data analysis

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

PLAYER_DATA_PATH = "C:/Users/Kazutadashi/Dropbox/Programming Projects/Lichess/player_data_2021.json"
PERFORMANCE_CATEGORIES = ("chess960", "puzzle", "racingKings", "ultraBullet", "blitz", "kingOfTheHill",
                          "crazyhouse", "threeCheck", "bullet", "correspondence", "classical", "rapid")
PERFORMANCE_SUB_CAT = ("games", "rating", "rd", "prog", "prov")
EXPORT_PATH = "C:/Users/Kazutadashi/Dropbox/Programming Projects/Lichess/player_dataframe.csv"

def load_data(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def create_json_dictionary(player_data, performance_cat, performance_sub_cat):

    player_dict = {}

    # Find performance data for each player
    for i in range(len(player_data['players'])):

        # Create player in dict
        player_dict[player_data["players"][i]["id"]] = []

        # get the current player we are currently looking at
        current_player = player_data["players"][i]["id"]

        #setting first value to ID for lookups
        current_player = player_data["players"][i]["id"]
        player_dict[current_player].append(current_player)

        # loop through each category and subcategory to get rating info
        for j in range(len(performance_cat)):
            for k in range(len(performance_sub_cat)):
                try:
                    player_dict[current_player].append(player_data["players"][i]["perfs"][performance_cat[j]][performance_sub_cat[k]])

                # If the rating doesnt exist, or there is no info for that rating, we fill with nan
                except Exception as exception:
                    player_dict[current_player].append(np.nan)

        # Now we add the special gamemodes, since they are structured differently
        special_categories = ["storm", "racer", "streak"]
        special_subcategories = ["runs", "score"]

        for spec_cat in special_categories:
            for spec_sub_cat in special_subcategories:
                try:
                    player_dict[current_player].append(player_data["players"][i]["perfs"][spec_cat][spec_sub_cat])
                except Exception as exception:
                    player_dict[current_player].append(np.nan)

    return player_dict

def create_player_dataframe(player_dict, performance_cat, performance_sub_cat):

    special_categories = ["storm", "racer", "streak"]
    special_subcategories = ["runs", "score"]

    columns = ["id"]
    for cat in performance_cat:
        for sub_cat in performance_sub_cat:
            columns.append(cat + "_" + sub_cat)

    for spec_cat in special_categories:
        for spec_sub_cat in special_subcategories:
            columns.append(spec_cat + "_" + spec_sub_cat)

    player_df = pd.DataFrame.from_dict(player_dict, orient="index", columns=columns)
    return player_df

def export_dataframe(df, export_path):
    df.to_csv(path_or_buf=export_path, index=False)


def main():

    player_data = load_data(PLAYER_DATA_PATH)
    json_dict = create_json_dictionary(player_data, PERFORMANCE_CATEGORIES, PERFORMANCE_SUB_CAT)
    player_df = create_player_dataframe(json_dict, PERFORMANCE_CATEGORIES, PERFORMANCE_SUB_CAT)
    export_dataframe(player_df, EXPORT_PATH)

main()