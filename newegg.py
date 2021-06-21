from os import link
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy import Selector
from bs4 import BeautifulSoup as bs
import time, json

def newegg_avg_price(itemname):
    print("scraping newegg for relevant prices..")
    option1 = Options()
    option1.headless = True
    driver1 = webdriver.Firefox(options=option1)
    #contruct item
    neweggitem = str(itemname)
    neweggitem = neweggitem.replace(" ", "+")
    neweggbase = "https://www.newegg.com/global/sg-en/p/pl?d=" + neweggitem

    #scraping newegg
    driver1.get(neweggbase)
    elem = driver1.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    driver1.quit()

    context = bs(source_code, 'lxml')
    currentprice = context.select(".item-cell .price-current strong")
    if len(currentprice) != 0:
        return currentprice[0].text
    else:
        kk = 0000
        return kk
    