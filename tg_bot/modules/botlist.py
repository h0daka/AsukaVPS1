import os
import html
import re

from tg_bot import pgram as client
from pyrogram import filters
from pyrogram.types import Message

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def escape_markdown(text):
    """Helper function to escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def mention_html(user_id, name):
    return u'<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))


def mention_markdown(user_id, name):
    return u'[{}](tg://user?id={})'.format(escape_markdown(name), user_id)


@client.on_message(filters.command(["botlist", "bots"]))
async def get_list_bots(_, message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    getbots = client.iter_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.user.is_bot:
            bots.append(f"[{nama}](tg://user?id={a.user.id})")
    teks = "╒═══「<b>• Bot List •</b> 」\n\n".format(grup.title)
    for x in bots:
        teks += "• {}\n".format(x)
    teks += "\n╘══「 • Total {} Bots • 」".format(len(bots))
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.reply_text(teks)
