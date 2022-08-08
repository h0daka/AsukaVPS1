from telethon import *
from telethon.tl.functions.account import *
from telethon.tl.functions.channels import *
from telethon.tl.functions.photos import *
from telethon.tl.types import *
from tg_bot.events import register
from tg_bot import telethn as borg
from html import *
import logging

logger = logging.getLogger(__name__)



@register(pattern="^/pfp ?(.*)")
async def pfp(e):
    ok = e.pattern_match.group(1)
    if ok:
        pass
    elif e.is_reply:
        gs = await e.get_reply_message()
        ok = gs.sender_id
    else:
        ok = e.chat_id
    hehe = await e.client.download_profile_photo(ok)
    if not hehe:
        return await e.reply("Pfp Not Found...")
    await e.reply(file=hehe)
    os.remove(hehe)
