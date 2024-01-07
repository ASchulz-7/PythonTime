BOOKS TO SCRAPE:

Description:

This project uses Python to extract information from http://books.toscrape.com into CSV files. 


STAGES: 
Phase 1: Pull all information on a single book:
	Information:product_page_url ● universal_ product_code (upc) ● book_title ● price_including_tax ● price_excluding_tax ● quantity_available ● product_description ● category ● review_rating ● image_url
Phase 2: pulls all books in a single category
Phase 3: pulls all book categories available 
Phase 4: Extracts each books information on to csv files by category, and extracts all images associated with the books.

Functions: 
- Category Selection - Pulls all categories
- Extract Book Links - Extracts all book links within category, ensuring to capture every page in each category
- Product Information - Pulls all product information and creates csv files by category with each books information
			Saves Book Covers to a generated folder, these covers are saved by their books unique id
-Main - runs the code

Installation: 
-pip3 install -r requirements.txt

Project Folder created by Code
-Cover Images - Houses all book covers labed by their unique numerical number
-BookFiles - Houses all CSV files organaized by book category



