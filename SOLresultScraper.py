#give it the url for a club's result page and it will find the results from that event, you can search it on course or club or position etc


#IMPORT WEBPAGE
import requests

html = requests.get("https://www.esoc.org.uk/results-files/2019/0922-pentland/stage2_index.html").text  # Pentland SOL brown results
#html = requests.get("https://www.scottish6days.com/results/2019/multistage_index.html").text
#html = requests.get("https://www.esoc.org.uk/results-files/2019/0203_BroxburnSprint/Results/stage1_index.html").text
#html = requests.get("http://www.rstrain.ndtilda.co.uk/results_18/scot_spring/stage5_index.html").text
#html = requests.get("https://www.scottish6days.com/results/2019/stage1_index.html").text
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

    #orderOfFields is a list containing all the keys for each position, e.g. name, age class, club, time etc
    if len(orderOfFields) == 0:
        #orderOfFields = []
        for x in soup.thead.tr.findAll("th"):
            xtext = x.text.lower()
            orderOfFields.append(xtext)
        print(orderOfFields)
    lengthOfOrderOfFields = len(orderOfFields)


    count = 0

    results = soup.findAll("div", {"class": "resultsblock"})	#finds divs with the class "resultsblock"
    for x in results:
        #print("finding course")
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

#PROBLEM:   it doesn't find any 'submenus', so doesn't actually get round to calling findResults(), as the procedure doesn't run at all.
#SOLUTION   it was looking for soup.div.div.div class="submenu" --> it was narrowing down the search options by looking only in divs of divs, problem solved now.
submenus = soup.findAll("div", {"class": "submenu"})
for x in submenus:
    print(x.h3)
    if x.h3.has_attr("Split"):
        print(x)
        pass
    else:

        for y in x.findAll("a"):
            if y.has_attr('href'):
                ystring = y.get('href')
                url = "https://www.esoc.org.uk/results-files/2019/0922-pentland/{}".format(ystring)
                #url = "https://www.scottish6days.com/results/2019/{}".format(ystring)
                #url = "https://www.esoc.org.uk/results-files/2019/0203_BroxburnSprint/Results/{}".format(ystring)
                #url = "http://www.rstrain.ndtilda.co.uk/results_18/scot_spring/{}".format(ystring)
                #url = "https://www.scottish6days.com/results/2019/{}".format(ystring)
                findResults(url)
            else:
                pass




print("Results found and sorted :)\n")
print("The courses were")
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
        print("{}: {}, {}, {}, {}, {}".format(result["course"], result["name"], result["club"], result["pos"], result["age class"], result["time"])) # prints a fancy formatted version (ask Dad how)
    else:
        break



while True:
    search = input("Do you want to search based on another category?\n")
    if search == "yes" or search == "Yes":

        print("The categories are:", orderOfFields)
        category = input("Which category do you want to search on?\n")

        searchValue = input("Search value?\n")
        searchValue = searchValue.upper()

        for course in resultsDictionary:
            
            for position in resultsDictionary[course]:
                
                #this line ¬ checks that the key exists, as some competitors don't have a club or an age or a value for 'behind'
                if category in resultsDictionary[course][position]:
                    if (resultsDictionary[course][position][category]).upper() == searchValue:
                        result = resultsDictionary[course][position]
                        print("{}: {}, {}, {}, {}, {}".format(result["course"], result[orderOfFields[0]], result[orderOfFields[1]], result[orderOfFields[2]], result[orderOfFields[3]], result[orderOfFields[4]]))
    else:
        break