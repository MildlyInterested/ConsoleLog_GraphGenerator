from itertools import accumulate
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

# renaming of the column in order for the merge into a single dataset will work
#NEEDED FOR UBER MERGER
def renaming_columns_so_the_shitty_code_wont_break(df_dict):
    for key in df_dict:
        print(key)
        source = "Source_" + key
        fps =  "FPS_"+key
        localGroups = "Groups_"+key
        localUnits =  "Units_"+key
        df_dict[key] = df_dict[key].rename(columns={"Source": source, "FPS": fps, "Local Groups": localGroups, "Local Units":localUnits})
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