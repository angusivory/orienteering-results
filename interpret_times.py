import json

with open("processing.json", "r+") as stats:
    dictionary = json.load(stats)

totalTimes = []
rTimes = []
processingTimes = []
totalRs = []

for run in dictionary:
    totalTimes.append(dictionary[run]["totaltime"])
    avgR = 0
    for x in dictionary[run]["rtimes"]:
        avgR += x
    #avgR = avgR/len(dictionary[run]["rtimes"])
    rTimes.append(avgR)
    processingTimes.append(dictionary[run]["processingTime"])
    totalRs.append(dictionary[run]["totalR"])

avgTotal = 0
for x in totalTimes:
    avgTotal += x
avgTotal = avgTotal/len(totalTimes)
print("avgTotal: {}ms".format(avgTotal))

def notneeded():
    avgRtimes = 0
    for x in rTimes:
        avgRtimes += x
    avgRtimes = avgRtimes/len(rTimes)
    print("avg time per request: {}ms".format(avgRtimes))

    avgtotalR = 0
    for z in totalRs:
        avgtotalR += z
    avgtotalR = avgtotalR/len(totalRs)
    print("avg time spent on getting requests: {}ms".format(avgtotalR))

avgProc = 0
for y in processingTimes:
    avgProc += y
avgProc = avgProc/len(processingTimes)
print("avgProc: {}ms".format(avgProc))



for x in dictionary:
    avgEventTime = 0
    for y in dictionary[x]["eventTimes"]:
        avgEventTime += y
    avgEventTime = avgEventTime/len(dictionary[x]["eventTimes"])
    print("avg event time for run {}: {}ms".format(x, avgEventTime))
