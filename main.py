#from typing imp
import requests
from bs4 import BeautifulSoup
import csv

import re
import os
import shutil
from pathlib import Path


# pulling all categories
def category_selection():
    print("Processing...")
    urls = "https://books.toscrape.com/"
    response = requests.get(urls)
    if response.ok:
        # create a list for all links of the categories:
        all_categories = []
        soup = BeautifulSoup(response.content, "html.parser")
        categories = soup.select(".side_categories a")
        for category in categories:
            href = category["href"]
            link = f"https://books.toscrape.com/{href}"
            all_categories.append(link)
        return all_categories
print(category_selection())



# print(category_selection(book_links))

# extract all book links within each category
def extract_book_links(category_url):
    print('----------start book category-----------')
    response = requests.get(category_url)
    if response.status_code == 200:
        print('yay')
    else:
        print('nope')
    soup = BeautifulSoup(response.content, 'html.parser')
    book_url = []
    h3_tags = soup.find_all('h3')
    #book_url = []

    for article in h3_tags:
        for link in article.find_all('a', href=True):
            url = link['href']
            links = 'http://books.toscrape.com/' + url
            if links not in book_url:
                book_url.append(
                    f'https://books.toscrape.com/catalogue/{article.contents[0]['href'].replace("../../../", "")}')

    return book_url

def turn_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        print("continue")
    else:
        print('needs fixed')
    soup = BeautifulSoup(r.content, 'html.parser')

    next_page = soup.find('ul', class_='pager')
    if next_page:
        for page in next_page:
            all_pages = page.find('li', class_='current').text
            number = page.find(all_pages.strip()[10:])

            counter = 2
            while number > 1:
                next_page_link = f'{url.replace('index.html', '')}page-{counter}.html'
                url.append(next_page_link)
                number -= 1
                counter += 1
    return turn_page(url)

#pulling book information for individual books
print("--------pending processing----------")
def product_information(book_url):
    # update so it's not an object,
    print('Ready to Read? -----obtaining book information, please hold-----')
    response = requests.get(book_url)


    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    # pulling image information
        image = soup.find('img')
        image_url = image['src']
        image_urls = image_url.replace("../../", "https://books.toscrape.com/")
       # print(image_url)

        titles = image['alt']

        # saving images for each book into folder "Cover Images
        if not os.path.exists('Cover Images'):
            os.makedirs('Cover Images')


        # f = open('Cover Images/' + titles +'.jpg', 'wb')
        r = requests.get(image_urls) #, stream=True)

        if r.status_code == 200:
          # fp = open('Cover Images/' + titles, 'wb')
          # fp.write(r.content)
          # fp.close()
            r.raw.decode_content = True

            with open('Cover Images/' + titles, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Download Success: ', titles)
        else:
            print("image not retrieved")

        # obtaining information on book

        obtain_category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string

        book_price = soup.find('p', class_ = 'price_color').text.strip()

        book_rating = soup.find('p', attrs={'class': 'star-rating'}).get('class')[1]

        book_availability = soup.find('p', class_ = 'availability').text.strip()

        product_description = soup.find('article', class_ = "product_page").find_all('p')[3].text.strip()



#individual product info values
        upc_data = soup.find('table', class_ = "table table-striped").find_all ('td') [0].text.strip()
        product_type_data = soup.find('table', class_ = "table table-striped").find_all ('td') [1].text.strip()
        price_exc_tax_data = soup.find('table', class_ = "table table-striped").find_all ('td') [2].text.strip()
        price_inc_tax_data = soup.find('table', class_ = "table table-striped").find_all ('td') [3].text.strip()
        tax_data = soup.find('table', class_ = "table table-striped").find_all ('td') [4].text.strip()
        availability_data = soup.find('table', class_ = "table table-striped").find_all ('td') [5].text.strip()
        num_reviews_data = soup.find('table', class_ = "table table-striped").find_all ('td') [6].text.strip()
           # print(upc_data, product_type_data, price_inc_tax_data,price_exc_tax_data,tax_data, availability_data, num_reviews_data)
        images = soup.find_all('img', {'src': True})

        columns = ['Title', 'Description', 'Book Rating', 'Book Avaliability',
                    'UPC', 'Product Type', 'Book Price', 'PET', 'PIT', 'Tax',
                    'Availability', 'Reviews', 'Image URL']

        #creating data dictionary to use later for csv creation
        data = {
                "link" : book_url,
                "Title": titles,
                "Description": product_description,
                "book_rating": book_rating,
                'book_availability': book_availability,
                'upc': upc_data,
                'product_type': product_type_data,
                'book price': book_price,
                'price_exc_tax_name': price_exc_tax_data,
                'price_inc_tax_name': price_inc_tax_data,
                'tax_name': tax_data,
                'Availability': availability_data,
                'Num_reviews_name': num_reviews_data,
                'image url' : images,
                'category' : obtain_category
                    }


        return data

#def obtain_image(book_url):
    #response = requests.get(book_url)

    #if response.status_code == 200:
    #    soup = BeautifulSoup(response.content, 'html.parser')
        # pulling image information
   #     image = soup.find('img')
   #     image_url = image['src']
       # image_urls = image_url.replace("../../", "https://books.toscrape.com/")
        # print(image_url)

     #   titles = image['alt']
    #    fp = open('Cover Images/' + titles, 'wb')
   #     fp.write(response.content)
  #      fp.close()
#running links through product information to obtain info for csv
def category_info(links):

    print("linking it all together...")
    info = []
    for link in links:

        book_info = product_information(link)
        info.append(book_info)
       # write_csv(info, book_info['category'])

    return info

#creating csv for each category
def write_csv(data, category_name):
# -----# need to figure out how to get only the csv for each individual category, not each csv adding onto previous info


    header = [
            "Product Page URL",
            "Image URL",
            "Title",
            "upc",
            "price_inc_tax_name",
            "Price_exc_tax_name",
            "Available",
            "Category",
            "Reviews",
            'Rating',
            "Product Description"
    ]
# create path for where books will go
    path = f"BookFiles/"
    Path(path).mkdir(parents=True, exist_ok=True)

#open csv in the name of the category
    with open(f"BookFiles/{category_name}.csv", "w", newline="", encoding="utf-8") as file:
        write = csv.DictWriter(file, fieldnames=header)
        write.writeheader()

#create a loop for data to run through
        for one_book in data:


                write.writerow({'Product Page URL': one_book['link'],
                                'upc': one_book['upc'],
                                'Title': one_book['Title'],
                                'price_inc_tax_name': one_book['price_inc_tax_name'],
                                'Price_exc_tax_name': one_book['price_exc_tax_name'],
                                'Available': one_book['Availability'],
                                'Product Description': one_book['Description'],
                                'Category': one_book['category'],
                                'Reviews': one_book['Num_reviews_name'],
                                'Rating': one_book['book_rating'],
                                'Image URL': one_book['image url']})


if __name__=='__main__':

    every_category = category_selection()
    links = extract_book_links(every_category)

    category_info(links)

