##Created to migrate the New Mexico Historical Review from OJS to Digital Commons
##This script crawls one specified URL (paste URL between quotes on line 12) and extracts selected metadata into lists, then writes output to a text file.

##importing libraries
import requests
from bs4 import BeautifulSoup

##disabling warnings - remove this if you want to see error messages.  Otherwise check your output carefully because you will not know if/where the script fails.
requests.packages.urllib3.disable_warnings()

##getting page content from the specified URL
page = requests.get("https://ejournals.unm.edu/index.php/nmhr/issue/view/402")

##creating BeautifulSoup object from page html
soup = BeautifulSoup(page.content, 'html.parser')

##opening text file and lists to store and write output
text_file = open("issue_data_apr-3-am.txt", "a")
data_raw = []

##dictionaries for creating season and publication metadata
seasondict = {"Winter" : "01", "Spring" : "04", "Summer" : "07", "Fall" : "10", "January" : "01", "April" : "04", "July" : "07", "October" : "10", "Winter," : "01", "Spring," : "04", "Summer," : "07", "Fall," : "10", "January," : "01", "April," : "04", "July," : "07", "October," : "10"}
seasondict2 = {"January" : "Winter", "April" : "Spring", "July" : "Summer", "October" : "Fall" , "January," : "Winter", "April," : "Spring", "July," : "Summer", "October," : "Fall"}

##parsing html object
vcontent = soup.find(id="content")

##getting volume, issue, date metadata
issdate = soup.find_all('h2')[0].get_text()
issother = soup.find_all('h3')[0].get_text()
#print issdate, issother

##writing vol/issue info to text file
text_file.write(issdate)
text_file.write (issother)
text_file.write('\n')

##building publication date
gooddate = issother.split()
year = gooddate[01]
badmonth = gooddate[0]
month = seasondict.get(badmonth)

##converting month in issue title to season

if badmonth in ("Winter", "Spring", "Summer", "Fall") :
    season = badmonth
else:
    season = seasondict2.get(badmonth)

pubdate = str(year) + "-" + str(month) + "-01"

varticles = vcontent.find_all(class_ ="tocArticle")

##starting the for loop to process articles on this issue page
counter = 0

for v in varticles:
##setting article title and view link to PDF
##will need to edit these links in output; change "view" or "viewIssue" to "download"; Digital Commons will pull copy of issue if OJS journal is open access
    #print(counter)
    art = varticles[counter]
    vtitle = art.find(class_="tocTitle").get_text()
    galleys = art.find("a", class_="file")
    try:
        vlink = galleys['href']
    except:
        pass
    
##setting document type
##quality checking of index doctypes in output will be required
    if vtitle == "View or download the full issue":  
        doctype = "full_issue"
    elif "Index" in vtitle:
        doctype = "index"
    elif "Book Reviews" in vtitle:
        doctype = "reviews"
    else:
        doctype = "article"

##setting author - multiple authors may have a lot of white space in between them, it would be nice to modify code to remove this
    try:
        vauthor = art.find(class_="tocAuthors").get_text()
    except:
        vauthor = ' '

##adding article metadata to list
    data_raw.append(vtitle.strip())
    data_raw.append(vlink.strip())
    data_raw.append(vauthor.strip())
    data_raw.append(doctype.strip())
    data_raw.append(pubdate.strip())

##convert list to delimited string
    data_out = '|'.join(data_raw).encode('utf-8').strip()
    #print data_out

##write line of article metadata to text file
        
    text_file.write(data_out)
    text_file.write('\n')

##resetting lists and counters    
    counter = counter+1
    del data_raw[:]

##end of loop that processes line of metadata

## close file 
                
text_file.close()
