import html
from lib2to3.pgen2.token import NUMBER
import random
from TG_ROBOT import dispatcher
from telegram import ParseMode, Update, Bot
from TG_ROBOT.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async
from telethon import Button, events
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.utils.helpers import escape_markdown

NUM1 = (
    "6cm",
    "9cm",
    "15cm",
    "16cm",
    "20cm",
    "22cm",
    "24cm",
    "25cm",
)

MEDIA = "https://telegra.ph/file/d55e9149fd684bbe62aa6.mp4"

def cock(update: Update, context: CallbackContext):
    msg = update.effective_message
    first_name = update.effective_user.first_name
    NUMBERS = random.choice(NUM1)
    msg.reply_video[MEDIA]("{} 's cock size is {}".format(
        first_name, NUMBERS
    )) 


COCK_HANDLER = DisableAbleCommandHandler("cock", cock, run_async=True)

dispatcher.add_handler(COCK_HANDLER)
