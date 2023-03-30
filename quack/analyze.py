import json
import os

folderName = "data/"
fileNames = os.listdir(folderName)
data = []

for fileName in fileNames:
    file = open(folderName + fileName)
    lines = file.readlines()
    file.close()
    data += [json.loads(line) for line in lines]

ips = set()

for i in data:
    if i["received_error"] and "EOF" not in i["received_error"]:
        print(i["server_ip"], i["domain"])
        ips.add(i["server_ip"])

print(len(ips))