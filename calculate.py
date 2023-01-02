# import pandas as pd

#calculate average player FPS
def calc_player_fps(complete_df):
    player_fps_columns = [col for col in complete_df.columns if "FPS" in col and "Server" not in col and "HC" not in col]
    complete_df["Average Player FPS"] = complete_df[player_fps_columns].median(axis=1)
    return complete_df
#TODO: discard entries with FPS < 3

#sum up all units columns excluding columns with name Server and HC
def player_units(complete_df):
    units_columns_players = [col for col in complete_df.columns if "Units" in col and "Server" not in col and "HC" not in col]
    #-1 to only counts extra local units, not player itself
    for col in units_columns_players:
        complete_df[col] = complete_df[col] - 1
    #interpolate missing values in units_columns_players
    for col in units_columns_players:
        complete_df[col] = complete_df[col].interpolate()
    complete_df["Units on Players"] = complete_df[units_columns_players].sum(axis=1)
    return complete_df

#sum up server and HC units columns
def nonplayer_units(complete_df):
    units_columns_nonplayers = [col for col in complete_df.columns if "Units" in col and ("Server" in col or "HC" in col)]
    #interpolate missing values in units_columns_players
    for col in units_columns_nonplayers:
        complete_df[col] = complete_df[col].interpolate()
    complete_df["Units on HC + Server"] = complete_df[units_columns_nonplayers].sum(axis=1)
    #sum up all units
    complete_df["Units on all"] = complete_df["Units on Players"] + complete_df["Units on HC + Server"]
    return complete_df