#SET UP ARGPARSE
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-o', '--option', action='store', 
				help='Stores soup manipulation choice woooo')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()
print ('You chose option:', results.option, '\n')

#IMPORT WEBPAGE
from urllib.request import urlopen
html = urlopen("https://fvo.org.uk/media/events/2019/dec/15/Abbotshaugh-2019-season-finale/bpf7l/index.html").read()

#SET UP SOUP
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []

#PROCESS OPTION
if not results.option:
	print('Choose an option, you silly goose!')
	print('To choose an option, enter python "webparse.py -o [number]"')
else:
	if int(results.option) == 1:
		print(soup.prettify())

	elif int(results.option) == 2:
		print(soup.title.string)


	elif int(results.option) == 3:	#PRINTS ONLY <a> WITH LINKS IN THEM
		for aTag in soup.find_all('a'):
			if not aTag.string:
				pass
			else:
				print(aTag)


	elif int(results.option) == 4:	#PRINTS <a> BUT all on the same line
		aTag = soup.find_all('a')
		print(aTag)

	elif int(results.option) == 5:
		print(len(soup.contents))
		
		print(soup.contents[0].name)
		print(soup.contents[1].name)
		print(soup.contents[2].name) #html
		print(soup.contents[3].name)

		print(len(soup.contents[2].contents))
		html_node = soup.contents[2]
		print(html_node.contents[0].name)
		print(html_node.contents[1].name)
		print(html_node.contents[2].name)
		print(html_node.contents[3].name) #body
		print(html_node.contents[4].name)

		print(len(html_node.contents[3].contents))
		body_node = html_node.contents[3]
		print(body_node.contents[0].name)
		print(body_node.contents[1].name) #div
		print(body_node.contents[2].name)
	  
		print(len(body_node.contents[1].contents))
		div_node = body_node.contents[1]
		print(div_node.contents[0].name)
		print(div_node.contents[1].name)
		print(div_node.contents[2].name)
		print(div_node.contents[3].name)
		print(div_node.contents[4].name)
		print(div_node.contents[5].name)
		print(div_node.contents[6].name)
		print(div_node.contents[7].name)
		print(div_node.contents[8].name)
		print(div_node.contents[9].name)
		print(div_node.contents[10].name)

	elif int(results.option) == 6:
		print(soup.get_text())
		
	elif int(results.option) == 7:
		for x in soup.find_all('table'):	#find all <table> tags
			print(x.attrs)

	elif int(results.option) == 8:
		for table in soup.find_all('table'):
			print(table.tbody.tr)

	elif int(results.option) == 9:
		
		resultsDictionary = {
			"blue" : {},
			"green" : {},
			"orange" : {},
			"yellow" : {}
		}

		#result lists 
		blue_results = []
		green_results = []
		orange_results = []
		yellow_results = []


		count = 0
		results = soup.findAll("div", {"class": "resultsblock"})	#finds divs with the class "resultsblock"
		for x in results:
			course = (x.div.h2.text)	#sets course to the course name
			course = course.lower()
			count += 1

			allTRs = x.findAll("tr") 
			for y in allTRs:
				number = 1
				allTDs = y.findAll("td")	#each <tr> tag has 6 <td> tags which hold each field
				for z in allTDs:
					#print(z.text)
					
					if number == 1:
						position = z.text
						resultsDictionary[course][position] = {}
						#print(resultsDictionary)
					elif number == 2:
						resultsDictionary[course][position]["name"] = z.text
					elif number == 3:
						resultsDictionary[course][position]["club"] = z.text
					elif number == 4:
						resultsDictionary[course][position]["age class"] = z.text
					elif number == 5:
						resultsDictionary[course][position]["time"] = z.text
					elif number == 6:
						pass

					number += 1


					if count == 1:						#quite clunky but does sort them into the different list - if it is going through the blue table, it add them to the blue list, if the green the to the green list etc
						blue_results.append(z.text)
					elif count ==2:
						green_results.append(z.text)
					elif count == 3:
						orange_results.append(z.text)
					elif count == 4:
						yellow_results.append(z.text)



	#	print(blue_results, "\n")
	#	print(green_results, "\n")
	#	print(orange_results, "\n")
	#	print(yellow_results, "\n")

	print("Results found and sorted :)")

	while True:
		question = input("Any results queries?\n")
		if question == "no":
			break
		else:
			chosenCourse = input("Which course?\n")
			chosenPos = input("Which postion do you want (1st, 2nd, 3rd, 4th etc)\n")
			print(resultsDictionary[chosenCourse][chosenPos])

	