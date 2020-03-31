from telegram.ext import Updater, CommandHandler
from modules import Statewise, District
import logging, os
START_TEXT = 'COVID-19 info bot. Type /help to see what i can do'
ABOUT_TEXT = 'Bot made by Dhanush Krishnan and Marvin Clement.'
HELP_TEXT = "List of available commands: \n/help - Get this list \n/covid <state_name> - Info on covid infection for specified state \n-/district -Info on covid infection for each district in specified state"

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
        data = Statewise.getCovid(state)
        update.message.reply_text(data)
    else:
        update.message.reply_text("Usage: /covid <state_name>")

def get_dist(update, context):
    if len(context.args) >= 1:
        state = str(context.args).capitalize()
        data = District.getDistricts(state)
        update.message.reply_text(data)
    else:
        update.message.reply_text("Usage: /district <state_name>")

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
