
import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
TOKEN = os.getenv("BOT_TOKEN")
import sys
import time

# Debug: покажем в логах, доступна ли переменная окружения (НЕ выводим сам токен)
if TOKEN:
    try:
        print(f"BOT_TOKEN present, length={len(TOKEN)}")
    except Exception:
        print("BOT_TOKEN present")
else:
    print("BOT_TOKEN not set in environment")
if not TOKEN:
    print("Ошибка: установите переменную окружения BOT_TOKEN в файле .env или окружении")
    # Подождём немного чтобы логи успели отправиться, затем выйдем
    time.sleep(1)
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
    app.run_polling()

if __name__ == "__main__":
    main()
