import os
import time
import requests
import subprocess
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Replace 'BOT_TOKEN' with your bot's API token
BOT_TOKEN = "BOT TOKEN"
save_path = "./"


def telegram_alert(error_message: str):
    bot_token = BOT_TOKEN
    my_chatID = "YOUR_CHAT_ID"
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={my_chatID}&parse_mode=Markdown&text={error_message}"
    response = requests.get(send_text)
    return response.json()

async def root_save(update: Update, context: CallbackContext):
    await update.message.reply_text("System online - Save to root")

async def desktop_save(update: Update, context: CallbackContext):
    global save_path

    save_path = os.path.join(os.path.expanduser("~"), "Desktop")
    await update.message.reply_text("System online - Save to desktop")

async def handle_file(update: Update, context: CallbackContext):
    try:
        document = update.message.document
        file_id = document.file_id
        file = await context.bot.get_file(file_id)
        
        file_path = os.path.join(save_path, document.file_name)
        await file.download_to_drive(file_path)
        
        await update.message.reply_text(f'File saved: {file_path}')
    except Exception as e:
        telegram_alert(f"ERROR >> {e}")

async def handle_image(update: Update, context: CallbackContext):
    try:
        photo = update.message.photo[-1]
        file_id = photo.file_id
        file = await context.bot.get_file(file_id)
        
        file_path = os.path.join(save_path, f"{file_id}.jpg")
        await file.download_to_drive(file_path)
        
        await update.message.reply_text(f'Image saved: {file_path}')
    except Exception as e:
        telegram_alert(f"ERROR >> {e}")

async def run_script(update: Update, context: CallbackContext):
    subprocess.Popen(["start", "cmd", "/c", "start", "pythonw", "controlium.pyw"], shell=True)
    telegram_alert("Program started")


if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler('root', root_save))
        application.add_handler(CommandHandler('desktop', desktop_save))
        application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
        application.add_handler(MessageHandler(filters.PHOTO, handle_image))
        application.add_handler(CommandHandler('run', run_script))
        
        application.run_polling()
    except Exception as e:
        telegram_alert(f"ERROR >> {e}")
        time.sleep(5)
