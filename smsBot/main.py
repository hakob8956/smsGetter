import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes, Application
from helper import *
from telegram.constants import MessageAttachmentType, ParseMode
import db
import uuid
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

with open('config.json') as config_file:
    config = json.load(config_file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Send your secret key via /secret command and get your notifications and sms, for help type /help command")


async def secret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uuid_id = str(update.effective_chat.id)
    secret_key = context.args[0] if context.args else ''
    device_name = ' '.join(context.args[1:]) if len(
        context.args) > 1 else 'Unknown Device'
    try:
        uuid.UUID(secret_key)
        db.set_secret_key_for_uuid(uuid_id, secret_key, device_name)
        message = f'You are successfully connected to the phone with device name: {device_name}'
    except ValueError:
        message = 'Incorrect secret key: not a valid UUID'
    except Exception as e:
        message = f'An error occurred: {str(e)}'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def revoke_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uuid = str(update.effective_chat.id)
    if not context.args:  # No secret_key provided
        try:
            db.delete_all_secret_keys(uuid)
            message = 'Successfully disconnected all devices.'
        except Exception as e:
            message = f'Something went wrong: {str(e)}'
    else:  # Secret key provided
        secret_key = ' '.join(context.args)
        try:
            db.delete_specific_secret_key(uuid, secret_key)
            message = f'Successfully disconnected the device with secret key: {secret_key}'
        except Exception as e:
            message = f'Something went wrong: {str(e)}'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def new_sms_callback(context: CallbackContext):
    results = get_sms()
    if results:
        for value in results:
            uuids = db.get_uuids_for_secret_key(value['secret_key'])
            message = get_message_from_response(value)
            if uuids and message:
                for uuid in uuids:
                    await context.bot.send_message(chat_id=uuid, text=message, parse_mode=ParseMode.MARKDOWN)


async def devices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uuid = str(update.effective_chat.id)
    secret_keys_with_names = db.get_secret_keys_by_uuid(uuid)
    if secret_keys_with_names:
        message = "Connected devices:\n" + \
            "\n".join([f"{name}: {key}" for key,
                      name in secret_keys_with_names])
    else:
        message = "No devices connected."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Welcome to the Notification Bot! Here are the commands you can use:\n"
        "/start - Initialize the bot and receive a greeting.\n"
        "/secret <secret_key> <device_name> - Connect a device with its secret key and an device name.\n"
        "/revoke [<secret_key>] - Disconnect one or all devices. If no key is specified, all devices will be disconnected.\n"
        "/devices - List all connected devices.\n"
        "/health - Display server, database, and mobile statuses.\n"
        "/help - Display this help message."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uuid = str(update.effective_chat.id)
    secret_keys_with_names = db.get_secret_keys_by_uuid(uuid)
    secret_keys = [key for key, _ in secret_keys_with_names]

    server_status = '🟢 online' if get_server_status() == 'online' else '🔴 offline'
    db_status = '🟢 online' if get_db_status() == 'online' else '🔴 offline'
    mobile_status = get_mobile_status(secret_keys)

    mobile_status_message = ""
    if isinstance(mobile_status, dict):
        for key, status in mobile_status.items():
            color = '🟢' if status == 'online' else '🔴'
            device_name = next(
                (name for k, name in secret_keys_with_names if k == key), 'Unknown Device')
            mobile_status_message += f"{device_name}: {color} {status}\n"
    else:
        mobile_status_message = mobile_status

    health_message = (
        f"Server status: {server_status}\n"
        f"DB status: {db_status}\n"
        f"Mobile status:\n{mobile_status_message}"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=health_message, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        config['telegram_key']).build()

    db.init_db()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('secret', secret))
    application.add_handler(CommandHandler('revoke', revoke_bot))
    application.add_handler(CommandHandler('devices', devices))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('health', health))

    job_queue = application.job_queue
    job_queue.run_repeating(new_sms_callback, interval=10, first=0)

    application.run_polling()
