import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from state_machine import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = Bot()


def start(update: Update, context: CallbackContext):
    """Start the conversation and ask user for choice pizza size."""

    bot.start()
    message = 'Какую вы хотите пиццу? Большую или маленькую?'
    update.message.reply_text(message)
    return


def stop(update: Update, context: CallbackContext):
    """Stop conversation."""

    bot.stop()
    message = 'Для начала формирования заказа введите команду "/start"'
    update.message.reply_text(message)
    return


def flow(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if bot.state == 'choice of size':
        if text == 'большую' or text == 'маленькую':
            bot.payment_method()
            bot.set_size(text)
            message = 'Как вы будете платить?'
            update.message.reply_text(message)
        else:
            update.message.reply_text('Пожалуйста, выберите размер пиццы')
    elif bot.state == 'choice of payment':
        if text == 'наличкой' or text == 'картой':
            bot.approve()
            bot.set_payment(text)
            message = f'Вы хотите {bot.size} пиццу, оплата - {bot.payment}?'
            update.message.reply_text(message)
        else:
            update.message.reply_text('Пожалуйста, выберите способ оплаты')
    elif bot.state == 'formation order':
        if text == 'да':
            bot.say_bye()
            message = 'Спасибо за заказ'
            update.message.reply_text(message)
        elif text == 'нет':
            bot.say_bye()
            message = 'Для начала формирования заказа введите команду "/start"'
            update.message.reply_text(message)
        else:
            message = ('Пожалуйста, подтвердите или отмените заказ, или остановите бота командой "stop".\n'
                       'Вы хотите маленькую пиццу, оплата - наличкой?')
            update.message.reply_text(message)


def main() -> None:
    """Run the bot."""

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(MessageHandler(Filters.text, flow))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
