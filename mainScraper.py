import requests

#add search for age classes

#add search for postcode, radius 25 or 50 miles

dateFrom = str(input("Set date from which to get results (dd/mm/yyyy)\n"))
dateFrom = dateFrom.split("/")
if not len(dateFrom) == 3:
    dateFrom = ["0", "0", "0"]

dateTo = str(input("Set end date to get results until (dd/mm/yyyy)\nIf you don't want a specific end date, type 'now'\n"))
dateTo = dateTo.split("/")
if not len(dateTo) == 3:
    dateTo = ["0", "0", "0"]


level = input("What level events? Type '0' for all, '1' for Major, '2' for National, '3' for Regional or '-4' for all except local.\n")
assoc = input("[opt] Specify region: BOF, BSOA, EAOA, EMOA, NEOA, NIOA, NWOA, SCOA, SEOA, SOA, SWOA, WMOA, WOA, YHOA, all.\n").upper()
associations = {"BOF": 14, "BSOA": 13, "EAOA": 1, "EMOA": 2, "NEOA": 3, "NIOA": 4, "NWOA": 5, "SCOA": 6, "SEOA": 7, "SOA": 8, "SWOA": 9, "WMOA": 10, "WOA": 11, "YHOA": 12}
if assoc in associations:
    assoc_num = associations[assoc]
else:
    assoc_num = 0
host_club = input("[opt] Specify host club abbr. or 'any'\n").upper()
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
if host_club in listofclubs:
    host_club_num = listofclubs[host_club]
else:
    host_club_num = 0    

website = ("https://www.britishorienteering.org.uk/index.php?page=0&evt_name=&evt_postcode=&evt_radius=0&evt_level={}&evt_type=0&event_club={}&evt_start_d={}&evt_start_m={}&evt_start_y={}&evt_end_d={}&evt_end_m={}&evt_end_y={}&evt_assoc={}&evt_start=1577836800&evt_end=1585907978&perpage=100&bSearch=1&pg=results".format(level, host_club_num, dateFrom[0], dateFrom[1], dateFrom[2], dateTo[0], dateTo[1], dateTo[2], assoc_num))

searchClub = str(input("Which club do you want to search for? (use abbr.)\n"))
searchClub = searchClub.upper()

print("Searching all {} level {} results hosted by {} from {}/{}/{} to {}/{}/{} in the {} region.".format(searchClub, level, host_club, dateFrom[0], dateFrom[1], dateFrom[2], dateTo[0], dateTo[1], dateTo[2], assoc))


#SET UP SOUP
html = requests.get(website).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []
eventDict = {}
keyno = 1

#getEventResults(website, club) function
def getEventResults(eventpage, venue, searchClub):
    #SET UP SOUP
    html = requests.get(eventpage).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    #results for each course are stored between the <table> tags.
    #DESIGN: from the event page: the program should put all the course hyperlinks into a list, do getResults() function on each of them.
    courseLinks = []
    resultsForEvent = {}

    #Function for retrieving results for each course
    def getResults(url, searchClub):

        #Function for checking if the club matches the inputed club             Why can't i define this elsewhere? - it only works if it is defined inside of this function.
        def checkClub(searchClub):
            for y in x.findAll("td"):
                if y.text == searchClub:
                    return True

        number = 1
        subhtml = requests.get(url).text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(subhtml, 'html.parser')

        try:
            course = soup.find("strong").text ###for some reason this is being stupid
        except:
            pass    #some events have no linked results, hence no strong text

        course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
        #print("course: {}".format(course))
        resultsForEvent[course] = {}

        #FIND RESULTS
        for x in soup.tbody.findAll("tr"):
            number = 1
            if checkClub(searchClub) is True:
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


    #MAIN PROGRAM LOOP
    event = soup.find("h2", {"id": "pagesubheading"})
    print(".")

    #adds all the course hyperlinks to a list
    courseLinks.append(eventpage)
    for x in soup.findAll("a"):
        if x.has_attr("href"):
            if 'course=' in x.get('href'):
                course = x.get('href')
                course = "https://www.britishorienteering.org.uk/{}".format(course)
                courseLinks.append(course)

    for url in courseLinks:
        getResults(url, searchClub)


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
                    print(result["name"], "was", ordinalPos, "on", result["course"])
                else:
                    print(result["name"], "was", ordinalPos, "on the", result["course"])










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
        getEventResults(eventpage, eventvenue, searchClub)