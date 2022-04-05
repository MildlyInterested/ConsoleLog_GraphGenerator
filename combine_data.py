import pandas as pd
from functools import reduce


# df = pd.read_csv("player_cleaned.csv")
# #convert to datetime while incrementing day if crossing midnight
# df["Server Time"]=pd.to_datetime(df["Server Time"])
# day_rollover = df['Server Time'].diff() < pd.Timedelta(0)
# df['Server Time'] += pd.to_timedelta(day_rollover.cumsum(), unit='d')

#import CSV while making sure to increment day if crossing midnight
def import_csv(import_csv, time_column="Server Time", day_rollover=True):
    df = pd.read_csv(import_csv)
    df[time_column] = pd.to_datetime(df[time_column])
    if day_rollover:
        day_rollover = df[time_column].diff() < pd.Timedelta(0)  # type: ignore
        df[time_column] += pd.to_timedelta(day_rollover.cumsum(), unit='d')
    return df

#get unique sources from df
def get_unique_sources(df, column_n = 1):
    sources_list = df.iloc[:,column_n].unique()
    return sources_list

#create dict from df for each source
def dict_from_df(df, sources_list, column_name = "Source", HC = False):
    df_dict = {}
    if not HC:
        for i in range(len(sources_list)):
            df_dict[sources_list[i]] = df[df[column_name]==sources_list[i]]
    else:
        k = 1
        for i in range(len(sources_list)):
            HC_key = "HC_{}".format(k)
            df_dict[HC_key] = df[df[column_name]==sources_list[i]]
            k += 1
    return df_dict

def the_uber_merger(left_df, right_df_dict, merge_on = 'Server Time', time_tolerance = 30, merge_direction = 'nearest'):
    #convert right_df_dict to list
    df_list = list(right_df_dict.values())
    #insert left_df into list as first so everything gets merged upon it
    df_list.insert(0, left_df)
    df_merged = reduce(lambda  left,right: pd.merge_asof(left,right,on=merge_on,tolerance=pd.Timedelta(seconds=time_tolerance), direction=merge_direction), df_list)
    return df_merged

server_df = import_csv("server_cleaned.csv")
player_df = import_csv("player_cleaned.csv")
hc_df = import_csv("hc_cleaned.csv")
unique_players = get_unique_sources(player_df)
unique_hcs = get_unique_sources(hc_df)
player_dict = dict_from_df(player_df, unique_players)
hc_dict = dict_from_df(hc_df, unique_hcs, HC = True)

#TODO
#implement multi merge
# https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
#TODO do merge_asof, replace NaN data with zeros afterwards
# merge_test = pd.merge_asof(server_df, hc_dict["HC_1"],on="Server Time", suffixes=("_server","_HC"), tolerance=pd.Timedelta(seconds=30), direction="nearest")
# MULTI MERGE
# df_merged = reduce(lambda  left,right: pd.merge_asof(left,right,on='Server Time',tolerance=pd.Timedelta(seconds=30), direction="nearest"), data_frames)
# data_frames needs to be list of dfs, the first one will be what will be merged upon so like this [server_df, hc_1_df, hc_2_df, hc_3_df]
# data_frames = list(hc_dict.values())
# add server_df to front of list .insert(0, server_df)