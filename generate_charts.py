###IMPORT###
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
# import altair as alt
# from altair_saver import save
import matplotlib.dates as md


####CODE####
sns.set_style("whitegrid")
df = pd.read_csv('server_logs_cleaned.csv', header=0)
#print(df) #sanity check
#print(df.dtypes)
df['Server Time'] = pd.to_datetime(df['Server Time']) #converts string to datetime (YYYY-mm-dd-HH-mm-ss)
df['Time Diff'] = df['Server Time'].diff()
m = df['Server Time'].diff() < pd.Timedelta(0)
df['Server Time'] += pd.to_timedelta(m.cumsum(), unit='d')
#print(df.dtypes)
print(m)
print(df)
df.to_csv('server_logs_panda.csv')

'''
plt.figure(figsize=(20,10))
plot1 = sns.lineplot(x="Server Time", y="Server FPS",ci=None, data=df)
plot1.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.savefig("Server_FPS.png", dpi=200)
plt.close()

plt.figure(figsize=(20,10))
plot2 = sns.lineplot(x="Server Time", y="Player Count",ci=None, data=df)
plot2.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.savefig("Player Count.png", dpi=200)
plt.close()

plt.figure(figsize=(20,10))
plot3 = sns.lineplot(x="Server Time", y="Guaranteed Messages",ci=None, data=df)
plot3.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.savefig("G-Messages.png", dpi=200)
plt.close()
'''

figure, axes = plt.subplots(7, 1, sharex=True, figsize=(35,25))
figure.suptitle('My beautiful Charts')
#figure.tight_layout()
figure.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.05)
sns.lineplot(ax=axes[0],x="Server Time", y="Server FPS",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
sns.lineplot(ax=axes[1],x="Server Time", y="Player Count",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
sns.lineplot(ax=axes[2],x="Server Time", y="Guaranteed Messages",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
sns.lineplot(ax=axes[3],x="Server Time", y="Non-G Messages",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
sns.lineplot(ax=axes[4],x="Server Time", y="RAM [MB]",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
sns.lineplot(ax=axes[5],x="Server Time", y="in [Kbps]",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
sns.lineplot(ax=axes[6],x="Server Time", y="out [Kbps]",ci=None, data=df).xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
plt.savefig("Combined.png", dpi=200)
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
