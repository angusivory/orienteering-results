#Eventually this should look through the BOF site for past results in a time period and find all the interlopers from those events and print them out.
#BOF results page: https://www.britishorienteering.org.uk/results

import requests
website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=77328"  #Craigmillar Castle
#website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=74350"  #CompassSport Heats
#website = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=77471"  #Birsemore

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
    subhtml = requests.get(url).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(subhtml, 'html.parser')

    course = soup.find("strong").text
    print(course.split("(")[0].rstrip().lstrip())   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name

    #FIND RESULTS


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