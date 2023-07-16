from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date

import pandas as pd

def get_element(css_selector, driver):
    element = None
    index = 0
    while element==None or element.text=="":
        
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,css_selector)))
            
        element = driver.find_element(By.CSS_SELECTOR,css_selector)
        index+=1

        if index==10:
            break
        

    return element

data = []
driver = webdriver.Chrome()
offset = 0
break_loop = False
while True:
    driver.get(f"https://www.fibula.com.mk/search?geo=cEG&offset={offset}&order=priceASC")
    
    for i in range(1, 11):
        df = dict()
        header = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) >\
                                                                          article > div.tw-offer-card__header > header > strong > a", driver)
        
        stars = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                                                         > article > div.tw-offer-card__header > header > strong > span", driver)
        price = None
        try:
            WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                                                             > article > div.tw-offer-card__price > div > span > b > ins")))
            price = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                                                             > article > div.tw-offer-card__price > div > span > b > ins", driver)
        except Exception:
            price = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                            > article > div.tw-offer-card__price > div > span > b", driver)
        

        price_for_period = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                       > article > div.tw-offer-card__factoids > ul > li:nth-child(1) > span",
                                       driver)
        
        nights_for_price = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                       > article > div.tw-offer-card__factoids > ul > li:nth-child(2) > span",
                                       driver)
        
        package = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                       > article > div.tw-offer-card__factoids > ul > li:nth-child(3) > span",
                                       driver)
        
        takeoff_from = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                       > article > div.tw-offer-card__factoids > ul > li:nth-child(4) > span",
                                       driver)
        link_on_fibula = get_element(f"body > div.tw-page > main > div > div > div > div > div > ol > li:nth-child({i}) \
                                     > article > div.tw-offer-card__header > header > strong > a", driver)
        print(header.text)
        print(stars.get_attribute('aria-label'))
        print(price.text)
        print(price_for_period.text)
        print(nights_for_price.text)
        print(package.text)
        print(takeoff_from.text)
        print(link_on_fibula.get_attribute("href"))

        df['hotel_name'] = header.text
        df['stars'] = stars.get_attribute('aria-label')
        df['price'] = price.text
        df['price_for_period'] = price_for_period.text
        df['nights_for_price'] = nights_for_price.text
        df['package'] = package.text
        df['takeoff_airport'] = takeoff_from.text
        df['link_on_fibula'] = link_on_fibula.get_attribute("href")

        data.append(df)
        if offset==120:
            break_loop = True
            break

    if break_loop:
        break

    offset += 10
print(data)
final_dataframe = pd.DataFrame(data)

final_dataframe.to_csv("hotels_fibula_hurgada.csv")