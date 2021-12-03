###IMPORT###
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import clean_logfile as clean
#from altair_saver import save
import matplotlib.dates as md
#import matplotlib.patches as mpatches


####CODE####
date = clean.cleanData()
sns.set_style("whitegrid")
df = pd.read_csv('rpt_cleaned.csv', header=0)
#print(df) #sanity check
#print(df.dtypes)
df['Server Time'] = pd.to_datetime(df['Server Time']) #converts string to datetime (YYYY-mm-dd-HH-mm-ss)
df['Time Diff'] = df['Server Time'].diff()
pastMidnight = df['Server Time'].diff() < pd.Timedelta(0)
df['Server Time'] += pd.to_timedelta(pastMidnight.cumsum(), unit='d')
#print(df.dtypes)
#print(pastMidnight)
#print(df['FPS'])
#df.to_csv('server_logs_panda.csv')


figure, axes = plt.subplots(3, 1, figsize=(35,25))
figure.suptitle("Server stats")
figure.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.05)
#TODO: Change array to read from "HC" and "SERVER"tags in data.
npc = ["Server", "HC1", "HC2"]
def getPlayers():
    players = []
    for name in df["Source"]:
        #TODO: check why error no vehicle shows up in rpt.
        if name not in npc and name not in players and name.find("Error") < 0:
            players.append(name)
    return players

def plotNpcValues():
    for src in npc:
        plotFPS(src)
        plotLocalUnits(src)
def plotPlayerFps():
    players = getPlayers()
    for player in players:
        plotFPS(player, 2)
def plotFPS(source, index=0):
    sns.lineplot(ax=axes[index], x="Server Time", y="FPS",ci=None, label=source, data=df.loc[df['Source'].isin([source])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
def plotLocalUnits(source):
    sns.lineplot(ax=axes[1], x="Server Time", y="Local units",ci=None, label=source, data=df.loc[df['Source'].isin([source])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

#sns.lineplot(ax=axes[0], x="Server Time", y="FPS",ci=None, label="Server" ,data=df.loc[df['Source'].isin(['Server'])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[0], x="Server Time", y="FPS",ci=None, label="HC1", data=df.loc[df['Source'].isin(['HC1'])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[0], x="Server Time", y="FPS",ci=None, label="HC2", data=df.loc[df['Source'].isin(['HC2'])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[1], x="Server Time", y="Local units",ci=None, label="Server" ,data=df.loc[df['Source'].isin(['Server'])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[1], x="Server Time", y="Local units",ci=None, label="HC1", data=df.loc[df['Source'].isin(['HC1'])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[1], x="Server Time", y="Local units",ci=None, label="HC2", data=df.loc[df['Source'].isin(['HC2'])]).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

#sns.lineplot(ax=axes[0],x="Server Time", y="Server FPS",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[1],x="Server Time", y="Player Count",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[2],x="Server Time", y="Guaranteed Messages",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[3],x="Server Time", y="Non-G Messages",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[4],x="Server Time", y="RAM [MB]",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[5],x="Server Time", y="in [Kbps]",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
#sns.lineplot(ax=axes[6],x="Server Time", y="out [Kbps]",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plotNpcValues()
plotPlayerFps()
plt.savefig("Combined.png", dpi=200)
#plt.show()
plt.close()

'''
#altair HTML output
fps_chart = alt.Chart(df).mark_line().encode(
    x='Server Time',
    y='Server FPS'
).save('Server_FPS.html')
 
alt.Chart(df).mark_line().encode(
    x='Server Time',
    y='Player Count'
).save('Player_Count.html')

alt.Chart(df).mark_line().encode(
    x='Server Time',
    y='Guaranteed Messages'
).save('Guaranteed_Messages.html')
'''
