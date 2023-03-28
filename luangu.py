import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm



class FISH:
    driver = driver_cate = webdriver.Chrome(ChromeDriverManager().install())

    def crawl_cate(self, url_id):
        url = f'https://www.amazon.com/gp/bestsellers/hi/{url_id}'
        self.driver.get(url)
        run=0
        result = list()
        while True:
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            result.extend(extract(soup))

            print(f"run: {run+1}, num data: {len(result)}")
            run+=1

            if not check_last_page(soup):
                elements = self.driver.find_elements_by_class_name("a-last")
                elements[-1].click()
            else: 
                break
        
        return result
    def crawl_asin(self, url_id):
        url = f'https://www.amazon.com/dp/{url_id}?th=1'
        self.driver.get(url)

        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        container_title = soup.find_all('span', class_='a-size-large product-title-word-break')
        title = container_title[0].text.strip()


        container_price = soup.find_all('span', class_='a-price-whole')
        price = container_price[0].text.strip()
        container_price_frac = soup.find_all('span', class_='a-price-fraction')
        price_frac = container_price_frac[0].text.strip()

        container_lprice = soup.find_all('span', class_='a-price a-text-price')
        tmp = container_lprice[0].find_all('span')
        lprice = tmp[-1].text.strip()

        container_rat = soup.find_all('i', class_='a-icon a-icon-star a-star-5')
        rat = container_rat[0].text.strip()

        container_ratc = soup.find_all('span', {'id': 'acrCustomerReviewText'})
        ratc = container_ratc[0].text

        img_url = soup.find_all('div', class_='imgTagWrapper')
        img_url = img_url[0].find_all('img')
        img_url = img_url[0].get('src')

        return {
            'title': title, 
            'price': price+price_frac, 
            'list_price': lprice, 
            'rating': rat, 
            'rating_count': ratc
        }
    def crawl(self, urls, mode='cate'):
        result = []
        for url_id in urls:
            if mode=='cate':
                print(url_id)
                r = self.crawl_cate(url_id) 
                result.extend(r)     
            else:
                r = self.crawl_asin(url_id)
                result.append(r)
        return result

    def close(self):
        self.driver.close()
        

if __name__ == '__main__':
    asin = ['B07MFZXR1B', 'B07CRG7BBH', 'B07VS8QCXC']
    category = ['172456', '193870011']
    myfish = FISH()
    # r = myfish.crawl(urls=category, mode='cate')
    # import json
    # with open('cate.json', 'w') as outfile:
    #     json.dump(r, outfile)

    r = myfish.crawl(urls=asin, mode='asin')
    import json
    with open('asin.json', 'w') as outfile:
        json.dump(r, outfile)

    