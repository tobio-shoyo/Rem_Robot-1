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

NUM = (
    6,
    9,
    15,
    16,
    20,
    22,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    32,
    33,
    35,
    37,
    36,
    38,
    40,
    41,
    42,
    44,
    45,
    50,
    60,
    62,
    65,
    68,
    78,
    98,
    82,
    105,
    138,

)


MEDIA = "https://telegra.ph/file/d55e9149fd684bbe62aa6.mp4"

def cock(update: Update, context: CallbackContext):
    msg = update.effective_message
    first_name = update.effective_user.first_name
    NUMBERS = random.choice(NUM)
    msg.reply_text("🍆 {} 's cock size is {}CM.".format(
        first_name, NUMBERS
    )) 

def cute(update: Update, context: CallbackContext):
    msg = update.effective_message
    first_name = update.effective_user.first_name
    NUMBERS = random.choice(NUM)
    msg.reply_text("🍑 {} is {}% Cute!".format(
        first_name, NUMBERS
    )) 

def boobs(update: Update, context: CallbackContext):
    msg = update.effective_message
    first_name = update.effective_user.first_name
    NUMBERS = random.choice(NUM)
    msg.reply_text("🍒 {} BooBs is {}!".format(
        first_name, NUMBERS
    )) 

def lesbian(update: Update, context: CallbackContext):
    msg = update.effective_message
    first_name = update.effective_user.first_name
    NUMBERS = random.choice(NUM)
    msg.reply_text("💜 {} is {}% lezbian!".format(
        first_name, NUMBERS
    )) 

def horny(update: Update, context: CallbackContext):
    msg = update.effective_message
    first_name = update.effective_user.first_name
    NUMBERS = random.choice(NUM)
    msg.reply_text("🔥 {} is {}% horny!".format(
        first_name, NUMBERS
    ))     


COCK_HANDLER = DisableAbleCommandHandler("cock", cock, run_async=True)
CUTE_HANDLER = DisableAbleCommandHandler("cute", cute, run_async=True)
BOOBS_HANDLER = DisableAbleCommandHandler("boobs", boobs, run_async=True)
HORNY_HANDLER = DisableAbleCommandHandler("horny", horny, run_async=True)
LESBIAN_HANDLER = DisableAbleCommandHandler("lezbian", "lesbian", lesbian, run_async=True)

dispatcher.add_handler(COCK_HANDLER)
dispatcher.add_handler(CUTE_HANDLER)
dispatcher.add_handler(BOOBS_HANDLER)
dispatcher.add_handler(HORNY_HANDLER)
dispatcher.add_handler(LESBIAN_HANDLER)
