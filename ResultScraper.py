#IMPORT WEBPAGE
import requests
#html = requests.get()"https://fvo.org.uk/media/events/2019/dec/15/Abbotshaugh-2019-season-finale/bpf7l/index.html").text
#html = requests.get("https://fvo.org.uk/media/events/2019/dec/11/mine-woods/967iz/index.html").text
#html = requests.get("https://www.esoc.org.uk/results-files/2019/1019_Bonaly/Results/index.html").text
#html = requests.get("https://www.esoc.org.uk/results-files/2019/0922-pentland/stage2_brown_course.html").text  # Pentland SOL brown results
#html = requests.get("https://www.stag-orienteering.co.uk/results-archive/2020/2020-01-05-pollok-country-park/index.html").text
html = requests.get("https://moravianorienteering.org/sites/default/files/events/2020/20200216%20Darnaway%20SOL1/index.html").text

#SET UP SOUP
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []


courseList = []

resultsDictionary = {}  #courses will be added as keys in line 30, then positions will be added as keys later


orderOfFields = []
for x in soup.thead.tr.findAll("th"):
    xtext = x.text.lower()
    orderOfFields.append(xtext)
print(orderOfFields)

lengthOfOrderOfFields = len(orderOfFields)


count = 0

results = soup.findAll("div", {"class": "resultsblock"})	#finds divs with the class "resultsblock"
for x in results:
    course = (x.div.h2.text)	#sets course to the course name
    course = course.lower()
    resultsDictionary[course] = {}
    courseList.append(course)
    count += 1

    allTRs = x.findAll("tr") 
    for y in allTRs:
        number = 1
        allTDs = y.findAll("td")	#each <tr> tag has 6 <td> tags which hold each field
        for z in allTDs:
            #print(z.text)
            
            if number == 1:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    position = z.text
                    resultsDictionary[course][position] = {}
                    resultsDictionary[course][position][orderOfFields[0]] = z.text
                    resultsDictionary[course][position]["course"] = course
            elif number == 2:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[1]] = z.text
            elif number == 3:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[2]] = z.text
            elif number == 4:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[3]] = z.text
            elif number == 5:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[4]] = z.text
            elif number == 6:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[5]] = z.text
            elif number == 7:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[6]] = z.text
            elif number == 8:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[7]] = z.text
            elif number == 9:
                if number > lengthOfOrderOfFields:
                    pass
                else:
                    resultsDictionary[course][position][orderOfFields[8]] = z.text
            number += 1



print("Results found and sorted :)\n")
print("The courses were ")
for x in courseList:
    print(x)

#print(resultsDictionary)

while True:
    question = input("Any results queries?\n")
    if question == "yes" or question == "Yes":
        chosenCourse = input("Which course?\n")
        chosenPos = input("Which postion do you want (1st, 2nd, 3rd, 4th etc)\n")
        #print(resultsDictionary[chosenCourse][chosenPos])
        result = resultsDictionary[chosenCourse][chosenPos]
        print("{}: {}, {}, {}, {}, {}".format(result["course"], result[orderOfFields[0]], result[orderOfFields[1]], result[orderOfFields[2]], result[orderOfFields[3]], result[orderOfFields[4]])) # prints a fancy formatted version (ask Dad how)
    else:
        break

clubsearch = input("Do you want to search based by club?\n")

if clubsearch == "yes" or clubsearch == "Yes":
    clubToBeSearched = input("Which club do you want to search on?\n")
    clubToBeSearched = clubToBeSearched.upper()
    for x in courseList:
        for y in resultsDictionary[x]:
            if resultsDictionary[x][y]["club"] == clubToBeSearched:
                result = resultsDictionary[x][y]
                print("{}: {}, {}, {}, {}, {}".format(result["course"], result[orderOfFields[0]], result[orderOfFields[1]], result[orderOfFields[2]], result[orderOfFields[3]], result[orderOfFields[4]]))