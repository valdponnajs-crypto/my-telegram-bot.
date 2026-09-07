import asyncio
from keep_alive import keep_alive
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)

WAITING_FOR_KEY = 0
VALID_KEYS = ["ble4012ei1", "ble4412ei1", "ble67412ei1", "ble31412ei1"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Здорово! 🛴💨\n\n"
        "У нас в наличии есть свободные самокаты: 🔥\n"
        "🟣 Юрент (модели Y102-1, Y102-2) ⚡\n"
        "🟡 Вуш 🚀\n"
        "🟠 Яндекс ГО 💥\n"
        "🔵 Джет ⚡\n\n"
        "🔑 Чтобы начать, напиши код доступа: 👇\n\n"
        "🛒 Если у вас нет ключа, то вы можете купить его в @scuterbugtg"
    )
    return WAITING_FOR_KEY

async def check_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    
    if user_key in VALID_KEYS:
        keyboard = [
            [InlineKeyboardButton("🔮 начать разблокировку", callback_data="start_unlock")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ Код успешно подтверждён, система подключена! 🔓\n"
            "💜 Сессионный токен сформирован и готов к работе.\n"
            "📡 Для запуска процедуры поиска нажмите кнопку ниже.\n"
            "📲 Убедитесь, что на вашем устройстве включён Bluetooth!",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ не правильный код! 🚫 Попробуй ещё раз:")
        return WAITING_FOR_KEY

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_unlock":
        keyboard = [
            [InlineKeyboardButton("🚀 старт", callback_data="click_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🚀 Подготовка к поиску транспорта завершена! 🔮\n"
            "⚡ Система готова проверить доступные типы устройств вокруг.\n"
            "📱 Для перехода к настройке вашей платформы нажмите старт.\n"
            "⚙️ Это позволит адаптировать соединение под ваш телефон!",
            reply_markup=reply_markup
        )

    elif query.data == "click_start":
        keyboard = [
            [InlineKeyboardButton("🤖 Андроид", callback_data="show_scooters_menu")],
            [InlineKeyboardButton("🍏 Айфон (iOS)", callback_data="show_scooters_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📲 у вас какой телефон айндройд и йос? 🤔\n\n"
            "⚙️ Выбор операционной системы необходим для калибровки.\n"
            "📡 Различные устройства используют разные протоколы BLE.\n"
            "⚡ Выберите вашу платформу для стабильной передачи пакетов!",
            reply_markup=reply_markup
        )

    elif query.data == "show_scooters_menu":
        keyboard = [
            [InlineKeyboardButton("🟣 Юрент", callback_data="scan_scooter")],
            [InlineKeyboardButton("🟡 Вуш", callback_data="scan_scooter")],
            [InlineKeyboardButton("🟠 Яндекс ГО", callback_data="scan_scooter")],
            [InlineKeyboardButton("🔵 Джет", callback_data="scan_scooter")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🛵 Выберите необходимую марку самоката из списка! 👇\n"
            "🔋 Вся техника проверяется на уровень заряда и сигнал.\n"
            "🎯 Нажмите на нужную кнопку для запуска сканирования.\n"
            "📍 Убедитесь, что вы находитесь в зоне видимости устройства!",
            reply_markup=reply_markup
        )

    elif query.data == "scan_scooter":
        await query.edit_message_text(
            "⏳ подождите 3 минут ⏰\n\n"
            "📡 Идёт сканирование окружающего пространства по BLE...\n"
            "🔋 Проверяются контроллеры и ближайшие батарейные блоки.\n"
            "📲 Не закрывайте приложение и не выключайте Bluetooth!"
        )
        
        await asyncio.sleep(180)
        
        keyboard = [
            [InlineKeyboardButton("📋 меню", callback_data="show_scooters_menu")],
            [InlineKeyboardButton("🔄 новая попытка", callback_data="retry")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "⚠️ не найдено самоката возможно ваш телефон не находиться возле акумулятора приподнесите телефон к акумулятору 🔋📱",
            reply_markup=reply_markup
        )

    elif query.data == "retry":
        await query.edit_message_text(
            "🚫 повторите через 6 часов перегрузка серверов. ⚠️"
        )

def main():
    TOKEN = "8928787707:AAF721G1vV9Ce65wlqhRMkkD_gvQ1KIQ_HE"

    # Запускаем фоновый веб-сервер
    keep_alive()

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_key)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
