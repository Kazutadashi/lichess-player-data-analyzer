# lichess-player-data-analyzer
Tools for gathering player rating data and data analysis for Lichess users

This is a project that focuses on collecting data from Lichess' API, cleaning it, converting into CSV/JSON formats, and analyzing the cleaned data. 
The cleaned data consists of various ratings and stats for 300,000 players on Lichess. 

The various scripts perform the following actions:

lichess_dataframe_maker.py - This file takes the JSON data and then converts it into a csv file or dataframe
lichess_data_cleaner.py    - This file takes in a large PGN (chess game) file, and scrapes the player names from the file. This is then used to collect 
                             data for each player in the PGN file to run analysis on
json_maker.py              - This file is responsible for making a single JSON file for all players so that it can easily be used later for analysis 
                             or CSV conversion.
lichess_data_analyzer.py   - This file is used to run different analyses on the player data to obtain useful information.
                          
