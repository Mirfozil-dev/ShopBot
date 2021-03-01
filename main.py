from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    Filters,
    MessageHandler
)
import config

languages = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Русский 🇷🇺', callback_data='ru'),
     InlineKeyboardButton(text='O`zbek 🇺🇿', callback_data='uz'),
     InlineKeyboardButton(text='English 🇬🇧', callback_data='en')]
])
# Keyboard to share contact
share_contact_ru = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отправить номер телефона', request_contact=True)],
    [KeyboardButton(text='Назад 🔙')]
], resize_keyboard=True, one_time_keyboard=True)
share_contact_en = ReplyKeyboardMarkup([
    [KeyboardButton(text='Share phone number', request_contact=True)],
    [KeyboardButton(text='Back 🔙')]
], resize_keyboard=True, one_time_keyboard=True)
share_contact_uz = ReplyKeyboardMarkup([
    [KeyboardButton(text='Telefon raqamini jonatish', request_contact=True)],
    [KeyboardButton(text='Ortga qaytish 🔙')]
], resize_keyboard=True, one_time_keyboard=True)
# Keyboard to share location
share_location_ru = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отправить локацию', request_location=True)],
    [KeyboardButton(text='Назад 🔙')]
], resize_keyboard=True, one_time_keyboard=True)
share_location_en = ReplyKeyboardMarkup([
    [KeyboardButton(text='Share location', request_location=True)],
    [KeyboardButton(text='Back 🔙')]
], resize_keyboard=True, one_time_keyboard=True)
share_location_uz = ReplyKeyboardMarkup([
    [KeyboardButton(text='Lokatsiyani yuvorish', request_location=True)],
    [KeyboardButton(text='Ortga qaytish 🔙')]
], resize_keyboard=True, one_time_keyboard=True)
main_menu_ru = ReplyKeyboardMarkup([
    ['Категории 🗒', 'Корзина 🗑'],
    ['О нас 💬', 'Настройки ⚙'],
], resize_keyboard=True, one_time_keyboard=True)
main_menu_uz = ReplyKeyboardMarkup([
    ['Kategoriyalar 🗒', 'Savat 🗑'],
    ['Biz haqimizda 💬', 'Sozlamalar ⚙'],
], resize_keyboard=True, one_time_keyboard=True)
main_menu_en = ReplyKeyboardMarkup([
    ['Categories 🗒', 'Basket 🗑'],
    ['About us 💬', 'Settings ⚙'],
], resize_keyboard=True, one_time_keyboard=True)


def start(update, context):
    update.message.reply_html('Welcome to our online shop 😊'
                              '\nPlease choose the language 👇'
                              '\n\nДобро пожаловать в наш интернет магазин 😊 '
                              '\nПожалуйста выберите язык 👇'
                              '\n\nBizning internet magazinga hush kelibsiz 😊'
                              '\nTilni tanlang 👇', reply_markup=languages)
    return 1


def language(update, context):
    bot = context.bot
    if update.callback_query:
        query = update.callback_query
        context.user_data['lang'] = query.data
        bot.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        if context.user_data['lang'] == 'ru':
            bot.send_message(
                chat_id=query.message.chat_id,
                text='Вы выбрали русский язык 🇷🇺 \nОтправьте свой номер телефона',
                reply_markup=share_contact_ru
            )
        elif context.user_data['lang'] == 'en':
            bot.send_message(
                chat_id=query.message.chat_id,
                text='You have choosed english language 🇬🇧 \nShare your phone number',
                reply_markup=share_contact_en
            )
        elif context.user_data['lang'] == 'uz':
            bot.send_message(
                chat_id=query.message.chat_id,
                text='Siz o`zbek tilini tanladingiz 🇺🇿 \nTelefon raqamingizni yuvoring',
                reply_markup=share_contact_uz
            )
    else:
        bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        if context.user_data['lang'] == 'ru':
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Вы выбрали русский язык 🇷🇺 \nОтправьте свой номер телефона',
                reply_markup=share_contact_ru
            )
        elif context.user_data['lang'] == 'en':
            bot.send_message(
                chat_id=update.message.chat_id,
                text='You have choosed english language 🇬🇧 \nShare your phone number',
                reply_markup=share_contact_en
            )
        elif context.user_data['lang'] == 'uz':
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Siz o`zbek tilini tanladingiz 🇺🇿 \nTelefon raqamingizni yuvoring',
                reply_markup=share_contact_uz
            )
    return 2


def shared_contact(update, context):
    context.user_data['phone_number'] = update.message.contact.phone_number

    if context.user_data['lang'] == 'ru':
        update.message.reply_html(text='Отправьте локацию 📍', reply_markup=share_location_ru)
    if context.user_data['lang'] == 'en':
        update.message.reply_html(text='Share location 📍', reply_markup=share_location_en)
    if context.user_data['lang'] == 'uz':
        update.message.reply_html(text='Lokatsiyangizni yuvoring 📍', reply_markup=share_location_uz)
    return 3


def shared_location(update, context):
    context.user_data['location_long'] = update.message.location.longitude
    context.user_data['location_lat'] = update.message.location.latitude

    if context.user_data['lang'] == 'ru':
        update.message.reply_html(text='Добро пожаловать! 😁 \n Выберите пункт в меню 👇', reply_markup=main_menu_ru)
    if context.user_data['lang'] == 'en':
        update.message.reply_html(text='Xush kelibsiz! 😁 \ n Menyuda biror narsani tanlang', reply_markup=main_menu_uz)
    if context.user_data['lang'] == 'uz':
        update.message.reply_html(text='Welcome! 😁 \ n Select an item in the menu 👇', reply_markup=main_menu_en)
    return 4


def main():
    updater = Updater(config.TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: {
                CallbackQueryHandler(language),
            },
            2: {
                MessageHandler(Filters.regex('^(Назад 🔙)$') | Filters.regex('^(Ortga qaytish 🔙)$') | Filters.regex(
                    '^(Back 🔙)$'), start),
                MessageHandler(Filters.contact, shared_contact)
            },
            3: {
                MessageHandler(Filters.regex('^(Назад 🔙)$') | Filters.regex('^(Ortga qaytish 🔙)$') | Filters.regex(
                    '^(Back 🔙)$'), language),
                MessageHandler(Filters.location, shared_location)
            }
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
