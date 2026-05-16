
import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.error import InvalidToken
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

ENV_PATH = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)
TOKEN = (os.getenv("BOT_TOKEN") or "").strip().strip('"').strip("'")

# Debug: покажем в логах, доступна ли переменная окружения (НЕ выводим сам токен)
if TOKEN:
    print(f"BOT_TOKEN present, length={len(TOKEN)}")
else:
    print("BOT_TOKEN not set in environment")

if not TOKEN or "ВАШ_ТОКЕН" in TOKEN or "BOTFATHER" in TOKEN.upper() or TOKEN == "your_telegram_bot_token_here":
    print(f"Ошибка: установите настоящий BOT_TOKEN в файле {ENV_PATH} или в переменных Railway")
    raise SystemExit(1)

CONGRATS = (
    "Апа, поздравляю вас с днем Рождения ❤️ Желаю вам в первую очередь крепкого здоровья, женского"
    " счастья, и побольше радости в жизни и меньше тревог! 😂❤️\n"
    "Я Вас очень сильно люблю, и горжусь, что у меня такая сильная и в то же время нежная, добрая, заботливая мама❤️🫂\n"
    "Люблю вас всем сердцем и очень сильно вами дорожу, с любовью, ваша дочь Алина🩷"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in context.bot_data:
        context.bot_data[user_id] = {"started": False}
    
    if not context.bot_data[user_id]["started"]:
        context.bot_data[user_id]["started"] = True
        await update.message.reply_text(
            'Этот бот был специально разработан для моей самой любимой мамы Саадат❤️ Для запуска этого бота нажмите на кнопку «Start»'
        )
    else:
        await update.message.reply_text(CONGRATS)

async def congrats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    lowered = text.lower()
    if "мама привет" in lowered or "мама, привет" in lowered or lowered.strip() == "мама привет":
        await update.message.reply_text(CONGRATS)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, congrats_handler))
    print("Бот запущен. Ожидание сообщений...")
    try:
        app.run_polling()
    except InvalidToken:
        print("Ошибка: Telegram отклонил BOT_TOKEN. Получите новый токен у @BotFather и обновите .env/Railway Variables.")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
