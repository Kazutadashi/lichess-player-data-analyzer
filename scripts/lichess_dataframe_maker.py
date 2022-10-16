# This file takes the JSON data and then converts it into a csv file or dataframe

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

PLAYER_DATA_PATH = "C:/Users/Kazutadashi/Dropbox/Programming Projects/Lichess/player_data_june_2021_200000-300000.json"
EXPORT_PATH = "C:/Users/Kazutadashi/Dropbox/Computer and Data Science/Datasets/Chess"
CSV_FILE_NAMES = ['player_dataframe_june_2021_0-50000.csv',
                  'player_dataframe_june_2021_50000-100000.csv',
                  'player_dataframe_june_2021_100000-150000.csv',
                  'player_dataframe_june_2021_150000-200000.csv',
                  'player_dataframe_june_2021_200000-300000.csv']

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

def load_data(path):
    #loads the JSON data
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def create_json_dictionary(player_data, single_features, rating_feature_dictionary, special_dictionary):
    # creates a dictionary using the JSON data pulled from the lichess API. This comes from the json_maker.py file
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
    #Creates a pandas dataframe using a python dictionary. The dictionary is created using create_json_dictionary.

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
    # expots a dataframe to CSV file
    df.to_csv(path_or_buf=export_path, index=False)

def join_csv_files(csv_filenames, output_path):
    # merges several CSV files into one with output_path as the name of the final file.
    joint_df = pd.concat(
        map(pd.read_csv, csv_filenames), ignore_index=True)
    joint_df.to_csv(path_or_buf=output_path)

def main():

    player_data = load_data(PLAYER_DATA_PATH)
    json_dict = create_json_dictionary(player_data, SINGLE_FEATURES, RATING_FEATURE_DICT, SPECIAL_DICT)
    player_df = create_player_dataframe(json_dict, SINGLE_FEATURES, RATING_FEATURE_DICT, SPECIAL_DICT)
    export_dataframe(player_df, EXPORT_PATH)
    join_csv_files(CSV_FILE_NAMES, 'july_data.csv')

main()