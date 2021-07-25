API_KEY = '1878033343:AAGjasdecnlxWnXEdxlUxqh9q-8lww151Iw'

#Carousell place holder
#search required "?" at the end 
SEARCH = 'https://www.carousell.sg/search/'
#condition NEW|OLD
CONDITION_NEW = '&condition_v2=NEW'
CONDITION_USED = '&condition_v2=USED'
MIN_PRICE = '&price_start='
MAX_PRICE = '&price_end='
PRICE_HIGH_LOW = '&sort_by=price%2Cdescending'
PRICE_LOW_HIGH = '&sort_by=price%2Cascending'
CAROUSELL_PROTECTION = '&caroupay=true'
FREE_SHIPPING = '&shipping_offer_free_shipping'
RECENT = '&sort_by=time_created%2Cdescending'

#XPATH
XPITEMNAME = "//div[1]/a[2]/p[1]/text()"
XPSELLERNAME = "//div[1]/a[1]/div[2]/p/text()"
XPLISTINGDATE = "//div[1]/a[1]/div[2]/div/p/text()"
XPITEMPRICE = "//div[1]/a[2]/p[2]/text()"
XPITEMLINK = "//div[1]/a[2]/@href"