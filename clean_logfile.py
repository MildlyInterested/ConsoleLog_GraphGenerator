import sys
import pandas as pd
"""
errors = []
linenum = 0
pattern = re.compile("Server load", re.IGNORECASE)  # Compile a case-insensitive regex

f = open("server_logs_cleaned.csv", "w")  # open file
f.write("Server Time,Server FPS,RAM [MB],out [Kbps],in [Kbps],Non-G Messages,Guaranteed Messages,BE-NG,BE-G,Player Count" + "\n")

with open ('server_console.log', mode='rt', errors='replace') as myfile:    
    for line in myfile:
        linenum += 1
        if pattern.search(line) != None:      # If a match is found
            errors.append((linenum, line.rstrip('\n')))
for err in errors:                            # Iterate over the list of tuples
    #print("Line " + str(err[0]) + ": " + err[1])
    timefixed = re.sub(r"(:\d\d:\d\d)",r"\1,",err[1]) #adds ","" after hh:mm:ss
    playerfixed = re.sub(r"\((.*?)\)","",timefixed) # get rid of "L:0, R:1, B:0, G:9, D:0" behind player counter
    semicolon = re.sub(":", ";", playerfixed, 2) #replaces first two ":"" with ";", important for server time
    numberfixed = re.sub("[^0-9,;]", "", semicolon) #gets rid of all non number characters, "," and ";" are kept
    resemicolon = re.sub(";", ":", numberfixed) #replaces ";" with ":" again, restores server time to original formatting

    f.write(resemicolon + '\n')
    print(resemicolon)
"""

    #Time, FPS if player
    #Time, FPS, local units if not player
    #Start with: [LOGGING] [STATS]

#########################################
errors = []
#Used to differentiate between players and non-players
#nonPlayers = ["HC", "SERVER"]
#opName = input("Please enter the filename of the rpt you fancy...:\n")
#if opName.find(".rpt") < 0:
#    print("you fucked up")
#    sys.exit()
opName = "2021_11_28_CHI.rpt"
output = open("rpt_cleaned.csv", "w")
output.write("Server Time,Source,FPS,Local units" + "\n")

def cleanData():
    logfile = open(opName, "r", errors='replace')
    for line in logfile:
        if line.find("[LOGGING] [STATS]") > 0:
            tmp = line[:line.find(" -  Active Scripts:")]
            if tmp.find(" - Total units:") > 0:
                tmp = tmp[:tmp.find(" - Total units:")]
            time = tmp[:tmp.find(" \"[LOGGING]")]
            source = tmp[tmp.find("Source: ") + 8:tmp.find(" - FPS:")]
            fps = tmp[tmp.find("FPS: ") + 5:tmp.find(" - Local groups:")]
            localUnit = tmp[tmp.find("Local units: ") + 13:]
            sum = time + "," + source + "," + fps + "," + localUnit + "\n"
            #print(sum) #sanity check
            output.write(sum)
    output.close()
    return opName

#def createDataset():
    #introduce logic to differentiate between players and non-players at the cleanData steps
    #playerMeanFps
    #serverFps
    #HCLocalUnits
    #player = open("playerFps.csv","w")
    #player.write("Server Time,Source,FPS" + "\n")
  #  server = open("serverFps.csv","w")
   # server.write("Server Time,FPS"+ "\n")
    #HC
    #for line in output:
        
