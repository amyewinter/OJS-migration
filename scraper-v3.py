#  This version modified on 8/15/2017 for UNM CIR Journal of Quality Improvement in HealthCare
#  This script parses OJS issues (NOT ARTICLES) outputted to an XML file, places the tags in a "header" list and the contents in a contents list.
#  In order to get each article on its own line, all writing must happen WITHIN iter loop


# importing libraries
import xml.etree.cElementTree as ET

# creating XML tree
tree = ET.parse("issues (8).xml")
root = tree.getroot()

data_headers = []
data_raw = []
data_contents = []

## open file to write data
text_file = open("issue_data.txt", "a")

# getting tags and text and putting them into lists -- everything must happen UNDER this loop, in order to get separate rows of data; otherwise everything gets output to one long row  
for node in tree.iter():

	#skipping nodes that have no content, or useless content
	if node.tag == "issues" or node.tag == "issue" or node.tag == 'embed' or node.tag == 'open_access' or node.tag == 'image' or node.tag == 'galley' or node.tag == 'label' or node.tag == 'file':
		continue

	#excluding issue tags -- has children but no content
	if node.tag != 'article':
		data_headers.append(node.tag)
		data_raw.append(node.text) 

	else:  #if tag is 'issue', stop looping and get ready to write the row
		#converting null values in data_raw to string for output

		for i in data_raw:
			#print i
			if i is None:
				data_contents.append('None')
			else:
				data_contents.append(i)	
				
#print data_headers
#print data_contents
#print data_raw
		
		#converting lists to strings for writing to file
        
		header_str = '|'.join(data_headers).encode('utf-8').strip()
		content_str = '|'.join(data_contents).encode('utf-8').strip()

		#print header_str, content_str
                
		## for TEXT FILE - write header row, tag row, then clear, then write next header/tag row
        
		text_file.write(header_str)
		text_file.write('\n')
		text_file.write(content_str)
		text_file.write('\n')

       
		## empty lists for next pass 
		del data_headers[:]
		del data_raw[:]
		del data_contents[:]
                
##  do not need to clear strings because string will be reassigned from list which is repopulated anew for each item
 
## close file 
                
text_file.close()



