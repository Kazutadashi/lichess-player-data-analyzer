import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def fix_stats(df):
    # setting the default rating of 1500 to nan if the user has no games played for these modes
    df.rapid_rating = np.where((df.rapid_games == 0), np.nan, df.rapid_rating)
    df.blitz_rating = np.where((df.blitz_games == 0), np.nan, df.blitz_rating)
    df.bullet_rating = np.where((df.bullet_games == 0), np.nan, df.bullet_rating)



def plot_stats(df, bins=10, plot_type=1):
    if plot_type == 1:
        fig, axes = plt.subplots(2, 3, figsize=(20, 10))
        fig.suptitle("Ranking Distributions")
        sns.histplot(data=df, x="rapid_rating", kde=True, ax=axes[0, 0], bins=bins)
        sns.histplot(data=df, x="blitz_rating", kde=True, ax=axes[0, 1], bins=bins)
        sns.histplot(data=df, x="bullet_rating", kde=True, ax=axes[0, 2], bins=bins)
        sns.histplot(data=df, x="puzzle_rating", kde=True, ax=axes[1, 0], bins=bins)
        sns.histplot(data=df, x="storm_score", kde=True, ax=axes[1, 1], bins=bins)
        sns.histplot(data=df, x="storm_runs", kde=True, ax=axes[1, 2], bins=bins)

        plt.show()
    else:
        print("something went wrong")

player_df = pd.read_csv("C:/Users/Kazutadashi/Dropbox/Programming Projects/Lichess/player_dataframe_june_2021_0-50000.csv")

fix_stats(player_df)

titled_players_df = player_df.loc[player_df['title'].notnull()]
titled_players_df = titled_players_df.loc[player_df['title'] != "BOT"]

low_title_df = titled_players_df.loc[(titled_players_df['title'] == "CM") | (titled_players_df['title'] == "FM") | (titled_players_df['title'] == "NM")]
print(low_title_df.puzzle_rating.describe())
