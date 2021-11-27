import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PAYMENT, APPROVE, EXIT = range(3)


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for choice pizza size."""

    buttons = ReplyKeyboardMarkup(keyboard=[['Большую', 'Маленькую']],
                                  resize_keyboard=True,
                                  input_field_placeholder='Большую или Маленькую')
    update.message.reply_text(
        'Какую вы хотите пиццу? Большую или маленькую?',
        reply_markup=buttons,
    )
    return PAYMENT


def payment_method(update: Update, context: CallbackContext) -> int:
    """Save previous choice and ask user about payment method."""

    text = update.message.text
    if text.lower() == 'большую' or text.lower() == 'маленькую':
        context.user_data['size'] = text
        buttons = ReplyKeyboardMarkup([['Наличкой', 'Картой']],
                                      resize_keyboard=True,
                                      input_field_placeholder='Картой или Наличкой')
        update.message.reply_text('Как вы будете платить?',
                                  reply_markup=buttons)
        return APPROVE
    else:
        update.message.reply_text('Пожалуйста, выберите размер пиццы')
        return start(update, context)


def approve(update: Update, context: CallbackContext) -> int:
    """Save previous choice and ask user confirm order."""

    text = update.message.text
    if text.lower() == 'наличкой' or text.lower() == 'картой':
        context.user_data['payment'] = text
        size = context.user_data['size'].lower()
        payment = context.user_data['payment'].lower()
        buttons = ReplyKeyboardMarkup([['Да', 'Нет'],
                                       ['/stop']],
                                      resize_keyboard=True,
                                      one_time_keyboard=True,
                                      input_field_placeholder='Да или Нет')
        update.message.reply_text(f'Вы хотите {size} пиццу, оплата - {payment}?',
                                  reply_markup=buttons)
        return EXIT
    else:
        update.message.reply_text('Пожалуйста, выберите способ оплаты')
        return APPROVE


def say_bye(update: Update, context: CallbackContext) -> int:
    """Thanks the user for order or stop conversation."""

    answer = update.message.text
    if answer.lower() == 'да':
        update.message.reply_text('Спасибо за заказ')
        return ConversationHandler.END
    elif answer.lower() == 'нет':
        update.message.reply_text('Для начала формирования заказа введите команду "/start"')
        return ConversationHandler.END
    else:
        update.message.reply_text('Пожалуйста, подтвердите или отмените заказ, или остановите бота командой "stop".\n'
                                  'Вы хотите маленькую пиццу, оплата - наличкой?')
        return EXIT


def stop(update: Update, context: CallbackContext) -> int:
    """Stop conversation."""

    user_data = context.user_data
    update.message.reply_text('Для начала формирования заказа введите команду "/start"')
    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PAYMENT: [MessageHandler(Filters.text & ~Filters.command, payment_method)],
            APPROVE: [MessageHandler(Filters.text & ~Filters.command, approve)],
            EXIT: [MessageHandler(Filters.text & ~Filters.command, say_bye)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
