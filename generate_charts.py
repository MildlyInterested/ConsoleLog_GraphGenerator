###IMPORT###
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
from altair_saver import save

####CODE####
sns.set_theme(style="darkgrid")
df = pd.read_csv('server_logs_cleaned.csv', header=0)
#print(df) #sanity check
#print(df.dtypes)
df['Server Time'] = pd.to_datetime(df['Server Time'])
#print(df.dtypes)
print(df)

plot1 = sns.lineplot(x="Server Time", y="Server FPS",ci=None, data=df)
plt.savefig("Server_FPS.png", dpi=800)
plt.close()

plot2 = sns.lineplot(x="Server Time", y="Player Count",ci=None, data=df)
plt.savefig("Player Count.png", dpi=800)
plt.close()

plot2 = sns.lineplot(x="Server Time", y="Guaranteed Messages",ci=None, data=df)
plt.savefig("G-Messages.png", dpi=800)
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
