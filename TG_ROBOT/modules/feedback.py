import random

from telegram import ParseMode
from telethon import Button

from TG_ROBOT import OWNER_ID, SUPPORT_CHAT
from TG_ROBOT import telethn as tbot

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    Doraemon = (
        "https://telegra.ph/file/951b192d0b86aea2f0000.jpg",
        "https://telegra.ph/file/5cf8e89f0d3b49a3c15fb.jpg",
        "https://telegra.ph/file/960685f142f1c0d87bde7.jpg",
        "",
        "",
    )
    NATFEED = ("https://telegra.ph/file/2dd04f407b16bc2cfdf76.jpg",)
    BUTTON = [[Button.url("View Feedback ✨", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Service"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(NATFEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(VEGETA),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(VEGETA), buttons=BUTTON)
