player_data = load_data(PLAYER_DATA_PATH)
json_dict = create_json_dictionary(player_data, PERFORMANCE_CATEGORIES, PERFORMANCE_SUB_CAT)
player_df = create_player_dataframe(json_dict, PERFORMANCE_CATEGORIES, PERFORMANCE_SUB_CAT)

export_dataframe(player_df, EXPORT_PATH)

fig, axes = plt.subplots(2, 3, figsize=(20, 10))
fig.suptitle("Ranking Distributions")
sns.histplot(data=player_df, x="rapid_rating", kde=True, ax=axes[0, 0])
sns.histplot(data=player_df, x="blitz_rating", kde=True, ax=axes[0, 1])
sns.histplot(data=player_df, x="bullet_rating", kde=True, ax=axes[0, 2])
sns.histplot(data=player_df, x="puzzle_rating", kde=True, ax=axes[1, 0])
sns.histplot(data=player_df, x="storm_score", kde=True, ax=axes[1, 1])
sns.histplot(data=player_df, x="storm_runs", kde=True, ax=axes[1, 2])

plt.show()