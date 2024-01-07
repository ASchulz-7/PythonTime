BOOKS TO SCRAPE
 

Description:
This project uses Python to extract information from http://books.toscrape.com into CSV files.
STAGES: Phase 1: Pull all information on a single book: Information:product_page_url ● universal_ product_code (upc) ● book_title ● price_including_tax ● price_excluding_tax ● quantity_available ● product_description ● category ● review_rating ● image_url Phase 2: pulls all books in a single category Phase 3: pulls all book categories available Phase 4: Extracts each books information on to csv files by category, and extracts all images associated with the books.
Functions:
•	Category Selection - Pulls all categories
•	Extract Book Links - Extracts all book links within category, ensuring to capture every page in each category
•	Product Information - Pulls all product information and creates csv files by category with each books information 
Saves Book Covers to a generated folder, these covers are saved by their books unique id -Main - runs the code

Installation: 
	-Link to Github:  https://github.com/ASchulz-7/PythonTime.git
 
-pip3 install -r requirements.txt
-	BeautifulSoup
-	Requests
-	Re
-	Os
-	Pathlib Path
-	
Project Folders created by Code 
-Cover Images - Houses all book covers labeled by their unique numerical number 
-BookFiles - Houses all CSV files organized by book category


Requirement.Txt: 
beautifulsoup4==4.12.2
certifi==2023.11.17
charset-normalizer==3.3.2
idna==3.6
numpy==1.26.2
pathlib==1.0.1
python-dateutil==2.8.2
pytz==2023.3.post1
requests==2.31.0
six==1.16.0
soupsieve==2.5
tzdata==2023.4
urllib3==2.1.0
![image](https://github.com/ASchulz-7/PythonTime/assets/148474825/24e32a73-52d3-44fb-9262-29b215b516a8)
 by book category



