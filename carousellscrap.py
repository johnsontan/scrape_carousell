from os import link
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time, json
from newegg import newegg_avg_price
import Constants as cons
from lxml.html import fromstring
from functions import reconstruct_posted_ago, reconstruct_seller_name

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
    #find the item name
    searchitem = str(currentitem).split("|")
    if len(searchitem) != 0:
        searchitem = searchitem[0]
    
    print("scraping carousell..")
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(option=option)

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

    #getting all the attributes vales and form an array
    context = bs(html, 'lxml')
    context2 = fromstring(html)
    context2 = context2.xpath("//div/div[3]/div/div[2]/main/div/div[1]/div/div")
    for ct2 in context2:
        sellerNameA = ct2.xpath(cons.XPSELLERNAME)
        listingDataA = ct2.xpath(cons.XPLISTINGDATE)
        itemNameA = ct2.xpath(cons.XPITEMNAME)
        itemPriceA = ct2.xpath(cons.XPITEMPRICE)
        itemLinkA1 = ct2.xpath(cons.XPITEMLINK)
    itemLinkA2 = []
    for ila in itemLinkA1:
        if (str(ila).startswith("/p/")):
            itemLinkA2.append(ila)

    listingDataA = reconstruct_posted_ago(sellerNameA, listingDataA)
    sellerNameA = reconstruct_seller_name(sellerNameA)
    
    allItemsA = []
    if(len(sellerNameA) == len(listingDataA) == len(itemNameA) == len(itemPriceA) == len(itemLinkA2)):
        tempLength = len(sellerNameA)
        tempArray = []
        count = 0
        while count < tempLength:
            tempArray.append(sellerNameA[count])
            tempArray.append(listingDataA[count])
            tempArray.append(itemNameA[count])
            tempArray.append(itemPriceA[count])
            tempArray.append(itemLinkA2[count])
            allItemsA.append(tempArray)
            tempArray = []
            count += 1

        

    #alldiv = context.findAll("div", class_='D_vT')
    jsonChild = []
    container = {}
    for keys in allItemsA:
        #seller name
        sellername= keys[0]
        #print(sellername)
        if len(sellername) != 0:
            nameout = sellername
        
        #listing date
        listingdate = keys[1]
        #print(listingdate)
        if len(listingdate) != 0:
            listout = listingdate
        
        #itemname
        itemname = keys[2]
        if len(itemname) != 0:
            itemnameout = itemname
        
        #itemprice
        itemprice = keys[3]
        if len(itemprice) != 0:
            price = str(itemprice)
            price = price.split("S$")
            if len(price) != 0:
                priceout = price[1]
        
        #itemlink
        itemlink = keys[4]
        if len(itemlink) >=2:
            #link1 = itemlink[1]['href']
            linkout = "carousell.sg" + itemlink
        

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
    driver.quit()
    return container

if __name__ == '__main__':
    find_items("nintendo switch console|lp400|hp500|new")

