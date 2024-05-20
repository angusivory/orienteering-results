import requests
import datetime
now = datetime.datetime.now()


def getCourseResults(url, resultsForEvent, clubQ, clubsearches, ageQ, age):
    coursepage = requests.get(url).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(coursepage, 'html.parser')

    try:
        course = soup.find("strong").text ###for some reason this is being stupid
        goahead = True
    except:
        goahead = False    #some events have no linked results, hence no strong text


    if goahead == True:
        course = course.split("(")[0].rstrip().lstrip().lower()   #splits the string on the '(', takes the first item (which is the course name), and removes spaces from either side of the course name
        #print("course: {}".format(course))
        resultsForEvent[course] = {}

        #FIND RESULTS
        number = 1
        for x in soup.tbody.findAll("tr"):
            number = 1
            if ageQ == True:
                query_check_age = checkAgeClass(x, ageclass)
            else:
                query_check_age = True
            if clubQ == True:
                query_check_club = checkClub(x, clubsearches)
            else:
                query_check_club = True
            
            if query_check_age == True and query_check_club == True:    
                for y in x.findAll("td"):
                    if number == 1:
                        position = y.text
                        resultsForEvent[course][position] = {}
                        resultsForEvent[course][position]["pos"] = y.text
                        resultsForEvent[course][position]["course"] = course
                    elif number == 2:
                        resultsForEvent[course][position]["name"] = y.text
                    elif number == 3:
                        resultsForEvent[course][position]["club"] = y.text
                    elif number == 6:
                        #resultsForEvent[course][position]["time"] = y.text
                        pass
                    else:
                        pass
                    number += 1

def checkClub(tr, searchClub):
    for field in tr.findAll("td"):
        if field.text in searchClub:
            return True
    return False

def checkAgeClass(tr, searchyears):
    for field in tr.findAll("td"):
        if str(field.text) in searchyears:
            return True
    return False

def check_age_valid(ageClass):
    if not ageClass[0].isalpha():
        return False
    
    try:
        value = int(ageClass[1:])
        return True
    except:
        return False

def round_to_five(x, base=5):
    return base * round(x/base)

def agetoyears():
    ageClass = str(input("Which age class do you want to search for? (e.g. M14, W21)\n"))
    if ageClass == "":
        return ""

    while not check_age_valid(ageClass):
        ageClass = str(input("Please use correct format e.g. M14, W21, not '{}'\n".format(ageClass)))
        
    gender = ageClass[0].upper()
    age = int(ageClass[1:])
    print("age: {}, gender: {}".format(age, gender))

    searchterms = []

    if age < 21:
        searchterms.append(str(now.year - int(age)))
        searchterms.append(str(now.year - (int(age) - 1)))
    elif 21 <= age <= 34:
        for year in range(now.year - 34, now.year - 20):
            searchterms.append(str(year))
    else:
        if age >= 100:
            print("senior years eh")
        age5 = round_to_five(age)
        for year in range(now.year - (age5 + 4), now.year - (age5 - 1)):
            searchterms.append(str(year))

    return searchterms



eventpage = "https://www.britishorienteering.org.uk/index.php?pg=results&eday=78465"

ageclass = agetoyears()
club = str(input("Which club do you want to search for? (use abbr. and CSAs for multiple clubs)\n")).upper()

if ageclass == "":
    ageQ = False
else:
    ageQ = True

if club == "":
    clubQ = False
    clubsearches = []
else:
    clubQ = True
    clubsearches = club.split(",")
    for x in range(0, len(clubsearches)):
        clubsearches[x] = clubsearches[x].strip()

print(ageclass, club)


#SET UP SOUP
html = requests.get(eventpage).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

courseLinks = []
resultsForEvent = {}

event = soup.find("h2", {"id": "pagesubheading"})
print(".")

courseLinks.append(eventpage)
for x in soup.findAll("a"):
    if x.has_attr("href"):
        if 'course=' in x.get('href'):
            course = x.get('href')
            course = "https://www.britishorienteering.org.uk/{}".format(course)
            courseLinks.append(course)

for url in courseLinks:
    getCourseResults(url, resultsForEvent, clubQ, clubsearches, ageQ, ageclass)


#after all the results have been found
competitors = 0
for x in resultsForEvent:
    for y in resultsForEvent[x]:
        competitors += 1

if competitors > 0:
    print("\n", event.text)
    for x in resultsForEvent:
        for y in resultsForEvent[x]:
            result = resultsForEvent[x][y]
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])  #function for converting integer to ordinal e.g. 1 --> 1st, 2 --> 2nd
            #this checks if the position is indeed a number, as a mispunch is represented by a "-"
            try:
                int(result["pos"])
                poss = int(result["pos"])
                ordinalPos = ordinal(poss)
            except ValueError:
                ordinalPos = result["pos"]

            if "course" in result["course"]:
                #print(result["name"], "was", ordinalPos, "on", result["course"])
                print("{}, {} was {} on {}".format(result["name"], result["club"], ordinalPos, result["course"]))
            else:
                #print(result["name"], "was", ordinalPos, "on the", result["course"])
                print("{}, {} was {} on the {} course".format(result["name"], result["club"], ordinalPos, result["course"]))
