import os, pytz, requests, time, timeago, datetime, json
from telegram.ext import Updater, CommandHandler
import logging
START_TEXT = 'COVID-19 info bot. Type /help to see what i can do'
ABOUT_TEXT = 'Bot made by Dhanush Krishnan and Marvin Clement.'
HELP_TEXT = "List of available commands: \n/help - Get this list \n/covid <state_name> - Info on covid infection for specified state \n-/district -Info on covid infection for each district in specified state"
now = datetime.datetime.now()
url = "https://api.covid19india.org/data.json"
url2 = "https://api.covid19india.org/state_district_wise.json"

def start(update, context):
    print("start")
    update.message.reply_text(text = START_TEXT)

def about(update, context):
    print("About")
    update.message.reply_text(text = ABOUT_TEXT)

def get_help(update, context):
    print("Help")
    update.message.reply_text(HELP_TEXT)

def get_info(update, context):
    if len(context.args) >= 1:
        state = str(context.args).capitalize()
        data = getCovid(state)
        update.message.reply_text(data)
    else:
        update.message.reply_text("Usage: /covid <state_name>")

def get_dist(update, context):
    if len(context.args) >= 1:
        state = str(context.args).capitalize()
        data = getDistricts(state)
        update.message.reply_text(data)
    else:
        update.message.reply_text("Usage: /district <state_name>")

def getCovid(state="Kerala"):
    curr_time = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
    curr_time_split = str(curr_time).split('.', 1)[0]
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    states = data["statewise"]
    for j in states:
        if j["state"] == state:
             k = j
             break
    reft = str(k['lastupdatedtime'])
    date = reft.split(" ", 1)[0]
    day = date.split("/", 2)[0]
    month = date.split("/", 2)[1]
    year = date.split("/", 2)[2]
    lref = year + "-" + month + "-" + day + " " + reft.split(" ", 1)[1]
    refresht = timeago.format(lref, curr_time_split)
    status = str("State: {} \nActive: {} \nRecovered: {} \nDeaths: {} \nTotal: {} \nRefreshed: {}".format(k['state'], k['active'], k['recovered'], k['deaths'], k['confirmed'], refresht))
    return status

def getDistricts(state="Kerala"):
    json_url = requests.get(url2)
    data = json.loads(json_url.text)
    district = data[state]["districtData"]
    distdata = str("District-wise Reports\n\n")
    for key,value in district.items():
        distdata = distdata + str("{} : {}\n".format(key,value["confirmed"]))
    return distdata

if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')

    NAME = "covid19info-bot"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(CommandHandler('help', get_help))
    updater.dispatcher.add_handler(CommandHandler('covid', get_info))
    updater.dispatcher.add_handler(CommandHandler('district', get_dist))

    # Start the webhook
    '''
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    '''
    #updater.start_polling()
    updater.idle()
