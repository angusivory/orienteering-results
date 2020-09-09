import requests
import datetime
now = datetime.datetime.now()

#add location search? - 25 miles of inputted postcode, or, ideally, looks up postcode from a town the user enters

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

def agetoyears():
    ageClass = str(input("Which age class do you want to search for? (e.g. M14, W21)\n"))
    
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

def getEventResults(eventpage, venue, SearchInfo):
    #SET UP SOUP
    html = requests.get(eventpage).text
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
        getCourseResults(url, SearchInfo, resultsForEvent)


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

def getCourseResults(url, searchInfo, resultsForEvent):
    coursepage = requests.get(url).text
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

class Params():
    def __init__(self):
        self.associations = {"BOF": 14, "BSOA": 13, "EAOA": 1, "EMOA": 2, "NEOA": 3, "NIOA": 4, "NWOA": 5, "SCOA": 6, "SEOA": 7, "SOA": 8, "SWOA": 9, "WMOA": 10, "WOA": 11, "YHOA": 12}
        self.dateFrom = str(input("Set date from which to get results (dd/mm/yyyy)\n"))
        self.dateFrom = self.dateFrom.split("/")
        if not len(self.dateFrom) == 3:
            self.dateFrom = ["0", "0", "0"]

        self.dateTo = str(input("Set end date to get results until (dd/mm/yyyy)\nIf you don't want a specific end date, type 'now'\n"))
        self.dateTo = self.dateTo.split("/")
        if not len(self.dateTo) == 3:
            self.dateTo = ["0", "0", "0"]

        self.level = input("What level events? Type '0' for all, '1' for Major, '2' for National, '3' for Regional or '-4' for all except local.\n")
        
        self.assoc = input("[opt] Specify region: BOF, BSOA, EAOA, EMOA, NEOA, NIOA, NWOA, SCOA, SEOA, SOA, SWOA, WMOA, WOA, YHOA, all.\n").upper()
        if self.assoc in self.associations:
            self.assoc_num = self.associations[self.assoc]
        else:
            self.assoc_num = 0

        self.host_club = input("[opt] Specify host club abbr. or 'any'\n").upper()
        if self.host_club in listofclubs:
            self.host_club_num = listofclubs[self.host_club]
        else:
            self.host_club_num = 0

        if str(input("Search by 'age' or 'club'?\n")) == "age":
            self.searchQuery = agetoyears()
            self.searchType = "age"
        else:
            self.searchQuery = str(input("Which club do you want to search for? (use abbr.)\n")).upper()
            self.searchType = "club"


#GET SEARCH INFO
SearchInfo = Params()
website = ("https://www.britishorienteering.org.uk/index.php?page=0&evt_name=&evt_postcode=&evt_radius=0&evt_level={}&evt_type=0&event_club={}&evt_start_d={}&evt_start_m={}&evt_start_y={}&evt_end_d={}&evt_end_m={}&evt_end_y={}&evt_assoc={}&evt_start=1577836800&evt_end=1585907978&perpage=100&bSearch=1&pg=results".format(SearchInfo.level, SearchInfo.host_club_num, SearchInfo.dateFrom[0], SearchInfo.dateFrom[1], SearchInfo.dateFrom[2], SearchInfo.dateTo[0], SearchInfo.dateTo[1], SearchInfo.dateTo[2], SearchInfo.assoc_num))
print("Searching all current {} level {} results hosted by {} from {}/{}/{} to {}/{}/{} in the {} region.".format(SearchInfo.searchQuery, SearchInfo.level, SearchInfo.host_club, SearchInfo.dateFrom[0], SearchInfo.dateFrom[1], SearchInfo.dateFrom[2], SearchInfo.dateTo[0], SearchInfo.dateTo[1], SearchInfo.dateTo[2], SearchInfo.assoc))

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

for x in eventDict:
    if "url" in eventDict[x]:
        eventpage = ("https://www.britishorienteering.org.uk{}".format(eventDict[x]["url"]))
        eventvenue = eventDict[x]["venue"]
        getEventResults(eventpage, eventvenue, SearchInfo)

if len(eventDict) == 100:
    print("Reached event limit - 100 events scraped")
else:
    print("Finished - {} events scraped".format(len(eventDict)))