##Created to migrate the New Mexico Historical Review from OJS to Digital Commons
##This script crawls a list of URLs loaded from a text file (specify filename on line 12) and extracts selected metadata into lists, then writes output to a text file.

##importing libraries
import requests
from bs4 import BeautifulSoup

##disabling warnings - remove this if you want to see error messages.  Otherwise check your output carefully because you will not know if/where the script fails.
requests.packages.urllib3.disable_warnings()

##loading list of URLs
with open('nmhr-urls-3.txt', 'r') as file:
    urls = file.read().splitlines()

##looping through the list of URLs to get metadata
for url in urls:
    try:
        r = requests.get(url)
		
		####creating BeautifulSoup object from page html
        soup = BeautifulSoup(r.content, 'html.parser')
		
		##opening text file and lists to store and write output
        text_file = open("issue_data_apr-2-pm.txt", "a")
        data_raw = []
		
        ##dictionaries for standardizing months and seasons
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
        text_file.write('\n')

        ##building publication date (for issues with standard title structure)
        #gooddate = issdate.split()
        #year = gooddate[05]
        #badmonth = gooddate[04]
        #month = seasondict.get(badmonth)

        ##building publication date (for issues with alternate title structure)
        gooddate = issother.split()
        year = gooddate[01]
        badmonth = gooddate[0]
        month = seasondict.get(badmonth)

        ##converting month in issue title to season

        if badmonth in ("Winter", "Spring", "Summer", "Fall") :
            season = badmonth
        else:
            season = seasondict2.get(badmonth)

		##creating publication date
        pubdate = str(year) + "-" + str(month) + "-01"
		
		##finding each article

        varticles = vcontent.find_all(class_ ="tocArticle")

     ##starting the for loop to get metadata for articles on this issue page
        counter = 0

        for v in varticles:
            
            ##setting article title and view link to PDF
            ##will need to edit these links in output; change "view" or "viewIssue" to "download"
    
            art = varticles[counter]
            vtitle = art.find(class_="tocTitle").get_text()
            galleys = art.find("a", class_="file")
            vlink = galleys['href']
    
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

            ##setting author- multiple authors may have a lot of white space in between them, it would be nice to modify code to remove this
            try:
                vauthor = art.find(class_="tocAuthors").get_text()
            except:
                vauthor = ' '
			##adding article metadata to list
            data_raw.append(vtitle.strip())
            data_raw.append(vlink.strip())
            data_raw.append(vauthor.strip())
            data_raw.append(doctype.strip())
            #data_raw.append(season.strip())  ##remove if script throws error writing season due to nonstandard HTML format of page
            data_raw.append(pubdate.strip())

            ##convert list to delimited string
            data_out = '|'.join(data_raw).encode('utf-8').strip()

            ##write line to text file
        
            text_file.write(data_out)
            text_file.write('\n')

            ##resetting lists and counters    
            counter = counter+1
            del data_raw[:]     
    ##goes to next URL in list, if current one does not exist or throws an error        
    except:
        pass
        
##end of loop that processes line of metadata; loops back to process next archive page URL
	##resetting vol/issue/date metadata variable
    issdate = ""

## close file 
text_file.close()


