import telegram
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import Constants as keys
from telegram.ext import *
import Response as R
from carousellscrap import find_items
import gc, time
from filtering import filter_json, build_menu, filter_by_date
import authorizeduser as auth

print("Bot started..")

runfunc = True

def start_command(update, context):
    username = update.message.chat.username
    if(username in auth.AUTH_USERS):
        update.message.reply_text("Scrape Carousell Singapore for the cheapest item (works well with electronics item search)\nType [/help] to get started.")
    else:
        update.message.reply_text("Unauthorized.")

def help_command(update, context):
    username = update.message.chat.username
    if(username in auth.AUTH_USERS):
        helpstring = "[HELP]\nAuto-tracker for Carousell Singapore\n\nCrawl function\n*** The program will scrape carousell for the specified item and return the 6 cheapest listings If either lowest price or highest price isn't specified, the program will return the relevant pricing based on Newegg ***\nFormat to search: /crawl[item]|[lowest price]|[highest price]|[condition]\nEXAMPLE: /crawl nintendo switch console|lp400|hp500|new\n[item] - the item name has to be right after '/crawl'\n[lowest price] - start by 'lp' and follow by the lowest price without spacing\n[highest price] - start by 'hp' and follow by the highest price without scpaing\n[condition] - input 'new' or 'used'\n\nAutocrawl function \n*** Similar to crawl function with extra addons to scrapy carousell at 30 mins inteval and return the latest specifed listing ***\nFormat to search: /autocrawl[item]|[lowest price]|[highest price]|[condition]\nEXAMPLE: /autocrawl airpods pro|lp200|hp250|used\n[item] - the item name has to be right after '/crawl'\n[lowest price] - start by 'lp' and follow by the lowest price without spacing\n[highest price] - start by 'hp' and follow by the highest price without scpaing\n[condition] - input 'new' or 'used'\n"
        update.message.reply_text(helpstring)
    else:
        update.message.reply_text("Unauthorized.")

def handle_message(update, context):
    username = update.message.chat.username
    if(username in auth.AUTH_USERS):
        text = str(update.message.text).lower()
        response = R.response(text)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Unauthorized.")

def scrapy_crawl(update, context):
    username = update.message.chat.username
    if(username in auth.AUTH_USERS):
        st = str(update.message.text)
        try:
            #construcitng json
            if st.startswith("/crawl"):
                st = st[7:]
            inputString = str(update.message.text)
            container = find_items(inputString)
            st = st.split("|")
            if len(st) != 0:
                st = st[0]

            reply_markup = filter_json(container)
            update.message.reply_text(st, reply_markup=reply_markup)
        except:
            update.message.reply_text("Error, please check your input.")

        #clear memory
        gc.collect()
    else:
        update.message.reply_text("Unauthorized.")

def scrapy_auto_crawl(update, context):
    username = update.message.chat.username
    if(username in auth.AUTH_USERS):
        st = str(update.message.text)
        if st.startswith("/autocrawl"):
                    st = st[11:]
        #stop btn
        outputlist = []
        global runfunc
        runfunc = True
        while runfunc:
            try:
                inputString = str(update.message.text)
                container = find_items(inputString)
                ss = st.split("|")
                if len(ss) != 0:
                    ss = ss[0]
                outputlist = filter_by_date(container)
                if len(outputlist) !=0:
                    outputlist.append(telegram.InlineKeyboardButton(text='STOP', callback_data='1'))
                    reply_markup1 = InlineKeyboardMarkup(build_menu(outputlist, n_cols=1))
                    update.message.reply_text(ss, reply_markup=reply_markup1)
                time.sleep(600) #set interval
            except:
                update.message.reply_text("Error, please check your input.")

def button(update, context):
    query = update.callback_query
    query.answer()
    global runfunc 
    runfunc = False
    #print(runfunc)


def error(update, context):
    print(f"Update{update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(CommandHandler("start", start_command))
    disp.add_handler(CommandHandler("help", help_command))
    disp.add_handler(CommandHandler("crawl", scrapy_crawl))
    disp.add_handler(CommandHandler("autocrawl", scrapy_auto_crawl, run_async=True))
    disp.add_handler(MessageHandler(Filters.text, handle_message))
    disp.add_handler(CallbackQueryHandler(button))

    disp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


#---- START BOT ----
main()
