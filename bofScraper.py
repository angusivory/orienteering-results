#Eventually this should look through the BOF site for past results in a time period and find all the interlopers from those events and print them out.
#BOF results page: https://www.britishorienteering.org.uk/results

import requests
website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=77328"  #Craigmillar Castle
#website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=74350"  #CompassSport Heats
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

event = soup.find("h2", {"id": "pagesubheading"})
print(event.text)

#Function for retrieving results for each course
def getResults(url):
    number = 1
    subhtml = requests.get(url).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(subhtml, 'html.parser')

    course = soup.find("strong").text
    course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
    print(course)
    resultsDictionary[course] = {}

    #FIND RESULTS

    for x in soup.tbody.findAll("tr"):
        number = 1
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

while True:
    question = str(input("Any results queries?\n"))
    if question == "yes" or question == "Yes":
        chosenCourse = input("Which course?\n")
        chosenPos = input("Which postion do you want (1, 2, 3, 4 etc)?\n")
        #print(resultsDictionary[chosenCourse][chosenPos])  this just prints the dictionary entry with no nice formatting
        result = resultsDictionary[chosenCourse][chosenPos]
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])  #function for converting integer to ordinal e.g. 1 --> 1st, 2 --> 2nd
        poss = int(result["pos"])
        ordinalPos = ordinal(poss)
        print(result["name"], result["club"], "was", ordinalPos, "on the", result["course"])
    else:
        break