


#Find out why club search is not working




#IMPORT WEBPAGE
import requests

#html = requests.get("https://www.esoc.org.uk/results-files/2019/0922-pentland/stage2_index.html").text  # Pentland SOL brown results
#html = requests.get("https://www.scottish6days.com/results/2019/multistage_index.html").text
#html = requests.get("https://www.esoc.org.uk/results-files/2019/0203_BroxburnSprint/Results/stage1_index.html").text
#html = requests.get("http://www.rstrain.ndtilda.co.uk/results_18/scot_spring/stage5_index.html").text
html = requests.get("https://www.scottish6days.com/results/2019/stage1_index.html").text
#html = requests.get("").text

#SET UP SOUP
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []


courseList = []
resultsDictionary = {}  #courses will be added as keys in line 30, then positions will be added as keys later
orderOfFields = []

def findResults(url):
    subhtml = requests.get(url).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(subhtml, 'html.parser')
    import re

    print("processing results...")

    orderOfFields = []
    for x in soup.thead.tr.findAll("th"):
        xtext = x.text.lower()

        orderOfFields.append(xtext)
    lengthOfOrderOfFields = len(orderOfFields)


    count = 0

    results = soup.findAll("div", {"class": "resultsblock"})	#finds divs with the class "resultsblock"
    for x in results:
        print("finding course")
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



#actual program now

submenus = soup.div.div.findAll("div", {"class": "submenu"})
for x in submenus:
    print(x.h3)
    if x.h3.has_attr("Split"):
        print(x)
        pass
    else:

        for y in x.findAll("a"):
            if y.has_attr('href'):
                ystring = y.get('href')                        #PROBLEM CURRENTLY IS THAT EVERY OTHER <a> TAG HAS NO HYPERLINK IN IT
                #url = "https://www.esoc.org.uk/results-files/2019/0922-pentland/{}".format(ystring)
                #url = "https://www.scottish6days.com/results/2019/{}".format(ystring)
                #url = "https://www.esoc.org.uk/results-files/2019/0203_BroxburnSprint/Results/{}".format(ystring)
                #url = "http://www.rstrain.ndtilda.co.uk/results_18/scot_spring/{}".format(ystring)
                url = "https://www.scottish6days.com/results/2019/{}".format(ystring)
                print(url)
                findResults(url)
            else:
                pass




print("Results found and sorted :)\n")
print("The courses were")
for x in courseList:
    print(x)

print("The keys were")
print(orderOfFields)
for x in orderOfFields:
    print(x)

#print(resultsDictionary)

while True:
    question = input("Any results queries?\n")
    if question == "yes" or question == "Yes":
        chosenCourse = input("Which course?\n")
        chosenPos = input("Which postion do you want (1st, 2nd, 3rd, 4th etc)\n")
        #print(resultsDictionary[chosenCourse][chosenPos])
        result = resultsDictionary[chosenCourse][chosenPos]
        print("{}: {}, {}, {}, {}, {}".format(result["course"], result["name"], result["club"], result["pos"], result["age class"], result["time"])) # prints a fancy formatted version (ask Dad how)
    else:
        break



while True:
    clubsearch = input("Do you want to search based on club\n")
    if clubsearch == "yes" or clubsearch == "Yes":
        clubToBeSearched = input("Which club do you want to search on?\n")
        clubToBeSearched = clubToBeSearched.upper()
        for x in resultsDictionary:
            for y in resultsDictionary[x]:
                if resultsDictionary[x][y]["club"] == clubToBeSearched:
                    intperson = resultsDictionary[x][y]
                    print("{}".format(intperson["course"]))
                    print("{}".format(intperson["name"]))
                    print("{}".format(intperson["pos"]))
                    print("{}".format(intperson["club"]))
                    print("{}".format(intperson["age class"]))
                    #print("{}: {}, {}, {}, {}, {}".format(intperson["course"], intperson["name"], intperson["club"], intperson["pos"], intperson["age class"], intperson["time"]))
    else:
        break