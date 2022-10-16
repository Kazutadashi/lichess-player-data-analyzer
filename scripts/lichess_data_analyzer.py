# this file is used for analysis

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as scs
import plotly.figure_factory as ff

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

def get_percentile(series, player_rating):
    # gets the player's percentile for the given mode

    # we remove NaN values, add the players rating, and sort the list.
    cleaned_series = series.dropna()
    cleaned_series = cleaned_series.append(pd.Series([player_rating]))
    cleaned_series = cleaned_series.sort_values()

    print("With a score of {}, You are better than {}% of players in the category {}.".format(
        player_rating,
        round(scs.percentileofscore(cleaned_series, player_rating, kind='weak'), 4),
        series.name))

    return scs.percentileofscore(cleaned_series, player_rating, kind='weak')

def plot_cdf_pdf(df, mode):
    cleaned_series = df[mode].dropna()

    fig = ff.create_distplot([cleaned_series.tolist()], [df[mode].name], show_hist=False, show_rug=False)
    fig.show()





