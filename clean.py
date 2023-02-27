import pandas as pd

def whiteSpaceData(leading_up, line, follow=" "): #find number thats following the passed string in the passed line, follow is following characters
    data = line[line.find(leading_up)+len(leading_up):line.find(follow,line.find(leading_up)+len(leading_up))]
    return data

#Server Time, Source, FPS, Local groups, Local units, Total units, Vehicles
def cleanRPT_server(inputfile, time_column="Server Time", day_rollover=True):
    df = pd.DataFrame(columns=["Server Time", "Source_Server", "FPS_Server", "Local groups_Server", "Local units_Server", "Total units_Server", "Vehicles_Server"])
    with open(inputfile, "r", errors='replace') as logfile:
        for line in logfile:
            if (line.find("[LOGGING] [STATS] [SERVER]") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" \"[LOGGING] [STATS]")]
                source = line[line.find("Source: ")+len("Source: "):line.find(" - FPS:")]
                fps = whiteSpaceData("FPS: ", line)
                localGroup = whiteSpaceData("Local groups: ", line)
                localUnit = whiteSpaceData("Local units: ", line)
                totalUnit = whiteSpaceData("Total units: ", line)
                vehicles = whiteSpaceData("Vehicles: ", line)
                row = [time, source, fps, localGroup, localUnit, totalUnit, vehicles]
                df = pd.concat([df, pd.DataFrame([row], columns=["Server Time", "Source_Server", "FPS_Server", "Local groups_Server", "Local units_Server", "Total units_Server", "Vehicles_Server"])], ignore_index=True)
    #TODO get panda to infer data types and not hardcode them
    df[time_column] = pd.to_datetime(df[time_column])
    if day_rollover:
        day_rollover = df[time_column].diff() < pd.Timedelta(0)
        df[time_column] += pd.to_timedelta(day_rollover.cumsum(), unit='d')
    for col in df.columns:
        if col == time_column or col == "Source_Server":
            continue
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

#Server Time, Source, FPS, Local groups, Local units
def cleanRPT_headless(inputfile, time_column="Server Time", day_rollover=True):
    df = pd.DataFrame(columns=["Server Time", "Source", "FPS", "Local groups", "Local units"])
    with open(inputfile, "r", errors='replace') as logfile:
        for line in logfile:
            if (line.find("[LOGGING] [STATS] [HC]") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" \"[LOGGING] [STATS]")]
                source = line[line.find("Source: ")+len("Source: "):line.find(" - FPS:")]
                fps = whiteSpaceData("FPS: ", line)
                localGroup = whiteSpaceData("Local groups: ", line)
                localUnit = whiteSpaceData("Local units: ", line)
                row = [time, source, fps, localGroup, localUnit]
                df = pd.concat([df, pd.DataFrame([row], columns=["Server Time", "Source", "FPS", "Local groups", "Local units"])], ignore_index=True)
    df[time_column] = pd.to_datetime(df[time_column])
    if day_rollover:
        day_rollover = df[time_column].diff() < pd.Timedelta(0)
        df[time_column] += pd.to_timedelta(day_rollover.cumsum(), unit='d')
    for col in df.columns:
        if col == time_column or col == "Source":
            continue
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

#Server Time, Source, FPS, Local groups, local units
def cleanRPT_player(inputfile, time_column="Server Time", day_rollover=True):
    df = pd.DataFrame(columns=["Server Time", "Source", "FPS", "Local groups", "Local units"])
    with open(inputfile, "r", errors='replace') as logfile:
        for line in logfile:
            if (line.find("[LOGGING] [STATS] [PLAYER]") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" \"[LOGGING] [STATS]")]
                source = line[line.find("Source: ")+len("Source: "):line.find(" - FPS:")]
                fps = whiteSpaceData("FPS: ", line)
                localGroup = whiteSpaceData("Local groups: ", line)
                localUnit = whiteSpaceData("Local units: ", line)
                row = [time, source, fps, localGroup, localUnit]
                df = pd.concat([df, pd.DataFrame([row], columns=["Server Time", "Source", "FPS", "Local groups", "Local units"])], ignore_index=True)
    df[time_column] = pd.to_datetime(df[time_column])
    if day_rollover:
        day_rollover = df[time_column].diff() < pd.Timedelta(0)
        df[time_column] += pd.to_timedelta(day_rollover.cumsum(), unit='d')
    for col in df.columns:
        if col == time_column or col == "Source":
            continue
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

#Server Time,FPS,RAM [MB],out [Kbps],in [Kbps],NonGuaranteed, Guaranteed, Playercount
def cleanLOG(inputfile, time_column="Server Time", day_rollover=True):
    df = pd.DataFrame(columns=["Server Time", "FPS_Server_log", "RAM [MB]", "out [Kbps]", "in [Kbps]", "NonGuaranteed", "Guaranteed", "Playercount"])
    with open(inputfile, "r", errors='replace') as logfile:
        for line in logfile:
            if (line.find("Server load:") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" Server load:")]
                fps = whiteSpaceData("FPS ", line,",")
                ram = whiteSpaceData("memory used: ", line)
                outgoing = whiteSpaceData("out: ", line)
                incoming = whiteSpaceData("in: ", line)
                nong_msg = whiteSpaceData("NG:", line,",")
                g_msg = whiteSpaceData("G:", line,",")
                players = whiteSpaceData("Players: ", line)
                row = [time, fps, ram, outgoing, incoming, nong_msg, g_msg, players]
                df = pd.concat([df, pd.DataFrame([row], columns=["Server Time", "FPS_Server_log", "RAM [MB]", "out [Kbps]", "in [Kbps]", "NonGuaranteed", "Guaranteed", "Playercount"])], ignore_index=True)
    df[time_column] = pd.to_datetime(df[time_column])
    if day_rollover:
        day_rollover = df[time_column].diff() < pd.Timedelta(0)
        df[time_column] += pd.to_timedelta(day_rollover.cumsum(), unit='d')
    for col in df.columns:
        if col == time_column or col == "Source":
            continue
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df