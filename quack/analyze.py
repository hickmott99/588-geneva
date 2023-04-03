import json
import os
from collections import defaultdict

folderName = "data/"
fileNames = os.listdir(folderName)
data = []

for fileName in fileNames:
    with open(folderName + fileName) as file:
        lines = file.readlines()
        data += [json.loads(line) for line in lines]

ips = set()
domains = set()
domainIpDict = defaultdict(lambda: set())   # domain -> set of ips
ipDomainDict = defaultdict(lambda: set())   # ip -> set of domains

for i in data:
    if i["received_error"] and ("timeout" in i["received_error"] or "reset" in i["received_error"]):
        ips.add(i["server_ip"])
        domains.add(i["domain"])
        domainIpDict[i["domain"]].add(i["server_ip"])
        ipDomainDict[i["server_ip"]].add(i["domain"])

sortedDomains = sorted(domainIpDict, key=lambda k: len(domainIpDict[k]), reverse=True)
sortedIps = sorted(ipDomainDict, key=lambda k: len(ipDomainDict[k]), reverse=True)

print("Unique IPs =", len(ips))
print("Unique domains =", len(domains))
print(sortedDomains[:20])

with open('genevadata.txt', 'a') as outputFile:
    for ip in sortedIps:
        print(ip, ipDomainDict[ip].pop(), file=outputFile)