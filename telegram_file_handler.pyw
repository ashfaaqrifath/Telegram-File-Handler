import os
import time
import requests
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Replace 'BOT_TOKEN' with your bot's API token
BOT_TOKEN = "YOUR BOT TOKEN"

# Path to the Desktop for images
IMAGE_SAVE_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
# Root directory for files
FILE_SAVE_PATH = "./"

pid = os.getpid()

def telegram_alert(error_message: str):
    bot_token = BOT_TOKEN
    my_chatID = "CHAT ID"
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={my_chatID}&parse_mode=Markdown&text={error_message}"
    response = requests.get(send_text)
    return response.json()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("System online - Send file or image")

async def handle_file(update: Update, context: CallbackContext):
    try:
        document = update.message.document
        file_id = document.file_id
        file = await context.bot.get_file(file_id)
        
        file_path = os.path.join(FILE_SAVE_PATH, document.file_name)
        await file.download_to_drive(file_path)
        
        await update.message.reply_text(f'File saved: {file_path}')
    except Exception as e:
        telegram_alert(f"ERROR >> {e}")

async def handle_image(update: Update, context: CallbackContext):
    try:
        photo = update.message.photo[-1]
        file_id = photo.file_id
        file = await context.bot.get_file(file_id)
        
        file_path = os.path.join(IMAGE_SAVE_PATH, f"{file_id}.jpg")
        await file.download_to_drive(file_path)
        
        await update.message.reply_text(f'Image saved: {file_path}')
    except Exception as e:
        telegram_alert(f"ERROR >> {e}")

async def run_script(update: Update, context: CallbackContext):
    subprocess.Popen(["start", "cmd", "/c", "start", "pythonw", "controlium.pyw"], shell=True)
    telegram_alert("Program started")

async def stop_script(update: Update, context: CallbackContext):
    telegram_alert("Program stopped")
    os._exit(0)

try:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(CommandHandler('run', run_script))
    application.add_handler(CommandHandler('stop', stop_script))
except Exception as e:
    telegram_alert(f"ERROR >> {e}")

while True:
    try:
        application.run_polling()
    except Exception as e:
        telegram_alert(f"ERROR >> {e}")
        time.sleep(5)
