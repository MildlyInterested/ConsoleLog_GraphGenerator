from os import times
import re
#line = "22:03:25 [LOGGING] [STATS] Source: Server - FPS: 61.78 - Local groups: 1 - Local units: 11 - Total units: 112 - Vehicles: 215 -  Active Scripts: [spawn: 15, execVM: 4, exec: 0, execFSM: 2]"
line = "22:03:28 [LOGGING] [STATS] Source: Sqn Ldr Hendrickx - FPS: 36.87 - Local groups: 1 - Local units: 1 -  Active Scripts: [spawn: 4, execVM: 2, exec: 0, execFSM: 3]"
fps = line[line.find("FPS: ")+len("FPS: "):line.find(" - Local groups:")]
source = line[line.find(" Source: ")+len(" Source: "):line.find(" - FPS:")]
time = line[+1:line.find(" [LOGGING] [STATS]")]
localUnit = line[line.find("Local units: ")+len("Local units: "):line.find(" ",line.find("Local units: ")+len("Local units: "))]
print(fps)
print(source)
print(time)
print(localUnit)