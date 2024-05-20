import requests
import datetime
import json
now = datetime.datetime.now()

class Timings():
    def __init__(self):
        self.start = ""
        self.doneInfo = ""
        self.stages = []
        self.before_event = []
        self.before_req = []
        self.after_req = []
        self.done = ""

times = Timings()


#add option to not search for club or age class
#add location search? - 25 miles of inputted postcode, or, ideally, looks up postcode from a town the user enters
#add option to search for course at events? although the course names differ for each so maybe not
#make use of M or W, or take it out so people don't think it looks for one but shows both.

searchYOBs = []
listofclubs = {"AIRE": 23, "AROS": 147, "AUOC": 158, "AYROC": 58, "BADO": 89, "BAOC": 117, 
                "BASOC": 62, "BKO": 91, "BL": 60, "BOF": 152, "BOK": 44, "CHIG": 92, 
                "CLARO": 24, "CLOK": 41, "CLYDE": 63, "COBOC": 38, "CUOC": 112, "DEE": 61, 
                "DEVON": 45, "DFOK": 94, "DRONGO": 139, "DUOC": 134, "DVO": 21, "EBOR": 25, 
                "ECKO": 65, "ELO": 67, "EPOC": 26, "ERYRI": 53, "ESOC": 68, "EUOC": 111, 
                "FERMO": 87, "FVO": 69, "GMOA": 120, "GO": 95, "GRAMP": 71, "GUOC": 153, 
                "HALO": 27, "HAVOC": 32, "HH": 96, "HOC": 39, "INT": 72, "INVOC": 73, 
                "IOM OK": 166, "JOK": 121, "KERNO": 46, "KFO": 74, "LEI": 29, "LOC": 64, 
                "LOG": 30, "LOK": 97, "LUOC": 157, "LUUOC": 151, "LVO": 88, "MA": 161, 
                "MAROC": 75, "MDOC": 66, "MOR": 76, "MV": 99, "MWOC": 54, "NATO": 50, 
                "NGOC": 15, "NN": 55, "NOC": 31, "NOR": 33, "NWO": 47, "NWOC": 90, 
                "OD": 19, "OROX": 163, "OUOC": 114, "PARCOR": 165, "PFO": 78, 
                "POTOC": 40, "QO": 48, "RAFO": 115, "RNRMOC": 128, "RR": 77, 
                "RSOC": 159, "SARUM": 49, "SAX": 148, "SBOC": 56, "SELOC": 79, "SHUOC": 129, 
                "SLOW": 100, "SMOC": 34, "SN": 101, "SO": 105, "SOC": 102, "SOFA": 103, 
                "SOLWAY": 80, "SOS": 35, "SPOOK": 137, "SROC": 81, "STAG": 82, "SUFFOC": 36, 
                "SWOC": 57, "SYO": 28, "TAY": 84, "TINTO": 86, "TVOC": 104, "UBOC": 132, 
                "WAOC": 37, "WAROC": 83, "WCH": 42, "WCOC": 85, "WIGHTO": 106, "WIM": 51, 
                "WRE": 43, "WSX": 52, "XPLORER": 160}

def check_age_valid(ageClass):
    if not ageClass[0].isalpha():
        return False
    
    try:
        value = int(ageClass[1:])
        return True
    except:
        return False

def round_to_five(x, base=5):
    return base * round(x/base)

def agetoyears(value):
    ageClass = value
    
    while not check_age_valid(ageClass):
        ageClass = str(input("Please use correct format e.g. M14, W21, not '{}'\n".format(ageClass)))
        
    gender = ageClass[0].upper()
    age = int(ageClass[1:])
    print("age: {}, gender: {}".format(age, gender))

    searchterms = []

    if age < 21:
        searchterms.append(str(now.year - int(age)))
        searchterms.append(str(now.year - (int(age) - 1)))
    elif 21 <= age <= 34:
        for year in range(now.year - 34, now.year - 20):
            searchterms.append(str(year))
    else:
        if age >= 100:
            print("senior years eh")
        age5 = round_to_five(age)
        for year in range(now.year - (age5 + 4), now.year - (age5 - 1)):
            searchterms.append(str(year))

    return searchterms

