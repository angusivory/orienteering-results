import requests
resultsDictionary = {}

#part of getResults() function from intBof.py 
#when run on its own, it finds all the club results for one course on a url

def checkClub(club):
    for y in x.findAll("td"):
        if y.text == club:
            return True

club = input("Which club?").upper()

number = 1
subhtml = requests.get("https://www.britishorienteering.org.uk/index.php?pg=results&eday=77328").text
from bs4 import BeautifulSoup
soup = BeautifulSoup(subhtml, 'html.parser')

course = soup.find("strong").text
course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
print(course)
resultsDictionary[course] = {}

#FIND RESULTS
for x in soup.tbody.findAll("tr"):
    number = 1
    checkClub(club)
    if checkClub(club) is True:
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

        print(result["name"], result["club"], "was", ordinalPos, "on the", result["course"])