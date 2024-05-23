from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Replace 'YOUR_TOKEN_HERE' with your bot's API token
BOT_TOKEN = "YOUR BOT TOKEN"
SAVE_PATH = "./"  # Root directory of your project

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("System online - Send file")

async def handle_file(update: Update, context: CallbackContext):
    document = update.message.document
    file_id = document.file_id
    file = await context.bot.get_file(file_id)
    
    # Define the path where the file will be saved
    file_path = os.path.join(SAVE_PATH, document.file_name)
    await file.download_to_drive(file_path)
    
    await update.message.reply_text(f'File saved successfully at {file_path}')

def main():
    # Create the Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
