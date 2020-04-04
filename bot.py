from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from modules import Statewise, District
import logging, os
START_TEXT = 'COVID-19 info bot. Type /help to see what i can do'
ABOUT_TEXT = 'Bot made by [Dhanush Krishnan](https://t.me/Ded_Boi) and [Marvin Clement](https://t.me/Credance). Forked from [PokeBot](https://t.me/Veg_Pokedex_Bot) ([Source](https://github.com/kshatriya-abhay/pokebot))'
HELP_TEXT = "List of available commands: \n/help - Get this list \n/icovid <i>state-name</i> - <i>Info on covid infection for specified state (India)</i> \n<b>Example - /icovid Kerala</b> \n/idist <i>state-name</i> - <i>Info on covid infection for each district in specified state (India)</i> \n<b>Example - /district Kerala</b> \n/inew <i>state_name</i> - <i>Shows number of new cases in your state from last refresh (India)</i> \n<b>Example - /inew Kerala</b> \n/inew_dist <i>state_name</i> - <i>Shows number of new cases in each districts in your state from last refresh (India)</i> \n<b>Example - /inew_dist Kerala</b>"

def start(update, context):
    update.message.reply_text(text = START_TEXT)

def about(update, context):
    update.message.reply_text(text = ABOUT_TEXT, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def get_help(update, context):
    update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML)

def get_info(update, context):
    if len(context.args) == 1:
        state = "".join(context.args).capitalize()
        data = Statewise.getCovid(state)
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    elif len(context.args) > 1:
        state = str()
        for i in context.args:
            if i == 'and':
                state += i + " "
            else:
                state += i.capitalize() + " "
        data = Statewise.getCovid(state[:len(state)-1])
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        update.message.reply_text("Usage: /icovid state_name")

def get_dist(update, context):
    if len(context.args) == 1:
        state = "".join(context.args).capitalize()
        data = District.getDistricts(state)
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    elif len(context.args) > 1:
        state = str()
        for i in context.args:
            if i == 'and':
                state += i + " "
            else:
                state += i.capitalize() + " "
        data = District.getDistricts(state[:len(state)-1])
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        update.message.reply_text("Usage: /idist state_name")

def get_delta(update, context):
    if len(context.args) == 1:
        state = "".join(context.args).capitalize()
        data = Statewise.getDelta(state)
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    elif len(context.args) > 1:
        state = str()
        for i in context.args:
            if i == 'and':
                state += i + " "
            else:
                state += i.capitalize() + " "
        data = Statewise.getDelta(state[:len(state)-1])
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        update.message.reply_text("Usage: /inew state_name")

def get_ddelta(update, context):
    if len(context.args) == 1:
        state = "".join(context.args).capitalize()
        data = District.getDelta(state)
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    elif len(context.args) > 1:
        state = str()
        for i in context.args:
            if i == 'and':
                state += i + " "
            else:
                state += i.capitalize() + " "
        data = District.getDelta(state[:len(state)-1])
        update.message.reply_text(data, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        update.message.reply_text("Usage: /inew_dist state_name")

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
    updater.dispatcher.add_handler(CommandHandler('icovid', get_info))
    updater.dispatcher.add_handler(CommandHandler('idist', get_dist))
    updater.dispatcher.add_handler(CommandHandler('inew', get_delta))
    updater.dispatcher.add_handler(CommandHandler('inew_dist', get_ddelta))

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    #updater.start_polling()
    updater.idle()
