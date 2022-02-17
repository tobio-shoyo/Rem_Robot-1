#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Stɑrry Shivɑm
#
# WallsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Licensed under GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
# Copyright (C) 2007 Free Software Foundation, Inc.
# you may not use this file except in compliance with the License.


import logging, os, random, nekos, requests, json, html, traceback, sys

from TG_ROBOT.modules import strings as s

from telegram.ext import Updater, CommandHandler, run_async, Filters, Defaults

from telegram import ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.error import BadRequest
from telegram.utils.helpers import mention_html

from threading import Thread
from functools import wraps


from TG_ROBOT import dispatcher , TOKEN, LOGGER, PORT

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ENV = bool(os.environ.get("ENV", False))

WEBHOOK = False
URL = "https://pixabay.com/api/"
PIX_API = "24446951-f5131704e39ee7908be3a51e4"    

# Log Errors caused by Updates


def error(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    # Finally, send the message
    context.bot.send_message(chat_id=894380120, text=message)


# Helper funcs ==============================================================================

BASE_URL = "https://pixabay.com/api/"

VALID_COLORS = (
    "grayscale",
    "transparent",
    "red",
    "orange",
    "yellow",
    "green",
    "turquoise",
    "blue",
    "lilac",
    "pink",
    "white",
    "gray",
    "black",
    "brown",
)

typing = ChatAction.TYPING
upload = ChatAction.UPLOAD_PHOTO


# Good bots should send actions.
def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action=action
            )
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


# Don't async
def keyboard(imgurl, author, authid):
    keyb = [
        [
            InlineKeyboardButton(text="PageLink  🌐", url=imgurl),
            InlineKeyboardButton(
                text="Author 👸", url=f"https://pixabay.com/users/{author}-{authid}"
            ),
        ]
    ]
    return keyb


# Don't async
def build_res(hits):
    pickrandom = random.choice(list(hits))
    hits = pickrandom

    class res(object):
        preview = hits.get("largeImageURL")
        views = hits.get("views")
        downloads = hits.get("downloads")
        likes = hits.get("likes")
        author = hits.get("user")
        authid = hits.get("user_id")
        tags = hits.get("tags")
        imgurl = hits.get("pageURL")
        document = hits.get("imageURL")

    return res


# Don't async
def send(update, context, res):
    chat = update.effective_chat
    msg = update.effective_message
    try:
        context.bot.send_photo(
            chat.id,
            photo=res.preview,
            caption=(
                s.WALL_STR.format(
                    res.likes, res.author, res.views, res.downloads, res.tags
                )
            ),
            reply_markup=InlineKeyboardMarkup(
                keyboard(res.imgurl, res.author, res.authid)
            ),
            timeout=60,
        )

        context.bot.send_document(chat.id, document=res.document, timeout=100)
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}")


# Wall funcs ===============================================================================


@run_async
@send_action(upload)
def wall(update, context):
    msg = update.effective_message
    query = "+".join(context.args).lower()

    if not query:
        return msg.reply_text(s.NO_ARGS)

    contents = requests.get(
        f"{BASE_URL}?key={PIX_API}&q={query}&page=1&per_page=200"
    ).json()

    hits = contents.get("hits")
    if not hits:
        msg.reply_text(s.NOT_FOUND)
        return
    else:
        send(update, context, build_res(hits))


@run_async
@send_action(upload)
def wallcolor(update, context):
    msg = update.effective_message
    try:
        color = context.args[0].lower()
    except IndexError:
        return msg.reply_text(s.NO_ARGS)

    if color not in VALID_COLORS:
        return msg.reply_text(s.INVALID_COLOR)

    contents = requests.get(
        f"{BASE_URL}?key={PIX_API}&colors={color}&page=2&per_page=200"
    ).json()

    hits = contents.get("hits")
    send(update, context, build_res(hits))


@run_async
@send_action(upload)
def editorschoice(update, context):
    contents = requests.get(
        f"{BASE_URL}?key={PIX_API}&editors_choice=true&page=2&per_page=200"
    ).json()

    hits = contents.get("hits")
    send(update, context, build_res(hits))


@run_async
@send_action(upload)
def randomwalls(update, context):
    contents = requests.get(f"{BASE_URL}?key={PIX_API}&page=2&per_page=200").json()

    hits = contents.get("hits")
    send(update, context, build_res(hits))


@run_async
@send_action(upload)
def animewall(update, context):
    update.effective_message.reply_document(nekos.img("wallpaper"))


@run_async
@send_action(typing)
def colors(update, context):
    update.effective_message.reply_text(
        s.COLOR_STR.format(
            mention_html(update.effective_user.id, update.effective_user.full_name)
        )
    )


@run_async
@send_action(typing)
def about(update, context):
    update.effective_message.reply_text(
        s.ABOUT_STR.format(
            mention_html(update.effective_user.id, update.effective_user.full_name)
        )
    )


@send_action(typing)
def api_status(update, context):
    msg = update.effective_message
    r = requests.get(f"{BASE_URL}?key={PIX_API}")
    if r.status_code == 200:
        status = "functional"
    elif r.status_code == 429:
        status = "limit exceeded!"
    else:
        status = f"Error! {r.status_code}"

    try:
        ratelimit = r.headers["X-RateLimit-Limit"]
        remaining = r.headers["X-RateLimit-Remaining"]

        text = f"API status: <code>{status}</code>\n"
        text += f"Requests limit: <code>{ratelimit}</code>\n"
        text += f"Requests remaining: <code>{remaining}</code>"

        msg.reply_text(text)

    except Exception:
        raise


# HANDLERS
def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(TOKEN, use_context=True, defaults=defaults)

    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.message.reply_text("Restarted!")
        Thread(target=stop_and_restart).start()

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", helper)
    wall_handler = CommandHandler(["wall", "wallpaper"], wall)
    wcolor_handler = CommandHandler("wcolor", wallcolor)
    random_handler = CommandHandler("random", randomwalls)
    editors_handler = CommandHandler("editors", editorschoice)
    colors_handler = CommandHandler("colors", colors)
    about_handler = CommandHandler("about", about)
    anime_handler = CommandHandler("anime", animewall)
    restart_handler = CommandHandler("reboot", restart, filters=Filters.user(894380120))
    apistatus_handler = CommandHandler(
        "status", api_status, filters=Filters.user(894380120)
    )

    # Register handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(wall_handler)
    dispatcher.add_handler(wcolor_handler)
    dispatcher.add_handler(editors_handler)
    dispatcher.add_handler(random_handler)
    dispatcher.add_handler(colors_handler)
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(anime_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(apistatus_handler)
    dispatcher.add_error_handler(error)

__help__ = """Here is the list of available commands i can help you with.\n
× /wall <query>: Gives you wallpapers related to you query.
× /wcolor <color>: Filter images by color properties. click: /colors to get list of colors available.
× /editors: Gives you images that have recived Editor's Choice award.
× /random: Gives you randomly choosen wallpapers.
× /anime: Gives you random anime wallpapers.
× /about: To get information about me!"""


__mod_name__ = "WALLPAPER"
