import re
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