import re
line = "18:12:08 Server load: FPS 27, memory used: 2487 MB, out: 71436 Kbps, in: 1190 Kbps, NG:0, G:86369, BE-NG:0, BE-G:0, Players: 80 (L:0, R:2, B:1, G:77, D:0)"
result = re.search('FPS (\d+)', line, re.IGNORECASE)

print(result.group(1))