import json
import os
from collections import defaultdict

folderName = "data/"
fileNames = os.listdir(folderName)
data = []

for fileName in fileNames:
    file = open(folderName + fileName)
    lines = file.readlines()
    file.close()
    data += [json.loads(line) for line in lines]

ips = set()
domains = set()
domainIpDict = defaultdict(lambda: set())   # domain -> set of ips

for i in data:
    if i["received_error"] and ("timeout" in i["received_error"] or "reset" in i["received_error"]):
        ips.add(i["server_ip"])
        domains.add(i["domain"])
        domainIpDict[i["domain"]].add(i["server_ip"])

print("Unique IPs =", len(ips))
print("Unique domains =", len(domains))
sortedDomains = sorted(domainIpDict, key=lambda k: len(domainIpDict[k]), reverse=True)
print(sortedDomains[:20])