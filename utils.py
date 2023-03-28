import re
from bs4 import BeautifulSoup

def get_new_price_and_list_price(product_price: str):
    pattern = r'\$[\d,]+\.\d{2}'
    price = re.findall(pattern, product_price)
    if len(price) == 2:
        return price[0], price[1]
    else:
        return price[0], ""
    

def get_product_rating(rating_info: str):
    key = 'stars.'
    rating = rating_info.split(key)[0] + key  
    rating_count = rating_info.split(key)[1].split()[0]
    return rating, rating_count


def extract(soup: BeautifulSoup):
    container = soup.find_all('div', class_='a-column a-span12 a-text-center _cDEzb_grid-column_2hIsc')
    list_result = []    
    for i in container:
        tmp = i.find_all('div', class_='p13n-sc-uncoverable-faceout')
        tmp2 = tmp[0].find_all('a')
        url = tmp2[0].get('href')

        tmp = i.find_all('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
        name = tmp[0].text
        
        tmp = i.find_all('span', class_='a-size-base a-color-price')
        if not tmp:
            tmp = i.find_all('span', class_='p13n-sc-price')
        if tmp:
            price = tmp[0].text
        else:
            price=None
        
        list_result.append({'url': url, 'name': name, 'price': price})
    return list_result

def check_last_page(soup: BeautifulSoup):
    container = soup.find_all('li', class_='a-last')
    tmp = container[0].find_all('a')
    if not tmp:
        return True 
    return False