# OJS-migration
This repository contains Python scripts written to convert XML data exported from Open Journal Systems (Articles and Issues plugin)
into CSV files, and examples of the XML data.

File list:


issues (8).xml :  Example output of the XML for an issue, from the OJS Articles and Issues plugin

scraper-v2.py:  Gets selected fields from the XML export and writes them to a text file

scraper-v3.py:  Alternate version of v2.  Uses the included XML file.


OJS-URL-issue-page-scraper-indiv.py:  Crawls a specified URL for a journal issue, extracts article-level metadata, and writes it to a text file.

OJS-URL-issue-page-scraper-list.py:  Crawls a provided list of URLs for multiple journal issues, extracts article-level metadata, and writes it to a text file.


