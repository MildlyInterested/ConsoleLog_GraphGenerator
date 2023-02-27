from ast import And
from dataclasses import replace
import sys
import pandas as pd


#########################################
#Used to differentiate between players and non-players
#nonPlayers = ["HC", "SERVER"]
#opName = input("Please enter the filename of the rpt you fancy...:\n")
#if opName.find(".rpt") < 0:
#    print("you fucked up")
#    sys.exit()

def whiteSpaceData(leading_up, line, follow=" "): #find number thats following the passed string in the passed line, follow is following characters
    data = line[line.find(leading_up)+len(leading_up):line.find(follow,line.find(leading_up)+len(leading_up))]
    return data

#TODO: combine functions below into one function
#TODO: track steam verification error (crashes) and player disconnecting (3FPS bug)

#Server Time, Source, FPS, Local groups, Local units, Total units, Vehicles
def cleanRPT_server(inputfile, outputfile, header=False):
    with open(inputfile, "r", errors='replace') as logfile, open(outputfile, "w") as outfile:
        if header:
            header_txt = "Server Time,Source_Server,FPS_Server,Local Groups_Server,Local Units_Server,Total units_Server,Vehicles_Server"
            outfile.write(header_txt+"\n")
        for line in logfile:
            if (line.find("[LOGGING] [STATS] [SERVER]") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" \"[LOGGING] [STATS]")]
                source = line[line.find("Source: ")+len("Source: "):line.find(" - FPS:")]
                fps = whiteSpaceData("FPS: ", line)
                localGroup = whiteSpaceData("Local groups: ", line)
                localUnit = whiteSpaceData("Local units: ", line)
                totalUnit = whiteSpaceData("Total units: ", line)
                vehicles = whiteSpaceData("Vehicles: ", line)
                sum = time+","+source+","+fps+","+localGroup+","+localUnit+","+totalUnit+","+vehicles+"\n"
                outfile.write(sum)

#Server Time, Source, FPS, Local groups, Local units
def cleanRPT_headless(inputfile, outputfile, header=False):
    with open(inputfile, "r", errors='replace') as logfile, open(outputfile, "w") as outfile:
        if header:
            header_txt = "Server Time,Source,FPS,Local Groups,Local Units"
            outfile.write(header_txt+"\n")
        for line in logfile:
            if (line.find("[LOGGING] [STATS] [HC]") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" \"[LOGGING] [STATS]")]
                source = line[line.find("Source: ")+len("Source: "):line.find(" - FPS:")]
                fps = whiteSpaceData("FPS: ", line)
                localGroup = whiteSpaceData("Local groups: ", line)
                localUnit = whiteSpaceData("Local units: ", line)
                sum = time+","+source+","+fps+","+localGroup+","+localUnit+"\n"
                outfile.write(sum)

#Server Time, Playername, FPS, Local groups, local units
def cleanRPT_player(inputfile, outputfile, header=False):
    with open(inputfile, "r", errors='replace') as logfile, open(outputfile, "w") as outfile:
        if header:
            header_txt = "Server Time,Source,FPS,Local Groups,Local Units"
            outfile.write(header_txt+"\n")
        for line in logfile:
            if (line.find("[LOGGING] [STATS] [PLAYER]") > 0) and (line.find("error") <= 0) and (line.find("Error") <= 0):
                time = line[0:line.find(" \"[LOGGING] [STATS]")]
                source = line[line.find("Source: ")+len("Source: "):line.find(" - FPS:")]
                fps = whiteSpaceData("FPS: ", line)
                localGroup = whiteSpaceData("Local groups: ", line)
                localUnit = whiteSpaceData("Local units: ", line)
                sum = time+","+source+","+fps+","+localGroup+","+localUnit+"\n"
                outfile.write(sum)

#Server Time,FPS,RAM [MB],out [Kbps],in [Kbps],NonGuaranteed, Guaranteed, Playercount
def cleanLOG(inputfile, outputfile, header=False):
    with open(inputfile, "r", errors='replace') as logfile, open(outputfile, "w") as outfile:
        if header:
            header_txt = "Server Time,FPS,RAM [MB],out [Kbps],in [Kbps],NonGuaranteed, Guaranteed, Playercount"
            outfile.write(header_txt+"\n")
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
                sum = time+","+fps+","+ram+","+outgoing+","+incoming+","+nong_msg+","+g_msg+","+players+"\n"
                outfile.write(sum)
                
#TODO don't save it in CSV, hold it in RAM
cleanRPT_server("test.rpt", "server_cleaned.csv", header=True)
cleanRPT_headless("test.rpt", "hc_cleaned.csv", header=True)
cleanRPT_player("test.rpt", "player_cleaned.csv", header=True)
cleanLOG("test.log", "log_cleaned.csv", header=True)