def getEventResults(eventpage, venue, SearchInfo, times):
    #SET UP SOUP
    if eventpage in SearchInfo.linksDict:
        html = SearchInfo.linksDict[eventpage]
        #print("using dict for {}".format(eventpage))
    else:
        times.before_req.append(datetime.datetime.now())
        html = requests.get(eventpage).text
        times.after_req.append(datetime.datetime.now())
        SearchInfo.linksDict[eventpage] = html

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    courseLinks = []
    resultsForEvent = {}

    event = soup.find("h2", {"id": "pagesubheading"})
    print(".")

    courseLinks.append(eventpage)
    for x in soup.findAll("a"):
        if x.has_attr("href"):
            if 'course=' in x.get('href'):
                course = x.get('href')
                course = "https://www.britishorienteering.org.uk/{}".format(course)
                courseLinks.append(course)
    

     
    for url in courseLinks:
        getCourseResults(url, SearchInfo, resultsForEvent, times)


    #after all the results have been found
    competitors = 0
    
    for x in resultsForEvent:
        for y in resultsForEvent[x]:
            competitors += 1

    if competitors > 0:
        if venue != "":
            venue = "at {}".format(venue)
        print("\n", event.text, venue)
        
        for x in resultsForEvent:
            for y in resultsForEvent[x]:
                result = resultsForEvent[x][y]
                ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])  #function for converting integer to ordinal e.g. 1 --> 1st, 2 --> 2nd
                #this checks if the position is indeed a number, as a mispunch is represented by a "-"
                try:
                    int(result["pos"])
                    poss = int(result["pos"])
                    ordinalPos = ordinal(poss)
                except ValueError:
                    ordinalPos = result["pos"]

                if "course" in result["course"]:
                    #print(result["name"], "was", ordinalPos, "on", result["course"])
                    print("{}, {} was {} on {}".format(result["name"], result["club"], ordinalPos, result["course"]))
                else:
                    #print(result["name"], "was", ordinalPos, "on the", result["course"])
                    print("{}, {} was {} on the {} course".format(result["name"], result["club"], ordinalPos, result["course"]))
    
    times.stages.append(datetime.datetime.now())

def getCourseResults(url, searchInfo, resultsForEvent, times):
    if url in SearchInfo.linksDict:
        coursepage = SearchInfo.linksDict[url]
        #print("using dict for coursepage: {}".format(url))
    else:
        times.before_req.append(datetime.datetime.now())
        coursepage = requests.get(url).text
        times.after_req.append(datetime.datetime.now())
        SearchInfo.linksDict[url] = html

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(coursepage, 'html.parser')

    try:
        course = soup.find("strong").text ###for some reason this is being stupid
        goahead = True
    except:
        goahead = False    #some events have no linked results, hence no strong text


    if goahead == True:
        course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
        #print("course: {}".format(course))
        resultsForEvent[course] = {}

        #FIND RESULTS
        number = 1
        
        for x in soup.tbody.findAll("tr"):
            number = 1

            

            if SearchInfo.searchType == "age":
                query_check = checkAgeClass(x, SearchInfo.searchQuery)
            elif SearchInfo.searchType == "club":
                query_check = checkClub(x, SearchInfo.searchQuery)
            
            if query_check == True:  
                  
                for y in x.findAll("td"):
                    if number == 1:
                        position = y.text
                        resultsForEvent[course][position] = {}
                        resultsForEvent[course][position]["pos"] = y.text
                        resultsForEvent[course][position]["course"] = course
                    elif number == 2:
                        resultsForEvent[course][position]["name"] = y.text
                    elif number == 3:
                        resultsForEvent[course][position]["club"] = y.text
                    elif number == 6:
                        #resultsForEvent[course][position]["time"] = y.text
                        pass
                    else:
                        pass
                    number += 1

