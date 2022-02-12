import html
import random
from TG_ROBOT import dispatcher
from telegram import ParseMode, Update, Bot
from TG_ROBOT.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async
from telethon import Button, events
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.utils.helpers import escape_markdown

NUM1 = (
    "6",
    "9",
    "15",
    "16",
)

def cock(update: Update, context: CallbackContext):
    args = context.args
    first_name = update.effective_user.first_name
    update.effective_message.reply_text({first_name})(" your dick size is "(random.choice(NUM1))),




COCK_HANDLER = DisableAbleCommandHandler("cock", cock, run_async=True)

dispatcher.add_handler(COCK_HANDLER)
