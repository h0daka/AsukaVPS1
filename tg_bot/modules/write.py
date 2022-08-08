import requests
from requests import get
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot import pbot


@pbot.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await pbot.send_message(
            message.chat.id, "**Please wait...**\n\nLemme write that..."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        caption = f"""
Here's your Homework

**Written By** @AsukaRobot
**Requested By :** {message.from_user.mention}
"""
        await pbot.send_photo(
            message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• Support •", url=f"https://t.me/AsukaSupport"
                        )
                    ]
                ]
            ),
        )
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await pbot.send_message(
            message.chat.id, "**Please wait...**\n\nLemme write that..."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        caption = f"""
Here's your Homework

**Written By @AsukaRobot
**Requested By :** {message.from_user.mention}
"""
        await pbot.send_photo(
            message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• Support •", url=f"https://t.me/AsukaSupport"
                        )
                    ]
                ]
            ),
        )
        await m.delete()


__mod_name__ = "Homework"

__help__ = """

 Writes the given text on white page with a pen 🖊

❍ /write <text> *:* Writes the given text.
 """
