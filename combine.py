import pandas as pd
from functools import reduce

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

#renaming of the column in order for the merge into a single dataset will work
#NEEDED FOR UBER MERGER
def renaming_columns_so_the_shitty_code_wont_break(df_dict):
    for key in df_dict:
        source = "Source_"+key
        fps =  "FPS_"+key
        localGroups = "Groups_"+key
        localUnits =  "Units_"+key
        df_dict[key] = df_dict[key].rename(columns={"Source": source, "FPS": fps, "Local groups": localGroups, "Local units":localUnits})
    return df_dict

#yes it works
def the_uber_merger(left_df, right_df_dict, merge_on = 'Server Time', time_tolerance = 2.5, merge_direction = 'nearest'):
    #convert right_df_dict to list
    df_list = list(right_df_dict.values())
    #insert left_df into list as first so everything gets merged upon it
    df_list.insert(0, left_df)
    df_merged = reduce(lambda  left,right: pd.merge_asof(left,right,on=merge_on,tolerance=pd.Timedelta(seconds=time_tolerance), direction=merge_direction), df_list)
    return df_merged

#merge server df onto log df
def merge_server(log_df, server_df, merge_on = 'Server Time', time_tolerance = 2.5, merge_direction = 'nearest'):
    merged_df = pd.merge_asof(log_df, server_df, on=merge_on, tolerance=pd.Timedelta(seconds=time_tolerance), direction='nearest')
    return merged_df

#merge hc df onto complete df
def merge_hc(complete_df, hc_df, merge_on = 'Server Time', time_tolerance = 2.5, merge_direction = 'nearest'):
    unique_hcs = get_unique_sources(hc_df)
    hc_dict = dict_from_df(hc_df, unique_hcs, HC = True)
    hc_dict_renamed = renaming_columns_so_the_shitty_code_wont_break(hc_dict)
    merged_df = the_uber_merger(complete_df, hc_dict_renamed, merge_on, time_tolerance, merge_direction)
    return merged_df

#merge player df onto complete df
def merge_player(complete_df, player_df, merge_on = 'Server Time', time_tolerance = 2.5, merge_direction = 'nearest'):
    unique_players = get_unique_sources(player_df)
    player_dict = dict_from_df(player_df, unique_players)
    player_dict_renamed = renaming_columns_so_the_shitty_code_wont_break(player_dict)
    merged_df = the_uber_merger(complete_df, player_dict_renamed, merge_on, time_tolerance, merge_direction)
    return merged_df