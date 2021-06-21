from os import link
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time, json
from newegg import newegg_avg_price
import Constants as cons

def LoadAllListings(driver):
        counter = 0
        end = True
        driver2 = driver
        try:
            while end:
                loadmorebtn = driver2.find_element_by_xpath('//button[text()="Load more"]')
                if not loadmorebtn: end = False
                loadmorebtn.click()
                time.sleep(1)
                counter += 1
                if counter==2: end = False
        except:
            return driver2
        return driver2

def construct_url(item):
    #spilting the item input
    url = ""
    itemPH = str(item)
    itemPH = itemPH.split("|")
    lowprice = ""
    highprice = ""
    searchitemname = ""
    
    if len(itemPH) != 0:
        searchitemname = itemPH[0]
        #build url
        url = cons.SEARCH + searchitemname + "?"
        for itemInput in itemPH:
            if itemInput.lower() == "cp":
                url += cons.CAROUSELL_PROTECTION
            elif itemInput.lower() == "rec":
                url += cons.RECENT
            elif itemInput.lower() == "fs":
                url += cons.RECENT
            elif itemInput.lower() == "new":
                url += cons.CONDITION_NEW
            elif itemInput.lower() == "used":
                url += cons.CONDITION_USED
            elif "lp" in itemInput.lower():
                lowprice = str(itemInput)
                lowprice = lowprice.replace("lp", "")
                url += cons.MIN_PRICE + lowprice.strip()
            elif "hp" in itemInput.lower():
                highprice = str(itemInput)
                highprice = highprice.replace("hp", "")
                url += cons.MAX_PRICE + highprice.strip()

    if (cons.MAX_PRICE not in url) or (cons.MIN_PRICE not in url):
        relvantprice = newegg_avg_price(searchitemname)
        relvantprice = str(relvantprice).replace(",", "")
    if (cons.MAX_PRICE not in url) and (relvantprice != 0000):
        topprice = float(relvantprice) * 1.1
        topprice = round(topprice, 2)
        url += cons.MAX_PRICE + str(topprice)
    if (cons.MIN_PRICE not in url) and (relvantprice != 0000):
        btmprice = float(relvantprice) * 0.65
        btmprice = round(btmprice, 2)
        url += cons.MIN_PRICE + str(btmprice)
    return url
    

def find_items(item):
    print("started..")
    currentitem = str(item)
    if currentitem.startswith("/crawl"):
            currentitem = currentitem[7:]

    if currentitem.startswith("/autocrawl"):
            currentitem = currentitem[11:]
    print(currentitem)
    print(item)
    #find the item name
    searchitem = str(currentitem).split("|")
    if len(searchitem) != 0:
        searchitem = searchitem[0]
    
    print("scraping carousell..")
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)

    #construct item
    print("Item: " + searchitem)
    base = construct_url(currentitem)
    currentitem2 = str(item)
    if currentitem2.startswith("/crawl"):
        base += cons.PRICE_LOW_HIGH
    if currentitem2.startswith("/autocrawl"):
        base += cons.RECENT
    print(base)
    driver.get(base)
    driver = LoadAllListings(driver)
    time.sleep(3)
    element = driver.find_element_by_id("root")
    html = driver.execute_script("return arguments[0].outerHTML;", element)

    context = bs(html, 'lxml')
    alldiv = context.findAll("div", class_='D_oi')
    jsonChild = []
    container = {}
    for keys in alldiv:
        #seller name
        sellername= keys.select(".D_eo.D_eB.D_ea")
        #print(sellername)
        if len(sellername) != 0:
            nameout =sellername[0].get_text()
        
        #listing date
        listingdate = keys.select(".D_oC")
        #print(listingdate)
        if len(listingdate) != 0:
            listout = listingdate[0].get_text()
        
        #itemname
        itemname = keys.select(".D_en.D_eB")
        if len(itemname) != 0:
            itemnameout = itemname[0].get_text()
        
        #itemprice
        itemprice = keys.select(".D_ol .D_cZ")
        if len(itemprice) != 0:
            price = str(itemprice[0].get_text())
            price = price.split("S$")
            if len(price) != 0:
                priceout = price[1]
        
        #itemlink
        itemlink = keys.select("div > a")
        if len(itemlink) >=2:
            link1 = itemlink[1]['href']
            linkout = "carousell.sg" + link1
        

        jsonChild.append({
            'name': nameout,
            'listingdate': listout,
            'itemname': itemnameout,
            'itemprice': priceout,
            'itemlink': linkout
        })

    container['carousell'] = 'carousell'
    container['items'] = jsonChild

    driver.quit()
    #transform to dict
    container = json.dumps(container)
    container = json.loads(container)
    return container

if __name__ == '__main__':
    find_items("nintendo switch console|lp400|hp500|new")

