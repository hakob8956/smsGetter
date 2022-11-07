from email import message
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, Application
from helper import *
from telegram.constants import MessageAttachmentType, ParseMode

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Send your secret key via /secret command and get your notifications and sms")


async def secret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uuid = str(update.effective_chat.id)
    secret_key = ' '.join(context.args)
    result = check_secret_key(uuid, secret_key)
    if result:
        message = 'You are successfully connected to the phone'
    else:
        message = 'Incorrect secret key'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def revoke_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uuid = str(update.effective_chat.id)
    result = revoke(uuid)
    if result:
        message = 'You are successfully disconnected from the phone'
    else:
        message = 'Something went wrong'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def new_sms(context: ContextTypes.DEFAULT_TYPE):
    result = get_sms()
    if result:
        for value in result:
            uuid = value['uuid']
            message = get_message_from_response(value)
            if uuid and message:
                await context.bot.send_message(chat_id=uuid, text=message, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('secret', secret))
    application.add_handler(CommandHandler('sms', new_sms))
    application.add_handler(CommandHandler('revoke', revoke_bot))
    job_queue = application.job_queue

    application.run_polling()
