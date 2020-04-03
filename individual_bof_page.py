import requests
resultsDictionary = {}

#part of getResults() function in bofScraper.py
    #will incorporate this back into bofScraper.py later

number = 1
subhtml = requests.get("https://www.britishorienteering.org.uk/index.php?pg=results&eday=77328").text
from bs4 import BeautifulSoup
soup = BeautifulSoup(subhtml, 'html.parser')

course = soup.find("strong").text
course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
print(course)
resultsDictionary[course] = {}

#FIND RESULTS

orderOfFields = ["pos", "name", "club", "time"]

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

print(resultsDictionary)