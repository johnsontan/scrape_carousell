import telegram
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

def get_itemprice(items):
    return items.get('itemprice')

def filter_json(jsonfile):
  #opening json file
  #f = open (jsonfile)
  #data = json.load(jsonfile)

  outputlist = []
  items = []
  items = jsonfile['items']
  for key in items:
      keyz = dict(key)
      link = ""
      itemdes = ""
      for k, v in keyz.items():
        if k=="listingdate":
          itemdes += v + " | "
        if k=="itemprice":
          itemdes += v
        if k == "itemlink":
          link = v
  
      outputlist.append(telegram.InlineKeyboardButton(text=itemdes, url=link))
  reply_markup = InlineKeyboardMarkup(build_menu(outputlist[:6], n_cols=1))
  return reply_markup


def filter_by_date(jsonfile):
  outputlist = []
  items = jsonfile['items']

  for key in items:
    keyz = dict(key)
    link = ""
    itemdes = ""
    for k, v in keyz.items():
      if k == "listingdate":
        listdate = str(v)
        if "minutes" in listdate:
          listdate = listdate.split(" ")
          #change the interval validation
          if int(listdate[0]) <= 45:
            link = keyz.get("itemlink")
            itemdes = keyz.get("listingdate") + " | "
            itemdes += keyz.get("itemprice")
            outputlist.append(telegram.InlineKeyboardButton(text=itemdes, url=link))
  print(outputlist)
  return outputlist

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu 
    
    #f.close()
    #os.remove(jsonfile)