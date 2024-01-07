import requests
from bs4 import BeautifulSoup
import csv

import re
import os
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
        categories= soup.select(".side_categories a")
        for category in categories:
            href = category["href"]
            link = f"https://books.toscrape.com/{href}"
            all_categories.append(link)
        return all_categories

# extract all book links within each category
def extract_book_links(category_url):
    print('----------start book category-----------')
#update url in order to pull book links from each page within each category

    book_url = []
    i = 1
    while(True):
        try:
            if i == 1:
                url = category_url
               # print(url)
            else:
                url = category_url.replace('index.html', 'page-{}.html').format(i)

            r = requests.get(url)
            if r.status_code == 200:
                print('correct')
            else:
                print('incorrect')
                if 'incorrect':
                    break
            soup = BeautifulSoup(r.content, 'html.parser')
            print(url)
# pull links for every book
            h3_tags = soup.find_all('h3')
            for article in h3_tags:
                for link in article.find_all('a', href=True):

                    url = link['href']
                    links = 'http://books.toscrape.com/' + url

                    if links not in book_url:
                        book_url.append(
                            f'https://books.toscrape.com/catalogue/{article.contents[0]['href'].replace("../../../", "")}')
            i += 1
        except:
                break
    print(book_url)
    return book_url




#pulling book information for individual books
print("--------pending processing----------")
def product_information(book_url):
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
        image_folder = Path('./Cover Images')
        if not os.path.exists('Cover Images'):
            os.makedirs('Cover Images')



        r = requests.get(image_urls, stream=True)
        upc = soup.find('table', class_ = "table table-striped").find_all ('td') [0].text.strip()

        if r.status_code == 200:
            with open(f'{'Cover Images/'} Cover-{upc}.jpg', 'wb') as f:
                f.write(r.content)


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
                'image url' : image_urls,
                'category' : obtain_category
                    }
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


        downloadables = ({'Product Page URL': book_url,
                              'upc': upc_data,
                              'Title': titles,
                              'price_inc_tax_name': price_inc_tax_data,
                              'Price_exc_tax_name': price_exc_tax_data,
                              'Available': book_availability,
                              'Product Description': product_description,
                              'Category': obtain_category,
                              'Reviews': num_reviews_data,
                              'Rating': book_rating,
                              'Image URL': image_urls})

        with open(f"BookFiles/{obtain_category}.csv", "a")as csv_file:
                    write = csv.DictWriter(csv_file, fieldnames=header)
                    if csv_file.tell() == 0:
                        write.writeheader()


            # create a loop for data to run through

                    write.writerow({'Product Page URL': book_url,
                            'upc': upc_data,
                            'Title': titles,
                            'price_inc_tax_name': price_inc_tax_data,
                            'Price_exc_tax_name': price_exc_tax_data,
                            'Available': book_availability,
                            'Product Description': product_description,
                            'Category': obtain_category,
                            'Reviews': num_reviews_data,
                            'Rating': book_rating,
                            'Image URL': image_urls})
                    print('-----CSV updated-----')
        return data



#creating csv for each category
def write_csv(data, category_name):

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
        write.writerow(header)

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
    info = []
    every_category = category_selection()
    for category_link in every_category:

        links = extract_book_links(category_link)
   
        for link in links:
            book_info = product_information(link)
            info.append(book_info)

   
