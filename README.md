# OJS-migration
This repository contains Python scripts to get metadata and/or files from Open Journal Systems two ways.  
scraper-v2 and scraper-v3 both parse XML files from the Articles and Issues plugin into CSV files.  
OJS-URL-issue-page-scraper files extract metadata from HTML pages and write it to text files.


File list:


issues (8).xml :  Example output of the XML for an issue, from the OJS Articles and Issues plugin

scraper-v2.py:  Gets selected fields from the XML export and writes them to a text file

scraper-v3.py:  Alternate version of v2.  Uses the included XML file.


OJS-URL-issue-page-scraper-indiv.py:  Crawls a specified URL for a journal issue, extracts article-level metadata, and writes it to a text file.

OJS-URL-issue-page-scraper-list.py:  Crawls a provided list of URLs for multiple journal issues, extracts article-level metadata, and writes it to a text file.


