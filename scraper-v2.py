#  As of 6/23/2017, this script parses OJS issues (NOT ARTICLES) exported to an XML file, places the tags in a "header" list and the contents in a contents list.
#  It breaks at section and article tags and starts a new line.
#  Last edited on 8/22/2017 for Himalayan Research Papers


# importing libraries
import xml.etree.cElementTree as ET

# creating XML tree
tree = ET.parse("issues (10).xml")
root = tree.getroot()

data_headers = []
data_raw = []
data_contents = []

## open file to write data
text_file = open("issue_data.txt", "a")

# getting tags and text and putting them into lists       
for node in tree.iter():

	#skipping nodes that have no content, or useless content
	if node.tag == 'embed' or node.tag == 'open_access' or node.tag == 'image' or node.tag == 'galley' or node.tag == 'label' or node.tag == 'file':
		continue

	#excluding section and article tags -- these have children but no content
	if node.tag != 'section' and node.tag != 'article':
		data_headers.append(node.tag)
		data_raw.append(node.text) 	
		#print data_raw
	
	else:

		#converting null values to string

		for i in data_raw:
			if i is None:
				data_contents.append('None')
			else:
				data_contents.append(i)	
				
		#print data_headers
		#print data_contents
		
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



