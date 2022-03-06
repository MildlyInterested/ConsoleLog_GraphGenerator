from enum import unique
from pickle import TRUE
from tkinter.messagebox import YES
import pandas as pd


# df = pd.read_csv("player_cleaned.csv")
# #convert to datetime while incrementing day if crossing midnight
# df["Server Time"]=pd.to_datetime(df["Server Time"])
# day_rollover = df['Server Time'].diff() < pd.Timedelta(0)
# df['Server Time'] += pd.to_timedelta(day_rollover.cumsum(), unit='d')

def import_csv(import_csv, time_column="Server Time", day_rollover=TRUE):
    df = pd.read_csv(import_csv)
    df[time_column] = pd.to_datetime(df[time_column])
    if day_rollover:
        day_rollover = df[time_column].diff() < pd.Timedelta(0)
        df[time_column] += pd.to_timedelta(day_rollover.cumsum(), unit='d')
    return df

player_df = import_csv("player_cleaned.csv")

# unique_sources = df.iloc[:,1].unique()
# k = 0
# df_dict = {}

# for i in range(len(unique_sources)): #store df for each player as a dict key
#     df_dict[unique_sources[i]] = df[df['Source']==unique_sources[i]]

# for i in range(len(unique_sources)): #store df for each HC and rename to defined values as a dict key
#     HC_key = "HC_{}".format(k)
#     df_dict[HC_key] = df[df['Source']==unique_sources[i]]
#     k += 1
#TODO create new df with dict like so
# HC2_df = df_dict["HC_1"]
#TODO do merge_asof, replace NaN data with zeros afterwards
#always have server column as original, LEFT argument, merge other df from the RIGHT
#TODO multiple merges needed depending on amount of HCs, this might be slightly fucky