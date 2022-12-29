import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import combine_data as cd

complete_df = cd.import_csv("complete_cleaned.csv", time_column="Server Time", day_rollover=True)

#get average of FPS columns excluding columns with name Server and HC
fps_columns = [col for col in complete_df.columns if "FPS" in col and "Server" not in col and "HC" not in col]
complete_df["Average FPS"] = complete_df[fps_columns].median(axis=1)

#sum up all units columns excluding columns with name Server and HC
units_columns_players = [col for col in complete_df.columns if "Units" in col and "Server" not in col and "HC" not in col]
#-1 to only counts extra local units, not player itself
for col in units_columns_players:
    complete_df[col] = complete_df[col] - 1
#interpolate missing values in units_columns_players
for col in units_columns_players:
    complete_df[col] = complete_df[col].interpolate()
complete_df["Total Units Players"] = complete_df[units_columns_players].sum(axis=1)

#sum up server and HC units columns
units_columns_nonplayers = [col for col in complete_df.columns if "Units" in col and ("Server" in col or "HC" in col)]
complete_df["Total Units Non-Players"] = complete_df[units_columns_nonplayers].sum(axis=1)
#add Total Units Non-Players and Total Units Players to get Total Units
complete_df["Total Units"] = complete_df["Total Units Players"] + complete_df["Total Units Non-Players"]

####### PLOT ########

# plot Total Units and Average FPS vs Server Time with two y axes
fig, ax1 = plt.subplots(figsize=(20,10))
l1, = ax1.plot(complete_df["Server Time"], complete_df["Total Units"], color="blue")
ax1.set_xlabel("Server Time")
ax1.set_ylabel("Total AI Units")
ax2 = ax1.twinx()
l2, = ax2.plot(complete_df["Server Time"], complete_df["Average FPS"], color="red")
ax2.set_ylabel("Average Player FPS")
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("axes", 1.05))
l3, = ax3.plot(complete_df["Server Time"], complete_df["FPS_Server"], color="green")
ax3.set_ylabel("Server FPS")
# plot average HC FPS vs Server Time
ax4 = ax1.twinx()
ax4.spines["right"].set_position(("axes", 1.1))
l4, = ax4.plot(complete_df["Server Time"], complete_df["FPS_HC_1"], color="orange")
l5, = ax4.plot(complete_df["Server Time"], complete_df["FPS_HC_2"], color="black")
ax4.set_ylabel("HC FPS")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax1.legend([l1, l2, l3, l4, l5], ["Total AI Units", "Average Player FPS", "Server FPS", "HC 1 FPS", "HC 2 FPS"], loc="upper right")
plt.title("Total AI Units and Average Player FPS vs Server Time")
plt.show()
plt.close()