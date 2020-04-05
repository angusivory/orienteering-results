import requests

dateFrom = str(input("Set date from which to get results (dd/mm/yyyy)\n"))
dateFrom = dateFrom.split("/")  #dateFrom is now a list: item 0 is the day, item 1 is the month, item 2 is the year
level = input("What level events? Type '0' for all, '1' for Major, '2' for National, '3' for Regional or '-4' for all except local.\n")

                                                        #this bit ¬ 'page=0' is a problem - even with showing 100 entries per page there are still multiple pages, the next with 'page=1' and 'page=2' if there are that many events. 
website = ("https://www.britishorienteering.org.uk/index.php?page=0&evt_name=&evt_postcode=&evt_radius=0&evt_level={}&evt_type=0&event_club=0&evt_start_d={}&evt_start_m={}&evt_start_y={}&evt_end_d=0&evt_end_m=0&evt_end_y=0&evt_assoc=0&evt_start=1577836800&evt_end=1585907978&perpage=100&bSearch=1&pg=results".format(level, dateFrom[0], dateFrom[1], dateFrom[2]))
club = str(input("Which club do you want to search for?\n"))
club = club.upper()

#SET UP SOUP
html = requests.get(website).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []
eventid = ["date", "eventName", "venue", "url"]
resultsDictionary = {}
keyno = 1

#getEventResults(website, club) function
def getEventResults(eventpage, club):
    #SET UP SOUP
    html = requests.get(eventpage).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    #results for each course are stored between the <table> tags.
    #DESIGN: from the event page: the program should put all the course hyperlinks into a list, do getResults() function on each of them.
    courseLinks = []
    eventDict = {}

    #Function for retrieving results for each course
    def getResults(url, club):

        #Function for checking if the club matches the inputed club             Why can't i define this elsewhere? - it only works if it is defined inside of this function.
        def checkClub(club):
            for y in x.findAll("td"):
                if y.text == club:
                    return True

        number = 1
        subhtml = requests.get(url).text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(subhtml, 'html.parser')

        course = soup.find("strong").text
        course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
        #print(course)
        eventDict[course] = {}

        #FIND RESULTS
        for x in soup.tbody.findAll("tr"):
            number = 1
            checkClub(club)
            if checkClub(club) is True:
                #print("club correct")
                for y in x.findAll("td"):
                    if number == 1:
                        position = y.text
                        eventDict[course][position] = {}
                        eventDict[course][position]["pos"] = y.text
                        eventDict[course][position]["course"] = course
                    elif number == 2:
                        eventDict[course][position]["name"] = y.text
                    elif number == 3:
                        eventDict[course][position]["club"] = y.text
                    elif number == 6:
                        #eventDict[course][position]["time"] = y.text
                        pass
                    else:
                        pass
                    number += 1


    #MAIN PROGRAM LOOP
    event = soup.find("h2", {"id": "pagesubheading"})
    #print("\n", event.text)


    #adds all the course hyperlinks to a list
    courseLinks.append(eventpage)
    for x in soup.findAll("a"):
        if x.has_attr("href"):
            if 'course' in x.get('href'):
                course = x.get('href')
                course = "https://www.britishorienteering.org.uk/{}".format(course)
                courseLinks.append(course)

    for url in courseLinks:
        #print("getting results from", url)
        getResults(url, club)

    #after all the results have been found
    competitors = 0
    for x in eventDict:
        for y in eventDict[x]:
            competitors += 1

    if competitors > 0:
        print("\n",event.text)
        for x in eventDict:
            for y in eventDict[x]:
                result = eventDict[x][y]
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
                    print(result["name"], "was", ordinalPos, "on", result["course"])
    else:
        print(".")










eventTable = soup.table
for x in eventTable.tbody.findAll("tr"):
    number = 1
    minidict = {}
    for y in x.findAll("td"):
        if number == 1:
            minidict["date"] = y.text
        elif number == 5:
            minidict["eventName"] = y.text
        elif number == 6:
            minidict["venue"] = y.text
        elif number == 7:
                aas = y.find("a")
                if aas:
                    minidict["url"] = y.a.get('href')
        number += 1
    resultsDictionary[keyno] = minidict
    keyno += 1

for x in resultsDictionary:
    if "url" in resultsDictionary[x]:
        eventpage = ("https://www.britishorienteering.org.uk{}".format(resultsDictionary[x]["url"]))
        getEventResults(eventpage, club)