import requests

eventpage = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=74350"
club = "FVO"

#getEventResults function(eventpage, club) to be incorporated into directResults.py


#SET UP SOUP
html = requests.get(eventpage).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []

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
print(event.text)


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