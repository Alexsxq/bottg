from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import logging

# Включим логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
SELECTING_LANGUAGE, SELECTING_ACTION, HANDLE_SUPPORT, HANDLE_UPGRADE = range(4)

# Тексты на разных языках
TEXTS = {
    'ru': {
        'start': 'Выберите язык:',
        'action': 'Что вас интересует?',
        'support_prompt': 'Пожалуйста, напишите ваш вопрос, и наша служба поддержки ответит вам как можно скорее.\n\nС уважением,\nCloudLeak ☁️🤍',
        'upgrade_prompt': 'Для приобретения повышения, пожалуйста, напишите ваш запрос, и наш менеджер свяжется с вами.\n\nС уважением,\nCloudLeak ☁️🤍',
        'support': 'Написать в поддержку',
        'upgrade': 'Приобрести повышение'
    },
    'en': {
        'start': 'Choose your language:',
        'action': 'What are you interested in?',
        'support_prompt': 'Hello!\n\nPlease submit your question, and our support team will get back to you as soon as possible.\n\nBest regards,\nCloudLeak ☁️🤍',
        'upgrade_prompt': 'Hello!\n\nFor upgrade purchase, please submit your request and our manager will contact you.\n\nBest regards,\nCloudLeak ☁️🤍',
        'support': 'Contact support',
        'upgrade': 'Purchase upgrade'
    },
    'uk': {
        'start': 'Виберіть мову:',
        'action': 'Що вас цікавить?',
        'support_prompt': 'Привіт!\n\nБудь ласка, напишіть ваше запитання, і наша служба підтримки відповість вам якомога швидше.\n\nЗ повагою,\nCloudLeak ☁️🤍',
        'upgrade_prompt': 'Привіт!\n\nДля придбання підвищення, будь ласка, напишіть ваш запит, і наш менеджер зв\'яжеться з вами.\n\nЗ повагою,\nCloudLeak ☁️🤍',
        'support': 'Написати в підтримку',
        'upgrade': 'Придбати підвищення'
    },
    'kk': {
        'start': 'Тілді таңдаңыз:',
        'action': 'Сізді не қызықтырады?',
        'support_prompt': 'Сәлем!\n\nӨтінеміз, сұрағыңызды жазыңыз, біздің қолдау қызметі мүмкіндігінше тезірек жауап береді.\n\nҚұрметпен,\nCloudLeak ☁️🤍',
        'upgrade_prompt': 'Сәлем!\n\nЖаңартуды сатып алу үшін өтінеміз, сұрағыңызды жазыңыз, біздің менеджер сізбен хабарласады.\n\nҚұрметпен,\nCloudLeak ☁️🤍',
        'support': 'Қолдау қызметіне жазу',
        'upgrade': 'Жаңартуды сатып алу'
    }
}

# ID администратора (замените на реальный)
ADMIN_CHAT_ID = "ВАШ_CHAT_ID_АДМИНА"

def start(update: Update, context: CallbackContext) -> int:
    """Начинаем разговор и спрашиваем про язык."""
    keyboard = [
        [
            InlineKeyboardButton("Русский", callback_data='ru'),
            InlineKeyboardButton("Қазақша", callback_data='kk'),
        ],
        [
            InlineKeyboardButton("Українська", callback_data='uk'),
            InlineKeyboardButton("English", callback_data='en'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите язык / Choose your language:", reply_markup=reply_markup)
    return SELECTING_LANGUAGE

def language_selected(update: Update, context: CallbackContext) -> int:
    """Сохраняем выбранный язык и предлагаем действие."""
    query = update.callback_query
    query.answer()
    language = query.data
    context.user_data['language'] = language
    
    keyboard = [
        [
            InlineKeyboardButton(TEXTS[language]['support'], callback_data='support'),
            InlineKeyboardButton(TEXTS[language]['upgrade'], callback_data='upgrade'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=TEXTS[language]['action'], reply_markup=reply_markup)
    return SELECTING_ACTION

def action_selected(update: Update, context: CallbackContext) -> int:
    """Обрабатываем выбранное действие."""
    query = update.callback_query
    query.answer()
    action = query.data
    language = context.user_data['language']
    
    if action == 'support':
        query.edit_message_text(text=TEXTS[language]['support_prompt'])
        return HANDLE_SUPPORT
    elif action == 'upgrade':
        query.edit_message_text(text=TEXTS[language]['upgrade_prompt'])
        return HANDLE_UPGRADE

def handle_support(update: Update, context: CallbackContext) -> int:
    """Пересылаем сообщение поддержки администратору."""
    user = update.message.from_user
    language = context.user_data.get('language', 'en')
    text = update.message.text
    
    # Пересылаем сообщение администратору
    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📨 Новый запрос в поддержку ({language}):\nОт: {user.full_name} (@{user.username or 'N/A'})\nID: {user.id}\n\n{text}"
    )
    
    # Отправляем подтверждение пользователю
    update.message.reply_text(TEXTS[language]['support_prompt'].split('\n\n')[0] + "\n\nВаше сообщение отправлено!")
    return ConversationHandler.END

def handle_upgrade(update: Update, context: CallbackContext) -> int:
    """Пересылаем запрос на повышение администратору."""
    user = update.message.from_user
    language = context.user_data.get('language', 'en')
    text = update.message.text
    
    # Пересылаем сообщение администратору
    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"💰 Запрос на повышение ({language}):\nОт: {user.full_name} (@{user.username or 'N/A'})\nID: {user.id}\n\n{text}"
    )
    
    # Отправляем подтверждение пользователю
    update.message.reply_text(TEXTS[language]['upgrade_prompt'].split('\n\n')[0] + "\n\nВаш запрос отправлен!")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Завершаем разговор."""
    update.message.reply_text('До свидания!')
    return ConversationHandler.END

def main() -> None:
    """Запускаем бота."""
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    updater = Updater("YOUR_BOT_TOKEN")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_LANGUAGE: [CallbackQueryHandler(language_selected)],
            SELECTING_ACTION: [CallbackQueryHandler(action_selected)],
            HANDLE_SUPPORT: [MessageHandler(Filters.text & ~Filters.command, handle_support)],
            HANDLE_UPGRADE: [MessageHandler(Filters.text & ~Filters.command, handle_upgrade)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
