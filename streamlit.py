import streamlit as st
import pandas as pd
import plotly
from plotly.subplots import make_subplots
import os
from datetime import timedelta
import numpy as np

import clean
import combine
import calculate

st.set_page_config(layout="wide", page_title="16AA Log Analyzer")
col1, col2 = st.columns(2)
with col1:
    st.title("Arma Log Analyzer")
    st.write("This is a community project to analyze the performance of the [16AA](https://16aa.net)'s Arma 3 Servers.")
    st.write("The source code can be found on [GitHub](https://github.com/MildlyInterested/ConsoleLog_GraphGenerator).")
    st.write("The data is collected by our [Mission Framework](https://github.com/16AA-Milsim/MissionFramework/blob/master/scripts/logging.sqf) and the `#monitords` [Arma admin command](https://community.bistudio.com/wiki/Multiplayer_Server_Commands#Commands).")
with col2:
    st.image("https://16aa.net/assets/img/logo/16AA-logo.png", width=200, use_column_width=True)

# get list of folders in log_data folder
log_data_folder = "log_data"
cache_data_folder = "cache_data"
folders = os.listdir(log_data_folder)
folders = [folder for folder in folders if os.path.isdir(os.path.join(log_data_folder, folder))]
folder = st.selectbox("**Select Date/Operation**", folders)
col1_1, col1_2 = st.columns(2)
#get file with .rpt extension in selected folder
rpt_files = [file for file in os.listdir(os.path.join(log_data_folder, folder)) if file.endswith(".rpt")]
with col1_1:
    rpt_file = st.selectbox("Select RPT file", rpt_files)
#get file with .log extension  in selected folder
log_files = [file for file in os.listdir(os.path.join(log_data_folder, folder)) if file.endswith(".log")]
log_files = [file for file in log_files if file.find("console") > -1]
with col1_2:    
    log_file = st.selectbox("Select LOG file", log_files)
# get full path to selected files
rpt_file = os.path.join(log_data_folder, folder, rpt_file)
log_file = os.path.join(log_data_folder, folder, log_file)

#check if df_name already exists, if it does we can save ourselves some intensive data cleaning
df_name = os.path.splitext(os.path.basename(rpt_file))[0] + "_" + os.path.splitext(os.path.basename(log_file))[0] + ".pickle"
#TODO hash based check?
if df_name in os.listdir(cache_data_folder):
    st.write("Dataframe already exists")
    with st.spinner("Loading dataframe..."):
        complete_df = pd.read_pickle(os.path.join(cache_data_folder, df_name))
    st.write("Dataframe loaded")
else:
    st.write("Dataframe does not exist")
    st.write("Dataframe will be created")
    with st.spinner("Cleaning data..."):
        server = clean.cleanRPT_server(rpt_file)
        headless = clean.cleanRPT_headless(rpt_file)
        player = clean.cleanRPT_player(rpt_file)
        log = clean.cleanLOG(log_file)
    with st.spinner("Merging dataframes..."):
        complete_df = combine.merge_server(log, server)
        complete_df = combine.merge_hc(complete_df, headless)
        complete_df = combine.merge_player(complete_df, player, time_tolerance=30)
    with st.spinner("Calculating data..."):
        complete_df = calculate.calc_player_fps(complete_df)
        complete_df = calculate.player_units(complete_df)
        complete_df = calculate.nonplayer_units(complete_df)
        complete_df = calculate.total_units(complete_df)
    #write complete_df with df_name into folder
    complete_df.to_pickle(os.path.join(cache_data_folder, df_name))
    st.write("Dataframe created")
multiselect_list = list(complete_df.columns)
multiselect_list.remove("Server Time")

filtered = st.multiselect("Filter Columns", options=multiselect_list, default=["Average Player FPS", "FPS_Server_log", "Total AI Units", "Playercount", "RAM [MB]", "out [Kbps]", "in [Kbps]", "NonGuaranteed", "Guaranteed"])
# filter time range with st slider
min_value = complete_df["Server Time"].min()
min_value = min_value.to_pydatetime()
max_value = complete_df["Server Time"].max()
max_value = max_value.to_pydatetime()
time_range = st.slider("Filter Time Range (Server Time)", min_value=min_value, max_value=max_value, value=(min_value, max_value), format="HH:mm:ss", step=timedelta(minutes=5))
complete_df = complete_df[(complete_df["Server Time"] >= time_range[0]) & (complete_df["Server Time"] <= time_range[1])]

stats_expander = st.expander("Statistical Shenanigans")
with stats_expander:
    pearson_correlations = complete_df[filtered].corr(method="pearson")
    # set upper triangle to nan
    mask = np.triu(np.ones_like(pearson_correlations, dtype=bool))
    pearson_correlations = pearson_correlations.mask(mask)
    #plot pearson correlations as heatmap
    fig = plotly.graph_objects.Figure(data=plotly.graph_objects.Heatmap(z=pearson_correlations.values, x=pearson_correlations.columns, y=pearson_correlations.columns, colorscale="RdBu", zmin=-1, zmax=1))
    fig.update_layout(title="Pearson Correlations", yaxis_autorange="reversed")
    st.plotly_chart(fig)
    st.write("Correlation does not imply causation. It only shows the linear relationship between two variables. For example, a high correlation between FPS and Playercount does not imply that FPS causes Playercount to increase. It could depend on a third variable or it could be a coincidence.")

categories = [[],[],[],[],[]]
for column in filtered:
    if column.find("FPS") > -1 or column.find("Playercount") > -1:
        categories[0].append(column)
    elif column.find("Units") > -1:
        categories[1].append(column)
    elif column.find("Kbps") > -1:
        categories[2].append(column)
    elif column.find("Guaranteed") > -1:
        categories[3].append(column)
    else:
        categories[4].append(column)

categories = [x for x in categories if x != []]
#flatten categories
categories_flat = [x for y in categories for x in y]

rowCount = len(categories)
figtree = make_subplots(rows=rowCount, cols=1,shared_xaxes=True)
first = []

for cat in categories:
    first.append(cat[0])
    for title in cat:
        figtree.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df[title], mode="lines", name=title), row=categories.index(cat)+1, col=1)
#TODO flatten the list categories to show the tooltip in the same order as the rendered traces
# flatCat = [x for x in categories]

hover_data = "<br>"
for i in range(len(categories_flat)):
    hover_data += categories_flat[i] + ": "+complete_df[categories_flat[i]].astype(str) + "<br>"
hover_data += "<extra></extra>"

figtree.update_layout(hovermode="x unified", height=800, xaxis_tickformat="%H:%M:%S")
figtree.update_xaxes(showticklabels=True, showgrid=True)
figtree.update_traces(xaxis='x1', connectgaps=True)
for value in first:
    figtree.update_traces(hovertemplate=hover_data, hoverinfo="text", selector=dict(name=value))
st.plotly_chart(figtree, use_container_width=True)