def checkClub(tr, searchClub):
    
    for field in tr.findAll("td"):
        if field.text == searchClub:
            return True
    return False

def checkAgeClass(tr, searchyears):
    
    for field in tr.findAll("td"):
        if str(field.text) in searchyears:
            return True
    return False


class Stuff():
    def __init__(self):
        self.searchType = "age"
        self.searchQuery = agetoyears("M16")
        self.linksDict = {}

def job():
    day = str(input("What day?\n"))
    month = str(input("What month?\n"))
    end_day = str(input("End day?\n"))
    end_month = str(input("End month?\n"))

times.start = datetime.datetime.now()
#GET SEARCH INFO
SearchInfo = Stuff()
website = ("https://www.britishorienteering.org.uk/index.php?page=0&evt_name=&evt_postcode=&evt_radius=0&evt_level=0evt_type=0&event_club=0&evt_start_d={}&evt_start_m={}&evt_start_y=2020&evt_end_d={}&evt_end_m={}&evt_end_y=2020&evt_assoc=0&evt_start=1577836800&evt_end=1585907978&perpage=100&bSearch=1&pg=results".format("01", "01", "10", "01"))
times.doneInfo = datetime.datetime.now()


#SET UP SOUP
html = requests.get(website).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []
eventDict = {}
keyno = 1

#EXTRACT EVENT LINKS
eventTable = soup.table

for row in eventTable.tbody.findAll("tr"):
    number = 1
    minidict = {}
    
    for y in row.findAll("td"):
        if number == 1:
            minidict["date"] = y.text
        elif number == 5:
            minidict["eventName"] = y.text
        elif number == 6:
            minidict["venue"] = y.text
        elif number == 7:
                try:
                    minidict["url"] = y.a.get('href')
                except:
                    pass
        number += 1
    eventDict[keyno] = minidict
    keyno += 1

with open("pages.json", "r+") as pages:
    SearchInfo.linksDict = json.load(pages)


for x in eventDict:
    if "url" in eventDict[x]:
        eventpage = ("https://www.britishorienteering.org.uk{}".format(eventDict[x]["url"]))
        eventvenue = eventDict[x]["venue"]
        times.before_event.append(datetime.datetime.now())
        getEventResults(eventpage, eventvenue, SearchInfo, times)

if len(eventDict) == 100:
    print("Reached event limit - 100 events scraped")
else:
    print("Finished - {} events scraped".format(len(eventDict)))

times.done = datetime.datetime.now()

with open("processing.json", "r+") as stats:
    dictionary = json.load(stats)

key = str(datetime.datetime.now())
dictionary[key] = {}


diff1 = (times.doneInfo - times.start).total_seconds() * 1000
dictionary[key]["diff1"] = diff1
print("start -> doneinfo: {}ms".format(diff1))
totalDiff = (times.done - times.start).total_seconds() * 1000
dictionary[key]["totaltime"] = totalDiff
print("total time: {}ms".format(totalDiff))

dictionary[key]["rtimes"] = []
totalRtime = 0
for x in range(0, len(times.before_req)):
    rtime = (times.after_req[x]-times.before_req[x]).total_seconds() * 1000
    dictionary[key]["rtimes"].append(rtime)
    print("request time: {}ms".format(rtime))
    totalRtime += rtime

dictionary[key]["totalR"] = totalRtime

dictionary[key]["eventTimes"] = []
for x in range(1, len(times.before_event)):
    event_time = (times.before_event[x] - times.before_event[x-1]).total_seconds() * 1000
    print("event time: {}ms".format(event_time))
    dictionary[key]["eventTimes"].append(event_time)

print("time spent on requests: {}ms".format(totalRtime))
processTime = totalDiff - totalRtime
dictionary[key]["processingTime"] = processTime
print("therefore, time spent on processing: {}ms".format(processTime))

with open("processing.json", "w+") as stats:
    json.dump(dictionary, stats)

with open("pages.json", "w+") as pages:
    json.dump(SearchInfo.linksDict, pages)