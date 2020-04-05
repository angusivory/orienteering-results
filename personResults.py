#name search: user enters name and it searches for them, then finds all their results (in a certain time period)


#name = str(input("Enter name (proper name)\n"))
name = "Angus Ivory"
name = name.split(" ")

website = "https://www.britishorienteering.org.uk/index.php?sitesearch=1&q={}%20{}".format(name[0], name[1])
#print(website)

import requests
#SET UP SOUP
html = requests.get(website).text
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
import re
hyperlinks = []

#somehow needs to get inside this: this is what stores the results of the search: 
 
#</div>
#	<gcse:search></gcse:search>	
#</div>

#may need to input bof number instead and input that into the profile page url directly, or try do google search query?? (ask dad how)