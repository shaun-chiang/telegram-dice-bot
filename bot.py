from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Job
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
import logging

HELP_MESSAGE = "Usage: /roll <# sided dice>"
ARGS = ""
TOKEN = "" # insert your own token here

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=HELP_MESSAGE)


def roll(bot, update, args):
    try:
        ARGS = args
        assert int(args[0]) > 1
        try:
            rand_number = random.randint(1, int(args[0])) + int(args[1])
            text_to_send = update.message.from_user.first_name + " rolled {0} on a d{1}, with added bonus +"+args[1]+"."
        except:
            text_to_send = update.message.from_user.first_name + " rolled {0} on a d{1}."
            rand_number = random.randint(1, int(args[0]))
        if rand_number == 1:
            text_to_send += " Critical Miss!"
        elif rand_number >= int(args[0]):
            text_to_send += " Critical Hit!"
        # keyboard = [[InlineKeyboardButton("Roll Again", callback_data='1')]]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(update.message.chat_id, text=text_to_send.format(rand_number, args[0]))
                        # reply_markup=reply_markup)
    except:
        bot.sendMessage(update.message.chat_id, text=HELP_MESSAGE)


def button(bot, update, job_queue):
    # query = update.callback_query
    # job_roll = Job(roll, 0.1, repeat=False, context = update.message.chat_id)
    # job_queue.put(job_roll)
    pass


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=HELP_MESSAGE)


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(TOKEN)
    j = updater.job_queue

    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(CallbackQueryHandler(button, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler('roll', roll, pass_args=True))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
