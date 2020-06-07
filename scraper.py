#Import web scraping packages
import requests
from bs4 import BeautifulSoup

#URL for scraping
LIMIT = 10
URL = 'https://www.yelp.com/search?find_desc=&find_loc=Staten%20Island&ns=1&sortby=rating'

#Extract maximum page number
def max_page():
    link = requests.get(URL)
    soup = BeautifulSoup(link.text, 'html.parser')
    pagination = soup.find_all("div",{"class":"pagination-link__373c0__1RtKT"})
    print(soup)
    page_list = []
    for page in pagination:
        page_list.append(int(page.get_text(strip=True)))
    last_page = page_list[-1]

    return last_page

    
#Get details for each review 
def extract_detail(result):
    #Restaurant Name
    name = result.find("a", {"class":"lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"})
    name = name.get_text(strip=True)

    #Restaurant Rating
    rate = result.find("span",{"class":"lemon--span__373c0__3997G display--inline__373c0__3JqBP border-color--default__373c0__3-ifU"})
    rate = rate.find("div")["aria-label"]

    #Number of Reviews
    num_rev = result.find("span",{"class":"lemon--span__373c0__3997G text__373c0__2Kxyz reviewCount__373c0__2r4xT text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa-"})
    num_rev = num_rev.get_text(strip=True)

    #Price
    price = result.find("span",{"class":"lemon--span__373c0__3997G text__373c0__2Kxyz priceRange__373c0__2DY87 text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa- text-bullet--after__373c0__3fS1Z"})
    if price is None:
        price = "Non-Profit"
    else:
        price = price.get_text(strip=True)

    #Tags
    tag = result.find("a",{"class":"lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--default__373c0__7tls6"})
    tag = tag.get_text(strip=True)

    details = {
        'Name': name,
        'Rating': rate,
        'Number of Reviews': num_rev,
        'Price': price,
        'Tag': tag
    }
    return details


#Iterate throgh each page & each hyperlink
def extract_review(max_page):
    reviews = []
    for page in range(max_page):
        print(f"-----------------Scraping Page {page+1}-----------------")
        page_url = f"{URL}&start={page*LIMIT}"
        link = requests.get(page_url)
        soup = BeautifulSoup(link.text, 'html.parser')
        results = soup.find_all("li",{"class":"lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"})
        for result in results[4:15]:
            details = extract_detail(result)
            reviews.append(details)
    return reviews


def get_reviews():
    last_page = max_page()
    reviews = extract_review(last_page)
    return reviews