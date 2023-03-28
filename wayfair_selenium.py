import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils import get_new_price_and_list_price, get_product_rating


def get_product():
    page = 1
    list_product_info = []
    while len(list_product_info) < 300:
        print(page)
        url = f'https://www.wayfair.com/furniture/sb0/sectionals-c413893.html?curpage={page}'
        driver = webdriver.Chrome()
        driver.get(url)
        sleep(3)
        list_product = driver.find_elements(By.XPATH, "//a[@class='_1yxeg5wb_6101']")
        for product in list_product:
            title = product.find_element(By.CSS_SELECTOR, "span.StyledBox-owpd5f-0").text
            brand = product.find_element(By.CLASS_NAME, "_1vgix4w6_6101").text
            price = product.find_element(By.CSS_SELECTOR, "div.SFPrice").text
            new_price, list_price = get_new_price_and_list_price(price)
            try:
                rating = product.find_element(By.CSS_SELECTOR, "p.vdvxm0_6101").text
                rating, rating_count = get_product_rating(rating)
            except NoSuchElementException:
                rating = ""
                rating_count = ""
            try:
                free_shipping = product.find_element(By.CSS_SELECTOR, 'p.oakhm65j_6101').text
            except NoSuchElementException:
                free_shipping = ""
            sponsored = product.find_element(By.CSS_SELECTOR, 'div.kzv0b81_6101.kzv0b81p_6101.kzv0b82u_6101.kzv0b81yc_6101').text
            product_info = {
                "Title": title,
                "Brand": brand,
                "New price": new_price,
                "List price": list_price,
                "Rating": rating,
                "Rating count": rating_count,
                "Shipping fee": free_shipping,
                "Sponsored": False if sponsored == "" else True
            }
            list_product_info.append(product_info)
        driver.quit()
        page +=1
    df = pd.DataFrame(list_product_info)
    df.to_csv('/home/luan/intrepid/yes.csv')