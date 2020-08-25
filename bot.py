from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from modules import Statewise, District
import logging, os
START_TEXT = 'COVID-19 info bot. Type /help to see what i can do'
ABOUT_TEXT = 'Bot made by [Dhanush Krishnan](https://t.me/Ded_Boi) and [Marvin Clement](https://t.me/Credance). Forked from [PokeBot](https://t.me/Veg_Pokedex_Bot) ([Source](https://github.com/kshatriya-abhay/pokebot))'
HELP_TEXT = "<b>List of available commands:</b> \n\n/help - Get this list \n/covid <i>state-name</i> - <i>Info on covid infection for specified state (India)</i> \n\n<b>Example - /covid Kerala</b> \n\n/dist <i>state-name</i> - <i>Info on covid infection for each district in specified state (India)</i> \n\n<b>Example - /dist Kerala</b>"
APP_TEXT = "*COVID19 Info app.*\n_Made with flutter._\n\n[Google Drive](https://bit.ly/2XXGklQ)"

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
        update.message.reply_text("Usage: /covid state_name")

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
        update.message.reply_text("Usage: /dist state_name")

def send_app(update, context):
    update.message.reply_text(APP_TEXT, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')

    NAME = os.getenv('NAME')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(CommandHandler('help', get_help))
    updater.dispatcher.add_handler(CommandHandler('covid', get_info))
    updater.dispatcher.add_handler(CommandHandler('dist', get_dist))
    updater.dispatcher.add_handler(CommandHandler('sendapp', send_app))

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    #updater.start_polling()
    updater.idle()
