from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date

import pandas as pd
import urllib
import yaml
def get_element(css_selector, driver):
    element = None
    index = 0
    while element==None or element.text=="":
        try:
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,css_selector)))
                
            element = driver.find_element(By.CSS_SELECTOR,css_selector)
            index+=1

            if index==10:
                break
        except TimeoutException:
            return None
    return element
with open(r'trip-advisor/configuration.yaml') as file:
    conf = yaml.load(file, Loader=yaml.FullLoader)
    print(conf)

path_hotels_file = conf['hotels_file']
df = pd.read_csv(path_hotels_file)
new_data = []


driver = webdriver.Chrome()
for index, row in df.iterrows():
    q = urllib.parse.quote(row['hotel_name']) + " Egypt"
    driver.get(f"https://www.tripadvisor.com/Search?q={q}")
    # top_result = get_element("#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div:nth-child(4)\
    #                           > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div > div > div > div", driver)
    title_on_trip_advisor = get_element("#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div:nth-child(4) > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div > div > div\
                                         > div > div.ui_column.is-9-desktop.is-8-mobile.is-9-tablet.content-block-column > div.location-meta-block > div.result-title > span", driver)
    number_reviews = get_element("#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div:nth-child(4) > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div > div > div > div > \
                       div.ui_column.is-9-desktop.is-8-mobile.is-9-tablet.content-block-column > div.location-meta-block > div.rating-review-count > div > a", driver)
    # link = number_reviews.get_attribute("href")

    number_bubbles = get_element("#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div:nth-child(4) > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div > div > div > div > \
                                 div.ui_column.is-9-desktop.is-8-mobile.is-9-tablet.content-block-column > div.location-meta-block > div.rating-review-count > div > span", driver)
    # print(title_on_trip_advisor.text)
    # print(number_reviews.text)
    # print(link)
    # print(number_bubbles.get_attribute("alt"))
    
    new_row = row.copy()
    new_row['title_on_trip_advisor'] = title_on_trip_advisor.text if title_on_trip_advisor is not None else ""
    new_row['number_bubbles'] = number_bubbles.get_attribute("alt") if number_bubbles is not None else ""
    new_row['number_reviews'] = number_reviews.text if number_bubbles is not None else ""
    new_row['link'] = number_reviews.get_attribute("href") if number_reviews is not None else ""
    new_data.append(new_row)

new_df = pd.DataFrame(new_data)

new_df.to_csv(conf['file_save_name'])
# driver = webdriver.Chrome()
# q = "Viva Blue Resort & diving sports"

# driver.get(f"https://www.tripadvisor.com/Search?q={q}")



