import streamlit as st
import pandas as pd
import plotly
from plotly.subplots import make_subplots
import scipy
from scipy import signal

import clean
import combine
import calculate

st.set_page_config(layout="wide")

server = clean.cleanRPT_server("test.rpt")
headless = clean.cleanRPT_headless("test.rpt")
player = clean.cleanRPT_player("test.rpt")
log = clean.cleanLOG("test.log")

complete_df = combine.merge_server(log, server)
complete_df = combine.merge_hc(complete_df, headless)
complete_df = combine.merge_player(complete_df, player, time_tolerance=30)

complete_df = calculate.calc_player_fps(complete_df)
complete_df = calculate.player_units(complete_df)
complete_df = calculate.nonplayer_units(complete_df)

multiselect_list = list(complete_df.columns)
multiselect_list.remove("Server Time")

filtered = st.multiselect("Filter columns", options=multiselect_list, default=["Average Player FPS", "Units on Players", "Units on HC + Server", "Units on all", "Playercount"])
categories = [[],[],[],[],[]]
for column in filtered:
    if column.find("FPS") > -1:
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

rowCount = len(categories)
figtree = make_subplots(rows=rowCount, cols=1,shared_xaxes=True)
first = []
for cat in categories:
    first.append(cat[0])
    for title in cat:
        figtree.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df[title], mode="lines", name=title), row=categories.index(cat)+1, col=1)
hover_data = "<br>"
for i in range(len(filtered)):
    hover_data += filtered[i] + ": "+complete_df[filtered[i]].astype(str) + "<br>"
hover_data += "<extra></extra>"

figtree.update_layout(hovermode="x unified", height=800, xaxis_rangeslider_visible=True, xaxis_tickformat="%H:%M:%S")
figtree.update_xaxes(showticklabels=True, showgrid=True)
figtree.update_traces(xaxis='x1')
for value in first:
    figtree.update_traces(hovertemplate=hover_data, hoverinfo="text", selector=({'name':value}))
st.plotly_chart(figtree, use_container_width=True)