import streamlit as st
import pandas as pd
import plotly
import altair as alt
import plotly.express as px
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

st.write(complete_df)
filtered = st.multiselect("Filter columns", options=list(complete_df.columns), default=["Server Time", "Average Player FPS", "Units on Players", "Units on HC + Server", "Units on all", "Playercount"])
st.write(complete_df[filtered])

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Average Player FPS", "AI Count", "Playercount"), x_title="Server Time")
fig.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df["Average Player FPS"], mode="lines", name="Average Player FPS"), row=1, col=1)
fig.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=signal.savgol_filter(complete_df["Average Player FPS"],53,3), mode="lines", name="Average Player FPS AVG"), row=1, col=1)
fig.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df["Units on Players"], mode="lines", name="Units on Players"), row=2, col=1)
fig.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df["Units on HC + Server"], mode="lines", name="Units on HC + Server"), row=2, col=1)
fig.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df["Units on all"], mode="lines", name="Units on all"), row=2, col=1)
fig.add_trace(plotly.graph_objects.Scatter(x=complete_df["Server Time"], y=complete_df["Playercount"], mode="lines", name="Playercount"), row=3, col=1)
fig.update_layout(hovermode="x unified", height=800, xaxis_rangeslider_visible=True, xaxis_tickformat="%H:%M:%S")
fig.update_xaxes(showticklabels=True, showgrid=True)
fig.update_traces(xaxis='x1')
st.plotly_chart(fig, use_container_width=True)
st.write(fig.layout)