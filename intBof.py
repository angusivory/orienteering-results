#An event's url is inputed and the program looks for all the people of a certain club in that event.

#BOF results page: https://www.britishorienteering.org.uk/results

import requests
website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=77328"  #Craigmillar Castle
website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=74350"  #CompassSport Heats
#website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=77471"  #Birsemore
#website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=77559"  #event in kent

#SET UP SOUP
html = requests.get(website).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []

#results for each course are stored between the <table> tags.
#DESIGN: from the event page: the program should put all the course hyperlinks into a list, do getResults() function on each of them.
courseLinks = []
resultsDictionary = {}


#Function for retrieving results for each course
def getResults(url):

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
    resultsDictionary[course] = {}

    #FIND RESULTS
    for x in soup.tbody.findAll("tr"):
        number = 1
        checkClub(club)
        if checkClub(club) is True:
            #print("club correct")
            for y in x.findAll("td"):
                if number == 1:
                    position = y.text
                    resultsDictionary[course][position] = {}
                    resultsDictionary[course][position]["pos"] = y.text
                    resultsDictionary[course][position]["course"] = course
                elif number == 2:
                    resultsDictionary[course][position]["name"] = y.text
                elif number == 3:
                    resultsDictionary[course][position]["club"] = y.text
                elif number == 6:
                    #resultsDictionary[course][position]["time"] = y.text
                    pass
                else:
                    pass
                number += 1


#MAIN PROGRAM LOOP
event = soup.find("h2", {"id": "pagesubheading"})
print(event.text)
club = input("Which club do you want to search for?\n").upper()

#adds all the course hyperlinks to a list
courseLinks.append(website)
for x in soup.findAll("a"):
    if x.has_attr("href"):
        if 'course' in x.get('href'):
            course = x.get('href')
            course = "https://www.britishorienteering.org.uk/{}".format(course)
            courseLinks.append(course)

for url in courseLinks:
    #print("getting results from", url)
    getResults(url)

#print(resultsDictionary)


competitors = 0
for x in resultsDictionary:
    for y in resultsDictionary[x]:
        competitors += 1

print("There were", competitors, "competitors from", club, "\n")

for x in resultsDictionary:
    for y in resultsDictionary[x]:
        result = resultsDictionary[x][y]
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])  #function for converting integer to ordinal e.g. 1 --> 1st, 2 --> 2nd
        #this checks if the position is indeed a number, as a mispunch is represented by a "-"
        try:
            int(result["pos"])
            poss = int(result["pos"])
            ordinalPos = ordinal(poss)
        except ValueError:
            ordinalPos = result["pos"]

        print(result["name"], "was", ordinalPos, "on the", result["course"])
        #print(result["name"], result["club"], "was", ordinalPos, "on the", result["course"])