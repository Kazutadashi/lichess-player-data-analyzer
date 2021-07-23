# This file takes the JSON data and then performs data analysis

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

PLAYER_DATA_PATH = "C:/Users/Kazutadashi/Dropbox/Programming Projects/Lichess/player_data_2021.json"
EXPORT_PATH = "C:/Users/Kazutadashi/Dropbox/Programming Projects/Lichess/player_dataframe.csv"

PERFORMANCE_SUB_CAT = ("games", "rating", "rd", "prog", "prov")
SPECIAL_SUB_CATEGORIES = ("runs", "score")
RATING_FEATURE_DICT = {
        "chess960": PERFORMANCE_SUB_CAT, "puzzle": PERFORMANCE_SUB_CAT, "racingKings": PERFORMANCE_SUB_CAT,
        "ultraBullet": PERFORMANCE_SUB_CAT, "blitz": PERFORMANCE_SUB_CAT, "kingOfTheHill": PERFORMANCE_SUB_CAT,
        "crazyhouse": PERFORMANCE_SUB_CAT, "threeCheck": PERFORMANCE_SUB_CAT, "bullet": PERFORMANCE_SUB_CAT,
        "correspondence": PERFORMANCE_SUB_CAT, "classical": PERFORMANCE_SUB_CAT, "rapid": PERFORMANCE_SUB_CAT,
        "storm": SPECIAL_SUB_CATEGORIES, "racer": SPECIAL_SUB_CATEGORIES, "streak": SPECIAL_SUB_CATEGORIES,
}

SPECIAL_DICT = {
    "profile": ("country", "location", "fideRating"),
    "playTime": ("total", "tv")
}
SINGLE_FEATURES = ("id", "patron", "language", "title", "nbFollowing", "nbFollowers", "completionRate")

# does this work now?

def load_data(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def create_json_dictionary(player_data, single_features, rating_feature_dictionary, special_dictionary):

    player_dict = {}

    # Find performance data for each player
    for i in range(len(player_data['players'])):

        # Create player in dict
        player_dict[player_data["players"][i]["id"]] = []

        current_player = player_data["players"][i]["id"]

        #add location and other data
        for item in single_features:
            try:
                player_dict[current_player].append(player_data["players"][i][item])
            except Exception as exception:
                player_dict[current_player].append(np.nan)

        #add rating stats
        for variant in rating_feature_dictionary:
            for value in rating_feature_dictionary[variant]:
                try:
                    player_dict[current_player].append(player_data["players"][i]["perfs"][variant][value])
                except Exception as exception:
                    player_dict[current_player].append(np.nan)

        #add special gamemode stats
        for key in special_dictionary:
            for value in special_dictionary[key]:
                try:
                    player_dict[current_player].append(player_data["players"][i][key][value])
                except Exception as exception:
                    player_dict[current_player].append(np.nan)

    return player_dict

def create_player_dataframe(player_dict, single_features, rating_feature_dictionary, special_dictionary):



    columns = []

    # adding single features titles
    for item in single_features:
        columns.append(item)

    # adding performance rating titles
    for variant in rating_feature_dictionary:
        for value in rating_feature_dictionary[variant]:
            columns.append(variant + "_" + value)

    # add special gamemode titles
    for key in special_dictionary:
        for value in special_dictionary[key]:
            columns.append(key + "_" + value)

    player_df = pd.DataFrame.from_dict(player_dict, orient="index", columns=columns)
    return player_df

def export_dataframe(df, export_path):
    df.to_csv(path_or_buf=export_path, index=False)


def main():

    player_data = load_data(PLAYER_DATA_PATH)
    json_dict = create_json_dictionary(player_data, SINGLE_FEATURES, RATING_FEATURE_DICT, SPECIAL_DICT)
    player_df = create_player_dataframe(json_dict, SINGLE_FEATURES, RATING_FEATURE_DICT, SPECIAL_DICT)
    export_dataframe(player_df, EXPORT_PATH)

main()